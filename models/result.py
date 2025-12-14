from pydantic import BaseModel, Field

from models.radar_source import RadarSource
from models.radar import Radar


class Result(BaseModel):
    source: RadarSource
    radar: Radar = Field(description="Octal encoded radar object")
