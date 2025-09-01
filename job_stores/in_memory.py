from typing import Dict, Optional
from models import Job, Status
from uuid import uuid4


class InMemoryJobStore:
    def __init__(self):
        self.jobs: Dict[str, Job] = {}

    def add_job(self) -> Job:
        job = Job(job_id=str(uuid4()), status=Status.PENDING)
        self.jobs[job.job_id] = job
        return job

    def get_job(self, job_id: str) -> Job:
        return self.jobs[job_id]

    def update_job(self, job_id: str, status: Status, result: Optional[int] = None):
        job = self.get_job(job_id)
        job.status = status
        if result:
            job.result = result
