from Database.password_utils import verify_password
from Database.sessions import create_session
from Database.sql_user import get_user_by_username


class LoginResult:
    def __init__(self, success, reason=None, session_id=None, role=None, doctor_id=None):
        self.success = success
        self.reason = reason
        self.session_id = session_id
        self.role = role
        self.doctor_id = doctor_id

def authenticate_user(username, password):
    user = get_user_by_username(username)

    if not user:
        return LoginResult(False, "no_user")

    stored_hash, role, doctor_id = user

    if not verify_password(password, stored_hash):
        return LoginResult(False, "bad_password")

    session_id = create_session(username, role, doctor_id)

    return LoginResult(
        True,
        session_id=session_id,
        role=role,
        doctor_id=doctor_id
    )