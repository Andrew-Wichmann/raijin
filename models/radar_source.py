import enum


class RadarSource(str, enum.Enum):
    BUILT = "built"
    CACHE = "cache"
    ARCHIVE = "archive"
    YOUR_MOMS_HOUSE = "your_moms_house"
