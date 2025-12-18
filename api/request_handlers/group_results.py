import pydantic
from models import ResultsRequest, ErrorResponse, ResultsResponse
from api.app import Raijin
from api.request_handlers.base import RaijinRequestHandler
import logging


class GroupResultsHandler(RaijinRequestHandler):
    application: Raijin

    async def get(self, group_id):
        try:
            group_id = int(group_id)
            response = self.application.job_service.results_by_group(group_id)
            self.raijin_write(ResultsResponse(group_id=group_id, results=response))
        except Exception as e:
            logging.exception("Exception in GroupResultsHandler")
            self.raijin_write(ErrorResponse(error=str(e)), 500)
