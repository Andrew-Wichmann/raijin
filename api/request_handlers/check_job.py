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
            request = CheckJobRequest.model_validate_json(self.request.body)
        except pydantic.ValidationError as e:
            self.raijin_write(ErrorResponse(error=str(e)), 500)
            return
        try:
            response = self.application.job_service.check_job(request)
            self.raijin_write(response)
        except Exception as e:
            logging.exception("Exception in CheckJobHandler")
            self.raijin_write(ErrorResponse(error=str(e)), 500)
