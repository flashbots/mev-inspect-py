from mev_inspect.schemas.traces import Classification, DecodedCallTrace, TraceType
from mev_inspect.schemas.transfers import Transfer
from mev_inspect.transfers import get_net_transfers, remove_child_transfers_of_transfers


def test_remove_child_transfers_of_transfers(get_transaction_hashes, get_addresses):
    [transaction_hash, other_transaction_hash] = get_transaction_hashes(2)

    [
        alice_address,
        bob_address,
        first_token_address,
        second_token_address,
        third_token_address,
    ] = get_addresses(5)

    outer_transfer = Transfer(
        block_number=123,
        transaction_hash=transaction_hash,
        trace_address=[0],
        from_address=alice_address,
        to_address=bob_address,
        amount=10,
        token_address=first_token_address,
    )

    inner_transfer = Transfer(
        **{
            **outer_transfer.dict(),
            **dict(
                trace_address=[0, 0],
                token_address=second_token_address,
            ),
        }
    )

    other_transfer = Transfer(
        block_number=123,
        transaction_hash=transaction_hash,
        trace_address=[1],
        from_address=bob_address,
        to_address=alice_address,
        amount=10,
        token_address=third_token_address,
    )

    separate_transaction_transfer = Transfer(
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


def test_net_transfers_same_token(get_addresses):

    alice_address, bob_address, token_address = get_addresses(3)
    transfer_alice_to_bob = DecodedCallTrace(
        block_number=123,
        transaction_hash="net_transfer_tx_hash",
        block_hash="block_hash",
        transaction_position=123,
        type=TraceType.call,
        action={},
        functionName="transfer",
        abiName="UniswapV3Pool",
        subtraces=123,
        trace_address=[0],
        classification=Classification.transfer,
        function_signature="transfer(address,uint256)",
        from_address=alice_address,
        to_address=token_address,
        inputs={"recipient": bob_address, "amount": 700},
    )
    transfer_bob_to_alice = DecodedCallTrace(
        block_number=123,
        transaction_hash="net_transfer_tx_hash",
        block_hash="block_hash",
        transaction_position=123,
        type=TraceType.call,
        action={},
        functionName="transfer",
        abiName="UniswapV3Pool",
        subtraces=123,
        trace_address=[3],
        classification=Classification.transfer,
        function_signature="transfer(address,uint256)",
        from_address=bob_address,
        to_address=token_address,
        inputs={"recipient": alice_address, "amount": 200},
    )

    expected_transfer = Transfer(
        block_number=123,
        transaction_hash="net_transfer_tx_hash",
        trace_address=[-1],
        from_address=alice_address,
        to_address=bob_address,
        amount=500,
        token_address=token_address,
    )

    net_transfer = get_net_transfers([transfer_alice_to_bob, transfer_bob_to_alice])

    assert expected_transfer == net_transfer[0]


def _equal_ignoring_order(first_list, second_list) -> bool:
    return all(first in second_list for first in first_list) and all(
        second in first_list for second in second_list
    )
