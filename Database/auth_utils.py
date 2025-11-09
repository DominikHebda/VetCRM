import hashlib
import os
import time
sessions = {}


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return salt.hex() + ":" + dk.hex()

def verify_password(password: str, stored_hash: str) -> bool:
    salt_hex, hash_hex = stored_hash.split(":")
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return dk.hex() == hash_hex

def create_session(username: str, user_role: str) -> str:
    """Tworzy nowy token sesji"""
    session_id = hashlib.sha256(f"{username}{time.time()}{os.urandom(16)}".encode()).hexdigest()
    sessions[session_id] = {"username": username, "role": user_role, "created_at": time.time()}
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