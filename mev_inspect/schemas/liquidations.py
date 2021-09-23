from pydantic import BaseModel
from mev_inspect.schemas.classified_traces import Protocol


class Liquidation(BaseModel):
    liquidated_user: str
    liquidator_user: str
    # collateral
    collateral_token_address: str
    # collateral_amount: int
    # debtToCover
    debt_token_address: str
    # purchaseAmount
    debt_purchase_amount: int
    received_token_address: str
    # received_amount: int
    protocol: Protocol
    transaction_hash: str
    block_number: str


class LiquidationData(Liquidation):
    liquidator_user: str
    collateral_amount: int
    received_token_address: str
    received_amount: int
