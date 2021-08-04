from typing import Optional, List
from enum import Enum
from pydantic import BaseModel
from .classified_traces import ClassifiedTrace, Protocol

class StrategyType(Enum):
	arbitrage = "arbitrage"
	liquidation = "liquidation"

class Strategy(BaseModel):
	strategy: StrategyType
	traces: List[ClassifiedTrace]
	protocols: List[Protocol]

class Liquidation(Strategy):
    collateral_type: str
    collateral_amount: int
    collateral_source: str
    reserve: str
