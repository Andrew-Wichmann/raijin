from pydantic import BaseModel


class SubmitJobResponse(BaseModel):
    job_id: str
