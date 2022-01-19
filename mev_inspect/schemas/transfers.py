from typing import List

from pydantic import BaseModel


class Transfer(BaseModel):
    block_number: int
    transaction_hash: str
    trace_address: List[int]
    from_address: str
    to_address: str
    amount: int
    token_address: str
