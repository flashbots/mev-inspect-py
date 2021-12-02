from mev_inspect.compound_liquidations import get_compound_liquidations
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.traces import Protocol
from mev_inspect.classifiers.trace import TraceClassifier
from tests.utils import load_test_block, load_comp_markets, load_cream_markets

comp_markets = load_comp_markets()
cream_markets = load_cream_markets()


def test_c_ether_liquidations():
    block_number = 13234998
    transaction_hash = (
        "0x78f7e67391c2bacde45e5057241f8b9e21a59330bce4332eecfff8fac279d090"
    )

    liquidations = [
        Liquidation(
            liquidated_user="0xb5535a3681cf8d5431b8acfd779e2f79677ecce9",
            liquidator_user="0xe0090ec6895c087a393f0e45f1f85098a6c33bef",
            debt_token_address="0x39aa39c021dfbae8fac545936693ac917d5e7563",
            debt_purchase_amount=268066492249420078,
            received_amount=4747650169097,
            protocol=Protocol.compound_v2,
            transaction_hash=transaction_hash,
            trace_address=[1],
            block_number=block_number,
        )
    ]
    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_compound_liquidations(classified_traces)
    assert result == liquidations

    block_number = 13207907
    transaction_hash = (
        "0x42a575e3f41d24f3bb00ae96f220a8bd1e24e6a6282c2e0059bb7820c61e91b1"
    )

    liquidations = [
        Liquidation(
            liquidated_user="0x45df6f00166c3fb77dc16b9e47ff57bc6694e898",
            liquidator_user="0xe0090ec6895c087a393f0e45f1f85098a6c33bef",
            debt_token_address="0x35a18000230da775cac24873d00ff85bccded550",
            debt_purchase_amount=414547860568297082,
            received_amount=321973320649,
            protocol=Protocol.compound_v2,
            transaction_hash=transaction_hash,
            trace_address=[1],
            block_number=block_number,
        )
    ]

    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_compound_liquidations(classified_traces)
    assert result == liquidations

    block_number = 13298725
    transaction_hash = (
        "0x22a98b27a1d2c4f3cba9d65257d18ee961d6c98f21c7eade37da0543847eb654"
    )

    liquidations = [
        Liquidation(
            liquidated_user="0xacbcf5d2970eef25f02a27e9d9cd31027b058b9b",
            liquidator_user="0xe0090ec6895c087a393f0e45f1f85098a6c33bef",
            debt_token_address="0x35a18000230da775cac24873d00ff85bccded550",
            debt_purchase_amount=1106497772527562662,
            received_amount=910895850496,
            protocol=Protocol.compound_v2,
            transaction_hash=transaction_hash,
            trace_address=[1],
            block_number=block_number,
        )
    ]
    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_compound_liquidations(classified_traces)
    assert result == liquidations


def test_c_token_liquidation():
    block_number = 13326607
    transaction_hash = (
        "0x012215bedd00147c58e1f59807664914b2abbfc13c260190dc9cfc490be3e343"
    )

    liquidations = [
        Liquidation(
            liquidated_user="0xacdd5528c1c92b57045041b5278efa06cdade4d8",
            liquidator_user="0xe0090ec6895c087a393f0e45f1f85098a6c33bef",
            debt_token_address="0x70e36f6bf80a52b3b46b3af8e106cc0ed743e8e4",
            debt_purchase_amount=1207055531,
            received_amount=21459623305,
            protocol=Protocol.compound_v2,
            transaction_hash=transaction_hash,
            trace_address=[1],
            block_number=block_number,
        )
    ]
    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_compound_liquidations(classified_traces)
    assert result == liquidations


def test_cream_token_liquidation():
    block_number = 12674514
    transaction_hash = (
        "0x0809bdbbddcf566e5392682a9bd9d0006a92a4dc441163c791b1136f982994b1"
    )

    liquidations = [
        Liquidation(
            liquidated_user="0x46bf9479dc569bc796b7050344845f6564d45fba",
            liquidator_user="0xa2863cad9c318669660eb4eca8b3154b90fb4357",
            debt_token_address="0x44fbebd2f576670a6c33f6fc0b00aa8c5753b322",
            debt_purchase_amount=14857434973806369550,
            received_amount=1547215810826,
            protocol=Protocol.cream,
            transaction_hash=transaction_hash,
            trace_address=[],
            block_number=block_number,
        )
    ]
    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_compound_liquidations(classified_traces)
    assert result == liquidations
