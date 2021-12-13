from typing import List, Tuple, Optional

from mev_inspect.traces import (
    get_child_traces,
    is_child_of_any_address,
)
from mev_inspect.schemas.traces import (
    ClassifiedTrace,
    CallTrace,
    DecodedCallTrace,
    Classification,
    Protocol,
)


from mev_inspect.transfers import get_transfer
from mev_inspect.schemas.transfers import Transfer
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
    "0x79be75ffc64dd58e66787e4eae470c8a1fd08ba4",
    # AAVE i
    "0x030ba81f1c18d280636f32af80b9aad02cf0854e",
    "0xbcca60bb61934080951369a648fb03df4f96263c",
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
            and trace.protocol == Protocol.aave
        ):

            parent_liquidations.append(trace.trace_address)
            liquidator = trace.from_address

            child_traces = get_child_traces(
                trace.transaction_hash, trace.trace_address, traces
            )

            (
                received_token_address,
                received_amount,
            ) = _get_payback_token_and_amount(trace, child_traces, liquidator)

            liquidations.append(
                Liquidation(
                    liquidated_user=trace.inputs["_user"],
                    debt_token_address=trace.inputs["_reserve"],
                    liquidator_user=liquidator,
                    debt_purchase_amount=trace.inputs["_purchaseAmount"],
                    protocol=Protocol.aave,
                    received_amount=received_amount,
                    received_token_address=received_token_address,
                    transaction_hash=trace.transaction_hash,
                    trace_address=trace.trace_address,
                    block_number=trace.block_number,
                )
            )

    return liquidations


def _get_payback_token_and_amount(
    liquidation: DecodedCallTrace, child_traces: List[ClassifiedTrace], liquidator: str
) -> Tuple[str, int]:

    """Look for and return liquidator payback from liquidation"""

    for child in child_traces:

        if isinstance(child, CallTrace):

            child_transfer: Optional[Transfer] = get_transfer(child)

            if child_transfer is not None:

                if (
                    child_transfer.to_address == liquidator
                    and child.from_address in AAVE_CONTRACT_ADDRESSES
                ):

                    return child_transfer.token_address, child_transfer.amount

    return liquidation.inputs["_collateral"], 0
