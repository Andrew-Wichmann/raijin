import time
from concurrent.futures import ThreadPoolExecutor, Future
from api.job_stores import JobStoreProtocol
from models import Status, Job
import logging
from api.config.task_processors.thread_pool import ThreadPoolTaskProcessorConfig

logger = logging.getLogger(__name__)


def _add(x: int, y: int) -> int:
    logger.info(f"adding {x} + {y}")
    time.sleep(10)
    return x + y


class ThreadPoolTaskProcessor:
    def __init__(
        self, job_store: JobStoreProtocol, config: ThreadPoolTaskProcessorConfig
    ):
        self.job_store = job_store
        self.executor = ThreadPoolExecutor(max_workers=config.max_workers)

    def add(self, x: int, y: int) -> Job:
        def _on_complete(fut: Future):
            if exception := fut.exception():
                logging.exception(f"Job failed: {exception}")
                self.job_store.update_job(job.job_id, status=Status.FAILED)
                return

            logger.info(f"completed {x} + {y}")
            result = fut.result()
            self.job_store.update_job(job.job_id, status=Status.COMPLETE, result=result)

        job = self.job_store.add_job()
        fut = self.executor.submit(_add, x, y)
        fut.add_done_callback(_on_complete)
        return job
