from fastapi import APIRouter, HTTPException
from app.schemas.sensor import SensorReading, AnalysisResult
from app.services.analysis import heuristic_risk
from app.services.openai_service import analyze_with_openai
from app.state import LATEST_ANALYSIS

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

    return ai_result

@router.get("/latest", response_model=dict)
def get_latest():
    return LATEST_ANALYSIS