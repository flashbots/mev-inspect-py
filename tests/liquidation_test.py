from typing import List

from mev_inspect.aave_liquidations import get_aave_liquidations
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.traces import Protocol
from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.transfers import ETH_TOKEN_ADDRESS
from tests.utils import load_test_block


def test_single_weth_liquidation():

    transaction_hash = (
        "0xb7575eedc9d8cfe82c4a11cd1a851221f2eafb93d738301995ac7103ffe877f7"
    )
    block_number = 13244807

    liquidations = [
        Liquidation(
            liquidated_user="0xd16404ca0a74a15e66d8ad7c925592fb02422ffe",
            liquidator_user="0x19256c009781bc2d1545db745af6dfd30c7e9cfa",
            debt_token_address="0xdac17f958d2ee523a2206206994597c13d831ec7",
            debt_purchase_amount=26503300291,
            received_amount=8182733924513576561,
            received_token_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            protocol=Protocol.aave,
            transaction_hash=transaction_hash,
            trace_address=[1, 1, 6],
            block_number=block_number,
        )
    ]

    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_aave_liquidations(classified_traces)

    _assert_equal_list_of_liquidations(result, liquidations)


def test_single_liquidation():

    transaction_hash = (
        "0xe6c0e3ef0436cb032e1ef292141f4fc4dcd47a75a2559602133114952190e76b"
    )
    block_number = 10921991

    liquidations = [
        Liquidation(
            liquidated_user="0x8d8d912fe4db5917da92d14fea05225b803c359c",
            liquidator_user="0xf2d9e54f0e317b8ac94825b2543908e7552fe9c7",
            debt_token_address="0xdac17f958d2ee523a2206206994597c13d831ec7",
            debt_purchase_amount=1069206535,
            received_amount=2657946947610159065393,
            received_token_address="0x80fb784b7ed66730e8b1dbd9820afd29931aab03",
            protocol=Protocol.aave,
            transaction_hash=transaction_hash,
            trace_address=[0, 7, 1, 0, 6],
            block_number=block_number,
        )
    ]

    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_aave_liquidations(classified_traces)

    _assert_equal_list_of_liquidations(result, liquidations)


def test_single_liquidation_with_atoken_payback():

    transaction_hash = (
        "0xde551a73e813f1a1e5c843ac2c6a0e40d71618f4040bb7d0cd7cf7b2b6cf4633"
    )
    block_number = 13376024

    liquidations = [
        Liquidation(
            liquidated_user="0x3d2b6eacd1bca51af57ed8b3ff9ef0bd8ee8c56d",
            liquidator_user="0x887668f2dc9612280243f2a6ef834cecf456654e",
            debt_token_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            debt_purchase_amount=767615458043667978,
            received_amount=113993647930952952550,
            received_token_address="0xa06bc25b5805d5f8d82847d191cb4af5a3e873e0",
            protocol=Protocol.aave,
            transaction_hash=transaction_hash,
            trace_address=[2],
            block_number=block_number,
        )
    ]

    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_aave_liquidations(classified_traces)

    _assert_equal_list_of_liquidations(result, liquidations)


def test_multiple_liquidations_in_block():

    transaction1 = "0xedd062c3a728db4b114f2e83cac281d19a9f753e36afa8a35cdbdf1e1dd5d017"
    transaction2 = "0x18492f250cf4735bd67a21c6cc26b7d9c59cf2fb077356dc924f36bc68a810e5"
    transaction3 = "0x191b05b28ebaf460e38e90ac6a801681b500f169041ae83a45b32803ef2ec98c"
    block_number = 12498502

    liquidation1 = Liquidation(
        liquidated_user="0x6c6541ae8a7c6a6f968124a5ff2feac8f0c7875b",
        liquidator_user="0x7185e240d8e9e2d692cbc68d30eecf965e9a7feb",
        debt_token_address="0x4fabb145d64652a948d72533023f6e7a623c7c53",
        debt_purchase_amount=457700000000000000000,
        received_amount=10111753901939162887,
        received_token_address="0x514910771af9ca656af840dff83e8264ecf986ca",
        protocol=Protocol.aave,
        transaction_hash=transaction1,
        trace_address=[],
        block_number=block_number,
    )

    liquidation2 = Liquidation(
        liquidated_user="0x6c6541ae8a7c6a6f968124a5ff2feac8f0c7875b",
        liquidator_user="0x7185e240d8e9e2d692cbc68d30eecf965e9a7feb",
        debt_token_address="0x0000000000085d4780b73119b644ae5ecd22b376",
        debt_purchase_amount=497030000000000000000,
        received_amount=21996356316098208090,
        received_token_address="0x514910771af9ca656af840dff83e8264ecf986ca",
        protocol=Protocol.aave,
        transaction_hash=transaction2,
        trace_address=[],
        block_number=block_number,
    )

    liquidation3 = Liquidation(
        liquidated_user="0xda874f844389df33c0fad140df4970fe1b366726",
        liquidator_user="0x7185e240d8e9e2d692cbc68d30eecf965e9a7feb",
        debt_token_address="0x57ab1ec28d129707052df4df418d58a2d46d5f51",
        debt_purchase_amount=447810000000000000000,
        received_amount=121531358145247546,
        received_token_address="0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2",
        protocol=Protocol.aave,
        transaction_hash=transaction3,
        trace_address=[],
        block_number=block_number,
    )

    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_aave_liquidations(classified_traces)
    liquidations = [liquidation1, liquidation2, liquidation3]

    _assert_equal_list_of_liquidations(result, liquidations)


def test_liquidations_with_eth_transfer():

    transaction_hash = (
        "0xf687fedbc4bbc25adb3ef3a35c20c38fb7d35d86d7633d5061d2e3c4f86311b7"
    )
    block_number = 13302365

    liquidation1 = Liquidation(
        liquidated_user="0xad346c7762f74c78da86d2941c6eb546e316fbd0",
        liquidator_user="0x27239549dd40e1d60f5b80b0c4196923745b1fd2",
        debt_token_address="0x514910771af9ca656af840dff83e8264ecf986ca",
        debt_purchase_amount=1809152000000000000,
        received_amount=15636807387264000,
        received_token_address=ETH_TOKEN_ADDRESS,
        protocol=Protocol.aave,
        transaction_hash=transaction_hash,
        trace_address=[2, 3, 2],
        block_number=block_number,
    )

    liquidation2 = Liquidation(
        liquidated_user="0xad346c7762f74c78da86d2941c6eb546e316fbd0",
        liquidator_user="0x27239549dd40e1d60f5b80b0c4196923745b1fd2",
        debt_token_address="0x514910771af9ca656af840dff83e8264ecf986ca",
        debt_purchase_amount=1809152000000000000,
        received_amount=8995273139160873,
        received_token_address=ETH_TOKEN_ADDRESS,
        protocol=Protocol.aave,
        transaction_hash=transaction_hash,
        trace_address=[2, 4, 2],
        block_number=block_number,
    )

    block = load_test_block(block_number)
    trace_classifier = TraceClassifier()
    classified_traces = trace_classifier.classify(block.traces)
    result = get_aave_liquidations(classified_traces)
    liquidations = [liquidation1, liquidation2]

    _assert_equal_list_of_liquidations(result, liquidations)


def _assert_equal_list_of_liquidations(
    actual_liquidations: List[Liquidation], expected_liquidations: List[Liquidation]
):
    for i in range(len(actual_liquidations)):
        assert actual_liquidations[i] == expected_liquidations[i]
