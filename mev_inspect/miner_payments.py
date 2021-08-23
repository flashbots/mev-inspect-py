from typing import Dict, List

from mev_inspect.schemas.classified_traces import ClassifiedTrace
from mev_inspect.schemas.miner_payments import MinerPayment
from mev_inspect.transfers import (
    get_eth_transfers,
    filter_transfers,
)


def get_miner_payments(
    miner_address: str, traces: List[ClassifiedTrace]
) -> List[MinerPayment]:
    eth_transfers = get_eth_transfers(traces)
    miner_eth_transfers = filter_transfers(
        eth_transfers, to_address=miner_address.lower()
    )

    eth_by_transaction: Dict[str, int] = {}
    for transfer in miner_eth_transfers:
        existing_amount = eth_by_transaction.get(transfer.transaction_hash, 0)
        eth_by_transaction[transfer.transaction_hash] = (
            existing_amount + transfer.amount
        )

    return [
        MinerPayment(
            transaction_hash=transaction_hash,
            total_eth_transfer_payment=eth_amount,
        )
        for transaction_hash, eth_amount in eth_by_transaction.items()
    ]
