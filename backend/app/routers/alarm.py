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
    PARTIAL_SMOKE = "PARTIAL_SMOKE"
    SMOKE = "SMOKE"
    CO_DETECTION = "CO_DETECTION"
    GAS_LEAK = "GAS_LEAK"
    EXTREME_HEAT = "EXTREME_HEAT"
    ELECTRICAL_FIRE = "ELECTRICAL_FIRE"
    HIGH_HUMIDITY = "HIGH_HUMIDITY"
    MIXED_HAZARD = "MIXED_HAZARD"
    CONTROLLED_BURN = "CONTROLLED_BURN"
    DUSTY_AIR = "DUSTY_AIR"
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
        AlarmScenario.PARTIAL_SMOKE: {
            "reading": AlarmReading(
                mq7=35,
                mq135=62,
                mq2=180,
                dht22_temp=26.5,
                dht22_humidity=54.0,
                flame_value=3050,
                flame_detected=False,
            ),
            "analysis": AnalysisResult(
                danger=False,
                danger_level="MEDIUM",
                suspected_gas="Early smoke detection",
                confidence=0.45,
                summary="Early stage smoke pattern detected - below critical threshold.",
                reasons=[
                    "MQ-2 shows minor elevation indicating possible smoke.",
                    "Temperature and humidity near baseline.",
                    "No flame signature detected yet.",
                ],
                actions=["Monitor closely", "Check for ignition source"],
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
                    "MQ-2 is elevated indicating combustion byproducts.",
                    "MQ-7 and MQ-135 are above baseline.",
                    "No flame confirmation yet - smoke without visible fire.",
                ],
                actions=["Increase ventilation", "Check for smoke source", "Evacuate if necessary"],
                trigger_buzzer=True,
                trigger_led=True,
            ),
        },
        AlarmScenario.CO_DETECTION: {
            "reading": AlarmReading(
                mq7=320,
                mq135=95,
                mq2=145,
                dht22_temp=26.0,
                dht22_humidity=50.0,
                flame_value=3150,
                flame_detected=False,
            ),
            "analysis": AnalysisResult(
                danger=True,
                danger_level="HIGH",
                suspected_gas="Carbon monoxide (CO)",
                confidence=0.82,
                summary="Elevated carbon monoxide detected - potential appliance malfunction.",
                reasons=[
                    "MQ-7 is critically high indicating CO presence.",
                    "MQ-2 and MQ-135 show minor elevation.",
                    "No flame or combustion visible.",
                ],
                actions=["Evacuate area", "Turn off gas appliances", "Call emergency services", "Ventilate immediately"],
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
                    "MQ-2 is critically high indicating LPG/propane.",
                    "MQ-7 and MQ-135 are elevated.",
                    "Temperature remains close to the room baseline.",
                ],
                actions=["Evacuate area", "Shut off gas source", "Ventilate immediately", "Call emergency"],
                trigger_buzzer=True,
                trigger_led=True,
            ),
        },
        AlarmScenario.EXTREME_HEAT: {
            "reading": AlarmReading(
                mq7=48,
                mq135=72,
                mq2=95,
                dht22_temp=52.0,
                dht22_humidity=35.0,
                flame_value=1200,
                flame_detected=False,
            ),
            "analysis": AnalysisResult(
                danger=True,
                danger_level="CRITICAL",
                suspected_gas="Extreme heat / radiant fire",
                confidence=0.85,
                summary="Extreme temperature spike detected - possible radiant heat from fire.",
                reasons=[
                    "Temperature is critically high at 52°C.",
                    "Humidity drops significantly due to heat.",
                    "Flame sensor value drops (sensor saturation near heat source).",
                ],
                actions=["Immediate evacuation", "Alert fire department", "Move away from heat source"],
                trigger_buzzer=True,
                trigger_led=True,
            ),
        },
        AlarmScenario.ELECTRICAL_FIRE: {
            "reading": AlarmReading(
                mq7=28,
                mq135=58,
                mq2=120,
                dht22_temp=38.0,
                dht22_humidity=44.0,
                flame_value=1900,
                flame_detected=False,
            ),
            "analysis": AnalysisResult(
                danger=True,
                danger_level="HIGH",
                suspected_gas="Electrical fire / rapid heat buildup",
                confidence=0.75,
                summary="Rapid temperature rise with moderate gas elevation - electrical fire pattern.",
                reasons=[
                    "Temperature rising steeply to 38°C.",
                    "MQ-2 elevated but not extreme.",
                    "Pattern suggests thermal origin rather than chemical.",
                ],
                actions=["Cut power supply", "Evacuate", "Use extinguishing measures", "Call fire department"],
                trigger_buzzer=True,
                trigger_led=True,
            ),
        },
        AlarmScenario.HIGH_HUMIDITY: {
            "reading": AlarmReading(
                mq7=26,
                mq135=42,
                mq2=22,
                dht22_temp=26.0,
                dht22_humidity=82.0,
                flame_value=3180,
                flame_detected=False,
            ),
            "analysis": AnalysisResult(
                danger=False,
                danger_level="MEDIUM",
                suspected_gas="High moisture conditions",
                confidence=0.25,
                summary="Elevated humidity detected - possible water leak or steam source.",
                reasons=[
                    "Humidity is 82% - significantly above baseline of 56%.",
                    "Gas sensors remain normal.",
                    "No temperature or flame indicators.",
                ],
                actions=["Check for water leaks", "Improve ventilation", "Monitor mold growth"],
                trigger_buzzer=False,
                trigger_led=False,
            ),
        },
        AlarmScenario.MIXED_HAZARD: {
            "reading": AlarmReading(
                mq7=245,
                mq135=215,
                mq2=520,
                dht22_temp=29.0,
                dht22_humidity=51.0,
                flame_value=2100,
                flame_detected=False,
            ),
            "analysis": AnalysisResult(
                danger=True,
                danger_level="CRITICAL",
                suspected_gas="Multiple hazards detected",
                confidence=0.88,
                summary="Multiple gas types and heat elevation - complex fire hazard situation.",
                reasons=[
                    "MQ-7 elevated indicating CO presence.",
                    "MQ-2 very high indicating combustible gases.",
                    "MQ-135 high indicating air quality degradation.",
                    "Temperature moderately elevated.",
                ],
                actions=["Evacuate immediately", "Multiple hazards present", "Contact emergency response"],
                trigger_buzzer=True,
                trigger_led=True,
            ),
        },
        AlarmScenario.CONTROLLED_BURN: {
            "reading": AlarmReading(
                mq7=142,
                mq135=168,
                mq2=380,
                dht22_temp=34.0,
                dht22_humidity=47.0,
                flame_value=1450,
                flame_detected=True,
            ),
            "analysis": AnalysisResult(
                danger=True,
                danger_level="CRITICAL",
                suspected_gas="Low-intensity fire / controlled burn",
                confidence=0.86,
                summary="Flame detected with moderate gas readings - low-intensity fire pattern.",
                reasons=[
                    "Flame sensor is triggered.",
                    "Temperature elevated but not extreme.",
                    "Gas readings indicate active combustion.",
                ],
                actions=["Sound alarm", "Evacuate", "Extinguish or allow to burn safely"],
                trigger_buzzer=True,
                trigger_led=True,
            ),
        },
        AlarmScenario.DUSTY_AIR: {
            "reading": AlarmReading(
                mq7=22,
                mq135=156,
                mq2=45,
                dht22_temp=26.0,
                dht22_humidity=58.0,
                flame_value=3100,
                flame_detected=False,
            ),
            "analysis": AnalysisResult(
                danger=False,
                danger_level="MEDIUM",
                suspected_gas="High particulate / dust",
                confidence=0.42,
                summary="Elevated air quality issues detected - likely dust or particulate matter.",
                reasons=[
                    "MQ-135 significantly elevated indicating air quality degradation.",
                    "MQ-7 and MQ-2 remain normal.",
                    "No temperature or flame indicators.",
                ],
                actions=["Check for dust sources", "Improve ventilation", "Clean air filters"],
                trigger_buzzer=False,
                trigger_led=False,
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