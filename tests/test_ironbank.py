from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.liquidations import get_liquidations
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.prices import ETH_TOKEN_ADDRESS
from mev_inspect.schemas.traces import Protocol
from tests.utils import load_test_block

# ironbank_markets = load_ironbank_markets()


# def test_cream_ether_liquidation(trace_classifier: TraceClassifier):
#     block_number = 13404932
#     transaction_hash = (
#         "0xf5f3df6ec9b51e8e88d0d9078b04373742294530b6bcb9be045525fcab71b915"
#     )
#
#     liquidations = [
#         Liquidation(
#             liquidated_user="0x44f9636ef615a73688a84da1d714a40be503157d",
#             liquidator_user="0x949ed86c385d191e96af136e2024d96e467d7651",
#             debt_token_address=ETH_TOKEN_ADDRESS,
#             debt_purchase_amount=1002704779407853614,
#             received_amount=417926832636968,
#             received_token_address="0x2db6c82ce72c8d7d770ba1b5f5ed0b6e075066d6",
#             protocol=Protocol.cream,
#             transaction_hash=transaction_hash,
#             trace_address=[1, 0, 5, 1],
#             block_number=block_number,
#         )
#     ]
#     block = load_test_block(block_number)
#     classified_traces = trace_classifier.classify(block.traces)
#     result = get_liquidations(classified_traces)

#     for liquidation in liquidations:
#         assert liquidation in result


def test_ironbank_token_liquidation(trace_classifier: TraceClassifier):
    block_number = 14422990
    transaction_hash = (
        "0xb7b6192174289b765f318d18ad8dbd2e51a55fa359fd580ffa59d9e4693a4b9f"
    )

    liquidations = [
        Liquidation(
            liquidated_user="0x1791d5ebbdfd565f136e60a3c43269b148f92b44",
            liquidator_user="0x811213d2d0e26ecf65714074cef59119dd7f36d9",
            debt_token_address="0xfafdf0c4c1cb09d430bf88c75d88bb46dae09967",
            debt_purchase_amount=398544459931981264561,
            received_amount=75246788,
            received_token_address="0x8fc8bfd80d6a9f17fb98a373023d72531792b431",
            protocol=Protocol.ironbank,
            transaction_hash=transaction_hash,
            trace_address=[0, 1, 1],
            block_number=block_number,
        )
    ]
    block = load_test_block(block_number)
    classified_traces = trace_classifier.classify(block.traces)
    result = get_liquidations(classified_traces)

    for liquidation in liquidations:
        print(liquidation)
        assert liquidation in result
