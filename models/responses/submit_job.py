from pydantic import BaseModel, Field
from typing import Optional

from models.ids import job_id as job_id_type, group_id as group_id_type


class SubmitJobResponse(BaseModel):
    job_id: job_id_type
    group_id: Optional[group_id_type] = Field(default=None)
