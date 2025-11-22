from pydantic import BaseModel, Field


class ProcessPoolTaskProcessorConfig(BaseModel):
    max_workers: int | None = Field(
        default=None,
        description="The max number of subprocesses to start that handle tasks",
    )
