import logging
import tornado

logging.basicConfig(level=logging.INFO)

from app import Raijin
from request_handlers import CheckJobHandler, SubmitJobHandler

if __name__ == "__main__":
    port = 8888
    logging.info(f"Starting app on http://localhost:{port}")
    app = Raijin([(r"/submit_job", SubmitJobHandler), (r"/check_job", CheckJobHandler)])
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
