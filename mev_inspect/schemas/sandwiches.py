from typing import List

from pydantic import BaseModel

from .swaps import Swap


class Sandwich(BaseModel):
    block_number: int
    sandwicher_address: str
    frontrun_transaction_hash: str
    backrun_transaction_hash: str
    sandwiched_swaps: List[Swap]
