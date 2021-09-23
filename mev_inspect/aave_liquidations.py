from typing import List


from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    DecodedCallTrace,
    Classification,
    Protocol,
)

from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.transfers import Transfer, EthTransfer, ERC20Transfer

liquidators: List[str] = []


def is_transfer_from_liquidator(trace: ClassifiedTrace, liquidator: str) -> bool:
    """Check if transfer is from liquidator"""

    transfer: Transfer

    try:

        transfer = ERC20Transfer.from_trace(trace)
        if transfer.from_address == liquidator:
            return True
        else:
            return False

    except ValueError:

        pass

    try:

        transfer = EthTransfer.from_trace(trace)
        if transfer.from_address == liquidator:
            return True
        else:
            return False

    except ValueError:

        if trace.from_address == liquidator:
            # print(trace.inputs)
            return True
        else:
            return False


def is_transfer_to_liquidator(trace: ClassifiedTrace, liquidator: str) -> bool:
    """Check if transfer is to liquidator"""

    transfer: Transfer

    try:

        transfer = ERC20Transfer.from_trace(trace)
        if transfer.to_address == liquidator:
            return True
        else:
            return False

    except ValueError:

        pass

    try:

        transfer = EthTransfer.from_trace(trace)
        if transfer.to_address == liquidator:
            print(transfer.amount, transfer.from_address)
            return True
        else:
            return False

    except ValueError:

        if trace.to_address == liquidator:
            # print(trace.inputs)
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

            liquidator = trace.from_address

            transfers_to = [
                EthTransfer.from_trace(t)
                for t in traces
                if is_transfer_to_liquidator(t, liquidator)
            ]
            print(transfers_to)

            transfers_from = [
                EthTransfer.from_trace(t)
                for t in traces
                if is_transfer_from_liquidator(t, liquidator)
            ]
            print(transfers_from)

            unique_transaction_hashes.append(trace.transaction_hash)

            liquidations.append(
                Liquidation(
                    liquidated_user=trace.inputs["_user"],
                    collateral_token_address=trace.inputs["_collateral"],
                    debt_token_address=trace.inputs["_reserve"],
                    liquidator_user=liquidator,
                    debt_purchase_amount=trace.inputs["_purchaseAmount"],
                    protocol=Protocol.aave,
                    # aToken lookup is out of scope for now, WIP
                    received_token_address=trace.inputs["_collateral"],
                    transaction_hash=trace.transaction_hash,
                    block_number=trace.block_number,
                )
            )

    print(liquidations)
    return liquidations
