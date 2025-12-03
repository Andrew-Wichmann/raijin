"""Radar request models."""

from pydantic import BaseModel


class RadarRequest(BaseModel):
    """Base radar request."""

    pass


class EquityOptionRadarRequest(RadarRequest):
    """Equity option radar request."""

    pass


class BondRadarRequest(RadarRequest):
    """Bond radar request."""

    pass


class CommodityRadarRequest(RadarRequest):
    """Commodity radar request."""

    pass


class FutureRadarRequest(RadarRequest):
    """Future radar request."""

    pass
