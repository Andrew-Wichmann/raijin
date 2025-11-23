from api.config.job_stores import JobStoreConfig
from api.config.job_stores.in_memory import InMemoryJobStoreConfig
from api.config.job_stores.sqlite import SQLiteJobStoreConfig
from api.job_stores.in_memory import InMemoryJobStore
from api.job_stores.sqlite import SQLiteJobStore
from api.job_stores.protocol import JobStoreProtocol


def from_config(config: JobStoreConfig) -> JobStoreProtocol:
    if isinstance(config.config, InMemoryJobStoreConfig):
        return InMemoryJobStore(config.config)
    if isinstance(config.config, SQLiteJobStoreConfig):
        return SQLiteJobStore(config.config)
    raise ValueError(f"Unknown config type: {type(config.config)}")
