from typing import List, Optional, Tuple

from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.traces import (
    Classification,
    ClassifiedTrace,
    DecodedCallTrace,
    Protocol,
)
from mev_inspect.schemas.transfers import Transfer
from mev_inspect.traces import get_child_traces, is_child_of_any_address
from mev_inspect.transfers import get_transfer


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
            (debt_token_address, debt_purchase_amount) = _get_debt_data(
                trace, child_traces, liquidator
            )

            (received_token_address, received_amount) = _get_received_data(
                trace, child_traces, liquidator
            )

            liquidations.append(
                Liquidation(
                    liquidated_user=trace.inputs["_user"],
                    debt_token_address=debt_token_address,
                    liquidator_user=liquidator,
                    debt_purchase_amount=debt_purchase_amount,
                    protocol=Protocol.aave,
                    received_amount=received_amount,
                    received_token_address=received_token_address,
                    transaction_hash=trace.transaction_hash,
                    trace_address=trace.trace_address,
                    block_number=trace.block_number,
                    error=trace.error,
                )
            )

    return liquidations


def _get_received_data(
    liquidation: DecodedCallTrace, child_traces: List[ClassifiedTrace], liquidator: str
) -> Tuple[str, int]:

    """Look for and return liquidator payback from liquidation"""
    for child in child_traces:

        child_transfer: Optional[Transfer] = get_transfer(child)

        if child_transfer is not None and child_transfer.to_address == liquidator:
            return child_transfer.token_address, child_transfer.amount

    if liquidation.error is not None:
        return liquidation.inputs["_collateral"], 0

    else:
        raise RuntimeError(
            f"No payback or input data found for liquidation in tx: {liquidation.transaction_hash}"
        )


def _get_debt_data(
    liquidation: DecodedCallTrace, child_traces: List[ClassifiedTrace], liquidator: str
) -> Tuple[str, int]:
    """Get transfer from liquidator to AAVE"""

    for child in child_traces:

        child_transfer: Optional[Transfer] = get_transfer(child)

        if child_transfer is not None:

            if child_transfer.from_address == liquidator:
                return child_transfer.token_address, child_transfer.amount

    if liquidation.error is not None:
        return liquidation.inputs["_reserve"], liquidation.inputs["_purchaseAmount"]

    else:
        raise RuntimeError(
            f"No transfer or input data found for liquidation in tx: {liquidation.transaction_hash}"
        )
