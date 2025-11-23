import tornado
import logging
from api.config import RaijinConfig
import api.job_stores
import api.task_processors
from api.job_stores.in_memory import InMemoryJobStore
from api.task_processors.thread import ThreadTaskProcessor

logger = logging.getLogger(__name__)


class Raijin(tornado.web.Application):
    def __init__(self, config: RaijinConfig, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.job_store = api.job_stores.from_config(config.store)
        self.task_processor = api.task_processors.from_config(
            self.job_store, config.task_processor
        )
        if isinstance(self.job_store, InMemoryJobStore) and not isinstance(
            self.task_processor, ThreadTaskProcessor
        ):
            raise ValueError(
                "In the interest of simplicity, in memory job store only works with the ThreadTaskProcessor"
            )
