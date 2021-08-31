from typing import Optional

from pydantic import BaseModel


class MinerPayment(BaseModel):
    block_number: int
    transaction_hash: str
    transaction_index: int
    miner_address: str
    coinbase_transfer: int
    base_fee_per_gas: int
    gas_price: int
    gas_price_with_coinbase_transfer: int
    gas_used: int
    transaction_to_address: Optional[str]
    transaction_from_address: Optional[str]
