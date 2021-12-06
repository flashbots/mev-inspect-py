from typing import List, Optional

from mev_inspect.traces import get_child_traces
from mev_inspect.schemas.traces import (
    ClassifiedTrace,
    Classification,
    Protocol,
)

from mev_inspect.schemas.liquidations import Liquidation

V2_COMPTROLLER_ADDRESS = "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B"
V2_C_ETHER = "0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5"
CREAM_COMPTROLLER_ADDRESS = "0x3d5BC3c8d13dcB8bF317092d84783c2697AE9258"
CREAM_CR_ETHER = "0xD06527D5e56A3495252A528C4987003b712860eE"


def get_compound_liquidations(
    traces: List[ClassifiedTrace],
) -> List[Liquidation]:

    """Inspect list of classified traces and identify liquidation"""
    liquidations: List[Liquidation] = []

    for trace in traces:
        if (
            trace.classification == Classification.liquidate
            and (
                trace.protocol == Protocol.compound_v2
                or trace.protocol == Protocol.cream
            )
            and trace.inputs is not None
            and trace.to_address is not None
        ):
            # First, we look for cEther liquidations (position paid back via tx.value)
            child_traces = get_child_traces(
                trace.transaction_hash, trace.trace_address, traces
            )
            seize_trace = _get_seize_call(child_traces)

            if seize_trace is not None and seize_trace.inputs is not None:
                c_token_collateral = trace.inputs["cTokenCollateral"]
                if trace.abi_name == "CEther":
                    liquidations.append(
                        Liquidation(
                            liquidated_user=trace.inputs["borrower"],
                            debt_token_address=c_token_collateral,
                            liquidator_user=seize_trace.inputs["liquidator"],
                            debt_purchase_amount=trace.value,
                            protocol=trace.protocol,
                            received_amount=seize_trace.inputs["seizeTokens"],
                            transaction_hash=trace.transaction_hash,
                            trace_address=trace.trace_address,
                            block_number=trace.block_number,
                        )
                    )
                elif (
                    trace.abi_name == "CToken"
                ):  # cToken liquidations where liquidator pays back via token transfer
                    liquidations.append(
                        Liquidation(
                            liquidated_user=trace.inputs["borrower"],
                            debt_token_address=c_token_collateral,
                            liquidator_user=seize_trace.inputs["liquidator"],
                            debt_purchase_amount=trace.inputs["repayAmount"],
                            protocol=trace.protocol,
                            received_amount=seize_trace.inputs["seizeTokens"],
                            transaction_hash=trace.transaction_hash,
                            trace_address=trace.trace_address,
                            block_number=trace.block_number,
                        )
                    )
    return liquidations


def _get_seize_call(traces: List[ClassifiedTrace]) -> Optional[ClassifiedTrace]:
    """Find the call to `seize` in the child traces (successful liquidation)"""
    for trace in traces:
        if trace.classification == Classification.seize:
            return trace
    return None
