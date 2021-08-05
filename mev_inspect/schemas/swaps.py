from typing import List, Optional

from pydantic import BaseModel

from mev_inspect.schemas.classified_traces import Protocol


class Swap(BaseModel):
    abi_name: str
    transaction_hash: str
    trace_address: List[int]
    protocol: Optional[Protocol]
    pool_address: str
    from_address: str
    to_address: str
    token_in_address: str
    token_in_amount: int
    token_out_address: str
    token_out_amount: int
