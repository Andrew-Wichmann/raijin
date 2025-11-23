from api.config.config_base import ConfigBase, Field


class SQLiteJobStoreConfig(ConfigBase):
    db_path: str = Field(default="db.sqlite", description="The SQLite database file")
    table_name: str = Field(
        default="jobs", description="The table to store job metadata in"
    )
