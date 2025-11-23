from typing import Dict, Optional
from models import Job, Status
from uuid import uuid4
from threading import Lock

from api.config.job_stores.in_memory import InMemoryJobStoreConfig


class InMemoryJobStore:
    def __init__(self, _: InMemoryJobStoreConfig):
        self.__jobs: Dict[str, Job] = {}
        self.__lock = Lock()

    def add_job(self) -> Job:
        job = Job(job_id=str(uuid4()), status=Status.PENDING)
        with self.__lock:
            self.__jobs[job.job_id] = job
        return job

    def get_job(self, job_id: str) -> Job:
        with self.__lock:
            return self.__jobs[job_id]

    def update_job(self, job_id: str, status: Status, result: Optional[int] = None):
        with self.__lock:
            job = self.__jobs[job_id]
            job.status = status
            if result is not None:
                job.result = result
