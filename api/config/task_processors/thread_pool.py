from api.config.config_base import ConfigBase, Field


class ThreadPoolTaskProcessorConfig(ConfigBase):
    max_workers: int | None = Field(
        default=None,
        description="The max number of threads to start that handle tasks",
    )
