import secrets

import bcrypt

from src.core.auth import verify_password
from src.data.User import User
from src.db.session import SessionLocal
from src.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    def register(self, name, password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        db = SessionLocal()
        db.add(User(name=name, password=hashed))
        db.commit()
        return True

    def authenticate(self, name: str, password: str):
        user: User = self.repo.get_by_name(name)
        if not user:
            return None
        if verify_password(password, user.password):
            token = secrets.token_hex(32)
            self.repo.set_token_by_id(user.id, token)
            user.session_token = token
            return user
        return None

    def validate_token(self, token):
        if not token:
            return False
        db = SessionLocal()
        user = db.query(User).filter(User.session_token == token).one()
        return bool(user)

    def logout(self, token):
        db = SessionLocal()
        user = db.query(User).filter(User.session_token == token).one()
        user.session_token = None
        db.commit()
