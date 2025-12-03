from pydantic import BaseModel


class ResultsRequest(BaseModel):
    job_id: int
