from pydantic import BaseModel, Field


class Result(BaseModel):
    source: str  # maybe enum
    radar: str = Field(description="Octal encoded radar object")
