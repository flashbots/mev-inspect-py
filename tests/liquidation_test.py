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


if __name__ == "__main__":
    unittest.main()
