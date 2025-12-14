import datetime
from typing import Protocol, Callable, Iterable
from models import Instrument, Response


class TaskProcessorProtocol(Protocol):
    def radarize(
        self,
        cob_date: datetime.date,
        requests: list[Instrument],
        on_task_complete: Callable[[list[Response]], None],
        on_error: Callable[[str], None],
        on_complete: Callable[[], None],
    ) -> None: ...
