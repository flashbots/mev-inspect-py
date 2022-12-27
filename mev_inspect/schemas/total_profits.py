from pydantic import BaseModel


class TotalProfits(BaseModel):
    block_number: int
    transaction_hash: str
    token_debt: str
    amount_debt: int
    token_received: str
    amount_received: int
