from typing import List

from pydantic import BaseModel

from .swaps import Swap


class Sandwich(BaseModel):
    block_number: int
    sandwicher_address: str
    frontrun_swap: Swap
    backrun_swap: Swap
    sandwiched_swaps: List[Swap]
