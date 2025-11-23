import sqlite3
import threading
from contextlib import contextmanager
from typing import Optional
from uuid import uuid4

from models import Job, Status
from api.config.job_stores.sqlite import SQLiteJobStoreConfig

_local = threading.local()


class SQLiteJobStore:
    def __init__(self, settings: SQLiteJobStoreConfig):
        self.settings = settings
        with self._conn as conn:
            conn.execute(
                f"""
            CREATE TABLE IF NOT EXISTS {self.settings.table_name} (
                job_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                result INTEGER
            )
        """
            )

    @property
    def _conn(self):
        if not hasattr(_local, "conn"):
            _local.conn = sqlite3.Connection(self.settings.db_path)
        return _local.conn

    def add_job(self) -> Job:
        job = Job(job_id=str(uuid4()), status=Status.PENDING)
        with self._conn as conn:
            conn.execute(
                f"INSERT INTO {self.settings.table_name} (job_id, status, result) VALUES (?, ?, ?)",
                (job.job_id, job.status, None),
            )
        return job

    def get_job(self, job_id: str) -> Job:
        with self._conn as conn:
            res = conn.execute(
                f"SELECT job_id, status, result FROM {self.settings.table_name} WHERE job_id == ?",
                (job_id,),
            ).fetchone()
        return Job(job_id=res[0], status=res[1], result=res[2])

    def update_job(self, job_id: str, status: Status, result: Optional[int] = None):
        with self._conn as conn:
            conn.execute(
                f"UPDATE {self.settings.table_name} SET status = ?, result = ? WHERE job_id == ?",
                (status.value, result, job_id),
            ).fetchone()
