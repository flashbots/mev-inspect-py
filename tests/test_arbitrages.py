import itertools
from typing import List

from mev_inspect.arbitrages import get_arbitrages, _order_swaps_by_trace_order
from mev_inspect.schemas.swaps import Swap
from mev_inspect.swaps import (
    UNISWAP_V2_PAIR_ABI_NAME,
    UNISWAP_V3_POOL_ABI_NAME,
)


def test_two_pool_arbitrage(get_transaction_hashes, get_addresses):
    block_number = 123
    [transaction_hash] = get_transaction_hashes(1)

    [
        account_address,
        first_pool_address,
        second_pool_address,
        unrelated_pool_address,
        first_token_address,
        second_token_address,
    ] = get_addresses(6)

    first_token_in_amount = 10
    first_token_out_amount = 10
    second_token_amount = 15

    arb_swaps = [
        Swap(
            abi_name=UNISWAP_V2_PAIR_ABI_NAME,
            transaction_hash=transaction_hash,
            block_number=block_number,
            trace_address=[0],
            pool_address=first_pool_address,
            from_address=account_address,
            to_address=second_pool_address,
            token_in_address=first_token_address,
            token_in_amount=first_token_in_amount,
            token_out_address=second_token_address,
            token_out_amount=second_token_amount,
        ),
        Swap(
            abi_name=UNISWAP_V3_POOL_ABI_NAME,
            transaction_hash=transaction_hash,
            block_number=block_number,
            trace_address=[1],
            pool_address=second_pool_address,
            from_address=first_pool_address,
            to_address=account_address,
            token_in_address=second_token_address,
            token_in_amount=second_token_amount,
            token_out_address=first_token_address,
            token_out_amount=first_token_out_amount,
        ),
    ]

    unrelated_swap = Swap(
        abi_name=UNISWAP_V3_POOL_ABI_NAME,
        transaction_hash=transaction_hash,
        block_number=block_number,
        trace_address=[2, 0],
        pool_address=unrelated_pool_address,
        from_address=account_address,
        to_address=account_address,
        token_in_address=second_token_address,
        token_in_amount=first_token_in_amount,
        token_out_address=first_token_address,
        token_out_amount=first_token_out_amount,
    )

    swaps = [
        unrelated_swap,
        *arb_swaps,
    ]

    arbitrages = get_arbitrages(swaps)

    assert len(arbitrages) == 1

    arbitrage = arbitrages[0]

    assert arbitrage.swaps == arb_swaps
    assert arbitrage.account_address == account_address
    assert arbitrage.profit_token_address == first_token_address
    assert arbitrage.start_amount == first_token_in_amount
    assert arbitrage.end_amount == first_token_out_amount
    assert arbitrage.profit_amount == first_token_out_amount - first_token_in_amount


def test_three_pool_arbitrage(get_transaction_hashes, get_addresses):
    block_number = 123
    [transaction_hash] = get_transaction_hashes(1)

    [
        account_address,
        first_pool_address,
        second_pool_address,
        third_pool_address,
        first_token_address,
        second_token_address,
        third_token_address,
    ] = get_addresses(7)

    first_token_in_amount = 10
    first_token_out_amount = 10
    second_token_amount = 15
    third_token_amount = 40

    swaps = [
        Swap(
            abi_name=UNISWAP_V2_PAIR_ABI_NAME,
            transaction_hash=transaction_hash,
            block_number=block_number,
            trace_address=[0],
            pool_address=first_pool_address,
            from_address=account_address,
            to_address=second_pool_address,
            token_in_address=first_token_address,
            token_in_amount=first_token_in_amount,
            token_out_address=second_token_address,
            token_out_amount=second_token_amount,
        ),
        Swap(
            abi_name=UNISWAP_V3_POOL_ABI_NAME,
            transaction_hash=transaction_hash,
            block_number=block_number,
            trace_address=[1],
            pool_address=second_pool_address,
            from_address=first_pool_address,
            to_address=third_pool_address,
            token_in_address=second_token_address,
            token_in_amount=second_token_amount,
            token_out_address=third_token_address,
            token_out_amount=third_token_amount,
        ),
        Swap(
            abi_name=UNISWAP_V3_POOL_ABI_NAME,
            transaction_hash=transaction_hash,
            block_number=block_number,
            trace_address=[2],
            pool_address=third_pool_address,
            from_address=second_pool_address,
            to_address=account_address,
            token_in_address=third_token_address,
            token_in_amount=third_token_amount,
            token_out_address=first_token_address,
            token_out_amount=first_token_out_amount,
        ),
    ]

    arbitrages = get_arbitrages(swaps)

    assert len(arbitrages) == 1

    arbitrage = arbitrages[0]

    assert arbitrage.swaps == swaps
    assert arbitrage.account_address == account_address
    assert arbitrage.profit_token_address == first_token_address
    assert arbitrage.start_amount == first_token_in_amount
    assert arbitrage.end_amount == first_token_out_amount
    assert arbitrage.profit_amount == first_token_out_amount - first_token_in_amount


def test_order_swaps_by_trace_order():
    trace_address_0 = []
    trace_address_1 = [0]
    trace_address_2 = [1]
    trace_address_3 = [1, 1]
    trace_address_4 = [2, 1, 3]
    trace_address_5 = [2, 2]

    permutated_trace_addresses: List[List[int]] = itertools.permutations(
        [
            trace_address_0,
            trace_address_1,
            trace_address_2,
            trace_address_3,
            trace_address_4,
            trace_address_5,
        ]
    )

    for trace_addresses in permutated_trace_addresses:
        print("permute")
        swaps: List[Swap] = []
        for trace_address in trace_addresses:
            swap = Swap(
                abi_name=UNISWAP_V3_POOL_ABI_NAME,
                transaction_hash="0xfake",
                block_number=0,
                trace_address=trace_address,
                pool_address="0xfake",
                from_address="0xfake",
                to_address="0xfake",
                token_in_address="0xfake",
                token_in_amount=1,
                token_out_address="0xfake",
                token_out_amount=1,
            )
            swaps.append(swap)
        ordered_swaps = _order_swaps_by_trace_order(swaps)

        assert ordered_swaps[0].trace_address == trace_address_0
        assert ordered_swaps[1].trace_address == trace_address_1
        assert ordered_swaps[2].trace_address == trace_address_2
        assert ordered_swaps[3].trace_address == trace_address_3
        assert ordered_swaps[4].trace_address == trace_address_4
        assert ordered_swaps[5].trace_address == trace_address_5
