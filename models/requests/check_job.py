from pydantic import BaseModel


class CheckJobRequest(BaseModel):
    job_id: str
