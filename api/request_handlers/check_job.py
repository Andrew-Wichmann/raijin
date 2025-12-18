import logging
import pydantic
from models import (
    ErrorResponse,
)
from api.app import Raijin
from api.request_handlers.base import RaijinRequestHandler


class CheckJobHandler(RaijinRequestHandler):
    application: Raijin

    async def get(self, job_id: str):
        try:
            response = self.application.job_service.check_job(int(job_id))
            self.raijin_write(response)
        except Exception as e:
            logging.exception("Exception in CheckJobHandler")
            self.raijin_write(ErrorResponse(error=str(e)), 500)
