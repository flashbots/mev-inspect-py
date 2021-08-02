from mev_inspect.schemas.classified_traces import ClassifiedTrace
from mev_inspect.schemas.liquidations import (
    Liquidation,
    LiquidationType,
    LiquidationStatus,
)


# TODO: check tx status and assign accordingly
# i.e if a tx checks if the opportunity is still available ("liquidateBorrowAllowed")
# or if it calls the COMP oracle for price data ("getUnderlyingPrice(address")
def is_pre_flight():
    pass


# TODO: fetch historic price (in ETH) of any given token at the block height the tx occured
# to calculate the profit in ETH accurately, regardless of what token the profit was held in
def get_historic_token_price():
    pass


# TODO: for any given cToken, get the underlying token from the comptroller markets
# i.e cDAI => DAI
def get_underlying_ctoken_asset():
    pass


# TODO: find if the searcher repays the loan from their own EOA, by buying it from a DEX, or w/ a flashloan
def find_collateral_source():
    pass


def inspect_compound_v2_ceth(classified_traces: list[ClassifiedTrace]) -> Liquidation:
    # TODO: complete this logic after asking about type choices

    # flow:
    # 1. decide if it's a pre-flight check tx or an actual liquidation
    # 2. parse `liquidateBorrow` and `seize` sub traces to determine actual amounts
    # 3. calculate net profit by finding out the worth of seized tokens
    # 4. use tokenflow module to find out profit independent of the inspector, calculate diff
    # 5. prepare return object to get it ready for db processing

    for classified_trace in classified_traces:
        if classified_trace.function_name == "liquidateBorrow":
            liquidation = Liquidation(
                tx_hash="0x0",
                borrower="0x0",
                collateral_provided="0x0",
                collateral_provided_amount=0,
                asset_seized="0x0",
                asset_seized_amount=0,
                profit_in_eth=0,
                tokenflow_estimate_in_eth=0,
                collateral_source="other",
                tokenflow_diff=0,
                status=LiquidationStatus.seized,
                type=LiquidationType.compound_v2_ceth_liquidation,
            )

    return liquidation
