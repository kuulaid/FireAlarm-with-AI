import json
from datetime import datetime
from openai import OpenAI
from app.core.config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a safety analysis assistant for an IoT gas/fire alert system.

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