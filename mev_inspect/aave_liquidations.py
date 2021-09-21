from typing import List

from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    DecodedCallTrace,
    Classification,
)

from mev_inspect.schemas.liquidations import Liquidation


def find_liquidations_from_traces(
    traces: List[ClassifiedTrace],
) -> List[Liquidation]:

    """Inspect list of classified traces and identify liquidation"""

    liquidations: List[ClassifiedTrace] = []
    seen_transactions: List[str] = []
    result: List[Liquidation] = []

    for trace in traces:

        if isinstance(trace, DecodedCallTrace):

            # Check for liquidation and register trace and unique liquidator
            if (
                trace.classification == Classification.liquidate
                and trace.transaction_hash not in seen_transactions
            ):

                liquidations.append(trace)

                # Found liquidation, now parse inputs for data
                for input in trace.inputs:

                    if input == "_purchaseAmount":
                        liquidation_amount = trace.inputs[input]
                    elif input == "_collateral":
                        collateral_address = trace.inputs[input]
                        # This will be the address of the sent token
                    elif input == "_reserve":
                        reserve = trace.inputs[input]
                        # This will be the address of the received token
                    elif input == "_user":

                        liquidated_user = trace.inputs[input]
                # Register liquidation
                result.append(
                    Liquidation(
                        liquidated_user=liquidated_user,
                        collateral_address=collateral_address,
                        collateral_amount=liquidation_amount,
                        collateral_source="",
                        reserve=reserve,
                    )
                )

    return result
