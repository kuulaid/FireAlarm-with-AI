from pymongo import MongoClient
from app.core.config import MONGODB_URI, DATABASE_NAME
import logging

logger = logging.getLogger(__name__)

try:
    print(f"Connecting to MongoDB: {MONGODB_URI}")
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Test connection
    client.admin.command('ping')
    print("MongoDB connection successful!")
    db = client[DATABASE_NAME]
    readings_collection = db.readings
    results_collection = db.results
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    client = None
    db = None
    readings_collection = None
    results_collection = None