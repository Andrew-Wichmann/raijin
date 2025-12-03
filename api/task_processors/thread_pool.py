from typing import List
import datetime
from concurrent.futures import ThreadPoolExecutor, Future
from api.job_stores import JobStoreProtocol
from models import Status, Job
import logging
from api.config.task_processors.thread_pool import ThreadPoolTaskProcessorConfig
from models.radar import Radar
from models.radar_request import RadarRequest

logger = logging.getLogger(__name__)


def _radarize(_: RadarRequest) -> List[Radar]:
    import time

    time.sleep(11)
    return [Radar("0123456701234567"), Radar("0123456701234567")]


class ThreadPoolTaskProcessor:
    def __init__(
        self, job_store: JobStoreProtocol, config: ThreadPoolTaskProcessorConfig
    ):
        self.job_store = job_store
        self.executor = ThreadPoolExecutor(max_workers=config.max_workers)

    def radarize(self, cob_date: datetime.date, requests: list[RadarRequest]) -> Job:
        def _on_complete(fut: Future):
            if exception := fut.exception():
                logging.exception(f"Job failed: {exception}")
                self.job_store.update_job(job.job_id, status=Status.FAILED)
                return
            results = fut.result()
            self.job_store.add_results(results)
            self.job_store.update_job(job.job_id, status=Status.COMPLETE)
            logger.info("completed")

        job = self.job_store.add_job()
        for req in requests:
            fut = self.executor.submit(_radarize, req)
            fut.add_done_callback(_on_complete)
        return job
