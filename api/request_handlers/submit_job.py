import tornado
import logging
import pydantic
from models import (
    SubmitJobRequest,
    ErrorResponse,
    SubmitJobResponse,
)
from api.app import Raijin
from api.request_handlers.base import RaijinRequestHandler


class SubmitJobHandler(RaijinRequestHandler):
    application: Raijin

    async def post(self):
        try:
            req = SubmitJobRequest.model_validate_json(self.request.body)
        except pydantic.ValidationError as e:
            self.raijin_write(ErrorResponse(error=str(e)), 400)
            return
        try:
            job = self.application.task_processor.radarize(req.cob_date, req.requests)
            self.raijin_write(SubmitJobResponse(job_id=job.job_id), 200)
        except Exception as e:
            logging.exception("Exception in SubmitJobHandler")
            self.raijin_write(ErrorResponse(error=str(e)), 500)
