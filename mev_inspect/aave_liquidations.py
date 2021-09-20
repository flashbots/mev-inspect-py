from typing import List

from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    DecodedCallTrace,
    Classification,
)
from mev_inspect.schemas.liquidations import Liquidation

contract_addresses = [
    "0x3dfd23A6c5E8BbcFc9581d2E864a68feb6a076d3",
    "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9",
    "0x398eC7346DcD622eDc5ae82352F02bE94C62d119",
]


def get_liquidations(traces: List[ClassifiedTrace]) -> List[Liquidation]:
    """Inspect list of classified traces and identify liquidation"""
    tx = []
    liquidations = []
    result = []

    # Protocol contract address must be in included

    # Used to remove double-counted 'from' transfers
    unique_transfers = []
    transfers_to = []
    transfers_from = []

    for trace in traces:

        if isinstance(trace, DecodedCallTrace):

            # Check for liquidation and register trace and unique liquidator
            if (
                trace.classification == Classification.liquidate
                and trace.transaction_hash not in tx
            ):

                liquidations.append(trace)
                contract_addresses.append(trace.from_address)
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

            # Check for transfer from a liquidator
            elif (
                trace.classification == Classification.transfer
                and "sender" in trace.inputs
                and trace.inputs["sender"] in contract_addresses
                and trace.transaction_hash not in unique_transfers
            ):

                # Add the transfer
                liquidator = next(
                    contract_addresses[i]
                    for i in range(len(contract_addresses))
                    if trace.inputs["sender"] == contract_addresses[i]
                )
                transfers_from.append(
                    ["from", liquidator, trace.transaction_hash, trace.inputs["amount"]]
                )
                unique_transfers.append(trace.transaction_hash)

            # Check for transfer to a liquidator
            elif (
                trace.classification == Classification.transfer
                and trace.inputs["recipient"] in contract_addresses
            ):
                # Add the transfer
                liquidator = next(
                    contract_addresses[i]
                    for i in range(len(contract_addresses))
                    if trace.inputs["recipient"] == contract_addresses[i]
                )
                transfers_to.append(
                    ["to", liquidator, trace.transaction_hash, trace.inputs["amount"]]
                )

    return result

    # for count, trace in enumerate(liquidations):
    # tx = trace.transaction_hash
    # convert token to ETH
    # profit = transfers[count][2] - transfers[count+1][2]

    # for count, trace in enumerate(transfers_to):
    # profits.append({"liquidator" : transfers_to[count][1],
    # "transaction" : transfers_to[count][2],
    # "profit" : transfers_to[count][3] - transfers_from[count][3]})
