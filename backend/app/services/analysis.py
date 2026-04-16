from typing import Dict, Any

from app.core.config import FLAME_ANALOG_THRESHOLD


def infer_flame_detected(reading) -> bool:
    explicit = getattr(reading, "flame_detected", None)
    if explicit is not None:
        return explicit

    flame_value = getattr(reading, "flame_value", None)
    if flame_value is None:
        return False

    return flame_value <= FLAME_ANALOG_THRESHOLD

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