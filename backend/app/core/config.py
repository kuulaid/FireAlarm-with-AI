import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fire_alarm")

# Flame sensor tuning for analog IR modules (0-4095 typical ADC range).
FLAME_ANALOG_MIN_VALUE = int(os.getenv("FLAME_ANALOG_MIN_VALUE", "0"))
FLAME_ANALOG_MAX_VALUE = int(os.getenv("FLAME_ANALOG_MAX_VALUE", "4095"))
FLAME_ANALOG_TRIGGER_THRESHOLD = int(os.getenv("FLAME_ANALOG_TRIGGER_THRESHOLD", "1100"))
FLAME_ANALOG_CLEAR_THRESHOLD = int(os.getenv("FLAME_ANALOG_CLEAR_THRESHOLD", "1400"))
FLAME_ANALOG_FILTER_ALPHA = float(os.getenv("FLAME_ANALOG_FILTER_ALPHA", "0.35"))
FLAME_TRIGGER_CONSECUTIVE_SAMPLES = int(os.getenv("FLAME_TRIGGER_CONSECUTIVE_SAMPLES", "3"))
FLAME_CLEAR_CONSECUTIVE_SAMPLES = int(os.getenv("FLAME_CLEAR_CONSECUTIVE_SAMPLES", "2"))
FLAME_STUCK_LOW_WINDOW = int(os.getenv("FLAME_STUCK_LOW_WINDOW", "8"))
FLAME_STUCK_LOW_MAX_DELTA = int(os.getenv("FLAME_STUCK_LOW_MAX_DELTA", "40"))
FLAME_STUCK_LOW_FLOOR = int(os.getenv("FLAME_STUCK_LOW_FLOOR", "120"))
FLAME_OVERRIDE_MIN_CONFIDENCE = float(os.getenv("FLAME_OVERRIDE_MIN_CONFIDENCE", "0.55"))

# Backward compatible alias used by existing code and prompts.
FLAME_ANALOG_THRESHOLD = int(
    os.getenv("FLAME_ANALOG_THRESHOLD", str(FLAME_ANALOG_TRIGGER_THRESHOLD))
)

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")