import threading
from typing import Callable
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


def _radarize(
    instruments: list[Instrument],
    cob_date: datetime.date,
    cancel_event: threading.Event,
) -> list[Response]:
    logger.info(f"Radarizing {len(instruments)} for cob_date {cob_date.isoformat()}")
    responses = []
    for instrument in instruments:
        if cancel_event.is_set():
            logger.warning("cancel event triggered. Dropping responses and exiting.")
            return []
        time.sleep(random.randint(0, 1))
        if random.randint(0, 100) <= 1:
            raise Exception("Boom")
        random_radar = "".join([random.choice("01234567") for _ in range(100)])
        responses.append(
            Response(
                instrument=instrument,
                result=Result(source=RadarSource.BUILT, radar=random_radar),
            )
        )
    return responses


class ThreadPoolTaskProcessor:
    BATCH_SIZE = 10

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
        children: list[Future[list[Response]]] = []
        cancel_event = threading.Event()
        lock = threading.Lock()

        def _on_task_complete(fut: Future[list[Response]]):
            nonlocal completed_requests
            nonlocal children
            nonlocal cancel_event
            with lock:
                if exception := fut.exception():
                    cancel_event.set()
                    logging.exception(f"Child task failed: {exception}")
                    on_error(str(exception))
                    for child in children:
                        child.cancel()
                    return
                results = fut.result()
                on_task_complete(results)
                completed_requests += len(results)
                logger.info(f"completed {completed_requests}/{len(requests)}")
                if completed_requests == len(requests):
                    on_complete()

        for i in range(0, len(requests), self.BATCH_SIZE):
            child = self.executor.submit(_radarize, requests[i : i + self.BATCH_SIZE], cob_date, cancel_event)
            child.add_done_callback(_on_task_complete)
            children.append(child)
