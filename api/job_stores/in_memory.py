from typing import Dict, Optional, List
from models import Job, Status
from models.ids import job_id, group_id
from threading import Lock

from api.config.job_stores.in_memory import InMemoryJobStoreConfig
from models.result import Result


class InMemoryJobStore:
    def __init__(self, _: InMemoryJobStoreConfig):
        self.__jobs: Dict[job_id, Job] = {}
        self.__results_by_job_id: Dict[job_id, List[Result]] = {}
        self.__results_by_group_id: Dict[group_id, List[Result]] = {}
        self.__lock = Lock()
        self.__current_job_id = 0

    def add_job(self, group_id: Optional[int] = None) -> Job:
        with self.__lock:
            job = Job(job_id=self.__current_job_id, group_id=group_id, status=Status.PENDING)
            self.__jobs[job.job_id] = job
            self.__current_job_id += 1
        return job

    def get_job(self, job_id: int) -> Job:
        with self.__lock:
            return self.__jobs[job_id]

    def update_job(self, job: Job, status: Status, error: Optional[str] = None):
        with self.__lock:
            job.status = status
            if error:
                job.error_message = error

    def add_results(self, job: Job, results: List[Result]):
        with self.__lock:
            if not self.__results_by_job_id.get(job.job_id):
                self.__results_by_job_id[job.job_id] = []
            self.__results_by_job_id[job.job_id].extend(results)

            if job.group_id:
                if not self.__results_by_group_id.get(job.group_id):
                    self.__results_by_group_id[job.group_id] = []
                self.__results_by_group_id[job.group_id].extend(results)

    # Might be nice to eventually make this a generator
    def get_results_by_job_id(self, job_id: job_id, page: int = 0, page_size: int = 0) -> List[Result]:
        with self.__lock:
            results = self.__results_by_job_id[job_id]
            if page_size == 0:
                page_size = len(results)
            return results[page * page_size : (page + 1) * page_size]

    # Might be nice to eventually make this a generator
    def get_results_by_group_id(self, group_id: group_id, page: int = 0, page_size: int = 0) -> List[Result]:
        with self.__lock:
            results = self.__results_by_group_id[group_id]
            if page_size == 0:
                page_size = len(results)
            return results[page * page_size : (page + 1) * page_size]
