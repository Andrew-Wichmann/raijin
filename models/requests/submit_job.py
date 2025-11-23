from pydantic import BaseModel


class SubmitJobRequest(BaseModel):
    x: int
    y: int


class SubmitJobResponse(BaseModel):
    job_id: str
