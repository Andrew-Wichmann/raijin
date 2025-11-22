from typing import Protocol
from models.models import Job


class TaskProcessorProtocol(Protocol):
    def add(self, x: int, y: int) -> Job: ...
