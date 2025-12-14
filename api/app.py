import tornado
import logging
from api.config import RaijinConfig
from api.job_service import JobService
import api.job_stores
import api.task_processors
from api.job_stores.in_memory import InMemoryJobStore
from api.task_processors.thread_pool import ThreadPoolTaskProcessor

logger = logging.getLogger(__name__)


class Raijin(tornado.web.Application):
    def __init__(self, config: RaijinConfig, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        job_store = api.job_stores.from_config(config.job_store)
        task_processor = api.task_processors.from_config(config.task_processor)
        # The in-memory and the SQLite stores only work with the threading processor due
        # to locking requirements
        if isinstance(job_store, InMemoryJobStore) and not isinstance(
            task_processor, ThreadPoolTaskProcessor
        ):
            raise ValueError(
                "In the interest of simplicity, in memory job store only works with the ThreadTaskProcessor"
            )

        self.job_service = JobService(
            job_store=job_store, task_processor=task_processor
        )
