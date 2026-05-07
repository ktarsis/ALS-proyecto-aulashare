from __future__ import annotations

from typing import Optional

from flask import abort
from flask_login import current_user

from app.comments.model import Comment, comments_for_resource
from app.ratings.model import Rating, average_rating_for_resource_model, find_rating_for_user_and_resource
from app.storage import get_sirope


def safe_id(obj) -> Optional[str]:
    if obj is None or not hasattr(obj, "__oid__"):
        return None
    return get_sirope().safe_from_oid(obj.__oid__)


def load_from_safe(safe_oid: str):
    if not safe_oid:
        return None
    sr = get_sirope()
    oid = sr.oid_from_safe(safe_oid)
    if oid is None or not sr.exists(oid):
        return None
    try:
        return sr.load(oid)
    except Exception:
        return None


def require_existing(safe_oid: str):
    obj = load_from_safe(safe_oid)
    if obj is None:
        abort(404)
    return obj


def is_authenticated_owner(owner_safe_id: str) -> bool:
    return current_user.is_authenticated and current_user.get_id() == owner_safe_id


def comments_count_for_resource(resource) -> int:
    return len(list(comments_for_resource(get_sirope(), safe_id(resource))))


def average_rating_for_resource(resource) -> float:
    return average_rating_for_resource_model(get_sirope(), safe_id(resource))


def current_user_rating_for_resource(resource) -> Optional[Rating]:
    if not current_user.is_authenticated:
        return None
    return find_rating_for_user_and_resource(get_sirope(), current_user.get_id(), safe_id(resource))
