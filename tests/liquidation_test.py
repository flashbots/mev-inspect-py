import unittest
from web3 import Web3

from mev_inspect.aave_liquidations import get_liquidations
from mev_inspect.schemas.liquidations import Liquidation
from mev_inspect.schemas.classified_traces import Protocol
from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.block import create_from_block_number


class TestAaveLiquidations(unittest.TestCase):
    def test_single_weth_liquidation(self):

        base_provider = Web3.HTTPProvider("http://")
        w3 = Web3(base_provider)
        transaction_hash = (
            "0xb7575eedc9d8cfe82c4a11cd1a851221f2eafb93d738301995ac7103ffe877f7"
        )
        block_number = 13244807
        should_cache = False

        liquidation = Liquidation(
            liquidated_user="0xd16404ca0a74a15e66d8ad7c925592fb02422ffe",
            liquidator_user="0x19256c009781bc2d1545db745af6dfd30c7e9cfa",
            collateral_token_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            debt_token_address="0xdac17f958d2ee523a2206206994597c13d831ec7",
            debt_purchase_amount=26503300291,
            received_token_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            received_amount=8182733924513576561,
            protocol=Protocol.aave,
            transaction_hash=transaction_hash,
            block_number=block_number,
        )

        block = create_from_block_number(base_provider, w3, block_number, should_cache)
        trace_classifier = TraceClassifier()
        classified_traces = trace_classifier.classify(block.traces)
        result = get_liquidations(classified_traces)

        self.assertEqual(result[0], liquidation)

    def test_single_liquidation(self):

        base_provider = Web3.HTTPProvider("http://")
        w3 = Web3(base_provider)
        transaction_hash = (
            "0xe6c0e3ef0436cb032e1ef292141f4fc4dcd47a75a2559602133114952190e76b"
        )
        block_number = 10921991
        should_cache = False

        liquidation = Liquidation(
            liquidated_user="0x8d8d912fe4db5917da92d14fea05225b803c359c",
            liquidator_user="0xf2d9e54f0e317b8ac94825b2543908e7552fe9c7",
            collateral_token_address="0x80fb784b7ed66730e8b1dbd9820afd29931aab03",
            debt_token_address="0xdac17f958d2ee523a2206206994597c13d831ec7",
            debt_purchase_amount=1069206535,
            received_token_address="0x80fb784b7ed66730e8b1dbd9820afd29931aab03",
            received_amount=2657946947610159065393,
            protocol=Protocol.aave,
            transaction_hash=transaction_hash,
            block_number=block_number,
        )

        block = create_from_block_number(base_provider, w3, block_number, should_cache)
        trace_classifier = TraceClassifier()
        classified_traces = trace_classifier.classify(block.traces)
        result = get_liquidations(classified_traces)

        self.assertEqual(result[0], liquidation)


# Fails precommit because these inspectors don't exist yet
# from mev_inspect import inspector_compound
# from mev_inspect import inspector_aave
#
#
# class TestLiquidations(unittest.TestCase):
#     def test_compound_liquidation(self):
#         tx_hash = "0x0ec6d5044a47feb3ceb647bf7ea4ffc87d09244d629eeced82ba17ec66605012"
#         block_no = 11338848
#         res = inspector_compound.get_profit(tx_hash, block_no)
#         # self.assertEqual(res['profit'], 0)
#
#     def test_aave_liquidation(self):
#         tx_hash = "0xc8d2501d28800b1557eb64c5d0e08fd6070c15b6c04c39ca05631f641d19ffb2"
#         block_no = 10803840
#         res = inspector_aave.get_profit(tx_hash, block_no)
#         # self.assertEqual(res['profit'], 0)


if __name__ == "__main__":
    unittest.main()
