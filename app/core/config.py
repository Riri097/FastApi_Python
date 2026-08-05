from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


# App configuration, values are read from .env
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
