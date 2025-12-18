import argparse
import logging
import tornado
import json

from api.app import Raijin
from api.config import RaijinConfig
from api.request_handlers.check_job import CheckJobHandler
from api.request_handlers.not_found import NotFoundHandler
from api.request_handlers.submit_job import SubmitJobHandler
from api.request_handlers.job_results import JobResultsHandler
from api.request_handlers.group_results import GroupResultsHandler
from api.request_handlers.groups import GroupsHandler

parser = argparse.ArgumentParser(description="Raijin Web Application")
parser.add_argument("--env_file", help="A custom env file to use")
args = parser.parse_args()

if args.env_file:
    # probably fine since we'll only be creating one instance
    RaijinConfig.model_config["env_file"] = args.env_file

config = RaijinConfig()

logging.basicConfig(level=config.log_level.value)

if __name__ == "__main__":
    port = 8888
    logging.info(f"Starting app on http://localhost:{port}")

    # super inappropriate json pretty print if switching to structlog
    logging.info(f"config: {json.dumps(config.model_dump(), indent=4)}")

    app = Raijin(
        config,
        [
            (r"/jobs", SubmitJobHandler),
            (r"/jobs/([0-9]+)", CheckJobHandler),
            (r"/jobs/([0-9]+)/results", JobResultsHandler),
            (r"/groups/([0-9]+)", GroupsHandler),
            (r"/groups/([0-9]+)/results", GroupResultsHandler),
            (r".*", NotFoundHandler),
        ],
    )
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
