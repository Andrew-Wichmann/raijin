import argparse
import logging
import tornado

from app import Raijin
from settings import RaijinSettings
from request_handlers import CheckJobHandler, SubmitJobHandler
import settings

parser = argparse.ArgumentParser(description="Raijin Web Application")
parser.add_argument("--env_file", help="A custom env file to use")
args = parser.parse_args()

if args.env_file:
    RaijinSettings.model_config["env_file"] = (
        args.env_file
    )  # probably fine since we'll only be creating one instance

settings = RaijinSettings()

logging.basicConfig(level=settings.log_level.value)

if __name__ == "__main__":
    port = 8888
    logging.info(f"Starting app on http://localhost:{port}")
    app = Raijin(
        settings, [(r"/submit_job", SubmitJobHandler), (r"/check_job", CheckJobHandler)]
    )
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
