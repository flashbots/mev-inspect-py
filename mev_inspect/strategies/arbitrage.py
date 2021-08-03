from typing import Dict, List, Optional

from pydantic import BaseModel

from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    Classification,
    Protocol,
)
from mev_inspect.schemas.strategies import Arbitrage


class EthTransfer(BaseModel):
    from_address: str
    to_address: str
    amount: int


class Transfer(BaseModel):
    protocol: Optional[Protocol]
    from_address: str
    to_address: str
    token_address: str
    amount: int


class BalanceTracker:
    def __init__(self):
        # account address => token address => balance
        self._balances: Dict[str, Dict[str, int]] = {}

    def update(self, transfer: Transfer) -> None:
        self._change_balance(
            transfer.from_address,
            transfer.token_address,
            -transfer.amount,
        )

        self._change_balance(
            transfer.to_address,
            transfer.token_address,
            transfer.amount,
        )

    def get_all_balances(
        self,
        account_address: str,
    ) -> Dict[str, int]:
        return self._balances.get(account_address, {})

    def get_balance(
        self,
        account_address: str,
        token_address: str,
    ) -> int:
        return self.get_all_balances(account_address).get(token_address, 0)

    def _change_balance(
        self,
        account_address: str,
        token_address: str,
        amount_change: int,
    ) -> None:
        if account_address not in self._balances:
            self._balances[account_address] = {
                token_address: amount_change,
            }
        else:
            existing_balances = self._balances[account_address]
            existing_token_balance = existing_balances.get(
                token_address,
                0,
            )
            updated_token_balance = existing_token_balance + amount_change
            self._balances[account_address][token_address] = updated_token_balance


class Swap(BaseModel):
    protocol: Optional[Protocol]
    pool_address: str
    from_address: str
    to_address: str
    token_in_address: str
    token_in_amount: int
    token_out_address: str
    token_out_amount: int


def get_arbitrages(traces: List[ClassifiedTrace]) -> List[Arbitrage]:
    all_arbitrages = []
    traces_by_transaction = _group_traces_by_transaction(traces)

    for transaction_traces in traces_by_transaction.values():
        all_arbitrages += _get_arbitrages_for_transaction(
            transaction_traces,
        )

    return all_arbitrages


def _group_traces_by_transaction(
    traces: List[ClassifiedTrace],
) -> Dict[str, List[ClassifiedTrace]]:
    grouped_traces: Dict[str, List[ClassifiedTrace]] = {}

    for trace in traces:
        hash = trace.transaction_hash
        existing_traces = grouped_traces.get(hash, [])
        grouped_traces[hash] = existing_traces + [trace]

    return grouped_traces


def _get_arbitrages_for_transaction(
    traces: List[ClassifiedTrace],
) -> List[Arbitrage]:
    swaps = _get_swaps(traces)
    print(swaps)
    return []


def _get_swaps(traces: List[ClassifiedTrace]) -> List[Swap]:
    ordered_traces = list(sorted(traces, key=lambda t: t.trace_address))

    swaps: List[Swap] = []

    prior_transfers = []

    for trace in ordered_traces:
        if trace.classification == Classification.transfer:
            transfer = _as_transfer(trace)
            prior_transfers.append(transfer)

        if trace.classification == Classification.swap:
            immediate_child_traces = [
                t
                for t in ordered_traces
                if (
                    len(t.trace_address) == len(trace.trace_address) + 1
                    and (
                        t.trace_address[: len(trace.trace_address)]
                        == trace.trace_address
                    )
                )
            ]

            if trace.abi_name == "UniswapV2Pair":
                pool_address = trace.to_address
                transfer_to_pool = [
                    transfer
                    for transfer in prior_transfers
                    if transfer.to_address == pool_address
                ][
                    -1
                ]  # todo

                internal_transfer = [
                    _as_transfer(child)
                    for child in immediate_child_traces
                    if child.classification == Classification.transfer
                ][
                    0
                ]  # todo

                swap = Swap(
                    pool_address=pool_address,
                    from_address=transfer_to_pool.from_address,
                    to_address=internal_transfer.to_address,
                    token_in_address=transfer_to_pool.token_address,
                    token_in_amount=transfer_to_pool.amount,
                    token_out_address=internal_transfer.token_address,
                    token_out_amount=internal_transfer.amount,
                )

                swaps.append(swap)

    return swaps


def _as_transfer(trace: ClassifiedTrace) -> Transfer:
    # todo - this should be enforced at the data level
    if trace.inputs is None:
        raise ValueError("Invalid transfer")

    if trace.protocol == Protocol.weth:
        return Transfer(
            protocol=trace.protocol,
            amount=trace.inputs["wad"],
            to_address=trace.inputs["dst"],
            from_address=trace.from_address,
            token_address=trace.to_address,
        )
    else:
        return Transfer(
            protocol=trace.protocol,
            amount=trace.inputs["amount"],
            to_address=trace.inputs["recipient"],
            from_address=trace.from_address,
            token_address=trace.to_address,
        )
