from typing import List, Optional

from pydantic import BaseModel

from mev_inspect.schemas.traces import Protocol


class NftTrade(BaseModel):
    abi_name: str
    transaction_hash: str
    transaction_position: int
    block_number: int
    trace_address: List[int]
    protocol: Optional[Protocol]
    error: Optional[str]
    seller_address: str
    buyer_address: str
    payment_token_address: str
    payment_amount: int
    collection_address: str
    token_id: int
