from typing import Optional
from pydantic import BaseModel
import enum


class SubmitJobRequest(BaseModel):
    x: int
    y: int


class ErrorResponse(BaseModel):
    error: str


class SubmitJobResponse(BaseModel):
    job_id: str


class CheckJobRequest(BaseModel):
    job_id: str


class Status(enum.Enum):
    NOT_FOUND = "NOT_FOUND"
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class Job(BaseModel):
    job_id: str
    status: Status
    result: Optional[int] = None


class CheckJobResponse(BaseModel):
    job: Job
    # status: Status
    # result: Optional[int]
