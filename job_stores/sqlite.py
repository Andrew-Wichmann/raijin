import sqlite3
from typing import Optional
from uuid import uuid4

from models import Job, Status
from settings import RaijinSettings

TABLE = "jobs"


class SQLiteJobStore:
    def __init__(self, settings: RaijinSettings):
        self.conn = sqlite3.Connection(settings.db_path)
        self.conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE} (
                job_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                result INTEGER
            )
        """
        )

    def add_job(self) -> Job:
        job = Job(job_id=str(uuid4()), status=Status.PENDING)
        self.conn.execute(
            f"INSERT INTO {TABLE} (job_id, status, result) VALUES (?, ?, ?)",
            (job.job_id, job.status, None),
        )
        return job

    def get_job(self, job_id: str) -> Job:
        res = self.conn.execute(
            f"SELECT job_id, status, result FROM {TABLE} WHERE job_id == ?", (job_id,)
        ).fetchone()
        return Job(job_id=res[0], status=res[1], result=res[2])

    def update_job(self, job_id: str, status: Status, result: Optional[int] = None):
        return
