from datetime import datetime, timezone
from enum import Enum

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.schemas.sensor import AnalysisResult

router = APIRouter(prefix="/api",
                   tags=["alarms"])


class AlarmScenario(str, Enum):
    LIVE = "LIVE"
    SAFE = "SAFE"
    WARM = "WARM"
    SMOKE = "SMOKE"
    GAS_LEAK = "GAS_LEAK"
    FIRE_TEST = "FIRE_TEST"


class AlarmReading(BaseModel):
    device_id: str = "manual-test"
    mq7: float
    mq135: float
    mq2: float
    dht22_temp: float
    dht22_humidity: float
    flame_value: float | None = None
    flame_detected: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AlarmState(BaseModel):
    is_active: bool
    feed_paused: bool = False
    scenario: str = AlarmScenario.LIVE
    reading: AlarmReading | None = None
    analysis: AnalysisResult | None = None


class AlarmUpdate(BaseModel):
    is_active: bool | None = None
    feed_paused: bool | None = None
    scenario: str | None = None


def build_alarm_preview(scenario: str) -> tuple[AlarmReading | None, AnalysisResult | None]:
    if scenario == AlarmScenario.LIVE:
        return None, None

    profiles = {
        AlarmScenario.SAFE: {
            "reading": AlarmReading(
                mq7=24,
                mq135=38,
                mq2=20,
                dht22_temp=26.0,
                dht22_humidity=56.0,
                flame_value=3200,
                flame_detected=False,
            ),
            "analysis": AnalysisResult(
                danger=False,
                danger_level="LOW",
                suspected_gas="None",
                confidence=0.05,
                summary="Safe baseline test at the room's normal ambient temperature of 26°C.",
                reasons=[
                    "Room temperature remains near 26°C.",
                    "Gas sensor values are within normal range.",
                    "No flame is detected.",
                ],
                actions=["Continue monitoring"],
                trigger_buzzer=False,
                trigger_led=False,
            ),
        },
        AlarmScenario.WARM: {
            "reading": AlarmReading(
                mq7=32,
                mq135=44,
                mq2=28,
                dht22_temp=30.0,
                dht22_humidity=60.0,
                flame_value=3000,
                flame_detected=False,
            ),
            "analysis": AnalysisResult(
                danger=False,
                danger_level="MEDIUM",
                suspected_gas="Heat / ventilation change",
                confidence=0.35,
                summary="Warm ambient variation without a flame signature.",
                reasons=[
                    "Temperature is higher than the 26°C baseline.",
                    "Humidity is typical for the room.",
                    "No flame is detected.",
                ],
                actions=["Observe for further change"],
                trigger_buzzer=False,
                trigger_led=False,
            ),
        },
        AlarmScenario.SMOKE: {
            "reading": AlarmReading(
                mq7=58,
                mq135=126,
                mq2=455,
                dht22_temp=27.0,
                dht22_humidity=53.0,
                flame_value=2880,
                flame_detected=False,
            ),
            "analysis": AnalysisResult(
                danger=True,
                danger_level="HIGH",
                suspected_gas="Smoke / combustion",
                confidence=0.78,
                summary="Smoke pattern detected with elevated gas readings.",
                reasons=[
                    "MQ-2 is elevated.",
                    "MQ-7 and MQ-135 are above baseline.",
                    "No flame confirmation yet.",
                ],
                actions=["Increase ventilation", "Check for smoke source"],
                trigger_buzzer=True,
                trigger_led=True,
            ),
        },
        AlarmScenario.GAS_LEAK: {
            "reading": AlarmReading(
                mq7=196,
                mq135=182,
                mq2=810,
                dht22_temp=26.0,
                dht22_humidity=49.0,
                flame_value=2950,
                flame_detected=False,
            ),
            "analysis": AnalysisResult(
                danger=True,
                danger_level="CRITICAL",
                suspected_gas="LPG / combustible gas",
                confidence=0.9,
                summary="Critical gas leak test with no flame signature.",
                reasons=[
                    "MQ-2 is critically high.",
                    "MQ-7 and MQ-135 are elevated.",
                    "Temperature remains close to the room baseline.",
                ],
                actions=["Evacuate area", "Shut off gas source", "Ventilate immediately"],
                trigger_buzzer=True,
                trigger_led=True,
            ),
        },
        AlarmScenario.FIRE_TEST: {
            "reading": AlarmReading(
                mq7=278,
                mq135=236,
                mq2=612,
                dht22_temp=32.0,
                dht22_humidity=42.0,
                flame_value=640,
                flame_detected=True,
            ),
            "analysis": AnalysisResult(
                danger=True,
                danger_level="CRITICAL",
                suspected_gas="Open flame / fire",
                confidence=0.97,
                summary="Direct fire test with flame sensor confirmation.",
                reasons=[
                    "Flame sensor is actively triggered.",
                    "Gas readings are elevated.",
                    "Temperature is above the room baseline.",
                ],
                actions=["Trigger evacuation", "Sound alarm", "Call emergency response"],
                trigger_buzzer=True,
                trigger_led=True,
            ),
        },
    }

    profile = profiles.get(scenario)
    if profile is None:
        return None, None

    return profile["reading"], profile["analysis"]

current_alarm_state = {
    "is_active": False,
    "feed_paused": False,
    "scenario": AlarmScenario.LIVE,
}

@router.get("/alarm", response_model=AlarmState)
def get_alarm_state():
    reading, analysis = build_alarm_preview(current_alarm_state.get("scenario", AlarmScenario.LIVE))
    return {
        "is_active": current_alarm_state["is_active"],
        "feed_paused": current_alarm_state.get("feed_paused", False),
        "scenario": current_alarm_state.get("scenario", AlarmScenario.LIVE),
        "reading": reading,
        "analysis": analysis,
    }

@router.post("/alarm", response_model=AlarmState)
def set_alarm_state(state: AlarmUpdate):
    if state.is_active is not None:
        current_alarm_state["is_active"] = state.is_active
    if state.feed_paused is not None:
        current_alarm_state["feed_paused"] = state.feed_paused
    if state.scenario is not None:
        current_alarm_state["scenario"] = state.scenario

    reading, analysis = build_alarm_preview(current_alarm_state.get("scenario", AlarmScenario.LIVE))
    return {
        "is_active": current_alarm_state["is_active"],
        "feed_paused": current_alarm_state["feed_paused"],
        "scenario": current_alarm_state["scenario"],
        "reading": reading,
        "analysis": analysis,
    }