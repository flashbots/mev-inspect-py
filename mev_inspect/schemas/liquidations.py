from typing import List, Optional
from pydantic import BaseModel
from mev_inspect.schemas.traces import Protocol


class Liquidation(BaseModel):
    liquidated_user: str
    liquidator_user: str
    debt_token_address: str
    debt_purchase_amount: int
    received_amount: int
    received_token_address: Optional[str]
    protocol: Protocol
    transaction_hash: str
    trace_address: List[int]
    block_number: str
