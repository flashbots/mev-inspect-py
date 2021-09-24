from typing import List

from mev_inspect.traces import get_child_traces
from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    DecodedCallTrace,
    Classification,
    Protocol,
)

from mev_inspect.schemas.liquidations import Liquidation

AAVE_CONTRACT_ADDRESSES: List[str] = [
    # AAVE Proxy
    "0x398ec7346dcd622edc5ae82352f02be94c62d119",
    # AAVE V2
    "0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9",
    # AAVE V1
    "0x3dfd23a6c5e8bbcfc9581d2e864a68feb6a076d3",
    # AAVE V2 WETH
    "0x030ba81f1c18d280636f32af80b9aad02cf0854e",
]


def is_liquidator_payback(trace: ClassifiedTrace, liquidator: str) -> bool:
    """Finds liquidator payback """

    if isinstance(trace, DecodedCallTrace):
        if "recipient" in trace.inputs:

            if (
                trace.inputs["recipient"] == liquidator
                and trace.from_address in AAVE_CONTRACT_ADDRESSES
            ):
                return True

        elif "dst" in trace.inputs:
            if (
                trace.inputs["dst"] == liquidator
                and trace.from_address in AAVE_CONTRACT_ADDRESSES
            ):
                return True

    return False


def get_received_amount(trace: DecodedCallTrace) -> int:

    if "amount" in trace.inputs:
        received_amount = int(trace.inputs["amount"])

    elif "wad" in trace.inputs:
        received_amount = int(trace.inputs["wad"])

    else:
        received_amount = 0

    return received_amount


def get_liquidations(
    traces: List[ClassifiedTrace],
) -> List[Liquidation]:

    """Inspect list of classified traces and identify liquidation"""
    liquidations: List[Liquidation] = []

    for trace in traces:

        if trace.classification == Classification.liquidate and isinstance(
            trace, DecodedCallTrace
        ):

            liquidator = trace.from_address

            child_traces = get_child_traces(
                trace.transaction_hash, trace.trace_address, traces
            )

            for child in child_traces:

                if child.classification == Classification.liquidate:
                    traces.remove(child)

                if is_liquidator_payback(child, liquidator):

                    assert isinstance(child, DecodedCallTrace)
                    received_amount = get_received_amount(child)

            liquidations.append(
                Liquidation(
                    liquidated_user=trace.inputs["_user"],
                    collateral_token_address=trace.inputs["_collateral"],
                    debt_token_address=trace.inputs["_reserve"],
                    liquidator_user=liquidator,
                    debt_purchase_amount=trace.inputs["_purchaseAmount"],
                    protocol=Protocol.aave,
                    received_amount=received_amount,
                    # aToken lookup is out of scope for now, WIP
                    received_token_address=trace.inputs["_collateral"],
                    transaction_hash=trace.transaction_hash,
                    block_number=trace.block_number,
                )
            )

    return liquidations
