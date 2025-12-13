from typing import Optional
from pydantic import BaseModel, Field
from models.instruments import Instrument
from models.result import Result


class Response(BaseModel):
    request: Instrument
    result: Result


class ResultsResponse(BaseModel):
    job_id: str = Field()
    responses: list[Response]
    group_id: Optional[str] = Field(default=None)
    next_page: Optional[str]
