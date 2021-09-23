from typing import List


from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    DecodedCallTrace,
    Classification,
    Protocol,
)

from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.transfers import EthTransfer

liquidators = []


def is_transfer_from_liquidator(
    trace: ClassifiedTrace,
) -> bool:
    """Check if transfer is from liquidator"""
    transfer = EthTransfer.from_trace(trace)
    if (
        trace.classification == Classification.transfer
        and transfer.from_address in liquidators
    ):
        return True
    else:
        return False


def is_transfer_to_liquidator(trace: ClassifiedTrace) -> bool:
    """Check if transfer is to liquidator"""
    transfer = EthTransfer.from_trace(trace)
    if (
        trace.classification == Classification.transfer
        and transfer.to_address in liquidators
    ):
        return True
    else:
        return False


def get_liquidations(
    traces: List[ClassifiedTrace],
) -> List[Liquidation]:

    """Inspect list of classified traces and identify liquidation"""
    # liquidation_traces: List[DecodedCallTrace] = []
    liquidations: List[Liquidation] = []
    transfers_to: List = []
    transfers_from: List = []
    unique_transaction_hashes: List = []

    for trace in traces:

        if (
            trace.classification == Classification.liquidate
            and isinstance(trace, DecodedCallTrace)
            and trace.transaction_hash not in unique_transaction_hashes
        ):

            liquidators.append(trace.from_address)
            transfer = EthTransfer.from_trace(trace)
            unique_transaction_hashes.append(trace.transaction_hash)

            liquidations.append(
                Liquidation(
                    liquidated_user=trace.inputs["_user"],
                    collateral_token_address=trace.inputs["_collateral"],
                    debt_token_address=trace.inputs["_reserve"],
                    liquidator_user=transfer.from_address,
                    debt_purchase_amount=trace.inputs["_purchaseAmount"],
                    protocol=Protocol.aave,
                    transaction_hash=trace.transaction_hash,
                    block_number=trace.block_number,
                )
            )

        elif is_transfer_from_liquidator(trace):

            # Add the transfer
            print(trace)
            transfers_from.append(EthTransfer.from_trace(trace))
            unique_transaction_hashes.append(trace.transaction_hash)

        elif is_transfer_to_liquidator(trace):

            # Add the transfer
            print(trace)
            transfers_to.append(EthTransfer.from_trace(trace))

    print(unique_transaction_hashes)
    print(transfers_to)
    print(transfers_from)
    print(liquidations)
    return liquidations
