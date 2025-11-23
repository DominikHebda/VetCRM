import hashlib
import os
import time
sessions = {}


def create_session(username: str, user_role: str, doctor_id: int | None = None) -> str:
    session_id = hashlib.sha256(f"{username}{time.time()}{os.urandom(16)}".encode()).hexdigest()
    sessions[session_id] = {
        "username": username,
        "role": user_role,
        "doctor_id": doctor_id,
        "created_at": time.time()   
    }
    return session_id

SESSION_TIMEOUT = 3600  # 1 godzina

def get_session(cookie_header: str):
    if not cookie_header:
        return None
    cookies = dict(x.strip().split("=", 1) for x in cookie_header.split(";") if "=" in x)
    session_id = cookies.get("session_id")
    if session_id and session_id in sessions:
        session = sessions[session_id]
        if time.time() - session["created_at"] < SESSION_TIMEOUT:
            return session
        else:
            del sessions[session_id]  # wygasła
    return None

def destroy_session(session_id: str):
    """Usuwa sesję"""
    if session_id in sessions:
        del sessions[session_id]