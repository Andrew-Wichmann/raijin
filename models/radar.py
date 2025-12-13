import typing
import pydantic

Radar = typing.Annotated[str, pydantic.Field(pattern=r"[0-7]+")]
