from pydantic import BaseModel
from models.job import Job
from models.status import Status


class CheckJobResponse(BaseModel):
    job: Job
    status: Status
