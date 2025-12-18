import pydantic
import logging
from models import ResultsRequest, ErrorResponse, job
from api.app import Raijin
from api.request_handlers.base import RaijinRequestHandler
from models.responses.results import ResultsResponse


class JobResultsHandler(RaijinRequestHandler):
    application: Raijin

    async def get(self, job_id):
        try:
            job_id = int(job_id)
            responses = self.application.job_service.results_by_job(job_id)
            self.raijin_write(ResultsResponse(job_id=job_id, responses=responses))
        except Exception as e:
            logging.exception("Exception in JobResultsHandler")
            self.raijin_write(ErrorResponse(error=str(e)), 500)
