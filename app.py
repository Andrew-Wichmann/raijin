import tornado
import logging
from settings import RaijinSettings, JobStore
from job_stores import InMemoryJobStore
from task_processor import TaskProcessor

logger = logging.getLogger(__name__)


class Raijin(tornado.web.Application):
    def __init__(self, settings: RaijinSettings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if settings.job_store == JobStore.IN_MEMORY:
            self.job_store = InMemoryJobStore()
        elif settings.job_store == JobStore.SQLITE:
            raise NotImplementedError("SQLite not implemented yet")
        elif settings.job_store == JobStore.REDIS:
            raise NotImplementedError("Redis not implemented yet")
        self.task_processor = TaskProcessor(self.job_store)
