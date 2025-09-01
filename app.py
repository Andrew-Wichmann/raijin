import tornado
import logging
from job_stores import InMemoryJobStore
from task_processor import TaskProcessor

logger = logging.getLogger(__name__)


class Raijin(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_store = InMemoryJobStore()
        self.task_processor = TaskProcessor(self.job_store)
