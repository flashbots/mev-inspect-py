from typing import Optional, List
from enum import Enum
from pydantic import BaseModel
from .classified_traces import ClassifiedTrace, Protocol

class StrategyType(Enum):
    arbitrage = "arbitrage"
    liquidation = "liquidation"

class Strategy(BaseModel):
    strategy: StrategyType
    protocols: List[Protocol]

class Liquidation(Strategy):
    collateral_type: str
    collateral_amount: int
    collateral_source: str
    reserve: str

class LiquidationData(Liquidation):
    profit: float
    traces: List[ClassifiedTrace]
