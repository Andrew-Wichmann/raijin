from api.job_stores.protocol import JobStoreProtocol
from api.task_processors.protocol import TaskProcessorProtocol
from api.task_processors.process_pool import ProcessPoolTaskProcessor
from api.task_processors.thread import ThreadTaskProcessor
from api.config.task_processors import TaskProcessorConfig
from api.config.task_processors.cbb import CBBTaskProcessorConfig
from api.config.task_processors.celery import CeleryTaskProcessorConfig
from api.config.task_processors.glue import GlueTaskProcessorConfig
from api.config.task_processors.thread import ThreadTaskProcessorConfig
from api.config.task_processors.l_pipe import LPipeTaskProcessorConfig
from api.config.task_processors.process_pool import ProcessPoolTaskProcessorConfig
from api.config.task_processors.ray import RayTaskProcessorConfig


def from_config(
    job_store: JobStoreProtocol, config: TaskProcessorConfig
) -> TaskProcessorProtocol:
    if isinstance(config.config, CBBTaskProcessorConfig):
        raise ValueError("CBB task processor not implemented")
    elif isinstance(config.config, CeleryTaskProcessorConfig):
        raise ValueError("Celery task processor not implemented")
    elif isinstance(config.config, GlueTaskProcessorConfig):
        raise ValueError("Glue task processor not implemented")
    elif isinstance(config.config, ThreadTaskProcessorConfig):
        return ThreadTaskProcessor(job_store, config.config)
    elif isinstance(config.config, LPipeTaskProcessorConfig):
        raise ValueError("LPipe task processor not implemented")
    elif isinstance(config.config, ProcessPoolTaskProcessorConfig):
        return ProcessPoolTaskProcessor(job_store, config.config)
    elif isinstance(config.config, RayTaskProcessorConfig):
        raise ValueError("Ray task processor not implemented")
    raise ValueError(f"Unhandled config type: {type(config)}")
