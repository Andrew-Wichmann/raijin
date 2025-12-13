import re


class Radar:
    def __init__(self, value: str):
        if not re.fullmatch(r"[0-7]+", value):
            raise ValueError("Radars must be octal strings")
        self.__value = value

    def __str__(self) -> str:
        return self.__value

    def __repr__(self) -> str:
        return f"Radar({self.__value[:5]!r}...)"
