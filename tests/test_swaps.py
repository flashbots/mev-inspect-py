from mev_inspect.swaps import (
    get_swaps,
    UNISWAP_V2_PAIR_ABI_NAME,
    UNISWAP_V3_POOL_ABI_NAME,
    BALANCER_V1_POOL_ABI_NAME,
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
        third_transaction_hash,
    ] = get_transaction_hashes(3)

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
        third_token_in_address,
        third_token_out_address,
        third_pool_address,
    ] = get_addresses(12)

    first_token_in_amount = 10
    first_token_out_amount = 20
    second_token_in_amount = 30
    second_token_out_amount = 40
    third_token_in_amount = 50
    third_token_out_amount = 60

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
        make_transfer_trace(
            block_number,
            third_transaction_hash,
            trace_address=[6, 0],
            from_address=bob_address,
            to_address=third_pool_address,
            token_address=third_token_in_address,
            amount=third_token_in_amount,
        ),
        make_transfer_trace(
            block_number,
            third_transaction_hash,
            trace_address=[6, 1],
            from_address=third_pool_address,
            to_address=bob_address,
            token_address=third_token_out_address,
            amount=third_token_out_amount,
        ),
        make_swap_trace(
            block_number,
            third_transaction_hash,
            trace_address=[6],
            from_address=bob_address,
            pool_address=third_pool_address,
            abi_name=BALANCER_V1_POOL_ABI_NAME,
            recipient_address=bob_address,
            recipient_input_key="recipient",
        ),
    ]

    swaps = get_swaps(traces)

    assert len(swaps) == 3

    for swap in swaps:
        if swap.abi_name == UNISWAP_V2_PAIR_ABI_NAME:
            uni_v2_swap = swap
        elif swap.abi_name == UNISWAP_V3_POOL_ABI_NAME:
            uni_v3_swap = swap
        elif swap.abi_name == BALANCER_V1_POOL_ABI_NAME:
            bal_v1_swap = swap
        else:
            assert False

    assert uni_v2_swap.abi_name == UNISWAP_V2_PAIR_ABI_NAME
    assert uni_v2_swap.transaction_hash == first_transaction_hash
    assert uni_v2_swap.block_number == block_number
    assert uni_v2_swap.trace_address == [1]
    assert uni_v2_swap.protocol is None
    assert uni_v2_swap.pool_address == first_pool_address
    assert uni_v2_swap.from_address == alice_address
    assert uni_v2_swap.to_address == bob_address
    assert uni_v2_swap.token_in_address == first_token_in_address
    assert uni_v2_swap.token_in_amount == first_token_in_amount
    assert uni_v2_swap.token_out_address == first_token_out_address
    assert uni_v2_swap.token_out_amount == first_token_out_amount

    assert uni_v3_swap.abi_name == UNISWAP_V3_POOL_ABI_NAME
    assert uni_v3_swap.transaction_hash == second_transaction_hash
    assert uni_v3_swap.block_number == block_number
    assert uni_v3_swap.trace_address == []
    assert uni_v3_swap.protocol is None
    assert uni_v3_swap.pool_address == second_pool_address
    assert uni_v3_swap.from_address == bob_address
    assert uni_v3_swap.to_address == carl_address
    assert uni_v3_swap.token_in_address == second_token_in_address
    assert uni_v3_swap.token_in_amount == second_token_in_amount
    assert uni_v3_swap.token_out_address == second_token_out_address
    assert uni_v3_swap.token_out_amount == second_token_out_amount

    assert bal_v1_swap.abi_name == BALANCER_V1_POOL_ABI_NAME
    assert bal_v1_swap.transaction_hash == third_transaction_hash
    assert bal_v1_swap.block_number == block_number
    assert bal_v1_swap.trace_address == [6]
    assert bal_v1_swap.protocol is None
    assert bal_v1_swap.pool_address == third_pool_address
    assert bal_v1_swap.from_address == bob_address
    assert bal_v1_swap.to_address == bob_address
    assert bal_v1_swap.token_in_address == third_token_in_address
    assert bal_v1_swap.token_in_amount == third_token_in_amount
    assert bal_v1_swap.token_out_address == third_token_out_address
    assert bal_v1_swap.token_out_amount == third_token_out_amount
