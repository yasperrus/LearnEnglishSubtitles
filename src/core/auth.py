import json
import os

import bcrypt

SESSION_FILE = "session.json"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def save_session(data: dict):
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def load_session():
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
