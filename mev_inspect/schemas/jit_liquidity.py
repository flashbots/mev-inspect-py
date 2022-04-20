from typing import List

from pydantic import BaseModel


from .swaps import Swap


class JITLiquidity(BaseModel):
    block_number: int
    bot_address: str
    pool_address: str
    mint_transaction_hash: str
    mint_trace: List[int]
    burn_transaction_hash: str
    burn_trace: List[int]
    swaps: List[Swap]
    token0_address: str
    token1_address: str
    mint_token0_amount: int
    mint_token1_amount: int
    burn_token0_amount: int
    burn_token1_amount: int
    token0_swap_volume: int
    token1_swap_volume: int



