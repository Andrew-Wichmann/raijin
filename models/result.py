from pydantic import BaseModel, Field

from models.radar_source import RadarSource
from models.radar import Radar
from models.instruments import Instrument


class Result(BaseModel):
    instrument: Instrument
    source: RadarSource
    radar: Radar = Field(description="Octal encoded radar object")
