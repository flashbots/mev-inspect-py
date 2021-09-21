from typing import List

from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    DecodedCallTrace,
    Classification,
)

from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.transfers import ERC20Transfer

LIQUIDATION_CONTRACT_ADDRESSES = [
    "0x3dfd23A6c5E8BbcFc9581d2E864a68feb6a076d3",
    "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9",
    "0x398eC7346DcD622eDc5ae82352F02bE94C62d119",
]


def find_liquidations_from_traces(
    traces: List,
) -> List:
    """Inspect list of classified traces and identify liquidation"""
    tx = []
    liquidations = []
    result = []
    unique_transfer_hashes: List[str]
    transfers_to: List[List] = [[]]
    transfers_from: List[List] = [[]]
    liquidator: str

    for trace in traces:

        if isinstance(trace, DecodedCallTrace):

            # Check for liquidation and register trace and unique liquidator
            if (
                trace.classification == Classification.liquidate
                and trace.transaction_hash not in tx
            ):

                liquidations.append(trace)
                LIQUIDATION_CONTRACT_ADDRESSES.append(trace.from_address)
                tx.append(trace.transaction_hash)

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

            elif is_transfer_from_liquidator(trace, unique_transfer_hashes):

                # Add the transfer
                liquidator = next(
                    (
                        LIQUIDATION_CONTRACT_ADDRESSES[i]
                        for i in range(len(LIQUIDATION_CONTRACT_ADDRESSES))
                        if trace.inputs["sender"] == LIQUIDATION_CONTRACT_ADDRESSES[i]
                    ),
                    "",
                )

                transfers_from.append(
                    ["from", liquidator, trace.transaction_hash, trace.inputs["amount"]]
                )
                unique_transfer_hashes.append(trace.transaction_hash)

            elif is_transfer_to_liquidator(trace):

                # Add the transfer
                liquidator = next(
                    (
                        LIQUIDATION_CONTRACT_ADDRESSES[i]
                        for i in range(len(LIQUIDATION_CONTRACT_ADDRESSES))
                        if trace.inputs["recipient"]
                        == LIQUIDATION_CONTRACT_ADDRESSES[i]
                    ),
                    "",
                )
                transfers_to.append(
                    ["to", liquidator, trace.transaction_hash, trace.inputs["amount"]]
                )

    return [result, transfers_to, transfers_from]


def is_transfer_from_liquidator(
    trace: ClassifiedTrace,
    unique_transfer_hashes: List[str],
) -> bool:
    """Check if transfer is from liquidator"""
    transfer = ERC20Transfer.from_trace(trace)
    if (
        trace.classification == Classification.transfer
        and transfer.from_address in LIQUIDATION_CONTRACT_ADDRESSES
        and trace.transaction_hash not in unique_transfer_hashes
    ):
        return True
    else:
        return False


def is_transfer_to_liquidator(trace: ClassifiedTrace) -> bool:
    """Check if transfer is to liquidator"""
    transfer = ERC20Transfer.from_trace(trace)
    if (
        trace.classification == Classification.transfer
        and transfer.to_address in LIQUIDATION_CONTRACT_ADDRESSES
    ):
        return True
    else:
        return False
