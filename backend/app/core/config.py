import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fire_alarm")
FLAME_ANALOG_THRESHOLD = int(os.getenv("FLAME_ANALOG_THRESHOLD", "1800"))

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")