import tornado
from typing import Optional
import logging
import pydantic
from models import ResultsRequest, ErrorResponse
from api.app import Raijin


class ResultsHandler(tornado.web.RequestHandler):
    application: Raijin

    async def get(self, job_id: Optional[int] = None, group_id: Optional[int] = None):
        try:
            req = ResultsRequest(job_id=job_id, group_id=group_id)
        except pydantic.ValidationError as e:
            self.set_status(400)
            self.set_header("Content-Type", "application/json")
            self.write(ErrorResponse(error=str(e)).model_dump_json())
            return
        logging.info(f"{req.model_dump()}")
