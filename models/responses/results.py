from pydantic import BaseModel
from models.radar import Radar


class ResultsResponse(BaseModel):
    radars: list[Radar]
