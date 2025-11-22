import tornado
import logging
import pydantic
from models import (
    CheckJobResponse,
    ErrorResponse,
    CheckJobRequest,
)
from api.app import Raijin


class CheckJobHandler(tornado.web.RequestHandler):
    application: Raijin

    async def post(self):
        try:
            req = CheckJobRequest.model_validate_json(self.request.body)
        except pydantic.ValidationError as e:
            self.set_status(400)
            self.set_header("Content-Type", "application/json")
            self.write(ErrorResponse(error=str(e)).model_dump_json())
            return
        try:
            job = self.application.job_store.get_job(req.job_id)
            self.set_status(200)
            self.set_header("Content-Type", "application/json")
            self.write(CheckJobResponse(job=job).model_dump_json())
        except Exception as e:
            logging.exception("Exception in CheckJobHandler")
            self.set_status(500)
            self.set_header("Content-Type", "application/json")
            self.write(ErrorResponse(error=str(e)).model_dump_json())
