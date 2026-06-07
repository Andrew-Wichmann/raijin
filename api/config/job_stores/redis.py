from api.config.config_base import ConfigBase, Field


class RedisStoreConfig(ConfigBase):
    host: str = Field(default="localhost", description="Redis server hostname")
    port: int = Field(default=6379, description="Redis server port")
    db: int = Field(default=0, description="Redis database index")
    key_prefix: str = Field(default="raijin:job:", description="Prefix for all job keys")
