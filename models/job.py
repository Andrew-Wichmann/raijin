from typing import Optional

from pydantic import BaseModel
from models.status import Status
from models.ids import job_id, group_id as group_id_type


class Job(BaseModel):
    job_id: job_id
    group_id: Optional[group_id_type] = None
    status: Status
