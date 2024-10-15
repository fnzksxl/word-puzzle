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


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
