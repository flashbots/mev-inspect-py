from typing import List

from pydantic import BaseModel


class PunkBid(BaseModel):
    block_number: int
    transaction_hash: str
    trace_address: List[int]
    from_address: str
    punk_index: int
    price: int
