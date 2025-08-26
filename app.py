import time
from typing import Optional, Tuple
import tornado
from concurrent.futures import Future
from models import Status


class TaskProcessor:
    def add(self, x: int, y: int) -> int:
        time.sleep(10)
        return x + y


class Raijin(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jobs: dict[str, Future] = {}
        self.task_processor = TaskProcessor()

    def check(self, job_id: str) -> Tuple[Status, Optional[int]]:
        if job_id not in self.jobs:
            return Status.NOT_FOUND, None
        future = self.jobs[job_id]
        if not future.done():
            return Status.PENDING, None
        result = future.result()
        del self.jobs[job_id]
        return Status.COMPLETE, result
