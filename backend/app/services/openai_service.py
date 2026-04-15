import json
from datetime import datetime
from openai import OpenAI
from app.core.config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a safety analysis assistant for an IoT gas/fire alert system.

CRITICAL LOCATION CONTEXT: The system is deployed in the Philippines (a tropical climate). 
- Normal ambient temperatures are hot and can range from 25°C up to 38°C (or higher during summer).
- Normal ambient humidity is very high, typically ranging from 60% to 90%.

RULES FOR ANALYSIS:
1. Do NOT trigger a fire danger or warning purely based on high temperature and high humidity, as these are normal weather conditions here.
2. Only elevate the danger level if high temperatures are accompanied by actual fire indicators:
   - A triggered flame sensor (flame_detected = True).
   - Dangerous spikes in gas sensor readings (MQ2 for smoke/combustibles, MQ7 for Carbon Monoxide, MQ135 for poor air quality).
   
Task:
- Analyze sensor readings from MQ-7, MQ-135, MQ-2, DHT22, and flame sensor.
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