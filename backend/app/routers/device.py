from fastapi import APIRouter, HTTPException
from app.schemas.sensor import SensorReading, AnalysisResult
from app.services.analysis import heuristic_risk
from app.services.openai_service import analyze_with_openai
from app.state import LATEST_ANALYSIS
from app.core.database import readings_collection, results_collection
from datetime import datetime

router = APIRouter(prefix="/api", tags=["device"])

@router.post("/readings", response_model=AnalysisResult)
def post_reading(reading: SensorReading):
    heuristic = heuristic_risk(reading)

    try:
        ai_result = analyze_with_openai(
            reading.model_dump(),
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

    # Safety override: never let the model suppress an obvious flame event
    if reading.flame_detected:
        ai_result["danger"] = True
        ai_result["danger_level"] = "CRITICAL"
        ai_result["trigger_buzzer"] = True
        ai_result["trigger_led"] = True
        if "Flame sensor detected fire" not in ai_result["reasons"]:
            ai_result["reasons"] = ["Flame sensor detected fire"] + ai_result.get("reasons", [])

    LATEST_ANALYSIS["reading"] = reading.model_dump()
    LATEST_ANALYSIS["analysis"] = ai_result

    # Save to database
    if readings_collection is not None:
        try:
            reading_doc = {
                "device_id": reading.device_id,
                "mq7": reading.mq7,
                "mq135": reading.mq135,
                "mq2": reading.mq2,
                "dht22_temp": reading.dht22_temp,
                "dht22_humidity": reading.dht22_humidity,
                "flame_detected": reading.flame_detected,
                "timestamp": reading.timestamp,
                "analysis": ai_result,
                "created_at": datetime.utcnow()
            }
            result = readings_collection.insert_one(reading_doc)
            print(f"Reading saved to MongoDB with ID: {result.inserted_id}")
            
            # Save results to separate collection
            if results_collection is not None:
                result_doc = {
                    "device_id": reading.device_id,
                    "reading_id": result.inserted_id,
                    "timestamp": reading.timestamp,
                    **ai_result,  # Unpack all analysis fields
                    "created_at": datetime.utcnow()
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
    # If no analysis in memory, fetch the latest from database
    if not LATEST_ANALYSIS.get("analysis") and readings_collection is not None:
        try:
            latest_reading = readings_collection.find_one(sort=[("created_at", -1)])
            if latest_reading:
                latest_reading["_id"] = str(latest_reading["_id"])
                return {
                    "reading": {
                        "mq7": latest_reading.get("mq7"),
                        "mq135": latest_reading.get("mq135"),
                        "mq2": latest_reading.get("mq2"),
                        "dht22_temp": latest_reading.get("dht22_temp"),
                        "dht22_humidity": latest_reading.get("dht22_humidity"),
                        "flame_detected": latest_reading.get("flame_detected"),
                        "timestamp": latest_reading.get("timestamp"),
                    },
                    "analysis": latest_reading.get("analysis"),
                }
        except Exception as db_error:
            print(f"Database error fetching latest: {db_error}")
    return LATEST_ANALYSIS

@router.get("/readings", response_model=list)
def get_readings(limit: int = 10):
    if readings_collection is None:
        print("MongoDB collection not available")
        return []
    try:
        readings = list(readings_collection.find().sort("created_at", -1).limit(limit))
        print(f"Retrieved {len(readings)} readings from MongoDB")
        # Convert ObjectId to string for JSON serialization
        for reading in readings:
            reading["_id"] = str(reading["_id"])
        return readings
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
        # Convert ObjectId to string for JSON serialization
        for result in results:
            result["_id"] = str(result["_id"])
            if "reading_id" in result:
                result["reading_id"] = str(result["reading_id"])
        return results
    except Exception as db_error:
        print(f"Database error retrieving results: {db_error}")
        return []