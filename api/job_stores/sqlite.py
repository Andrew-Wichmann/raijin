import sqlite3
import threading
import random

from models import Job, Status
from api.config.job_stores.sqlite import SQLiteJobStoreConfig

_local = threading.local()


class SQLiteJobStore:
    def __init__(self, settings: SQLiteJobStoreConfig):
        self.settings = settings
        with self._conn as conn:
            conn.execute(
                f"""
                    CREATE TABLE IF NOT EXISTS {self.settings.job_table_name} (
                        job_id INT PRIMARY KEY,
                        group_id INT,
                        status TEXT NOT NULL
                    )
                """
            )
            conn.execute(
                f"""
                    CREATE TABLE IF NOT EXISTS {self.settings.radar_table_name} (
                        jid TEXT PRIMARY KEY,
                        radar BLOB NOT NULL
                    )
                """
            )
            conn.execute(
                f"""
                    CREATE TABLE IF NOT EXISTS {self.settings.results_table_name} (
                        job_id INT NOT NULL,
                        jid TEXT NOT NULL,
                        PRIMARY KEY (job_id, jid),
                        FOREIGN KEY (job_id) REFERENCES {self.settings.job_table_name},
                        FOREIGN KEY (jid) REFERENCES {self.settings.radar_table_name}
                    )
                """
            )

    @property
    def _conn(self):
        if not hasattr(_local, "conn"):
            _local.conn = sqlite3.Connection(self.settings.db_path)
            _local.conn.execute("PRAGMA foreign_keys = ON")
        return _local.conn

    def add_job(self) -> Job:
        job = Job(
            job_id=random.randint(0, 999999), status=Status.PENDING
        )  # temp hack. Better to do autoincrementing PK
        with self._conn as conn:
            conn.execute(
                f"INSERT INTO {self.settings.job_table_name} (job_id, status) VALUES (?, ?)",
                (job.job_id, job.status),
            )
        return job

    def get_job(self, job_id: int) -> Job:
        with self._conn as conn:
            res = conn.execute(
                f"SELECT job_id, status FROM {self.settings.job_table_name} WHERE job_id == ?",
                (job_id,),
            ).fetchone()
        return Job(job_id=res[0], status=res[1])

    def update_job(self, job_id: int, status: Status):
        with self._conn as conn:
            conn.execute(
                f"UPDATE {self.settings.job_table_name} SET status = ? WHERE job_id == ?",
                (status.value, job_id),
            ).fetchone()
