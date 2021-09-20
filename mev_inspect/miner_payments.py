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
    miner_address: str,
    base_fee_per_gas: int,
    traces: List[ClassifiedTrace],
    receipts: List[Receipt],
) -> List[MinerPayment]:
    miner_payments = []

    traces_by_transaction_hash = get_traces_by_transaction_hash(traces)

    for receipt in receipts:
        transaciton_traces = traces_by_transaction_hash.get(
            receipt.transaction_hash, []
        )

        if len(transaciton_traces) == 0:
            continue

        first_trace = sorted(transaciton_traces, key=lambda t: t.trace_address)[0]

        eth_transfers = get_eth_transfers(transaciton_traces)
        miner_eth_transfers = filter_transfers(
            eth_transfers, to_address=miner_address.lower()
        )

        coinbase_transfer = sum(transfer.amount for transfer in miner_eth_transfers)

        gas_cost = receipt.effective_gas_price * receipt.gas_used
        total_gas_cost = gas_cost + coinbase_transfer
        gas_price_with_coinbase_transfer = (
            total_gas_cost / receipt.gas_used if receipt.gas_used != 0 else 0
        )

        miner_payments.append(
            MinerPayment(
                miner_address=miner_address,
                block_number=receipt.block_number,
                transaction_hash=receipt.transaction_hash,
                transaction_index=receipt.transaction_index,
                gas_price=receipt.effective_gas_price,
                gas_price_with_coinbase_transfer=gas_price_with_coinbase_transfer,
                base_fee_per_gas=base_fee_per_gas,
                gas_used=receipt.gas_used,
                coinbase_transfer=coinbase_transfer,
                transaction_to_address=first_trace.to_address,
                transaction_from_address=first_trace.from_address,
            )
        )

    return miner_payments
