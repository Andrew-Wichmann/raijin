import enum


class Status(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    RESTARTING = "RESTARTING"
    CANCELED = "CANCELED"
    FAILED = "FAILED"
