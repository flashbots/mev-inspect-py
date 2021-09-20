from pydantic import BaseModel


class Liquidation(BaseModel):
    liquidated_user: str
    collateral_address: str
    collateral_amount: int
    collateral_source: str
    reserve: str
