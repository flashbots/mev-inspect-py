from typing import List, Optional

from mev_inspect.schemas.swaps import Swap
from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.swaps import get_swaps
from tests.utils import load_test_block


def test_0x_swap() -> None:

    abi_name = "UniswapV2Pair"
    transaction_hash = (
        "0x0da110d2bf500a818d973fb7dab7db5905bfe4e027375b2b72ee3d464a391732"
    )
    block_number = 13302365
    pool_address = "0x99b42f2b49c395d2a77d973f6009abb5d67da343"
    from_address = "0x0000005c9426e6910f22f0c00ed3690a4884dd6e"
    to_address = "0x0000006daea1723962647b7e189d311d757fb793"
    token_in_address = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    token_in_amount = 16303300000000000000
    token_out_address = "0x25f8087ead173b73d6e8b84329989a8eea16cf73"
    token_out_amount = 8747897101475046749094
    trace_address = {0, 3}

    expected_swap = Swap(
        abi_name=abi_name,
        transaction_hash=transaction_hash,
        block_number=block_number,
        trace_address=trace_address,
        pool_address=pool_address,
        from_address=from_address,
        to_address=to_address,
        token_in_address=token_in_address,
        token_in_amount=token_in_amount,
        token_out_address=token_out_address,
        token_out_amount=token_out_amount,
        error=None,
        protocol=None,
    )

    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    swaps_in_test_block = get_swaps(classified_traces)
    observed_swap = _find_swap_by_tx_hash(swaps_in_test_block, transaction_hash)

    assert expected_swap == observed_swap


def _find_swap_by_tx_hash(swaps: List[Swap], transaction_hash: str) -> Optional[Swap]:

    expected_swap: Optional[Swap]

    for swap in swaps:

        if swap.transaction_hash == transaction_hash:
            expected_swap = swap
            break

        else:
            expected_swap = None

    return expected_swap
