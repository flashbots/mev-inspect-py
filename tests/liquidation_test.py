import unittest

from mev_inspect.aave_liquidations import get_liquidations
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.classified_traces import Protocol
from mev_inspect.classifiers.trace import TraceClassifier
from tests.utils import load_test_block


class TestAaveLiquidations(unittest.TestCase):
    def test_single_weth_liquidation(self):

        transaction_hash = (
            "0xb7575eedc9d8cfe82c4a11cd1a851221f2eafb93d738301995ac7103ffe877f7"
        )
        block_number = 13244807

        liquidation = Liquidation(
            liquidated_user="0xd16404ca0a74a15e66d8ad7c925592fb02422ffe",
            liquidator_user="0x19256c009781bc2d1545db745af6dfd30c7e9cfa",
            collateral_token_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            debt_token_address="0xdac17f958d2ee523a2206206994597c13d831ec7",
            debt_purchase_amount=26503300291,
            received_amount=8182733924513576561,
            protocol=Protocol.aave,
            transaction_hash=transaction_hash,
            block_number=block_number,
        )

        block = load_test_block(block_number)
        trace_classifier = TraceClassifier()
        classified_traces = trace_classifier.classify(block.traces)
        result = get_liquidations(classified_traces)

        self.assertEqual(result[0], liquidation)
        self.assertEqual(len(result), 1)

    def test_single_liquidation(self):

        transaction_hash = (
            "0xe6c0e3ef0436cb032e1ef292141f4fc4dcd47a75a2559602133114952190e76b"
        )
        block_number = 10921991

        liquidation = Liquidation(
            liquidated_user="0x8d8d912fe4db5917da92d14fea05225b803c359c",
            liquidator_user="0xf2d9e54f0e317b8ac94825b2543908e7552fe9c7",
            collateral_token_address="0x80fb784b7ed66730e8b1dbd9820afd29931aab03",
            debt_token_address="0xdac17f958d2ee523a2206206994597c13d831ec7",
            debt_purchase_amount=1069206535,
            received_amount=2657946947610159065393,
            protocol=Protocol.aave,
            transaction_hash=transaction_hash,
            block_number=block_number,
        )

        block = load_test_block(block_number)
        trace_classifier = TraceClassifier()
        classified_traces = trace_classifier.classify(block.traces)
        result = get_liquidations(classified_traces)

        self.assertEqual(result[0], liquidation)
        self.assertEqual(len(result), 1)

    def test_single_liquidation_2(self):

        transaction_hash = (
            "0x7369b6c1e1b15a761cad3e618b4df2eb84747c58fa34230e752cc2eaf241c493"
        )
        block_number = 13179291

        liquidation = Liquidation(
            liquidated_user="0xbec69dfce4c1fa8b7843fee1ca85788d84a86b06",
            liquidator_user="0x19256c009781bc2d1545db745af6dfd30c7e9cfa",
            collateral_token_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            debt_token_address="0x6b175474e89094c44da98b954eedeac495271d0f",
            debt_purchase_amount=128362984518555820706221,
            received_amount=37818925894787751803,
            protocol=Protocol.aave,
            transaction_hash=transaction_hash,
            block_number=block_number,
        )

        block = load_test_block(block_number)
        trace_classifier = TraceClassifier()
        classified_traces = trace_classifier.classify(block.traces)
        result = get_liquidations(classified_traces)

        self.assertEqual(result[1], liquidation)
        self.assertEqual(len(result), 2)

    def multiple_liquidations_in_block(self):

        transaction1 = (
            "0xedd062c3a728db4b114f2e83cac281d19a9f753e36afa8a35cdbdf1e1dd5d017"
        )
        transaction2 = (
            "0x18492f250cf4735bd67a21c6cc26b7d9c59cf2fb077356dc924f36bc68a810e5"
        )
        transaction3 = (
            "0x191b05b28ebaf460e38e90ac6a801681b500f169041ae83a45b32803ef2ec98c"
        )
        block_number = 12498502

        liquidation1 = Liquidation(
            liquidated_user="0x6c6541ae8a7c6a6f968124a5ff2feac8f0c7875b",
            liquidator_user="0x7185e240d8e9e2d692cbc68d30eecf965e9a7feb",
            collateral_token_address="0x514910771af9ca656af840dff83e8264ecf986ca",
            debt_token_address="0x4fabb145d64652a948d72533023f6e7a623c7c53",
            debt_purchase_amount=228905512631913119672,
            received_amount=10111753901939162887,
            protocol=Protocol.aave,
            transaction_hash=transaction1,
        )

        liquidation2 = Liquidation(
            liquidated_user="0x6c6541ae8a7c6a6f968124a5ff2feac8f0c7875b",
            liquidator_user="0x19256c009781bc2d1545db745af6dfd30c7e9cfa",
            collateral_token_address="0x514910771af9ca656af840dff83e8264ecf986ca",
            debt_token_address="0x0000000000085d4780b73119b644ae5ecd22b376",
            debt_purchase_amount=497030000000000000000,
            received_amount=21996356316098208090,
            protocol=Protocol.aave,
            transaction_hash=transaction2,
            block_number=block_number,
        )

        liquidation3 = Liquidation(
            liquidated_user="0xda874f844389df33c0fad140df4970fe1b366726",
            liquidator_user="0x7185e240d8e9e2d692cbc68d30eecf965e9a7feb",
            collateral_token_address="0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2",
            debt_token_address="0x57ab1ec28d129707052df4df418d58a2d46d5f51",
            debt_purchase_amount=447810000000000000000,
            received_amount=121531358145247546,
            protocol=Protocol.aave,
            transaction_hash=transaction3,
            block_number=block_number,
        )

        block = load_test_block(block_number)
        trace_classifier = TraceClassifier()
        classified_traces = trace_classifier(block.traces)
        result = get_liquidations(classified_traces)

        self.assertEqual(result, [liquidation1, liquidation2, liquidation3])


if __name__ == "__main__":
    unittest.main()
