from typing import List, Union


from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    DecodedCallTrace,
    Classification,
    Protocol,
)

from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.transfers import Transfer, EthTransfer, ERC20Transfer

liquidators: List[str] = []


def is_transfer_from_liquidator(
    trace: ClassifiedTrace, liquidator: str
) -> Union[Transfer, ClassifiedTrace]:
    """Check if transfer is from liquidator"""
    transfer: Union[Transfer, ClassifiedTrace]
    result: Union[Transfer, ClassifiedTrace]

    try:

        transfer = ERC20Transfer.from_trace(trace)
        if transfer.from_address == liquidator:
            result = transfer

    except ValueError:

        pass

    try:

        transfer = EthTransfer.from_trace(trace)
        if transfer.from_address == liquidator:
            result = transfer

    except ValueError:

        if trace.from_address == liquidator:
            result = trace

    return result


def is_transfer_to_liquidator(
    trace: ClassifiedTrace, liquidator: str
) -> Union[Transfer, ClassifiedTrace]:
    """Check if transfer is to liquidator"""

    transfer: Union[Transfer, ClassifiedTrace]
    result: Union[Transfer, ClassifiedTrace]
    try:

        transfer = ERC20Transfer.from_trace(trace)
        if transfer.to_address == liquidator:
            result = transfer

    except ValueError:

        pass

    try:

        transfer = EthTransfer.from_trace(trace)
        if transfer.to_address == liquidator:
            result = transfer

    except ValueError:

        if trace.to_address == liquidator:
            result = trace

    return result


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

            for t in traces:

                from_result = is_transfer_from_liquidator(t, liquidator)
                if from_result:
                    transfers_from.append(from_result)

                to_result = is_transfer_to_liquidator(t, liquidator)
                if to_result:
                    transfers_to.append(to_result)

            print(transfers_to)
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
