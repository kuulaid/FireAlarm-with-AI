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


# Comprehensive multi-reading scenario database
SCENARIO_PROGRESSIONS = {
    AlarmScenario.SAFE: [
        (AlarmReading(mq7=24, mq135=38, mq2=20, dht22_temp=26.0, dht22_humidity=56.0, flame_value=3200, flame_detected=False),
         AnalysisResult(danger=False, danger_level="LOW", suspected_gas="None", confidence=0.05, summary="Safe baseline test at 26°C.",
             reasons=["Room temperature remains near 26°C.", "Gas sensor values are within normal range.", "No flame is detected."],
             actions=["Continue monitoring"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=23, mq135=39, mq2=21, dht22_temp=26.1, dht22_humidity=55.8, flame_value=3210, flame_detected=False),
         AnalysisResult(danger=False, danger_level="LOW", suspected_gas="None", confidence=0.04, summary="Safe baseline - stable conditions.",
             reasons=["All sensors within normal range.", "No change detected."], actions=["Continue monitoring"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=25, mq135=37, mq2=19, dht22_temp=25.9, dht22_humidity=56.2, flame_value=3190, flame_detected=False),
         AnalysisResult(danger=False, danger_level="LOW", suspected_gas="None", confidence=0.05, summary="Safe baseline - stable conditions.",
             reasons=["All sensors within normal range.", "No change detected."], actions=["Continue monitoring"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=24, mq135=38, mq2=20, dht22_temp=26.0, dht22_humidity=56.0, flame_value=3200, flame_detected=False),
         AnalysisResult(danger=False, danger_level="LOW", suspected_gas="None", confidence=0.05, summary="Safe baseline - stable conditions.",
             reasons=["All sensors within normal range.", "No change detected."], actions=["Continue monitoring"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=24, mq135=38, mq2=20, dht22_temp=26.0, dht22_humidity=56.0, flame_value=3200, flame_detected=False),
         AnalysisResult(danger=False, danger_level="LOW", suspected_gas="None", confidence=0.05, summary="Safe baseline - stable conditions.",
             reasons=["All sensors within normal range.", "No change detected."], actions=["Continue monitoring"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=24, mq135=38, mq2=20, dht22_temp=26.0, dht22_humidity=56.0, flame_value=3200, flame_detected=False),
         AnalysisResult(danger=False, danger_level="LOW", suspected_gas="None", confidence=0.05, summary="Safe baseline - stable conditions.",
             reasons=["All sensors within normal range.", "No change detected."], actions=["Continue monitoring"], trigger_buzzer=False, trigger_led=False)),
    ],
    AlarmScenario.WARM: [
        (AlarmReading(mq7=26, mq135=40, mq2=22, dht22_temp=27.5, dht22_humidity=58.0, flame_value=3100, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Heat / ventilation change", confidence=0.25, summary="Temperature beginning to rise.",
             reasons=["Slight temperature increase to 27.5°C.", "Gas levels stable."], actions=["Observe for further change"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=28, mq135=41, mq2=24, dht22_temp=28.5, dht22_humidity=59.0, flame_value=3080, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Heat / ventilation change", confidence=0.30, summary="Room temperature continuing to rise.",
             reasons=["Temperature at 28.5°C.", "No flame or hazardous gas."], actions=["Check ventilation", "Observe"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=30, mq135=42, mq2=26, dht22_temp=29.5, dht22_humidity=59.5, flame_value=3050, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Heat / ventilation change", confidence=0.33, summary="Room temperature elevated to 29.5°C.",
             reasons=["Temperature rising steadily.", "Gas sensors remain normal."], actions=["Check ventilation", "Monitor temperature"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=32, mq135=44, mq2=28, dht22_temp=30.0, dht22_humidity=60.0, flame_value=3000, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Heat / ventilation change", confidence=0.35, summary="Warm ambient variation without flame.",
             reasons=["Temperature is higher than 26°C baseline.", "Humidity typical."], actions=["Observe for further change"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=31, mq135=43, mq2=27, dht22_temp=29.8, dht22_humidity=60.2, flame_value=3010, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Heat / ventilation change", confidence=0.34, summary="Temperature slightly decreasing.",
             reasons=["Heat levels stabilizing.", "No hazards detected."], actions=["Continue monitoring"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=30, mq135=42, mq2=26, dht22_temp=29.2, dht22_humidity=60.5, flame_value=3020, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Heat / ventilation change", confidence=0.33, summary="Room cooling toward baseline.",
             reasons=["Temperature declining.", "No hazardous indicators."], actions=["Continue monitoring"], trigger_buzzer=False, trigger_led=False)),
    ],
    AlarmScenario.PARTIAL_SMOKE: [
        (AlarmReading(mq7=28, mq135=45, mq2=60, dht22_temp=26.2, dht22_humidity=54.0, flame_value=3120, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Early smoke detection", confidence=0.35, summary="Early stage smoke - below critical.",
             reasons=["MQ-2 showing minor elevation.", "Temperature and humidity near baseline."], actions=["Monitor closely", "Check for ignition source"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=32, mq135=52, mq2=110, dht22_temp=26.5, dht22_humidity=53.5, flame_value=3080, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Possible smoke source", confidence=0.42, summary="Smoke indicators increasing slightly.",
             reasons=["MQ-2 climbing to 110.", "Other sensors near baseline."], actions=["Investigate immediately", "Check for fire sources"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=35, mq135=58, mq2=150, dht22_temp=26.7, dht22_humidity=53.2, flame_value=3050, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Early smoke detection", confidence=0.45, summary="Smoke pattern becoming clearer.",
             reasons=["MQ-2 at 150 - moderate smoke.", "Temperature starting to rise slightly."], actions=["Search for fire", "Prepare evacuation"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=34, mq135=55, mq2=140, dht22_temp=26.6, dht22_humidity=53.4, flame_value=3060, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Early smoke detection", confidence=0.44, summary="Smoke levels stabilizing.",
             reasons=["MQ-2 at 140.", "No rapid escalation."], actions=["Monitor closely", "Locate source"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=36, mq135=60, mq2=170, dht22_temp=26.8, dht22_humidity=53.1, flame_value=3040, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Smoke increasing", confidence=0.48, summary="Smoke intensity increasing again.",
             reasons=["MQ-2 climbing to 170.", "Potential escalation to high danger."], actions=["Heighten alert", "Emergency response"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=35, mq135=62, mq2=180, dht22_temp=26.5, dht22_humidity=54.0, flame_value=3050, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Early smoke detection", confidence=0.45, summary="Early stage smoke - below critical.",
             reasons=["MQ-2 shows minor elevation.", "Temperature and humidity near baseline.", "No flame detected."],
             actions=["Monitor closely", "Check for ignition source"], trigger_buzzer=False, trigger_led=False)),
    ],
    AlarmScenario.SMOKE: [
        (AlarmReading(mq7=42, mq135=95, mq2=320, dht22_temp=27.2, dht22_humidity=52.8, flame_value=2920, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Smoke / combustion", confidence=0.70, summary="Smoke pattern detected - alarm activating.",
             reasons=["MQ-2 elevated to 320.", "Temperature rising with smoke."], actions=["Ventilation", "Check for smoke source", "Evacuate"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=50, mq135=110, mq2=380, dht22_temp=27.5, dht22_humidity=52.5, flame_value=2880, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Smoke / combustion", confidence=0.75, summary="Heavy smoke pattern - strong alarm.",
             reasons=["MQ-2 escalating to 380.", "MQ-7 and MQ-135 elevated."], actions=["Immediate ventilation", "Locate fire source", "Begin evacuation"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=58, mq135=126, mq2=455, dht22_temp=27.0, dht22_humidity=53.0, flame_value=2880, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Smoke / combustion", confidence=0.78, summary="Smoke pattern with elevated gas readings.",
             reasons=["MQ-2 elevated.", "MQ-7 and MQ-135 above baseline.", "No flame confirmation yet."],
             actions=["Ventilation", "Check smoke source"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=54, mq135=120, mq2=420, dht22_temp=27.3, dht22_humidity=52.7, flame_value=2890, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Smoke / combustion", confidence=0.76, summary="Smoke continuing at elevated levels.",
             reasons=["Heavy combustion byproducts.", "Sustained gas elevation."], actions=["Ventilate immediately", "Search for source"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=48, mq135=115, mq2=390, dht22_temp=27.1, dht22_humidity=52.9, flame_value=2900, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Smoke / combustion", confidence=0.73, summary="Smoke levels declining slightly.",
             reasons=["Gas readings decreasing.", "Possible ventilation working."], actions=["Continue ventilation", "Monitor levels"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=42, mq135=108, mq2=340, dht22_temp=27.0, dht22_humidity=53.1, flame_value=2910, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Smoke / combustion", confidence=0.71, summary="Smoke clearing but dangerous.",
             reasons=["Gas levels declining.", "Monitor for re-escalation."], actions=["Maintain ventilation", "Continue evacuation"], trigger_buzzer=True, trigger_led=True)),
    ],
    AlarmScenario.CO_DETECTION: [
        (AlarmReading(mq7=180, mq135=85, mq2=120, dht22_temp=26.2, dht22_humidity=50.5, flame_value=3160, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Possible CO detection", confidence=0.70, summary="Elevated CO levels detected.",
             reasons=["MQ-7 significantly elevated to 180.", "Other sensors near normal."], actions=["Check gas appliances", "Ventilate", "Call emergency"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=240, mq135=88, mq2=132, dht22_temp=26.3, dht22_humidity=50.3, flame_value=3140, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Carbon monoxide (CO)", confidence=0.78, summary="CO levels rising - appliance malfunction.",
             reasons=["MQ-7 elevated to 240.", "Rapid increase trend."], actions=["Evacuate area", "Turn off gas", "Call emergency"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=320, mq135=95, mq2=145, dht22_temp=26.0, dht22_humidity=50.0, flame_value=3150, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Carbon monoxide (CO)", confidence=0.82, summary="Elevated carbon monoxide detected.",
             reasons=["MQ-7 critically high.", "No flame or combustion.", "Minor gas elevation."],
             actions=["Evacuate area", "Turn off gas appliances", "Call emergency", "Ventilate immediately"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=300, mq135=92, mq2=140, dht22_temp=26.1, dht22_humidity=50.2, flame_value=3155, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Carbon monoxide (CO)", confidence=0.80, summary="CO levels sustained - still malfunctioning.",
             reasons=["MQ-7 critically high.", "No improvement."], actions=["Evacuate", "Keep ventilated"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=350, mq135=98, mq2=155, dht22_temp=26.0, dht22_humidity=49.8, flame_value=3145, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Carbon monoxide (CO)", confidence=0.85, summary="CO escalating to critical.",
             reasons=["MQ-7 extremely high at 350.", "Dangerous concentration."], actions=["Immediate evacuation", "Emergency services", "Do not return"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=320, mq135=95, mq2=145, dht22_temp=26.0, dht22_humidity=50.0, flame_value=3150, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Carbon monoxide (CO)", confidence=0.82, summary="CO levels remain elevated.",
             reasons=["Sustained high CO.", "Ongoing hazard."], actions=["Remain evacuated", "Professional assessment"], trigger_buzzer=True, trigger_led=True)),
    ],
    AlarmScenario.GAS_LEAK: [
        (AlarmReading(mq7=120, mq135=130, mq2=480, dht22_temp=26.1, dht22_humidity=49.5, flame_value=2980, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="LPG / combustible gas", confidence=0.82, summary="Gas leak detected - critical.",
             reasons=["MQ-2 very high at 480.", "MQ-7 and MQ-135 elevated."], actions=["Evacuate immediately", "Turn off gas", "Call emergency"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=150, mq135=160, mq2=650, dht22_temp=26.0, dht22_humidity=49.2, flame_value=2960, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="LPG / combustible gas", confidence=0.87, summary="Gas leak escalating rapidly.",
             reasons=["All sensors critical elevation.", "Rapid concentration."], actions=["Evacuate immediately", "No ignition", "Hazmat response"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=196, mq135=182, mq2=810, dht22_temp=26.0, dht22_humidity=49.0, flame_value=2950, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="LPG / combustible gas", confidence=0.9, summary="Critical gas leak with no flame.",
             reasons=["MQ-2 critically high.", "MQ-7 and MQ-135 elevated.", "Temperature near baseline."],
             actions=["Evacuate area", "Shut off gas source", "Ventilate immediately", "Call emergency"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=175, mq135=175, mq2=750, dht22_temp=26.0, dht22_humidity=49.1, flame_value=2955, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="LPG / combustible gas", confidence=0.88, summary="Gas leak persisting - still critical.",
             reasons=["Sustained high gas.", "Explosive atmosphere."], actions=["Remain evacuated", "Professional response"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=160, mq135=170, mq2=700, dht22_temp=26.0, dht22_humidity=49.3, flame_value=2960, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="LPG / combustible gas", confidence=0.86, summary="Gas levels declining slightly.",
             reasons=["Leak rate slowing.", "Danger persists."], actions=["Remain outside", "Monitor from safe distance"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=140, mq135=160, mq2=620, dht22_temp=26.1, dht22_humidity=49.2, flame_value=2970, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="LPG / combustible gas", confidence=0.84, summary="Gas continuing but concentration dropping.",
             reasons=["Natural dispersion.", "Still dangerous."], actions=["Continue evacuation", "Await all-clear"], trigger_buzzer=True, trigger_led=True)),
    ],
    AlarmScenario.EXTREME_HEAT: [
        (AlarmReading(mq7=35, mq135=58, mq2=72, dht22_temp=38.5, dht22_humidity=38.0, flame_value=1950, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Extreme heat / radiant fire", confidence=0.75, summary="Significant temperature spike.",
             reasons=["Temperature at 38.5°C.", "Humidity dropping."], actions=["Search for heat source", "Prepare evacuation"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=40, mq135=65, mq2=80, dht22_temp=45.0, dht22_humidity=36.5, flame_value=1600, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Extreme heat / fire", confidence=0.88, summary="Temperature critically elevated.",
             reasons=["Temperature at 45°C.", "Rapid heat buildup."], actions=["Immediate evacuation", "Do not approach heat source"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=48, mq135=72, mq2=95, dht22_temp=52.0, dht22_humidity=35.0, flame_value=1200, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Extreme heat / radiant fire", confidence=0.85, summary="Extreme temperature detected.",
             reasons=["Temperature critically high at 52°C.", "Humidity drops due to heat.", "Flame sensor saturated."],
             actions=["Immediate evacuation", "Alert fire department", "Move away from heat source"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=46, mq135=70, mq2=88, dht22_temp=50.5, dht22_humidity=35.5, flame_value=1250, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Extreme heat / fire", confidence=0.84, summary="Extreme heat persisting.",
             reasons=["Temperature sustained above 50°C.", "Active fire likely."], actions=["Evacuate completely", "Professional firefighting"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=42, mq135=68, mq2=82, dht22_temp=48.0, dht22_humidity=36.0, flame_value=1400, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Extreme heat / fire", confidence=0.82, summary="Heat declining slightly.",
             reasons=["Temperature dropping to 48°C.", "Fire may be contained."], actions=["Remain evacuated", "Await firefighters"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=38, mq135=65, mq2=76, dht22_temp=44.0, dht22_humidity=37.0, flame_value=1550, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Extreme heat / fire", confidence=0.80, summary="Extreme heat declining.",
             reasons=["Temperature down to 44°C.", "Improvement detected."], actions=["Stay clear", "Monitor from distance"], trigger_buzzer=True, trigger_led=True)),
    ],
    AlarmScenario.ELECTRICAL_FIRE: [
        (AlarmReading(mq7=20, mq135=48, mq2=80, dht22_temp=32.5, dht22_humidity=46.0, flame_value=2400, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Electrical fire / rapid heat", confidence=0.68, summary="Temperature rising rapidly.",
             reasons=["Temperature at 32.5°C.", "Moderate smoke."], actions=["Cut power", "Check electrical panel", "Prepare evacuation"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=24, mq135=55, mq2=95, dht22_temp=35.5, dht22_humidity=45.2, flame_value=2200, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Electrical fire / rapid heat", confidence=0.72, summary="Rapid heat escalation confirmed.",
             reasons=["Temperature to 35.5°C.", "Gas indicators increasing."], actions=["Shut off electricity", "Evacuate", "Call fire department"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=28, mq135=58, mq2=120, dht22_temp=38.0, dht22_humidity=44.0, flame_value=1900, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Electrical fire / rapid heat", confidence=0.75, summary="Rapid rise with moderate gas.",
             reasons=["Temperature at 38°C.", "MQ-2 elevated but not extreme.", "Thermal origin pattern."],
             actions=["Cut power supply", "Evacuate", "Use extinguishing", "Call fire department"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=26, mq135=56, mq2=110, dht22_temp=37.2, dht22_humidity=44.5, flame_value=2000, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Electrical fire / rapid heat", confidence=0.73, summary="Fire continuing - sustained heat.",
             reasons=["Temperature at 37.2°C.", "Fire spreading."], actions=["Evacuate immediately", "Power off"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=23, mq135=54, mq2=102, dht22_temp=36.0, dht22_humidity=45.0, flame_value=2050, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Electrical fire / rapid heat", confidence=0.71, summary="Heat levels declining.",
             reasons=["Temperature dropping to 36°C.", "Smoke decreasing."], actions=["Continue evacuation", "Await firefighters"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=20, mq135=52, mq2=95, dht22_temp=34.5, dht22_humidity=45.5, flame_value=2100, flame_detected=False),
         AnalysisResult(danger=True, danger_level="HIGH", suspected_gas="Electrical fire / rapid heat", confidence=0.69, summary="Fire weakening - suppression working.",
             reasons=["Temperature decreasing.", "Threat declining."], actions=["Remain evacuated", "Professional assessment"], trigger_buzzer=True, trigger_led=True)),
    ],
    AlarmScenario.HIGH_HUMIDITY: [
        (AlarmReading(mq7=24, mq135=40, mq2=20, dht22_temp=26.1, dht22_humidity=68.0, flame_value=3190, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="High moisture conditions", confidence=0.20, summary="Humidity beginning to rise.",
             reasons=["Humidity at 68%.", "Gas sensors normal."], actions=["Check for leaks", "Check HVAC"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=25, mq135=41, mq2=21, dht22_temp=26.0, dht22_humidity=74.0, flame_value=3185, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="High moisture conditions", confidence=0.25, summary="Humidity increasing to 74%.",
             reasons=["Significant moisture rise.", "May indicate active leak."], actions=["Inspect for water intrusion", "Improve ventilation"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=25, mq135=41, mq2=21, dht22_temp=26.0, dht22_humidity=78.0, flame_value=3182, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="High moisture conditions", confidence=0.30, summary="Very high humidity detected.",
             reasons=["Humidity at 78%.", "Moisture continuously increasing."], actions=["Find and stop water source", "Dehumidify area"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=26, mq135=42, mq2=22, dht22_temp=26.0, dht22_humidity=82.0, flame_value=3180, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="High moisture conditions", confidence=0.25, summary="Elevated humidity - water leak possible.",
             reasons=["Humidity 82% - above baseline 56%.", "Gas sensors normal.", "No temperature or flame."],
             actions=["Check water leaks", "Improve ventilation", "Monitor mold growth"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=26, mq135=41, mq2=22, dht22_temp=26.0, dht22_humidity=80.0, flame_value=3181, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="High moisture conditions", confidence=0.24, summary="Humidity stabilizing at elevated state.",
             reasons=["Steady high humidity around 80%.", "Water source continuous."], actions=["Locate water source"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=25, mq135=41, mq2=21, dht22_temp=26.0, dht22_humidity=76.0, flame_value=3183, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="High moisture conditions", confidence=0.23, summary="Humidity declining with intervention.",
             reasons=["Dehumidification working.", "Water source addressed."], actions=["Continue ventilation", "Monitor mold"], trigger_buzzer=False, trigger_led=False)),
    ],
    AlarmScenario.MIXED_HAZARD: [
        (AlarmReading(mq7=140, mq135=150, mq2=350, dht22_temp=27.5, dht22_humidity=52.5, flame_value=2400, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Multiple hazards detected", confidence=0.82, summary="Multiple dangers detected.",
             reasons=["CO present.", "Combustible gases.", "Temperature elevated."], actions=["Evacuate immediately", "Multiple hazard response"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=180, mq135=185, mq2=450, dht22_temp=28.0, dht22_humidity=51.8, flame_value=2300, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Multiple hazards escalating", confidence=0.86, summary="Multiple hazard concentrations rising.",
             reasons=["CO at 180.", "Combustible gases at 450.", "Extreme complexity."], actions=["Evacuate all personnel", "Hazmat team required"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=245, mq135=215, mq2=520, dht22_temp=29.0, dht22_humidity=51.0, flame_value=2100, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Multiple hazards detected", confidence=0.88, summary="Multiple gas types and heat elevation.",
             reasons=["MQ-7 elevated.", "MQ-2 very high.", "MQ-135 high.", "Temperature elevated."],
             actions=["Evacuate immediately", "Multiple hazards", "Contact emergency response"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=225, mq135=210, mq2=490, dht22_temp=28.5, dht22_humidity=51.3, flame_value=2150, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Multiple hazards sustained", confidence=0.87, summary="Hazards continuing at critical levels.",
             reasons=["All sensors critical.", "Sustained danger."], actions=["Stay evacuated", "Professional response ongoing"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=190, mq135=190, mq2=420, dht22_temp=28.0, dht22_humidity=51.5, flame_value=2200, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Multiple hazards declining", confidence=0.84, summary="Hazard levels declining.",
             reasons=["Concentrations dropping.", "Positive trend."], actions=["Continue evacuation"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=160, mq135=170, mq2=360, dht22_temp=27.5, dht22_humidity=52.0, flame_value=2250, flame_detected=False),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Multiple hazards clearing", confidence=0.82, summary="Hazards improving but still critical.",
             reasons=["Concentrations falling.", "Evacuation necessary."], actions=["Monitor from safe distance"], trigger_buzzer=True, trigger_led=True)),
    ],
    AlarmScenario.CONTROLLED_BURN: [
        (AlarmReading(mq7=85, mq135=120, mq2=280, dht22_temp=31.0, dht22_humidity=49.0, flame_value=2050, flame_detected=True),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Low-intensity fire", confidence=0.80, summary="Flame detected - fire alarm activated.",
             reasons=["Flame sensor triggered.", "Gas elevated.", "Temperature rising."], actions=["Fire response", "Begin evacuation"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=110, mq135=145, mq2=320, dht22_temp=32.2, dht22_humidity=48.5, flame_value=1750, flame_detected=True),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Medium-intensity fire", confidence=0.84, summary="Fire intensifying - rapid response needed.",
             reasons=["Flame growing.", "Temperature at 32.2°C.", "Gas escalating."], actions=["Immediate evacuation", "Alert fire department"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=142, mq135=168, mq2=380, dht22_temp=34.0, dht22_humidity=47.0, flame_value=1450, flame_detected=True),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Low-intensity fire", confidence=0.86, summary="Flame with moderate gas readings.",
             reasons=["Flame sensor triggered.", "Temperature elevated.", "Active combustion."],
             actions=["Sound alarm", "Evacuate", "Extinguish or burn safely"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=135, mq135=162, mq2=360, dht22_temp=33.5, dht22_humidity=47.5, flame_value=1500, flame_detected=True),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Fire in progress", confidence=0.85, summary="Fire at moderate intensity.",
             reasons=["Flame confirmed active.", "Gas and heat sustained."], actions=["Fire suppression", "Maintain evacuation"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=120, mq135=155, mq2=340, dht22_temp=33.0, dht22_humidity=48.0, flame_value=1600, flame_detected=True),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Fire being suppressed", confidence=0.83, summary="Fire beginning to be contained.",
             reasons=["Flame stabilizing.", "Gas levels plateauing."], actions=["Continue suppression", "Monitor closely"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=100, mq135=140, mq2=310, dht22_temp=31.5, dht22_humidity=48.5, flame_value=1750, flame_detected=True),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Fire weakening", confidence=0.81, summary="Fire successfully suppressing.",
             reasons=["Flame fading.", "Temperature and gases declining."], actions=["Continue suppression", "Await all-clear"], trigger_buzzer=True, trigger_led=True)),
    ],
    AlarmScenario.DUSTY_AIR: [
        (AlarmReading(mq7=20, mq135=95, mq2=35, dht22_temp=26.1, dht22_humidity=58.5, flame_value=3110, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Dust / particulates", confidence=0.35, summary="Air quality degrading.",
             reasons=["MQ-135 at 95.", "Other sensors normal.", "No flame."], actions=["Check dust sources", "Improve ventilation"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=21, mq135=120, mq2=38, dht22_temp=26.0, dht22_humidity=58.2, flame_value=3105, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="High particulate matter", confidence=0.40, summary="Air quality poor.",
             reasons=["MQ-135 at 120.", "Major particulate."], actions=["Activate air filters", "Ventilate area"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=22, mq135=156, mq2=45, dht22_temp=26.0, dht22_humidity=58.0, flame_value=3100, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="High particulate / dust", confidence=0.42, summary="Elevated air quality issues.",
             reasons=["MQ-135 significantly elevated.", "MQ-7 and MQ-2 normal.", "No temperature or flame."],
             actions=["Check dust sources", "Improve ventilation", "Clean air filters"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=21, mq135=150, mq2=42, dht22_temp=26.0, dht22_humidity=58.1, flame_value=3102, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="High particulate matter", confidence=0.40, summary="Air quality remains poor.",
             reasons=["MQ-135 at 150.", "Improvement beginning."], actions=["Continue ventilation", "Clean filters"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=20, mq135=130, mq2=38, dht22_temp=26.0, dht22_humidity=58.2, flame_value=3107, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Particulate declining", confidence=0.38, summary="Air quality improving.",
             reasons=["MQ-135 down to 130.", "Dust clearing."], actions=["Continue filters", "Monitor air quality"], trigger_buzzer=False, trigger_led=False)),
        (AlarmReading(mq7=20, mq135=110, mq2=36, dht22_temp=26.0, dht22_humidity=58.3, flame_value=3109, flame_detected=False),
         AnalysisResult(danger=False, danger_level="MEDIUM", suspected_gas="Dust clearing", confidence=0.35, summary="Air quality returning to normal.",
             reasons=["MQ-135 near-normal at 110.", "Effective ventilation."], actions=["Maintain filters", "Return to normal"], trigger_buzzer=False, trigger_led=False)),
    ],
    AlarmScenario.FIRE_TEST: [
        (AlarmReading(mq7=150, mq135=165, mq2=400, dht22_temp=28.5, dht22_humidity=45.0, flame_value=1800, flame_detected=True),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Fire ignition detected", confidence=0.92, summary="Open flame confirmed.",
             reasons=["Flame sensor triggered.", "Temperature rising.", "Gas escalating."], actions=["Activate fire alarm", "Begin evacuation", "Alert fire department"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=200, mq135=200, mq2=520, dht22_temp=30.0, dht22_humidity=43.5, flame_value=1400, flame_detected=True),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Fire spreading", confidence=0.95, summary="Fire escalating rapidly.",
             reasons=["Active flame.", "Temperature at 30°C and rising.", "All hazard indicators critical."],
             actions=["Full evacuation", "Emergency response required"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=278, mq135=236, mq2=612, dht22_temp=32.0, dht22_humidity=42.0, flame_value=640, flame_detected=True),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Open flame / fire", confidence=0.97, summary="Fire test with flame confirmation.",
             reasons=["Flame sensor actively triggered.", "Gas readings elevated.", "Temperature above baseline."],
             actions=["Trigger evacuation", "Sound alarm", "Call emergency response"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=260, mq135=220, mq2=580, dht22_temp=31.5, dht22_humidity=42.5, flame_value=750, flame_detected=True),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Fire in full effect", confidence=0.96, summary="Full fire scenario.",
             reasons=["Sustained flame presence.", "Maximum hazard levels."], actions=["Ensure evacuation complete", "Await firefighters"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=240, mq135=210, mq2=550, dht22_temp=31.0, dht22_humidity=43.0, flame_value=900, flame_detected=True),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Fire ongoing", confidence=0.95, summary="Fire still active and dangerous.",
             reasons=["Sustained threat level.", "Continued hazard."], actions=["Remain evacuated", "Professional response"], trigger_buzzer=True, trigger_led=True)),
        (AlarmReading(mq7=220, mq135=195, mq2=510, dht22_temp=30.2, dht22_humidity=43.5, flame_value=1100, flame_detected=True),
         AnalysisResult(danger=True, danger_level="CRITICAL", suspected_gas="Fire being suppressed", confidence=0.93, summary="Fire levels declining.",
             reasons=["Hazard indicators dropping.", "Suppression effective."], actions=["Monitor from safe location", "Await all-clear"], trigger_buzzer=True, trigger_led=True)),
    ],
}


def build_alarm_preview(scenario: str, reading_index: int = 0) -> tuple[AlarmReading | None, AnalysisResult | None]:
    """Returns a reading and analysis for a scenario at a given index."""
    if scenario == AlarmScenario.LIVE:
        return None, None

    readings = SCENARIO_PROGRESSIONS.get(scenario, [])
    if not readings:
        return None, None

    # Cycle through readings
    idx = reading_index % len(readings)
    return readings[idx]


current_alarm_state = {
    "is_active": False,
    "feed_paused": False,
    "scenario": AlarmScenario.LIVE,
    "reading_index": 0,
}

@router.get("/alarm", response_model=AlarmState)
def get_alarm_state():
    scenario = current_alarm_state.get("scenario", AlarmScenario.LIVE)
    reading, analysis = build_alarm_preview(scenario, current_alarm_state["reading_index"])
    
    # Increment index for next call (cycles through readings)
    if scenario != AlarmScenario.LIVE and reading is not None:
        readings = SCENARIO_PROGRESSIONS.get(scenario, [])
        current_alarm_state["reading_index"] = (current_alarm_state["reading_index"] + 1) % len(readings)
    
    return {
        "is_active": current_alarm_state["is_active"],
        "feed_paused": current_alarm_state.get("feed_paused", False),
        "scenario": scenario,
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
        # Reset index when scenario changes
        current_alarm_state["reading_index"] = 0

    scenario = current_alarm_state.get("scenario", AlarmScenario.LIVE)
    reading, analysis = build_alarm_preview(scenario, current_alarm_state["reading_index"])
    
    # Increment index for next call
    if scenario != AlarmScenario.LIVE and reading is not None:
        readings = SCENARIO_PROGRESSIONS.get(scenario, [])
        current_alarm_state["reading_index"] = (current_alarm_state["reading_index"] + 1) % len(readings)
    
    return {
        "is_active": current_alarm_state["is_active"],
        "feed_paused": current_alarm_state["feed_paused"],
        "scenario": scenario,
        "reading": reading,
        "analysis": analysis,
    }
