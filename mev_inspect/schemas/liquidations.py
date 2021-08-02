from enum import Enum
from .utils import CamelModel


class LiquidationType(Enum):
    compound_v2_ceth_liquidation = "compound_v2_ceth_liquidation"
    compound_v2_ctoken_liquidation = "compound_v2_ctoken_liquidation"  # TODO: add logic to handle ctoken liquidations


class LiquidationStatus(Enum):
    seized = "seized"  # succesfully completed
    check = "check"  # just a liquidation check. i.e searcher only checks if opportunity is still available and reverts accordingly
    out_of_gas = "out_of_gas"  # tx ran out of gas


class LiquidationCollateralSource(Enum):
    aave_flashloan = "aave_flashloan"
    dydx_flashloan = "dydx_flashloan"
    uniswap_flashloan = "uniswap_flashloan"
    searcher_eoa = "searcher_eoa"  # searchers own funds
    other = "other"


class Liquidation(CamelModel):
    tx_hash: str
    borrower: str  # account that got liquidated
    collateral_provided: str  # collateral provided by searcher, 'ether' or token contract address
    collateral_provided_amount: int  # amount of collateral provided
    asset_seized: str  # asset that was given to searcher at a discount upon liquidation
    asset_seized_amount: int  # amount of asset that was given to searcher upon liquidation
    profit_in_eth: int  # profit estimated by strategy inspector
    tokenflow_estimate_in_eth: int  # profit estimated by tokenflow
    tokenflow_diff: int  # diff between tokenflow and strategy inspector
    status: LiquidationStatus
    type: LiquidationType
    collateral_source: LiquidationCollateralSource
