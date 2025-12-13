import logging
import pydantic
from models import (
    CheckJobResponse,
    ErrorResponse,
    CheckJobRequest,
)
from api.app import Raijin
from api.request_handlers.base import RaijinRequestHandler


class CheckJobHandler(RaijinRequestHandler):
    application: Raijin

    async def post(self):
        try:
            req = CheckJobRequest.model_validate_json(self.request.body)
        except pydantic.ValidationError as e:
            self.raijin_write(ErrorResponse(error=str(e)), 500)
            return
        try:
            job = self.application.job_store.get_job(req.job_id)
            self.raijin_write(CheckJobResponse(job=job, status=job.status))
        except Exception as e:
            logging.exception("Exception in CheckJobHandler")
            self.raijin_write(ErrorResponse(error=str(e)), 500)
