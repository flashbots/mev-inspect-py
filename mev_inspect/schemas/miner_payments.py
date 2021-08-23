from pydantic import BaseModel


class MinerPayment(BaseModel):
    transaction_hash: str
    total_eth_transfer_payment: int
