import time
from typing import Optional
import tornado
from concurrent.futures import Future
from models import Status, Job


class JobStore:
    def __init__(self):
        pass

    def get_job(self, job_id: str) -> Job:
        return Job(job_id=job_id, status=Status.PENDING)

    def update_job(self, job_id: str, status: Status, result: Optional[int] = None):
        pass


class TaskProcessor:
    def add(self, job_id: str, x: int, y: int):
        job_store = JobStore()
        job_store.update_job(job_id, status=Status.PENDING)
        time.sleep(10)
        job_store.update_job(job_id, status=Status.COMPLETE, result=x + y)


class Raijin(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jobs: dict[str, Future] = {}
        self.job_store = JobStore()
        self.task_processor = TaskProcessor()

    def check(self, job_id: str) -> Job:
        return self.job_store.get_job(job_id)
