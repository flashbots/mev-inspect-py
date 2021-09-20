from mev_inspect.schemas.transfers import ERC20Transfer
from mev_inspect.transfers import remove_child_transfers_of_transfers


def test_remove_child_transfers_of_transfers(get_transaction_hashes, get_addresses):
    [transaction_hash, other_transaction_hash] = get_transaction_hashes(2)

    [
        alice_address,
        bob_address,
        first_token_address,
        second_token_address,
        third_token_address,
    ] = get_addresses(5)

    outer_transfer = ERC20Transfer(
        block_number=123,
        transaction_hash=transaction_hash,
        trace_address=[0],
        from_address=alice_address,
        to_address=bob_address,
        amount=10,
        token_address=first_token_address,
    )

    inner_transfer = ERC20Transfer(
        **{
            **outer_transfer.dict(),
            **dict(
                trace_address=[0, 0],
                token_address=second_token_address,
            ),
        }
    )

    other_transfer = ERC20Transfer(
        block_number=123,
        transaction_hash=transaction_hash,
        trace_address=[1],
        from_address=bob_address,
        to_address=alice_address,
        amount=10,
        token_address=third_token_address,
    )

    separate_transaction_transfer = ERC20Transfer(
        **{
            **inner_transfer.dict(),
            **dict(transaction_hash=other_transaction_hash),
        }
    )

    transfers = [
        outer_transfer,
        inner_transfer,
        other_transfer,
        separate_transaction_transfer,
    ]

    expected_transfers = [
        outer_transfer,
        other_transfer,
        separate_transaction_transfer,
    ]

    removed_transfers = remove_child_transfers_of_transfers(transfers)
    assert _equal_ignoring_order(removed_transfers, expected_transfers)


def _equal_ignoring_order(first_list, second_list) -> bool:
    return all(first in second_list for first in first_list) and all(
        second in first_list for second in second_list
    )
