import typing as T
from pydantic import BaseModel, model_validator

from api.config.job_stores.hydra import HydraStoreConfig
from api.config.job_stores.in_memory import InMemoryJobStoreConfig
from api.config.job_stores.postgres import PostgresStoreConfig
from api.config.job_stores.redis import RedisStoreConfig
from api.config.job_stores.sqlite import SQLiteJobStoreConfig


class StoreConfig(BaseModel):
    in_memory: InMemoryJobStoreConfig | None = None
    sqlite: SQLiteJobStoreConfig | None = None
    postgres: PostgresStoreConfig | None = None
    redis: RedisStoreConfig | None = None
    hydra: HydraStoreConfig | None = None

    @model_validator(mode="after")
    def one_and_only_one_config(self):
        stores_configured = [
            k
            for k, v in self.model_dump().items()
            if v is not None and v.get("enabled", False)
        ]
        if len(stores_configured) == 0:
            raise ValueError(
                f"No store configured. Provide a configuration for a {' or '.join(k for k, _ in self.model_dump().items())} store"
            )
        if len(stores_configured) > 1:
            raise ValueError(
                f"Ambiguous store configuration. Multiple stores configured. Only one configuration is allowed. Stores configured: {stores_configured}"
            )
        return self

    @property
    def config(
        self,
    ) -> T.Union[
        InMemoryJobStoreConfig,
        SQLiteJobStoreConfig,
        PostgresStoreConfig,
        RedisStoreConfig,
        HydraStoreConfig,
    ]:
        for field in self.model_dump():
            value = getattr(self, field)
            if value is not None and value.enabled:
                return value
        raise ValueError("Somehow there is no non-empty config")
