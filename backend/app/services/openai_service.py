import json
from datetime import datetime
from openai import OpenAI
from app.core.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    FLAME_ANALOG_TRIGGER_THRESHOLD,
    FLAME_ANALOG_CLEAR_THRESHOLD,
)

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = f"""
You are a safety analysis assistant for an IoT gas/fire alert system.

CRITICAL LOCATION CONTEXT: The system is deployed in the Philippines (a tropical climate). 
- Normal ambient temperatures are hot and can range from 25°C up to 38°C (or higher during summer).
- Normal ambient humidity is very high, typically ranging from 60% to 90%.

RULES FOR ANALYSIS:
1. Do NOT trigger a fire danger or warning purely based on high temperature and high humidity, as these are normal weather conditions here.
2. Only elevate the danger level if high temperatures are accompanied by actual fire indicators:
    - A triggered flame sensor. The raw flame sensor is analog, and lower `flame_value` readings mean stronger flame detection.
    - Treat `flame_value <= {FLAME_ANALOG_TRIGGER_THRESHOLD}` as the backend trigger zone when sustained across samples.
    - Treat `flame_value >= {FLAME_ANALOG_CLEAR_THRESHOLD}` as the backend clear zone.
    - If backend provides `flame_filtered_value` and `flame_confidence`, trust those over a single raw sample.
    - If backend sets `flame_sensor_fault=true`, treat flame input as unreliable and avoid elevating risk on flame alone.
   - Dangerous spikes in gas sensor readings (MQ2 for smoke/combustibles, MQ7 for Carbon Monoxide, MQ135 for poor air quality).
   
Task:
- Analyze sensor readings from MQ-7, MQ-135, MQ-2, DHT22, and flame sensor.
- If `flame_value` is present, use it as an analog fire indicator and explain that lower values indicate flame.
- Infer the most likely hazard type.
- Return ONLY valid JSON.
- Do not claim certainty beyond the data.
- If the reading is ambiguous, say so.
- Prefer safety: when risk is high, recommend triggering buzzer and LED.

Output JSON keys:
danger (boolean)
danger_level ("LOW" | "MEDIUM" | "HIGH" | "CRITICAL")
suspected_gas (string)
confidence (number from 0 to 1)
summary (string)
reasons (array of strings)
actions (array of strings)
trigger_buzzer (boolean)
trigger_led (boolean)
"""

def analyze_with_openai(reading: dict, heuristic: dict) -> dict:
    # Ensure timestamp is serializable
    reading_dict = reading.copy()
    if 'timestamp' in reading_dict and isinstance(reading_dict['timestamp'], datetime):
        reading_dict['timestamp'] = reading_dict['timestamp'].isoformat()

    user_payload = {
        "sensor_reading": reading_dict,
        "heuristic": heuristic
    }

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(user_payload)
            }
        ],
        temperature=0.2,
    )

    text = response.choices[0].message.content

    return json.loads(text)