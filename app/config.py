from dotenv import load_dotenv
from functools import lru_cache

import os

load_dotenv()


class Settings:
    # DB Settings
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_PORT = os.getenv("DB_PORT")

    # JWT Settings
    ALGORITHM = os.getenv("ALGORITHM")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ACCESS_EXPIRE_TIME = int(os.getenv("ACCESS_EXPIRE_TIME"))
    REFRESH_EXPIRE_TIME = int(os.getenv("REFRESH_EXPIRE_TIME"))

    # GOOGLE Settings
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
