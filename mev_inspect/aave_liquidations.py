from typing import List

from mev_inspect.schemas.classified_traces import (
    DecodedCallTrace,
    Classification,
)

from mev_inspect.schemas.liquidations import Liquidation


LIQUIDATION_CONTRACT_ADDRESSES = [
    "0x3dfd23A6c5E8BbcFc9581d2E864a68feb6a076d3",
    "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9",
    "0x398eC7346DcD622eDc5ae82352F02bE94C62d119",
]


def find_liquidations_from_traces(
    traces: List[ClassifiedTrace],
) -> List[Liquidation]:

    """Inspect list of classified traces and identify liquidation"""

    seen_transactions: List[str] = []
    liquidations: List[ClassifiedTrace] = []
    result: List[Liquidation] = []

    for trace in traces:

        if isinstance(trace, DecodedCallTrace):

            # Check for liquidation and register trace and unique liquidator
            if (
                trace.classification == Classification.liquidate
                and trace.transaction_hash not in seen_transactions
            ):

                liquidations.append(trace)
                LIQUIDATION_CONTRACT_ADDRESSES.append(trace.from_address)
                seen_transactions.append(trace.transaction_hash)

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
