from contextlib import contextmanager
from typing import Callable
from api.job_stores.protocol import JobStoreProtocol
from models import Job
from models.result import Result
from models.status import Status
import logging

logger = logging.getLogger(__name__)


@contextmanager
def _safe_transition(on_exception: Callable[[str], None]):
    try:
        yield
    except Exception as e:
        logging.exception("Error transitioning task.")
        on_exception(str(e))


class JobStateMachine:
    def __init__(
        self,
        job: Job,
        job_store: JobStoreProtocol,
        update: Callable[[Job, Status, Status], None],
    ) -> None:
        self.job_store = job_store
        self.job = job
        self.update = update

    def start(self):
        with _safe_transition(self.error):
            if self.job.status == Status.PENDING:
                self.job_store.update_job(job=self.job, status=Status.RUNNING)
            else:
                logger.error(f"Can not transition job from {self.job.status} to {Status.RUNNING}")

    def task_complete(self, results: list[Result]):
        with _safe_transition(self.error):
            self.job_store.add_results(job=self.job, results=results)

    def complete(self, force=False):
        with _safe_transition(self.error):
            if self.job.status == Status.RUNNING or force:
                init = self.job.status
                self.job_store.update_job(job=self.job, status=Status.COMPLETE)
                self.update(self.job, init, self.job.status)
                return
            else:
                logger.error(f"Can not transition job from {self.job.status} to {Status.COMPLETE} without a force")

    def error(self, error: str):
        with _safe_transition(self.error):
            init = self.job.status
            self.job_store.update_job(job=self.job, status=Status.FAILED, error=error)
            self.update(self.job, init, self.job.status)
            return

    def cancel(self):
        with _safe_transition(self.error):
            if self.job.status in (Status.RUNNING, Status.PENDING):
                init = self.job.status
                self.job_store.update_job(job=self.job, status=Status.CANCELED)
                self.update(self.job, init, self.job.status)
                return
            else:
                logger.error(f"Can not transition job from {self.job.status} to {Status.CANCELED}")

    def restart(self):
        with _safe_transition(self.error):
            if self.job.status in (
                Status.RUNNING,
                Status.PENDING,
                Status.CANCELED,
                Status.FAILED,
            ):
                init = self.job.status
                self.job_store.update_job(job=self.job, status=Status.RESTARTING)
                self.update(self.job, init, self.job.status)
                return
            else:
                logger.error(f"Can not transition job from {self.job.status} to {Status.CANCELED}")
