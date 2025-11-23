from pydantic import BaseModel, Field


class ThreadTaskProcessorConfig(BaseModel):
    max_workers: int | None = Field(
        default=None,
        description="The max number of threads to start that handle tasks",
    )
