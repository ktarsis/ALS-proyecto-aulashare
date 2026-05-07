import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "aulashare-dev-secret-key")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
