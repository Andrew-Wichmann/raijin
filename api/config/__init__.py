from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from api.config.job_stores import StoreConfig, InMemoryJobStoreConfig
from api.config.task_processors import TaskProcessorConfig
from api.config.task_processors.process_pool import ProcessPoolTaskProcessorConfig


class LogLevelConfig(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class RaijinConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RAIJIN_", env_nested_delimiter="__")

    log_level: LogLevelConfig = Field(
        default=LogLevelConfig.INFO, description="Log level for the app"
    )
    task_processor: TaskProcessorConfig = Field(
        default=TaskProcessorConfig(process_pool=ProcessPoolTaskProcessorConfig()),
        description="The processor to handle job submissions",
    )
    store: StoreConfig = Field(
        default=StoreConfig(in_memory=InMemoryJobStoreConfig()),
        description="The config for job store",
    )
