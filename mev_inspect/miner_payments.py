from typing import List

from mev_inspect.schemas.classified_traces import ClassifiedTrace
from mev_inspect.schemas.miner_payments import MinerPayment
from mev_inspect.traces import get_traces_by_transaction_hash
from mev_inspect.transfers import (
    filter_transfers,
    get_eth_transfers,
)


def get_miner_payments(
    miner_address: str, traces: List[ClassifiedTrace]
) -> List[MinerPayment]:
    miner_payments = []

    for transaction_hash, transaciton_traces in get_traces_by_transaction_hash(traces):
        eth_transfers = get_eth_transfers(list(transaciton_traces))
        miner_eth_transfers = filter_transfers(
            eth_transfers, to_address=miner_address.lower()
        )
        total_eth_transfer_payment = sum(
            transfer.amount for transfer in miner_eth_transfers
        )

        if total_eth_transfer_payment > 0:
            miner_payments.append(
                MinerPayment(
                    transaction_hash=transaction_hash,
                    total_eth_transfer_payment=total_eth_transfer_payment,
                )
            )

    return miner_payments
