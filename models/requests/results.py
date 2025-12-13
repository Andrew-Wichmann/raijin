from typing import Optional
from pydantic import BaseModel, Field, model_validator


class ResultsRequest(BaseModel):
    job_id: Optional[int] = Field()
    group_id: Optional[int] = Field(default=None)

    @model_validator(mode="after")
    def xor_job_group_id(self):
        if not bool(self.job_id) ^ bool(self.group_id):
            raise ValueError(
                f"ResultsRequest must have job_id or group_id set. Got {self.job_id=} {self.group_id=}"
            )
        return self
