from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import CORS_ORIGINS
from app.routers.device import router as device_router
from app.routers.alarm import router as alarm

app = FastAPI(title="Project Alab Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"--- CORS ORIGINS LOADED: {CORS_ORIGINS} ---")

app.include_router(device_router)
app.include_router(alarm)

@app.get("/")
def root():
    return {"message": "Project Alab API is running"}