from typing import List

from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.sandwiches import get_sandwiches
from mev_inspect.schemas.sandwiches import Sandwich
from mev_inspect.schemas.swaps import Swap
from mev_inspect.swaps import get_swaps
from tests.utils import load_test_block


def test_back_heavy_sandwich_profits(trace_classifier: TraceClassifier):
    block_number = 13699765
    expected_sandwicher = "0x51399b32cd0186bb32230e24167489f3b2f47870"
    expected_token_address = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    expected_profit_amount = -435805264121298944

    block = load_test_block(block_number)
    classified_traces = trace_classifier.classify(block.traces)
    swaps: List[Swap] = get_swaps(classified_traces)
    result: List[Sandwich] = get_sandwiches(swaps)

    for observed_sandwich in result:
        if observed_sandwich.sandwicher_address == expected_sandwicher:
            assert expected_token_address == observed_sandwich.profit_token_address
            assert expected_profit_amount == observed_sandwich.profit_amount


def test_front_heavy_sandwich_profits(trace_classifier: TraceClassifier):
    block_number = 14659109
    expected_sandwicher = "0x01ff6318440f7d5553a82294d78262d5f5084eff"
    expected_token_address = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    expected_profit_amount = -180511102573164864

    block = load_test_block(block_number)
    classified_traces = trace_classifier.classify(block.traces)
    swaps: List[Swap] = get_swaps(classified_traces)
    result: List[Sandwich] = get_sandwiches(swaps)

    for observed_sandwich in result:
        if observed_sandwich.sandwicher_address == expected_sandwicher:
            assert expected_token_address == observed_sandwich.profit_token_address
            assert expected_profit_amount == observed_sandwich.profit_amount
