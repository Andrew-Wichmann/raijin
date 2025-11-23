import typing as T
from pydantic import BaseModel, model_validator
from .thread_pool import ThreadPoolTaskProcessorConfig
from .process_pool import ProcessPoolTaskProcessorConfig
from .cbb import CBBTaskProcessorConfig
from .celery import CeleryTaskProcessorConfig
from .glue import GlueTaskProcessorConfig
from .l_pipe import LPipeTaskProcessorConfig
from .ray import RayTaskProcessorConfig


class TaskProcessorConfig(BaseModel):
    thread_pool: ThreadPoolTaskProcessorConfig | None = None
    process_pool: ProcessPoolTaskProcessorConfig | None = None
    cbb: CBBTaskProcessorConfig | None = None
    celery: CeleryTaskProcessorConfig | None = None
    glue: GlueTaskProcessorConfig | None = None
    l_pipe: LPipeTaskProcessorConfig | None = None
    ray: RayTaskProcessorConfig | None = None

    @model_validator(mode="after")
    def one_and_only_one_config(self):
        task_processors_configured = [
            k
            for k, v in self.model_dump().items()
            if v is not None and v.get("enabled", False)
        ]
        if len(task_processors_configured) == 0:
            raise ValueError(
                f"No task processor configured. Provide a configuration for a {' or '.join(k for k, _ in self.model_dump().items())} processor"
            )
        return self

    @property
    def config(
        self,
    ) -> T.Union[
        ThreadPoolTaskProcessorConfig,
        ProcessPoolTaskProcessorConfig,
        CBBTaskProcessorConfig,
        CeleryTaskProcessorConfig,
        GlueTaskProcessorConfig,
        LPipeTaskProcessorConfig,
        RayTaskProcessorConfig,
    ]:
        # Safe to get first element because one_and_only_one_config ensures there is one config
        for field in self.model_dump():
            value = getattr(self, field)
            if value is not None and value.enabled:
                return value
        raise ValueError("Somehow there is no non-empty config")
