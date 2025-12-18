import datetime
from concurrent.futures import ProcessPoolExecutor, Future
from api.job_stores import JobStoreProtocol
from models import Status, Job, Result
import logging
from api.config.task_processors.process_pool import ProcessPoolTaskProcessorConfig
from models.instruments import Instrument
from typing import Callable


logger = logging.getLogger(__name__)


def _radarize(instrument: Instrument, cob_date: datetime.date) -> int:
    return 0


class ProcessPoolTaskProcessor:
    def __init__(self, config: ProcessPoolTaskProcessorConfig):
        self.executor = ProcessPoolExecutor(max_workers=config.max_workers)

    def radarize(
        self,
        cob_date: datetime.date,
        requests: list[Instrument],
        on_task_complete: Callable[[list[Result]], None],
        on_error: Callable[[str], None],
        on_complete: Callable[[], None],
    ) -> None:
        pass
        # def _on_complete(fut: Future):
        #    if exception := fut.exception():
        #        logging.exception(f"Job failed: {exception}")
        #        self.job_store.update_job(job.job_id, status=Status.FAILED)
        #        return

        #    logger.info("completed")
        #    result = fut.result()
        #    self.job_store.update_job(job.job_id, status=Status.COMPLETE)

        # job = self.job_store.add_job()
        # for req in requests:
        #    fut = self.executor.submit(_radarize, req, cob_date)
        #    fut.add_done_callback(_on_complete)
        # return job
