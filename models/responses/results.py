from typing import Optional
from pydantic import BaseModel, Field
from models.radar_request import RadarRequest
from models.result import Result


class Response(BaseModel):
    request: RadarRequest
    result: Result


class ResultsResponse(BaseModel):
    job_id: str = Field()
    responses: list[Response]
    group_id: Optional[str] = Field(default=None)
    next_page: Optional[str]
