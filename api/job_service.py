import logging
from api.job_state_machine import JobStateMachine
from api.job_stores.protocol import JobStoreProtocol
from api.task_processors.protocol import TaskProcessorProtocol

from models import (
    CheckJobResponse,
    SubmitJobRequest,
    ResultsResponse,
    ResultsRequest,
    Response,
    Job,
)
from models.responses.submit_job import SubmitJobResponse
from models.status import Status
from models.ids import group_id, job_id

logger = logging.getLogger(__name__)


class JobService:
    def __init__(self, job_store: JobStoreProtocol, task_processor: TaskProcessorProtocol):
        self.job_store = job_store
        self.task_processor = task_processor

    def _job_updated(self, job: Job, from_status: Status, to_status: Status):
        logger.info(f"Updated {job} from {from_status} to {to_status}")

    # TODO: I don't think the service should know about requests and responses. So factor those out.
    def submit_job(self, request: SubmitJobRequest) -> SubmitJobResponse:
        job = self.job_store.add_job()
        state_machine = JobStateMachine(job, self.job_store, update=self._job_updated)
        self.task_processor.radarize(
            request.cob_date,
            request.requests,
            on_complete=state_machine.complete,
            on_error=state_machine.error,
            on_task_complete=state_machine.task_complete,
        )
        state_machine.start()
        if request.group_id:
            return SubmitJobResponse(job_id=job.job_id, group_id=job.group_id)
        else:
            return SubmitJobResponse(job_id=job.job_id)

    # TODO: I don't think the service should know about requests and responses. So factor those out.
    def check_job(self, job_id: job_id) -> CheckJobResponse:
        job = self.job_store.get_job(job_id)
        return CheckJobResponse(job=job, status=job.status)

    def results_by_group(self, group_id: group_id) -> list[Response]:
        return self.job_store.get_results_by_group_id(group_id)

    def results_by_job(self, job_id: job_id) -> list[Response]:
        return self.job_store.get_results_by_job_id(job_id)
