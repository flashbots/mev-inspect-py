from typing import Dict, List, Optional

from pydantic import BaseModel

from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    Classification,
    Protocol,
)
from mev_inspect.schemas.strategies import Arbitrage


class Transfer(BaseModel):
    from_address: str
    to_address: str
    amount: int
    token_address: str


class Swap(BaseModel):
    transaction_hash: str
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
            child_traces = _get_child_traces(trace.trace_address, traces)
            swap = _build_swap(trace, prior_transfers, child_traces)

            if swap is not None:
                swaps.append(swap)

    return swaps


def _build_swap(
    trace: ClassifiedTrace,
    prior_transfers: List[Transfer],
    child_traces: List[ClassifiedTrace],
) -> Optional[Swap]:
    if trace.abi_name == "UniswapV2Pair":
        pool_address = trace.to_address
        transfers_to_pool = [
            transfer
            for transfer in prior_transfers
            if transfer.to_address == pool_address
        ]

        # expecting a prior transfer to the pool
        if len(transfers_to_pool) == 0:
            return None

        most_recent_transfer_to_pool = transfers_to_pool[-1]
        all_pool_internal_transfers = [
            _as_transfer(child)
            for child in child_traces
            if child.classification == Classification.transfer
        ]

        # expecting exactly one transfer inside the pool
        if len(all_pool_internal_transfers) != 1:
            return None

        pool_internal_transfer = all_pool_internal_transfers[0]

        return Swap(
            transaction_hash=trace.transaction_hash,
            pool_address=pool_address,
            from_address=most_recent_transfer_to_pool.from_address,
            to_address=pool_internal_transfer.to_address,
            token_in_address=most_recent_transfer_to_pool.token_address,
            token_in_amount=most_recent_transfer_to_pool.amount,
            token_out_address=pool_internal_transfer.token_address,
            token_out_amount=pool_internal_transfer.amount,
        )

    return None


def _get_child_traces(
    parent_trace_address: List[int],
    traces: List[ClassifiedTrace],
) -> List[ClassifiedTrace]:
    ordered_traces = sorted(traces, key=lambda t: t.trace_address)
    child_traces = []

    for trace in ordered_traces:
        if _is_child_trace_address(
            parent_trace_address,
            trace.trace_address,
        ):
            child_traces.append(trace)

    return child_traces


def _is_child_trace_address(
    parent_trace_address: List[int],
    maybe_child_trace_address: List[int],
) -> bool:
    parent_trace_length = len(parent_trace_address)
    return (len(maybe_child_trace_address) == parent_trace_length + 1) and (
        maybe_child_trace_address[:parent_trace_length] == parent_trace_address
    )


def _as_transfer(trace: ClassifiedTrace) -> Transfer:
    # todo - this should be enforced at the data level
    if trace.inputs is None:
        raise ValueError("Invalid transfer")

    if trace.protocol == Protocol.weth:
        return Transfer(
            amount=trace.inputs["wad"],
            to_address=trace.inputs["dst"],
            from_address=trace.from_address,
            token_address=trace.to_address,
        )
    else:
        return Transfer(
            amount=trace.inputs["amount"],
            to_address=trace.inputs["recipient"],
            from_address=trace.from_address,
            token_address=trace.to_address,
        )
