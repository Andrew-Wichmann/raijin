import datetime
from typing import Optional
from pydantic import BaseModel, Field
from models.instruments import Instrument


class SubmitJobRequest(BaseModel):
    cob_date: datetime.date = Field(
        description="The close of business (cob) date to pin market data to to produce radars for"
    )
    requests: list[Instrument] = Field(
        description="The instruments to generate radars for"
    )
    group_id: Optional[str] = Field(
        default=None,
        description="An optional id to correlate batched requests together.",
    )
    enable_cache: bool = Field(
        default=True,
        description="Whether or not to use cache results and whether to cache results",
    )
