from typing import List
from pydantic import BaseModel
from mev_inspect.schemas.classified_traces import Protocol


class Liquidation(BaseModel):
    liquidated_user: str
    liquidator_user: str
    collateral_token_address: str
    debt_token_address: str
    debt_purchase_amount: int
    received_amount: int
    protocol: Protocol
    transaction_hash: str
    trace_address: List[int]
    block_number: str
