from typing import List

from mev_inspect.schemas.classified_traces import ClassifiedTrace
from mev_inspect.schemas.miner_payments import MinerPayment
from mev_inspect.schemas.receipts import Receipt
from mev_inspect.traces import get_traces_by_transaction_hash
from mev_inspect.transfers import (
    filter_transfers,
    get_eth_transfers,
)


def get_miner_payments(
    miner_address: str, traces: List[ClassifiedTrace], receipts: List[Receipt]
) -> List[MinerPayment]:
    miner_payments = []

    traces_by_transaction_hash = get_traces_by_transaction_hash(traces)

    for receipt in receipts:
        transaciton_traces = traces_by_transaction_hash[receipt.transaction_hash]
        eth_transfers = get_eth_transfers(transaciton_traces)
        miner_eth_transfers = filter_transfers(
            eth_transfers, to_address=miner_address.lower()
        )

        wei_transfered_to_miner = sum(
            transfer.amount for transfer in miner_eth_transfers
        )

        miner_payments.append(
            MinerPayment(
                miner_address=miner_address,
                block_number=receipt.block_number,
                transaction_hash=receipt.transaction_hash,
                transaction_index=receipt.transaction_index,
                effective_gas_price=receipt.effective_gas_price,
                gas_used=receipt.gas_used,
                wei_transfered_to_miner=wei_transfered_to_miner,
            )
        )

    return miner_payments
