import os
from typing import Optional

import redis
import sirope

_redis_conn: Optional[redis.Redis] = None
_sirope: Optional[sirope.Sirope] = None


def get_redis_connection() -> redis.Redis:
    global _redis_conn
    if _redis_conn is None:
        _redis_conn = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
    return _redis_conn


def get_sirope() -> sirope.Sirope:
    global _sirope
    if _sirope is None:
        _sirope = sirope.Sirope(get_redis_connection())
    return _sirope
