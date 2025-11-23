from api.config.config_base import ConfigBase, Field


class ProcessPoolTaskProcessorConfig(ConfigBase):
    max_workers: int | None = Field(
        default=None,
        description="The max number of subprocesses to start that handle tasks",
    )
