from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api",
                   tags=["alarms"])


class AlarmState(BaseModel):
    is_active: bool

current_alarm_state = {"is_active": False}

@router.get("/alarm", response_model=AlarmState)
def get_alarm_state():
    return current_alarm_state

@router.post("/alarm", response_model=AlarmState)
def set_alarm_state(state: AlarmState):
    current_alarm_state["is_active"] = state.is_active
    return current_alarm_state