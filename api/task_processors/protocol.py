import datetime
from typing import Protocol
from models import Job, RadarRequest


class TaskProcessorProtocol(Protocol):
    def radarize(
        self, cob_date: datetime.date, requests: list[RadarRequest]
    ) -> Job: ...
