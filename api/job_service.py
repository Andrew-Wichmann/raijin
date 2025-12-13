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
)
from models.responses.submit_job import SubmitJobResponse


class JobService:
    def __init__(
        self, job_store: JobStoreProtocol, task_processor: TaskProcessorProtocol
    ):
        self.job_store = job_store
        self.task_processor = task_processor

    def submit_job(self, request: SubmitJobRequest) -> SubmitJobResponse:
        job = self.task_processor.radarize(request.cob_date, request.requests)
        if request.group_id:
            return SubmitJobResponse(job_id=job.job_id, group_id=job.group_id)
        else:
            return SubmitJobResponse(job_id=job.job_id)

    def check_job(self, request: CheckJobRequest) -> CheckJobResponse:
        job = self.job_store.get_job(request.job_id)
        return CheckJobResponse(job=job, status=job.status)

    def results(self, request: ResultsRequest) -> ResultsResponse:
        if request.job_id is not None:
            return ResultsResponse(
                job_id=request.job_id,
                responses=[
                    Response(
                        instrument=Instrument(identifier="abc123"),
                        result=Result(
                            source="cache SHOULD MAKE THIS AN ENUM", radar="ABC123"
                        ),
                    )
                ],
            )
        elif request.group_id is not None:
            return ResultsResponse(
                group_id=request.group_id,
                responses=[
                    Response(
                        instrument=Instrument(identifier="abc123"),
                        result=Result(
                            source="cache SHOULD MAKE THIS AN ENUM", radar="ABC123"
                        ),
                    )
                ],
            )
        else:
            raise ValueError(
                f"Invalid request. Expected a job_id or a group_id. Received: {request}"
            )
