import logging
from api.job_state_machine import JobStateMachine
from api.job_stores.protocol import JobStoreProtocol
from api.task_processors.protocol import TaskProcessorProtocol

from models import (
    CheckJobRequest,
    CheckJobResponse,
    SubmitJobRequest,
    ResultsResponse,
    ResultsRequest,
    Response,
    Instrument,
    Result,
    Job,
)
from models.responses.submit_job import SubmitJobResponse
from models.status import Status

logger = logging.getLogger(__name__)


class JobService:
    def __init__(
        self, job_store: JobStoreProtocol, task_processor: TaskProcessorProtocol
    ):
        self.job_store = job_store
        self.task_processor = task_processor

    def _job_updated(self, job: Job, from_status: Status, to_status: Status):
        logger.info(f"Updated {job} from {from_status} to {to_status}")

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

    def check_job(self, request: CheckJobRequest) -> CheckJobResponse:
        job = self.job_store.get_job(request.job_id)
        return CheckJobResponse(job=job, status=job.status)

    def results(self, request: ResultsRequest) -> ResultsResponse:
        if request.job_id is not None:
            responses = self.job_store.get_results_by_job_id(request.job_id)
            return ResultsResponse(
                job_id=request.job_id,
                responses=responses,
            )
        elif request.group_id is not None:
            responses = self.job_store.get_results_by_group_id(request.group_id)
            return ResultsResponse(
                group_id=request.group_id,
                responses=responses,
            )
        else:
            raise ValueError(
                f"Invalid request. Expected a job_id or a group_id. Received: {request}"
            )
