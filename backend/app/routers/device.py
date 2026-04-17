from fastapi import APIRouter, HTTPException
from app.schemas.sensor import SensorReading, AnalysisResult
from app.services.analysis import heuristic_risk
from app.services.analysis import evaluate_flame_signal
from app.services.openai_service import analyze_with_openai
from app.state import LATEST_ANALYSIS, FLAME_SIGNAL_STATE, ALARM_ACTUATOR_STATE
from app.core.database import readings_collection, results_collection
from app.core.config import FLAME_OVERRIDE_MIN_CONFIDENCE
from datetime import datetime, timedelta, timezone

UTC_PLUS_8 = timezone(timedelta(hours=8))


def normalize_timestamp(value, naive_is_utc: bool = False):
    if value is None:
        return datetime.now(UTC_PLUS_8)

    if isinstance(value, str):
        value = value.replace("Z", "+00:00")
        value = datetime.fromisoformat(value)

    if value.tzinfo is None:
        if naive_is_utc:
            value = value.replace(tzinfo=timezone.utc)
        else:
            value = value.replace(tzinfo=UTC_PLUS_8)

    return value.astimezone(UTC_PLUS_8)


def normalize_reading_doc(doc):
    normalized = dict(doc)

    if "timestamp" in normalized:
        normalized["timestamp"] = normalize_timestamp(normalized["timestamp"], naive_is_utc=True)

    if "created_at" in normalized:
        normalized["created_at"] = normalize_timestamp(normalized["created_at"], naive_is_utc=True)

    if "_id" in normalized:
        normalized["_id"] = str(normalized["_id"])

    if "reading_id" in normalized:
        normalized["reading_id"] = str(normalized["reading_id"])

    return normalized


def serialize_datetime_to_iso(dt):
    """Convert datetime object to ISO string for JSON responses."""
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt

router = APIRouter(prefix="/api", tags=["device"])

@router.post("/readings", response_model=AnalysisResult)
def post_reading(reading: SensorReading):
    signal_state = FLAME_SIGNAL_STATE.get(reading.device_id, {})
    flame_signal = evaluate_flame_signal(reading, state=signal_state)

    FLAME_SIGNAL_STATE[reading.device_id] = {
        "filtered_value": flame_signal["filtered_value"],
        "detected": flame_signal["detected"],
        "trigger_count": flame_signal["trigger_count"],
        "clear_count": flame_signal["clear_count"],
        "recent_values": flame_signal["recent_values"],
    }

    normalized_reading = reading.model_copy(
        update={
            "timestamp": normalize_timestamp(reading.timestamp),
            "flame_detected": flame_signal["detected"],
            "flame_filtered_value": flame_signal["filtered_value"],
            "flame_confidence": flame_signal["confidence"],
            "flame_sensor_fault": flame_signal["sensor_fault"],
        }
    )
    heuristic = heuristic_risk(normalized_reading)

    if flame_signal["valid"] and flame_signal["reason"] not in heuristic["reasons"]:
        heuristic["reasons"].append(flame_signal["reason"])

    try:
        ai_result = analyze_with_openai(
            normalized_reading.model_dump(),
            heuristic
        )
    except Exception as e:
        # Fallback if AI fails
        ai_result = {
            "danger": heuristic["danger"],
            "danger_level": heuristic["risk_level"],
            "suspected_gas": "Unknown / mixed gas",
            "confidence": 0.55 if heuristic["danger"] else 0.35,
            "summary": "OpenAI analysis failed. Using heuristic fallback.",
            "reasons": heuristic["reasons"],
            "actions": ["Check sensors", "Ventilate area", "Inspect for leaks"],
            "trigger_buzzer": heuristic["danger"],
            "trigger_led": heuristic["danger"],
        }

    # Safety override: only force CRITICAL when flame confidence is high and signal is healthy.
    if (
        normalized_reading.flame_detected
        and not normalized_reading.flame_sensor_fault
        and (normalized_reading.flame_confidence or 0.0) >= FLAME_OVERRIDE_MIN_CONFIDENCE
    ):
        ai_result["danger"] = True
        ai_result["danger_level"] = "CRITICAL"
        ai_result["trigger_buzzer"] = True
        ai_result["trigger_led"] = True
        if "Flame sensor detected fire" not in ai_result["reasons"]:
            ai_result["reasons"] = ["Flame sensor detected fire"] + ai_result.get("reasons", [])

    # Keep actuator flags aligned with the final danger decision so downstream clients
    # do not depend on the model returning a perfectly consistent payload.
    if ai_result.get("danger") or ai_result.get("danger_level") in ("HIGH", "CRITICAL"):
        ai_result["trigger_buzzer"] = True
        ai_result["trigger_led"] = True

    # Sync live analysis to actuator state unless manual scenario mode is active.
    if not ALARM_ACTUATOR_STATE.get("feed_paused", False):
        ALARM_ACTUATOR_STATE["is_active"] = bool(ai_result.get("trigger_buzzer", False))
        ALARM_ACTUATOR_STATE["scenario"] = "LIVE"

    LATEST_ANALYSIS["reading"] = normalized_reading.model_dump()
    LATEST_ANALYSIS["analysis"] = ai_result

    # Save to database
    if readings_collection is not None:
        try:
            reading_doc = {
                "device_id": normalized_reading.device_id,
                "mq7": normalized_reading.mq7,
                "mq135": normalized_reading.mq135,
                "mq2": normalized_reading.mq2,
                "dht22_temp": normalized_reading.dht22_temp,
                "dht22_humidity": normalized_reading.dht22_humidity,
                "flame_value": normalized_reading.flame_value,
                "flame_filtered_value": normalized_reading.flame_filtered_value,
                "flame_confidence": normalized_reading.flame_confidence,
                "flame_sensor_fault": normalized_reading.flame_sensor_fault,
                "flame_detected": normalized_reading.flame_detected,
                "timestamp": normalized_reading.timestamp,
                "analysis": ai_result,
                "created_at": datetime.now(UTC_PLUS_8)
            }
            result = readings_collection.insert_one(reading_doc)
            print(f"Reading saved to MongoDB with ID: {result.inserted_id}")
            
            # Save results to separate collection
            if results_collection is not None:
                result_doc = {
                    "device_id": normalized_reading.device_id,
                    "reading_id": result.inserted_id,
                    "flame_value": normalized_reading.flame_value,
                    "flame_filtered_value": normalized_reading.flame_filtered_value,
                    "flame_confidence": normalized_reading.flame_confidence,
                    "flame_sensor_fault": normalized_reading.flame_sensor_fault,
                    "timestamp": normalized_reading.timestamp,
                    **ai_result,  # Unpack all analysis fields
                    "created_at": datetime.now(UTC_PLUS_8)
                }
                result_insert = results_collection.insert_one(result_doc)
                print(f"Analysis result saved to MongoDB with ID: {result_insert.inserted_id}")


            #Only 50 scans history, deletes 51+
            cursor = readings_collection.find({}, {"_id": 1}).sort("created_at", -1).skip(50)
            ids_to_delete = [doc["_id"] for doc in cursor]
            
            if ids_to_delete:
                readings_collection.delete_many({"_id": {"$in": ids_to_delete}})
                if results_collection is not None:
                    results_collection.delete_many({"reading_id": {"$in": ids_to_delete}})
                print(f"Deleted {len(ids_to_delete)} old scans to maintain 50 limit.")

        except Exception as db_error:
            print(f"Database error saving: {db_error}")
    else:
        print("MongoDB collection not available. Data not saved to database.")

    return ai_result

