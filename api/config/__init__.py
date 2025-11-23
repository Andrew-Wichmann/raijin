from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from api.config.job_stores import JobStoreConfig, InMemoryJobStoreConfig
from api.config.task_processors import TaskProcessorConfig
from api.config.task_processors.thread_pool import ThreadPoolTaskProcessorConfig


class LogLevelConfig(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class RaijinConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RAIJIN__", env_nested_delimiter="__")

    log_level: LogLevelConfig = Field(
        default=LogLevelConfig.INFO, description="Log level for the app"
    )
    task_processor: TaskProcessorConfig = Field(
        default=TaskProcessorConfig(
            thread_pool=ThreadPoolTaskProcessorConfig(enabled=True)
        ),
        description="The processor to handle job submissions",
    )
    job_store: JobStoreConfig = Field(
        default=JobStoreConfig(in_memory=InMemoryJobStoreConfig(enabled=True)),
        description="The config for job store",
    )
