from typing import List

from mev_inspect.arbitrages import get_arbitrages, _get_all_routes
from mev_inspect.schemas.swaps import Swap
from mev_inspect.classifiers.specs.uniswap import (
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
        third_token_address,
    ] = get_addresses(7)

    first_token_in_amount = 10
    first_token_out_amount = 11
    second_token_amount = 15
    transaction_position = 0

    arb_swaps = [
        Swap(
            abi_name=UNISWAP_V2_PAIR_ABI_NAME,
            transaction_hash=transaction_hash,
            transaction_position=transaction_position,
            block_number=block_number,
            trace_address=[0],
            contract_address=first_pool_address,
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
            transaction_position=transaction_position,
            block_number=block_number,
            trace_address=[1],
            contract_address=second_pool_address,
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
        transaction_position=transaction_position,
        block_number=block_number,
        trace_address=[2, 0],
        contract_address=unrelated_pool_address,
        from_address=account_address,
        to_address=account_address,
        token_in_address=second_token_address,
        token_in_amount=first_token_in_amount,
        token_out_address=third_token_address,
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
    first_token_out_amount = 11
    second_token_amount = 15
    third_token_amount = 40
    transaction_position = 0

    swaps = [
        Swap(
            abi_name=UNISWAP_V2_PAIR_ABI_NAME,
            transaction_hash=transaction_hash,
            transaction_position=transaction_position,
            block_number=block_number,
            trace_address=[0],
            contract_address=first_pool_address,
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
            transaction_position=transaction_position,
            block_number=block_number,
            trace_address=[1],
            contract_address=second_pool_address,
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
            transaction_position=transaction_position,
            block_number=block_number,
            trace_address=[2],
            contract_address=third_pool_address,
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


def test_get_all_routes():
    # A -> B, B -> A
    start_swap = create_generic_swap("0xa", "0xb")
    end_swap = create_generic_swap("0xb", "0xa")
    routes = _get_all_routes(start_swap, end_swap, [])
    assert len(routes) == 1

    # A->B, B->C, C->A
    start_swap = create_generic_swap("0xa", "0xb")
    other_swaps = [create_generic_swap("0xb", "0xc")]
    end_swap = create_generic_swap("0xc", "0xa")
    routes = _get_all_routes(start_swap, end_swap, other_swaps)
    assert len(routes) == 1

    # A->B, B->C, C->A + A->D
    other_swaps.append(create_generic_swap("0xa", "0xd"))
    routes = _get_all_routes(start_swap, end_swap, other_swaps)
    assert len(routes) == 1

    # A->B, B->C, C->A + A->D B->E
    other_swaps.append(create_generic_swap("0xb", "0xe"))
    routes = _get_all_routes(start_swap, end_swap, other_swaps)
    assert len(routes) == 1

    # A->B, B->A, B->C, C->A
    other_swaps = [create_generic_swap("0xb", "0xa"), create_generic_swap("0xb", "0xc")]
    routes = _get_all_routes(start_swap, end_swap, other_swaps)
    assert len(routes) == 1
    expect_simple_route = [["0xa", "0xb"], ["0xb", "0xc"], ["0xc", "0xa"]]
    assert len(routes[0]) == len(expect_simple_route)
    for i in range(len(expect_simple_route)):
        assert expect_simple_route[i][0] == routes[0][i].token_in_address
        assert expect_simple_route[i][1] == routes[0][i].token_out_address

    # A->B, B->C, C->D, D->A, B->D
    end_swap = create_generic_swap("0xd", "0xa")
    other_swaps = [
        create_generic_swap("0xb", "0xc"),
        create_generic_swap("0xc", "0xd"),
        create_generic_swap("0xb", "0xd"),
    ]
    routes = _get_all_routes(start_swap, end_swap, other_swaps)
    assert len(routes) == 2


def create_generic_swap(
    tok_a: str = "0xa",
    tok_b: str = "0xb",
    amount_a_in: int = 1,
    amount_b_out: int = 1,
    trace_address: List[int] = [],
):
    return Swap(
        abi_name=UNISWAP_V3_POOL_ABI_NAME,
        transaction_hash="0xfake",
        transaction_position=0,
        block_number=0,
        trace_address=trace_address,
        contract_address="0xfake",
        from_address="0xfake",
        to_address="0xfake",
        token_in_address=tok_a,
        token_in_amount=amount_a_in,
        token_out_address=tok_b,
        token_out_amount=amount_b_out,
    )
