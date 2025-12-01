from api.config.config_base import ConfigBase, Field


class SQLiteJobStoreConfig(ConfigBase):
    db_path: str = Field(default="db.sqlite", description="The SQLite database file")
    job_table_name: str = Field(
        default="job", description="The table to store job metadata in"
    )
    radar_table_name: str = Field(
        default="radar", description="The table to store radars"
    )
    results_table_name: str = Field(
        default="results", description="The table to store the results of a job in"
    )
