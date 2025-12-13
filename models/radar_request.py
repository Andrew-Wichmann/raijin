from pydantic import BaseModel, Field


class RadarRequest(BaseModel):
    identifier: str = Field()


class BondRadarRequest(RadarRequest):
    isin: str = Field(description="ISIN id")
    cusip: str = Field(description="CUSIP id")


class EquityOptionRadarRequest(RadarRequest):
    osi: str = Field(description="OSI id")


class FutureRadarRequest(RadarRequest):
    pass


class CommodityRadarRequest(RadarRequest):
    bbg_id: str = Field(description="Bloomberg id for the commodity")
