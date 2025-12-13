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
            request = SubmitJobRequest.model_validate_json(self.request.body)
        except pydantic.ValidationError as e:
            self.raijin_write(ErrorResponse(error=str(e)), 400)
            return
        try:
            response = self.application.job_service.submit_job(request)
            self.raijin_write(response, 200)
        except Exception as e:
            logging.exception("Exception in SubmitJobHandler")
            self.raijin_write(ErrorResponse(error=str(e)), 500)
