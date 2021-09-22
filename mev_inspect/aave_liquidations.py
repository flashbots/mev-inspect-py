from typing import List


from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    DecodedCallTrace,
    Classification,
    Protocol,
)

from mev_inspect.schemas.liquidations import Liquidation


def get_liquidations(
    traces: List[ClassifiedTrace],
) -> List[Liquidation]:

    """Inspect list of classified traces and identify liquidation"""
    # liquidation_traces: List[DecodedCallTrace] = []
    liquidations: List[Liquidation] = []

    for trace in traces:

        if trace.classification == Classification.liquidate and isinstance(
            trace, DecodedCallTrace
        ):

            liquidations.append(
                Liquidation(
                    liquidated_user=trace.inputs["_user"],
                    liquidator_user=trace.inputs["_liquidator"],
                    collateral_token_address=trace.inputs["_collateral"],
                    collateral_amount=trace.inputs["_liquidatedCollateralAmount"],
                    debt_token_address=trace.inputs["_reserve"],
                    debt_purchase_amount=trace.inputs["_purchaseAmount"],
                    # received_token_address=,
                    # received_amount=,
                    protocol=Protocol.aave,
                    transaction_hash=trace.transaction_hash,
                    block_number=trace.block_number,
                )
            )

    print(liquidations)
    return liquidations
