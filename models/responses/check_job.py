from pydantic import BaseModel
from models.job import Job


class CheckJobResponse(BaseModel):
    job: Job
    # status: Status
    # result: Optional[int]
