import datetime
from typing import Protocol
from models import Job, Instrument


class TaskProcessorProtocol(Protocol):
    def radarize(self, cob_date: datetime.date, requests: list[Instrument]) -> Job: ...
