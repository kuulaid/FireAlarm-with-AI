from typing import Dict, Any

from app.core.config import (
    FLAME_ANALOG_MIN_VALUE,
    FLAME_ANALOG_MAX_VALUE,
    FLAME_ANALOG_TRIGGER_THRESHOLD,
    FLAME_ANALOG_CLEAR_THRESHOLD,
    FLAME_ANALOG_FILTER_ALPHA,
    FLAME_TRIGGER_CONSECUTIVE_SAMPLES,
    FLAME_CLEAR_CONSECUTIVE_SAMPLES,
    FLAME_STUCK_LOW_WINDOW,
    FLAME_STUCK_LOW_MAX_DELTA,
    FLAME_STUCK_LOW_FLOOR,
)


def evaluate_flame_signal(reading, state: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    Evaluate analog flame readings with smoothing + hysteresis + debounce.

    Lower analog values indicate stronger flame for common IR flame modules.
    """
    flame_value = getattr(reading, "flame_value", None)
    if flame_value is None:
        explicit = bool(getattr(reading, "flame_detected", False))
        return {
            "detected": explicit,
            "filtered_value": None,
            "confidence": 0.8 if explicit else 0.0,
            "valid": False,
            "sensor_fault": False,
            "reason": "No analog flame value; using explicit digital state",
            "trigger_count": 1 if explicit else 0,
            "clear_count": 0 if explicit else 1,
            "recent_values": [],
        }

    if flame_value < FLAME_ANALOG_MIN_VALUE or flame_value > FLAME_ANALOG_MAX_VALUE:
        return {
            "detected": False,
            "filtered_value": None,
            "confidence": 0.0,
            "valid": False,
            "sensor_fault": True,
            "reason": f"Analog flame value out of valid range ({FLAME_ANALOG_MIN_VALUE}-{FLAME_ANALOG_MAX_VALUE})",
            "trigger_count": 0,
            "clear_count": 0,
            "recent_values": [],
        }

    state = state or {}
    previous_filtered = state.get("filtered_value")
    previous_detected = bool(state.get("detected", False))
    previous_trigger_count = int(state.get("trigger_count", 0))
    previous_clear_count = int(state.get("clear_count", 0))
    previous_recent_values = list(state.get("recent_values", []))

    filtered_value = (
        flame_value
        if previous_filtered is None
        else (FLAME_ANALOG_FILTER_ALPHA * flame_value)
        + ((1.0 - FLAME_ANALOG_FILTER_ALPHA) * previous_filtered)
    )

    trigger_count = previous_trigger_count
    clear_count = previous_clear_count

    if filtered_value <= FLAME_ANALOG_TRIGGER_THRESHOLD:
        trigger_count += 1
        clear_count = 0
    elif filtered_value >= FLAME_ANALOG_CLEAR_THRESHOLD:
        clear_count += 1
        trigger_count = 0

    detected = previous_detected
    reason = "Maintaining previous flame state in hysteresis band"

    if trigger_count >= FLAME_TRIGGER_CONSECUTIVE_SAMPLES:
        detected = True
        reason = (
            f"Analog flame signal below trigger threshold for {trigger_count} consecutive samples"
        )
    elif clear_count >= FLAME_CLEAR_CONSECUTIVE_SAMPLES:
        detected = False
        reason = (
            f"Analog flame signal above clear threshold for {clear_count} consecutive samples"
        )

    if filtered_value <= FLAME_ANALOG_TRIGGER_THRESHOLD:
        confidence = min(1.0, (FLAME_ANALOG_TRIGGER_THRESHOLD - filtered_value) / FLAME_ANALOG_TRIGGER_THRESHOLD)
    elif filtered_value >= FLAME_ANALOG_CLEAR_THRESHOLD:
        confidence = 0.0
    else:
        band_width = max(1.0, FLAME_ANALOG_CLEAR_THRESHOLD - FLAME_ANALOG_TRIGGER_THRESHOLD)
        confidence = max(0.0, 1.0 - ((filtered_value - FLAME_ANALOG_TRIGGER_THRESHOLD) / band_width))

    recent_values = (previous_recent_values + [int(flame_value)])[-max(2, FLAME_STUCK_LOW_WINDOW):]
    sensor_fault = False
    if len(recent_values) >= max(2, FLAME_STUCK_LOW_WINDOW):
        value_span = max(recent_values) - min(recent_values)
        avg_value = sum(recent_values) / len(recent_values)
        if value_span <= FLAME_STUCK_LOW_MAX_DELTA and avg_value <= FLAME_STUCK_LOW_FLOOR:
            sensor_fault = True
            detected = False
            confidence = 0.0
            trigger_count = 0
            clear_count = max(clear_count, 1)
            reason = (
                "Flame analog signal appears stuck low (possible ESP32 ADC2/WiFi interference or wiring issue)"
            )

    return {
        "detected": detected,
        "filtered_value": round(filtered_value, 2),
        "confidence": round(confidence, 3),
        "valid": True,
        "sensor_fault": sensor_fault,
        "reason": reason,
        "trigger_count": trigger_count,
        "clear_count": clear_count,
        "recent_values": recent_values,
    }

def infer_flame_detected(reading, state: Dict[str, Any] | None = None) -> bool:
    return evaluate_flame_signal(reading, state=state)["detected"]

def heuristic_risk(reading) -> Dict[str, Any]:
    """
    Very simple fallback heuristic.
    Tune these thresholds after real sensor calibration.
    """
    score = 0
    reasons = []

    flame_detected = infer_flame_detected(reading)
    flame_value = getattr(reading, "flame_value", None)

    if flame_detected:
        score += 60
        if flame_value is None:
            reasons.append("Flame sensor detected heat/flame")
        else:
            reasons.append(f"Flame sensor analog value {flame_value} indicates flame")

    if reading.mq2 >= 500:
        score += 20
        reasons.append("MQ-2 reading is high")
    elif reading.mq2 >= 350:
        score += 10
        reasons.append("MQ-2 reading is elevated")

    if reading.mq7 >= 450:
        score += 20
        reasons.append("MQ-7 reading is high")
    elif reading.mq7 >= 300:
        score += 10
        reasons.append("MQ-7 reading is elevated")

    if reading.mq135 >= 500:
        score += 15
        reasons.append("MQ-135 reading is high")
    elif reading.mq135 >= 350:
        score += 8
        reasons.append("MQ-135 reading is elevated")

    if reading.dht22_temp >= 45:
        score += 10
        reasons.append("Temperature is very high")

    if reading.dht22_humidity <= 20:
        score += 5
        reasons.append("Humidity is very low")

    if score >= 70:
        level = "CRITICAL"
    elif score >= 45:
        level = "HIGH"
    elif score >= 20:
        level = "MEDIUM"
    else:
        level = "LOW"

    danger = level in ("HIGH", "CRITICAL")

    return {
        "risk_score": score,
        "risk_level": level,
        "reasons": reasons,
        "danger": danger,
    }