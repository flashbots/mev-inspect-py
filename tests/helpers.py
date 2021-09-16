from typing import List

from mev_inspect.schemas.blocks import TraceType
from mev_inspect.schemas.classified_traces import (
    Classification,
    ClassifiedTrace,
    CallTrace,
    DecodedCallTrace,
)


def make_transfer_trace(
    block_number: int,
    transaction_hash: str,
    trace_address: List[int],
    from_address: str,
    to_address: str,
    token_address: str,
    amount: int,
):
    return CallTrace(
        transaction_hash=transaction_hash,
        block_number=block_number,
        type=TraceType.call,
        trace_address=trace_address,
        classification=Classification.transfer,
        from_address=from_address,
        to_address=token_address,
        inputs={
            "recipient": to_address,
            "amount": amount,
        },
        block_hash=str(block_number),
        action={},
        subtraces=0.0,
    )


def make_swap_trace(
    block_number: int,
    transaction_hash: str,
    trace_address: List[int],
    from_address: str,
    pool_address: str,
    abi_name: str,
    recipient_address: str,
    recipient_input_key: str,
):
    return DecodedCallTrace(
        transaction_hash=transaction_hash,
        block_number=block_number,
        type=TraceType.call,
        trace_address=trace_address,
        action={},
        subtraces=0,
        classification=Classification.swap,
        from_address=from_address,
        to_address=pool_address,
        inputs={recipient_input_key: recipient_address},
        abi_name=abi_name,
        block_hash=str(block_number),
    )


def make_unknown_trace(
    block_number: int,
    transaction_hash: str,
    trace_address: List[int],
):
    return ClassifiedTrace(
        block_number=block_number,
        transaction_hash=transaction_hash,
        trace_address=trace_address,
        action={},
        subtraces=0,
        block_hash=str(block_number),
        type=TraceType.call,
        classification=Classification.unknown,
    )


def make_many_unknown_traces(
    block_number: int,
    transaction_hash: str,
    trace_addresses: List[List[int]],
) -> List[ClassifiedTrace]:

    return [
        make_unknown_trace(
            block_number,
            transaction_hash,
            trace_address,
        )
        for trace_address in trace_addresses
    ]
