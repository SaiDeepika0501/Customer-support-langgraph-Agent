sessions = {}


def get_session(session_id: str):
    return sessions.get(session_id, {})


def update_session(session_id: str, updates: dict):
    if session_id not in sessions:
        sessions[session_id] = {}

    sessions[session_id].update(updates)

    return sessions[session_id]