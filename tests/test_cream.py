from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.liquidations import get_liquidations
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.prices import ETH_TOKEN_ADDRESS
from mev_inspect.schemas.traces import Protocol
from tests.utils import load_cream_markets, load_test_block

cream_markets = load_cream_markets()


def test_cream_ether_liquidation(trace_classifier: TraceClassifier):
    block_number = 13404932
    transaction_hash = (
        "0xf5f3df6ec9b51e8e88d0d9078b04373742294530b6bcb9be045525fcab71b915"
    )

    liquidations = [
        Liquidation(
            liquidated_user="0x44f9636ef615a73688a84da1d714a40be503157d",
            liquidator_user="0x949ed86c385d191e96af136e2024d96e467d7651",
            debt_token_address=ETH_TOKEN_ADDRESS,
            debt_purchase_amount=1002704779407853614,
            received_amount=417926832636968,
            received_token_address="0x2db6c82ce72c8d7d770ba1b5f5ed0b6e075066d6",
            protocol=Protocol.cream,
            transaction_hash=transaction_hash,
            trace_address=[1, 0, 5, 1],
            block_number=block_number,
        )
    ]
    block = load_test_block(block_number)
    classified_traces = trace_classifier.classify(block.traces)
    result = get_liquidations(classified_traces)

    for liquidation in liquidations:
        assert liquidation in result


def test_cream_token_liquidation(trace_classifier: TraceClassifier):
    block_number = 12674514
    transaction_hash = (
        "0x0809bdbbddcf566e5392682a9bd9d0006a92a4dc441163c791b1136f982994b1"
    )

    liquidations = [
        Liquidation(
            liquidated_user="0x46bf9479dc569bc796b7050344845f6564d45fba",
            liquidator_user="0xa2863cad9c318669660eb4eca8b3154b90fb4357",
            debt_token_address="0x514910771af9ca656af840dff83e8264ecf986ca",
            debt_purchase_amount=14857434973806369550,
            received_amount=1547215810826,
            received_token_address="0x44fbebd2f576670a6c33f6fc0b00aa8c5753b322",
            protocol=Protocol.cream,
            transaction_hash=transaction_hash,
            trace_address=[],
            block_number=block_number,
        )
    ]
    block = load_test_block(block_number)
    classified_traces = trace_classifier.classify(block.traces)
    result = get_liquidations(classified_traces)

    for liquidation in liquidations:
        assert liquidation in result
