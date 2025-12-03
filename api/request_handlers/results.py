import tornado
import logging
import pydantic
from models import (
    ResultsResponse,
    ErrorResponse,
    ResultsRequest,
)
from api.app import Raijin


class ResultsHandler(tornado.web.RequestHandler):
    application: Raijin

    async def post(self):
        try:
            req = ResultsRequest.model_validate_json(self.request.body)
        except pydantic.ValidationError as e:
            self.set_status(400)
            self.set_header("Content-Type", "application/json")
            self.write(ErrorResponse(error=str(e)).model_dump_json())
            return
        try:
            # TODO: Implement actual results retrieval
            self.set_status(501)
            self.set_header("Content-Type", "application/json")
            self.write(ErrorResponse(error="Not implemented").model_dump_json())
        except Exception as e:
            logging.exception("Exception in ResultsHandler")
            self.set_status(500)
            self.set_header("Content-Type", "application/json")
            self.write(ErrorResponse(error=str(e)).model_dump_json())
