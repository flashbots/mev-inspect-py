import json
from typing import Dict, List, Optional

from pydantic import BaseModel

from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    Classification,
    Protocol,
)
from mev_inspect.schemas.strategies import Arbitrage


class Transfer(BaseModel):
    transaction_hash: str
    trace_address: List[int]
    from_address: str
    to_address: str
    amount: int
    token_address: str


class Swap(BaseModel):
    abi_name: str
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
    print(json.dumps([swap.dict() for swap in swaps], indent=4))
    return []


def _get_swaps(traces: List[ClassifiedTrace]) -> List[Swap]:
    ordered_traces = list(sorted(traces, key=lambda t: t.trace_address))

    swaps: List[Swap] = []
    prior_traces: List[ClassifiedTrace] = []

    for trace in ordered_traces:
        if trace.classification == Classification.swap:
            child_traces = _get_child_traces(trace.trace_address, traces)
            swap = _build_swap(trace, prior_traces, child_traces)

            if swap is not None:
                swaps.append(swap)

        prior_traces.append(trace)

    return swaps


def _build_swap(
    trace: ClassifiedTrace,
    prior_traces: List[ClassifiedTrace],
    child_traces: List[ClassifiedTrace],
) -> Optional[Swap]:
    if trace.abi_name == "UniswapV2Pair":
        return _parse_uniswap_v2_swap(trace, prior_traces, child_traces)
    elif trace.abi_name == "UniswapV3Pool":
        return _parse_uniswap_v3_swap(trace, child_traces)

    return None


def _parse_uniswap_v3_swap(
    trace: ClassifiedTrace,
    child_traces: List[ClassifiedTrace],
) -> Optional[Swap]:
    if trace.inputs is None:
        return None

    pool_address = trace.to_address
    recipient_address = (
        trace.inputs["recipient"]
        if trace.inputs is not None and "recipient" in trace.inputs
        else trace.from_address
    )

    child_transfers = _remove_inner_transfers(
        [
            _as_transfer(child_trace)
            for child_trace in child_traces
            if child_trace.classification == Classification.transfer
        ]
    )

    transfers_to_pool = [
        child for child in child_transfers if child.to_address == pool_address
    ]

    transfers_from_pool_to_recipient = [
        child
        for child in child_transfers
        if (
            child.from_address == pool_address and child.to_address == recipient_address
        )
    ]

    if len(transfers_to_pool) == 1 and len(transfers_from_pool_to_recipient) == 1:
        transfer_in = transfers_to_pool[0]
        transfer_out = transfers_from_pool_to_recipient[0]

        return Swap(
            abi_name="UniswapV3Pool",
            transaction_hash=trace.transaction_hash,
            pool_address=pool_address,
            from_address=transfer_in.from_address,
            to_address=transfer_out.to_address,
            token_in_address=transfer_in.token_address,
            token_in_amount=transfer_in.amount,
            token_out_address=transfer_out.token_address,
            token_out_amount=transfer_out.amount,
        )

    return None


def _parse_uniswap_v2_swap(
    trace: ClassifiedTrace,
    prior_traces: List[ClassifiedTrace],
    child_traces: List[ClassifiedTrace],
) -> Optional[Swap]:

    pool_address = trace.to_address
    recipient_address = (
        trace.inputs["to"]
        if trace.inputs is not None and "to" in trace.inputs
        else trace.from_address
    )

    prior_transfers = [
        _as_transfer(prior_trace)
        for prior_trace in prior_traces
        if prior_trace.classification == Classification.transfer
    ]

    child_transfers = [
        _as_transfer(child)
        for child in child_traces
        if child.classification == Classification.transfer
    ]

    transfers_to_pool = [
        transfer for transfer in prior_transfers if transfer.to_address == pool_address
    ]

    transfers_from_pool_to_recipient = [
        transfer
        for transfer in child_transfers
        if (
            transfer.to_address == recipient_address
            and transfer.from_address == pool_address
        )
    ]

    # expecting a prior transfer to the pool
    if len(transfers_to_pool) == 0:
        return None

    # expecting exactly one transfer inside the pool
    if len(transfers_from_pool_to_recipient) != 1:
        return None

    transfer_in = transfers_to_pool[-1]
    transfer_out = transfers_from_pool_to_recipient[0]

    return Swap(
        abi_name="UniswapV2Pair",
        transaction_hash=trace.transaction_hash,
        pool_address=pool_address,
        from_address=transfer_in.from_address,
        to_address=transfer_out.to_address,
        token_in_address=transfer_in.token_address,
        token_in_amount=transfer_in.amount,
        token_out_address=transfer_out.token_address,
        token_out_amount=transfer_out.amount,
    )


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
    return (len(maybe_child_trace_address) > parent_trace_length) and (
        maybe_child_trace_address[:parent_trace_length] == parent_trace_address
    )


def _remove_inner_transfers(transfers: List[Transfer]) -> List[Transfer]:
    updated_transfers = []
    transfer_trace_addresses: List[List[int]] = []

    sorted_transfers = sorted(transfers, key=lambda t: t.trace_address)

    for transfer in sorted_transfers:
        if not any(
            _is_subtrace(parent_address, transfer.trace_address)
            for parent_address in transfer_trace_addresses
        ):
            updated_transfers.append(transfer)

        transfer_trace_addresses.append(transfer.trace_address)

    return updated_transfers


def _is_subtrace(parent_trace_address, child_trace_address) -> bool:
    return (
        len(child_trace_address) > len(parent_trace_address)
        and child_trace_address[: len(parent_trace_address)] == parent_trace_address
    )


def _as_transfer(trace: ClassifiedTrace) -> Transfer:
    # todo - this should be enforced at the data level
    if trace.inputs is None:
        raise ValueError("Invalid transfer")

    if trace.protocol == Protocol.weth:
        return Transfer(
            transaction_hash=trace.transaction_hash,
            trace_address=trace.trace_address,
            amount=trace.inputs["wad"],
            to_address=trace.inputs["dst"],
            from_address=trace.from_address,
            token_address=trace.to_address,
        )
    else:
        return Transfer(
            transaction_hash=trace.transaction_hash,
            trace_address=trace.trace_address,
            amount=trace.inputs["amount"],
            to_address=trace.inputs["recipient"],
            from_address=trace.inputs.get("sender", trace.from_address),
            token_address=trace.to_address,
        )
