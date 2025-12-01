from pydantic import BaseModel, Field
from typing import Optional


class SubmitJobResponse(BaseModel):
    job_id: int
    group_id: Optional[str] = Field(default=None)
