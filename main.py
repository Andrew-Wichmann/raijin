import logging
import tornado

from app import Raijin
from request_handlers import CheckJobHandler, SubmitJobHandler

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    port = 8888
    logging.info(f"Starting app on http://localhost:{port}")
    app = Raijin([(r"/submit_job", SubmitJobHandler), (r"/check_job", CheckJobHandler)])
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
