from typing import Optional
from pydantic import BaseModel, Field
from models.instruments import Instrument
from models.result import Result
from models.ids import group_id as group_id_type, job_id as job_id_type


class Response(BaseModel):
    instrument: Instrument
    result: Result


class ResultsResponse(BaseModel):
    job_id: Optional[job_id_type] = Field(default=None)
    group_id: Optional[group_id_type] = Field(default=None)
    responses: list[Response]
    next_page: Optional[str] = Field(default=None)