@router.get("/latest", response_model=dict)
def get_latest():
    # Always prefer the latest database record to avoid stale in-memory data.
    if readings_collection is not None:
        try:
            latest_reading = readings_collection.find_one(sort=[("created_at", -1)])
            if latest_reading:
                latest_reading = normalize_reading_doc(latest_reading)
                return {
                    "reading": {
                        "_id": latest_reading.get("_id"),
                        "device_id": latest_reading.get("device_id"),
                        "mq7": latest_reading.get("mq7"),
                        "mq135": latest_reading.get("mq135"),
                        "mq2": latest_reading.get("mq2"),
                        "dht22_temp": latest_reading.get("dht22_temp"),
                        "dht22_humidity": latest_reading.get("dht22_humidity"),
                        "flame_value": latest_reading.get("flame_value"),
                        "flame_filtered_value": latest_reading.get("flame_filtered_value"),
                        "flame_confidence": latest_reading.get("flame_confidence"),
                        "flame_sensor_fault": latest_reading.get("flame_sensor_fault"),
                        "flame_detected": latest_reading.get("flame_detected"),
                        "timestamp": serialize_datetime_to_iso(latest_reading.get("timestamp")),
                        "created_at": serialize_datetime_to_iso(latest_reading.get("created_at")),
                    },
                    "analysis": latest_reading.get("analysis"),
                }
        except Exception as db_error:
            print(f"Database error fetching latest: {db_error}")

    # Fallback for cases where DB is unavailable.
    return LATEST_ANALYSIS

@router.get("/readings", response_model=list)
def get_readings(limit: int = 10):
    if readings_collection is None:
        print("MongoDB collection not available")
        return []
    try:
        readings = list(readings_collection.find().sort("created_at", -1).limit(limit))
        print(f"Retrieved {len(readings)} readings from MongoDB")
        normalized = [normalize_reading_doc(reading) for reading in readings]
        # Ensure all datetimes are ISO strings for JSON serialization
        for doc in normalized:
            if "timestamp" in doc:
                doc["timestamp"] = serialize_datetime_to_iso(doc["timestamp"])
            if "created_at" in doc:
                doc["created_at"] = serialize_datetime_to_iso(doc["created_at"])
        return normalized
    except Exception as db_error:
        print(f"Database error retrieving readings: {db_error}")
        return []

@router.get("/health/db")
def check_db_health():
    """Check MongoDB connection health"""
    if readings_collection is None or results_collection is None:
        return {"status": "disconnected", "message": "MongoDB connection not established"}
    try:
        from app.core.database import client
        client.admin.command('ping')
        readings_count = readings_collection.count_documents({})
        results_count = results_collection.count_documents({})
        return {
            "status": "connected", 
            "readings_count": readings_count,
            "results_count": results_count
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/results", response_model=list)
def get_results(limit: int = 10, device_id: str = None):
    """Get analysis results"""
    from app.core.database import results_collection
    if results_collection is None:
        print("MongoDB results collection not available")
        return []
    try:
        filter_query = {}
        if device_id:
            filter_query["device_id"] = device_id
        results = list(results_collection.find(filter_query).sort("created_at", -1).limit(limit))
        print(f"Retrieved {len(results)} results from MongoDB")
        normalized = [normalize_reading_doc(result) for result in results]
        # Ensure all datetimes are ISO strings for JSON serialization
        for doc in normalized:
            if "timestamp" in doc:
                doc["timestamp"] = serialize_datetime_to_iso(doc["timestamp"])
            if "created_at" in doc:
                doc["created_at"] = serialize_datetime_to_iso(doc["created_at"])
        return normalized
    except Exception as db_error:
        print(f"Database error retrieving results: {db_error}")
        return []
