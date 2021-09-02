from mev_inspect.arbitrages import get_arbitrages
from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.swaps import get_swaps

from .utils import load_test_block


def test_arbitrage_real_block():
    block = load_test_block(12914944)

    trace_clasifier = TraceClassifier()
    classified_traces = trace_clasifier.classify(block.traces)

    swaps = get_swaps(classified_traces)
    assert len(swaps) == 51

    arbitrages = get_arbitrages(list(swaps))
    assert len(arbitrages) == 1

    arbitrage = arbitrages[0]

    assert len(arbitrage.swaps) == 3
    assert (
        arbitrage.profit_token_address == "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    )
    assert arbitrage.profit_amount == 53560707941943273628
