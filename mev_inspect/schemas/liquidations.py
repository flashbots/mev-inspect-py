from typing import List
from pydantic import BaseModel
from .classified_traces import ClassifiedTrace


class Liquidation(BaseModel):
    liquidated_usr: str
    collateral_address: str
    collateral_amount: int
    collateral_source: str
    reserve: str


class LiquidationData(Liquidation):
    profit: float
    traces: List[ClassifiedTrace]
