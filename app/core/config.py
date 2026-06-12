from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # MongoDB
    MONGODB_URI: str
    MONGODB_DB_NAME: str = "minersbuddy"

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # App
    SECRET_KEY: str = "your-secret-key-change-in-production"
    DEBUG: bool = False
    API_VERSION: str = "v1"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
