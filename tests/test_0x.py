from mev_inspect.schemas.swaps import Swap
from mev_inspect.swaps import get_swaps
from mev_inspect.schemas.traces import Protocol
from mev_inspect.classifiers.trace import TraceClassifier
from tests.utils import load_test_block


def test_fillLimitOrder_swap():

    transaction_hash = (
        "0xa043976d736ec8dc930c0556dffd0a86a4bfc80bf98fb7995c791fb4dc488b5d"
    )
    block_number = 13666312

    swap = Swap(
        abi_name="INativeOrdersFeature",
        transaction_hash=transaction_hash,
        block_number=block_number,
        trace_address=[0, 2, 0, 1],
        contract_address="0xdef1c0ded9bec7f1a1670819833240f027b25eff",
        from_address="0x00000000000e1d0dabf7b7c7b68866fc940d0db8",
        to_address="0xdef1c0ded9bec7f1a1670819833240f027b25eff",
        token_in_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        token_in_amount=35000000000000000000,
        token_out_address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        token_out_amount=143949683150,
        protocol=Protocol.zero_ex,
        error=None,
    )

    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_swaps(classified_traces)

    assert result.count(swap) == 1


def test__fillLimitOrder_swap():

    transaction_hash = (
        "0x9255addffa2dbeb9560c5e20e78a78c949488d2054c70b2155c39f9e28394cbf"
    )
    block_number = 13666184

    swap = Swap(
        abi_name="INativeOrdersFeature",
        transaction_hash=transaction_hash,
        block_number=block_number,
        trace_address=[0, 1],
        contract_address="0xdef1c0ded9bec7f1a1670819833240f027b25eff",
        from_address="0xdef1c0ded9bec7f1a1670819833240f027b25eff",
        to_address="0xdef1c0ded9bec7f1a1670819833240f027b25eff",
        token_in_address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        token_in_amount=30000000,
        token_out_address="0x9ff79c75ae2bcbe0ec63c0375a3ec90ff75bbe0f",
        token_out_amount=100000001,
        protocol=Protocol.zero_ex,
        error=None,
    )

    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_swaps(classified_traces)

    assert result.count(swap) == 1


def test_RfqLimitOrder_swap():

    transaction_hash = (
        "0x1c948eb7c59ddbe6b916cf68f5df86eb44a7c9e728221fcd8ab750f137fd2a0f"
    )
    block_number = 13666326

    swap = Swap(
        abi_name="INativeOrdersFeature",
        transaction_hash=transaction_hash,
        block_number=block_number,
        trace_address=[0, 1, 13, 0, 1],
        contract_address="0xdef1c0ded9bec7f1a1670819833240f027b25eff",
        from_address="0xdef171fe48cf0115b1d80b88dc8eab59176fee57",
        to_address="0xdef1c0ded9bec7f1a1670819833240f027b25eff",
        token_in_address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
        token_in_amount=288948250430,
        token_out_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        token_out_amount=70500000000000000000,
        protocol=Protocol.zero_ex,
        error=None,
    )

    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_swaps(classified_traces)

    assert result.count(swap) == 1


def test__RfqLimitOrder_swap():

    transaction_hash = (
        "0x4f66832e654f8a4d773d9769571155df3722401343247376d6bb56626db29b90"
    )
    block_number = 13666363

    swap = Swap(
        abi_name="INativeOrdersFeature",
        transaction_hash=transaction_hash,
        block_number=block_number,
        trace_address=[1, 0, 1, 0, 1],
        contract_address="0xdef1c0ded9bec7f1a1670819833240f027b25eff",
        from_address="0xdef1c0ded9bec7f1a1670819833240f027b25eff",
        to_address="0xdef1c0ded9bec7f1a1670819833240f027b25eff",
        token_in_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        token_in_amount=979486121594935552,
        token_out_address="0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce",
        token_out_amount=92404351093861841165644172,
        protocol=Protocol.zero_ex,
        error=None,
    )

    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_swaps(classified_traces)

    assert result.count(swap) == 1
