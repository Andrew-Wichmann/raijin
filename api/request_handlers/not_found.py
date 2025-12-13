from api.request_handlers.base import RaijinRequestHandler
from models import ErrorResponse

class NotFoundHandler(RaijinRequestHandler):
    def prepare(self):
        self.raijin_write(ErrorResponse(error="Not Found"), 404)

