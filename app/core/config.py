
from functools import lru_cache

from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings) :
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

# lru_cache is used to cache the settings object so that it is only created once and reused 
# throughout the application. This is important because creating a new settings object for every 
# request would be inefficient and could lead to inconsistencies if the environment variables change
#  during the application's lifetime.
@lru_cache
def get_settings() -> Settings:
    return Settings()

