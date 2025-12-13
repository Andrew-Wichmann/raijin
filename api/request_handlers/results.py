import logging
import pydantic
from models import ResultsRequest, ErrorResponse, ResultsResponse, Response, Instrument, Result
from api.app import Raijin
from api.request_handlers.base import RaijinRequestHandler


class ResultsHandler(RaijinRequestHandler):
    application: Raijin

    async def get(self):
        try:
            job_id = self.get_argument('job_id', default=None)
            group_id = self.get_argument('group_id', default=None)
            if job_id and group_id:
                raise ValueError("Can not request results from a job and a group. You must provide either a job or a group id")
            elif not job_id and not group_id:
                raise ValueError("You must provide a job or a group id")
            elif job_id:
                request = ResultsRequest(job_id=int(job_id))
            elif group_id:
                request = ResultsRequest(group_id=int(group_id))
            else:
                raise ValueError("Logic itself is broken")

        except (pydantic.ValidationError, ValueError) as e:
            self.raijin_write(ErrorResponse(error=str(e)), 400)
            return

        response = self.application.job_service.results(request)
        self.raijin_write(response)
