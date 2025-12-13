from pydantic import BaseModel, Field

from models.radar import Radar


class Result(BaseModel):
    source: str  # maybe enum
    radar: Radar = Field(description="Octal encoded radar object")
