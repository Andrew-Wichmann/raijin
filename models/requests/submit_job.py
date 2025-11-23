from pydantic import BaseModel


class SubmitJobRequest(BaseModel):
    x: int
    y: int
