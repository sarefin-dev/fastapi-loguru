from functools import lru_cache

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated


class AppSettings(BaseSettings):
    app_name: str = "Fast Api with Loguru"
    environment: str = "Development"
    debug: bool = True

    # Logging
    log_level: str = "INFO"
    log_dir: str = "logs"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()


SettingsDesp = Annotated[AppSettings, Depends(get_settings)]
