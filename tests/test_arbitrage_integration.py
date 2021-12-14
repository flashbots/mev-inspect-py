from mev_inspect.arbitrages import get_arbitrages
from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.swaps import get_swaps

from .utils import load_test_block


def test_arbitrage_real_block(trace_classifier: TraceClassifier):
    block = load_test_block(12914944)
    classified_traces = trace_classifier.classify(block.traces)

    swaps = get_swaps(classified_traces)
    assert len(swaps) == 51

    arbitrages = get_arbitrages(list(swaps))
    assert len(arbitrages) == 2

    arbitrage_1 = [
        arb
        for arb in arbitrages
        if arb.transaction_hash
        == "0x448245bf1a507b73516c4eeee01611927dada6610bf26d403012f2e66800d8f0"
    ][0]
    arbitrage_2 = [
        arb
        for arb in arbitrages
        if arb.transaction_hash
        == "0xfcf4558f6432689ea57737fe63124a5ec39fd6ba6aaf198df13a825dd599bffc"
    ][0]

    assert len(arbitrage_1.swaps) == 3
    assert (
        arbitrage_1.profit_token_address == "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    )
    assert len(arbitrage_1.swaps) == 3
    assert (
        arbitrage_1.swaps[1].token_in_address
        == "0x25f8087ead173b73d6e8b84329989a8eea16cf73"
    )
    assert (
        arbitrage_1.swaps[1].token_out_address
        == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    )
    assert arbitrage_1.profit_amount == 750005273675102326

    assert len(arbitrage_2.swaps) == 3
    assert (
        arbitrage_2.profit_token_address == "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    )
    assert len(arbitrage_2.swaps) == 3
    assert (
        arbitrage_2.swaps[1].token_in_address
        == "0x25f8087ead173b73d6e8b84329989a8eea16cf73"
    )
    assert (
        arbitrage_2.swaps[1].token_out_address
        == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    )
    assert arbitrage_2.profit_amount == 53560707941943273628
