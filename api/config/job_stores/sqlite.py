from pydantic import BaseModel, Field


class SQLiteJobStoreConfig(BaseModel):
    db_path: str = Field(default="db.sqlite", description="The SQLite database file")
    table_name: str = Field(
        default="jobs", description="The table to store job metadata in"
    )
