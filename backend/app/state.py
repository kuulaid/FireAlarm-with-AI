LATEST_ANALYSIS = {
    "reading": None,
    "analysis": None
}

# Tracks analog flame signal state per device to avoid one-sample false positives.
FLAME_SIGNAL_STATE = {}

# Shared actuator state used by alarm controls and live analysis updates.
ALARM_ACTUATOR_STATE = {
    "is_active": False,
    "feed_paused": False,
    "scenario": "LIVE",
    "reading_index": 0,
}

