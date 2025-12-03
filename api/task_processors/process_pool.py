import datetime
from concurrent.futures import ProcessPoolExecutor, Future
from api.job_stores import JobStoreProtocol
from models import Status, Job
import logging
from api.config.task_processors.process_pool import ProcessPoolTaskProcessorConfig
from models.radar_request import RadarRequest

logger = logging.getLogger(__name__)


def _radarize(radar_request: RadarRequest) -> int:
    return 0


class ProcessPoolTaskProcessor:
    def __init__(
        self, job_store: JobStoreProtocol, config: ProcessPoolTaskProcessorConfig
    ):
        self.job_store = job_store
        self.executor = ProcessPoolExecutor(max_workers=config.max_workers)

    def radarize(self, cob_date: datetime.date, requests: list[RadarRequest]) -> Job:
        def _on_complete(fut: Future):
            if exception := fut.exception():
                logging.exception(f"Job failed: {exception}")
                self.job_store.update_job(job.job_id, status=Status.FAILED)
                return

            logger.info("completed")
            result = fut.result()
            self.job_store.update_job(job.job_id, status=Status.COMPLETE, result=result)

        job = self.job_store.add_job()
        for req in requests:
            fut = self.executor.submit(_radarize, req)
            fut.add_done_callback(_on_complete)
        return job
