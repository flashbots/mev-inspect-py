from mev_inspect.swaps import (
    get_swaps,
    UNISWAP_V2_PAIR_ABI_NAME,
    UNISWAP_V3_POOL_ABI_NAME,
)

from .helpers import (
    make_unknown_trace,
    make_transfer_trace,
    make_swap_trace,
)


def test_swaps(
    get_transaction_hashes,
    get_addresses,
):
    block_number = 123

    [
        first_transaction_hash,
        second_transaction_hash,
    ] = get_transaction_hashes(2)

    [
        alice_address,
        bob_address,
        carl_address,
        first_token_in_address,
        first_token_out_address,
        first_pool_address,
        second_token_in_address,
        second_token_out_address,
        second_pool_address,
    ] = get_addresses(9)

    first_token_in_amount = 10
    first_token_out_amount = 20
    second_token_in_amount = 30
    second_token_out_amount = 40

    traces = [
        make_unknown_trace(block_number, first_transaction_hash, []),
        make_transfer_trace(
            block_number,
            first_transaction_hash,
            trace_address=[0],
            from_address=alice_address,
            to_address=first_pool_address,
            token_address=first_token_in_address,
            amount=first_token_in_amount,
        ),
        make_swap_trace(
            block_number,
            first_transaction_hash,
            trace_address=[1],
            from_address=alice_address,
            pool_address=first_pool_address,
            abi_name=UNISWAP_V2_PAIR_ABI_NAME,
            recipient_address=bob_address,
            recipient_input_key="to",
        ),
        make_transfer_trace(
            block_number,
            first_transaction_hash,
            trace_address=[1, 0],
            from_address=first_pool_address,
            to_address=bob_address,
            token_address=first_token_out_address,
            amount=first_token_out_amount,
        ),
        make_swap_trace(
            block_number,
            second_transaction_hash,
            trace_address=[],
            from_address=bob_address,
            pool_address=second_pool_address,
            abi_name=UNISWAP_V3_POOL_ABI_NAME,
            recipient_address=carl_address,
            recipient_input_key="recipient",
        ),
        make_transfer_trace(
            block_number,
            second_transaction_hash,
            trace_address=[0],
            from_address=second_pool_address,
            to_address=carl_address,
            token_address=second_token_out_address,
            amount=second_token_out_amount,
        ),
        make_transfer_trace(
            block_number,
            second_transaction_hash,
            trace_address=[1],
            from_address=bob_address,
            to_address=second_pool_address,
            token_address=second_token_in_address,
            amount=second_token_in_amount,
        ),
    ]

    swaps = get_swaps(traces)

    assert len(swaps) == 2

    if swaps[0].abi_name == UNISWAP_V2_PAIR_ABI_NAME:
        [first_swap, second_swap] = swaps  # pylint: disable=unbalanced-tuple-unpacking
    else:
        [second_swap, first_swap] = swaps  # pylint: disable=unbalanced-tuple-unpacking

    assert first_swap.abi_name == UNISWAP_V2_PAIR_ABI_NAME
    assert first_swap.transaction_hash == first_transaction_hash
    assert first_swap.block_number == block_number
    assert first_swap.trace_address == [1]
    assert first_swap.protocol is None
    assert first_swap.pool_address == first_pool_address
    assert first_swap.from_address == alice_address
    assert first_swap.to_address == bob_address
    assert first_swap.token_in_address == first_token_in_address
    assert first_swap.token_in_amount == first_token_in_amount
    assert first_swap.token_out_address == first_token_out_address
    assert first_swap.token_out_amount == first_token_out_amount

    assert second_swap.abi_name == UNISWAP_V3_POOL_ABI_NAME
    assert second_swap.transaction_hash == second_transaction_hash
    assert second_swap.block_number == block_number
    assert second_swap.trace_address == []
    assert second_swap.protocol is None
    assert second_swap.pool_address == second_pool_address
    assert second_swap.from_address == bob_address
    assert second_swap.to_address == carl_address
    assert second_swap.token_in_address == second_token_in_address
    assert second_swap.token_in_amount == second_token_in_amount
    assert second_swap.token_out_address == second_token_out_address
    assert second_swap.token_out_amount == second_token_out_amount
