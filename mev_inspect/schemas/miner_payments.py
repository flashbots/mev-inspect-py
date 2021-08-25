from pydantic import BaseModel


class MinerPayment(BaseModel):
    block_number: int
    transaction_hash: str
    transaction_index: int
    miner_address: str
    wei_transfered_to_miner: int
    effective_gas_price: int
    gas_used: int
