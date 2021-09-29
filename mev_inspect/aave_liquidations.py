from typing import List

from mev_inspect.traces import (
    get_child_traces,
    is_child_of_any_address,
)
from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    DecodedCallTrace,
    Classification,
    Protocol,
)

from mev_inspect.schemas.transfers import ERC20Transfer
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
    # AAVE AMM Market DAI
    "0x79bE75FFC64DD58e66787E4Eae470c8a1FD08ba4",
]


def get_aave_liquidations(
    traces: List[ClassifiedTrace],
) -> List[Liquidation]:

    """Inspect list of classified traces and identify liquidation"""
    liquidations: List[Liquidation] = []
    parent_liquidations: List[List[int]] = []

    for trace in traces:

        if (
            trace.classification == Classification.liquidate
            and isinstance(trace, DecodedCallTrace)
            and not is_child_of_any_address(trace, parent_liquidations)
        ):

            parent_liquidations.append(trace.trace_address)
            liquidator = trace.from_address

            child_traces = get_child_traces(
                trace.transaction_hash, trace.trace_address, traces
            )

            received_amount = _get_liquidator_payback(child_traces, liquidator)

            liquidations.append(
                Liquidation(
                    liquidated_user=trace.inputs["_user"],
                    collateral_token_address=trace.inputs["_collateral"],
                    debt_token_address=trace.inputs["_reserve"],
                    liquidator_user=liquidator,
                    debt_purchase_amount=trace.inputs["_purchaseAmount"],
                    protocol=Protocol.aave,
                    received_amount=received_amount,
                    transaction_hash=trace.transaction_hash,
                    trace_address=trace.trace_address,
                    block_number=trace.block_number,
                )
            )
    return liquidations


def _get_liquidator_payback(
    child_traces: List[ClassifiedTrace], liquidator: str
) -> int:
    for child in child_traces:
        if child.classification == Classification.transfer:

            child_transfer = ERC20Transfer.from_trace(child)

            if (child_transfer.to_address == liquidator) and (
                child.from_address in AAVE_CONTRACT_ADDRESSES
            ):
                return child_transfer.amount

    return 0
