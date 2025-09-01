from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class JobStore(str, Enum):
    IN_MEMORY = "in_memory"
    SQLITE = "sqlite"
    REDIS = "redis"


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class RaijinSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RAIJIN_")

    log_level: LogLevel = Field(
        default=LogLevel.INFO, description="Log level for the app"
    )
    job_store: JobStore = Field(
        default=JobStore.IN_MEMORY, description="The store type to store job data in"
    )
