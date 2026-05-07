from __future__ import annotations

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.storage import get_sirope


class User(UserMixin):
    def __init__(self, username: str, email: str, password: str):
        self.username = username.strip()
        self.username_lower = self.username.lower()
        self.email = email.strip()
        self.email_lower = self.email.lower()
        self.password_hash = generate_password_hash(password)
        self.created_at = datetime.utcnow()

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        if not hasattr(self, "__oid__"):
            return None
        return get_sirope().safe_from_oid(self.__oid__)


def find_user_by_email(sr, email: str):
    normalized = email.strip().lower()
    return sr.find_first(User, lambda u: u.email_lower == normalized)


def find_user_by_username(sr, username: str):
    normalized = username.strip().lower()
    return sr.find_first(User, lambda u: u.username_lower == normalized)
