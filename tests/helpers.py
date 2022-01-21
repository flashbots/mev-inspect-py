from typing import List

from mev_inspect.schemas.traces import (
    Classification,
    ClassifiedTrace,
    DecodedCallTrace,
    Protocol,
    TraceType,
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
    return DecodedCallTrace(
        transaction_hash=transaction_hash,
        transaction_position=0,
        block_number=block_number,
        type=TraceType.call,
        trace_address=trace_address,
        classification=Classification.transfer,
        from_address=from_address,
        to_address=token_address,
        abi_name="ERC20",
        function_name="transfer",
        function_signature="transfer(address,uint256)",
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
    contract_address: str,
    abi_name: str,
    function_signature: str,
    protocol: Protocol,
    recipient_address: str,
    recipient_input_key: str,
):
    return DecodedCallTrace(
        transaction_hash=transaction_hash,
        transaction_position=0,
        block_number=block_number,
        type=TraceType.call,
        trace_address=trace_address,
        action={},
        subtraces=0,
        classification=Classification.swap,
        from_address=from_address,
        to_address=contract_address,
        function_name="swap",
        function_signature=function_signature,
        inputs={recipient_input_key: recipient_address},
        abi_name=abi_name,
        protocol=protocol,
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
        transaction_position=0,
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
