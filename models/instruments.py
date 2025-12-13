from pydantic import BaseModel, Field


class Instrument(BaseModel):
    identifier: str = Field()


class BondInstrument(Instrument):
    isin: str = Field(description="ISIN id")
    cusip: str = Field(description="CUSIP id")


class EquityOptionInstrument(Instrument):
    osi: str = Field(description="OSI id")


class FutureInstrument(Instrument):
    pass


class CommodityInstrument(Instrument):
    bbg_id: str = Field(description="Bloomberg id for the commodity")
