import datetime
from typing import Protocol, Callable, Iterable, List
from models import Instrument, Result


class TaskProcessorProtocol(Protocol):
    def radarize(
        self,
        cob_date: datetime.date,
        requests: List[Instrument],
        on_task_complete: Callable[[List[Result]], None],
        on_error: Callable[[str], None],
        on_complete: Callable[[], None],
    ) -> None: ...
