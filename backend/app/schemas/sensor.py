from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Literal, List

class SensorReading(BaseModel):
    device_id: str = Field(..., examples=["iot-device-001"])
    mq7: float = Field(..., description="Carbon monoxide sensor raw or calibrated value")
    mq135: float = Field(..., description="Air quality / harmful gas sensor value")
    mq2: float = Field(..., description="LPG / smoke / combustible gas sensor value")
    dht22_temp: float = Field(..., description="Temperature in Celsius")
    dht22_humidity: float = Field(..., description="Humidity percentage")
    flame_detected: bool = Field(..., description="True if flame/IR sensor detects fire")
    timestamp: Optional[datetime] = None

class AnalysisResult(BaseModel):
    danger: bool
    danger_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    suspected_gas: str
    confidence: float
    summary: str
    reasons: List[str]
    actions: List[str]
    trigger_buzzer: bool
    trigger_led: bool