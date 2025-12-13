import tornado
import pydantic

class RaijinRequestHandler(tornado.web.RequestHandler):
    def raijin_write(self, response: pydantic.BaseModel, status=200):
        body = response.model_dump_json()
        self.set_status(status)
        self.set_header("Content-Type", "application/json")
        self.set_header("X-Message-Type", response.__class__.__name__)
        self.write(body)
