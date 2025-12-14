import threading
from typing import Callable, Iterable, List
from itertools import islice
import random
import time
import datetime
from concurrent.futures import ThreadPoolExecutor, Future
from api.job_stores import JobStoreProtocol
from models import Status, Job
import logging
from api.config.task_processors.thread_pool import ThreadPoolTaskProcessorConfig
from models.radar import Radar
from models.instruments import Instrument
from models.radar_source import RadarSource
from models.responses.error import ErrorResponse
from models.responses.results import Response
from models.result import Result

logger = logging.getLogger(__name__)


def _radarize(instruments: List[Instrument], cob_date: datetime.date) -> List[Response]:
    logger.info(f"Radarizing {len(instruments)} for cob_date {cob_date.isoformat()}")
    responses = []
    for instrument in instruments:
        time.sleep(1)
        random_radar = "".join([random.choice("01234567") for _ in range(100)])
        responses.append(
            Response(
                instrument=instrument,
                result=Result(source=RadarSource.BUILT, radar=random_radar),
            )
        )
    return responses


class ThreadPoolTaskProcessor:
    def __init__(self, config: ThreadPoolTaskProcessorConfig):
        self.executor = ThreadPoolExecutor(max_workers=config.max_workers)

    def radarize(
        self,
        cob_date: datetime.date,
        requests: list[Instrument],
        on_task_complete: Callable[[list[Response]], None],
        on_error: Callable[[str], None],
        on_complete: Callable[[], None],
    ) -> None:
        completed_requests = 0
        lock = threading.Lock()

        def _on_task_complete(fut: Future):
            if exception := fut.exception():
                logging.exception(f"Child task failed: {exception}")
                on_error(str(exception))
                return
            results = fut.result()
            on_task_complete(results)
            with lock:
                nonlocal completed_requests
                completed_requests += len(results)
                logger.info(f"completed {completed_requests}/{len(requests)}")
                if completed_requests == len(requests):
                    on_complete()

        requests_iter = iter(requests)
        while batch := list(islice(requests_iter, 10)):
            child = self.executor.submit(_radarize, batch, cob_date)
            child.add_done_callback(_on_task_complete)
