from typing import Optional

from pydantic import BaseModel
from models.status import Status


class Job(BaseModel):
    job_id: str
    status: Status
    result: Optional[int] = None
