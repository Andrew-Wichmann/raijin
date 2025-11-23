import enum


class Status(str, enum.Enum):
    NOT_FOUND = "NOT_FOUND"
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
