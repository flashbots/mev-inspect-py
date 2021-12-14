from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.sandwiches import get_sandwiches
from mev_inspect.swaps import get_swaps

from .utils import load_test_block, load_test_sandwiches


def test_arbitrage_real_block():
    block = load_test_block(12775690)
    expected_sandwiches = load_test_sandwiches(12775690)

    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)

    swaps = get_swaps(classified_traces)
    assert len(swaps) == 21

    sandwiches = get_sandwiches(list(swaps))
    assert sandwiches == expected_sandwiches
