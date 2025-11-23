from pydantic import BaseModel, Field


class ConfigBase(BaseModel):
    enabled: bool = Field(
        default=False, description="Determines whether this config is active or not."
    )
