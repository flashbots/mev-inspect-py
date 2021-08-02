import unittest
from mev_inspect.trace_classifier import TraceClassifier
from mev_inspect.classifier_specs import CLASSIFIER_SPECS
from mev_inspect.block import _get_cache_path
from mev_inspect.strategy_inspectors.compound_v2_ceth import inspect_compound_v2_ceth

# from mev_inspect.schemas.classified_traces import Classification
from mev_inspect.schemas.liquidations import (
    LiquidationCollateralSource,
    LiquidationType,
    LiquidationStatus,
)
from mev_inspect.schemas import Block


class TestCompoundV2Liquidation(unittest.TestCase):
    def test_compound_v2_ceth_liquidation(self):
        tx_hash = "0xd09e499f2c2d6a900a974489215f25006a5a3fa401a10b8d67fa99480cbb62fb"
        block_no = 12900060
        cache_path = _get_cache_path(block_no)
        block_data = Block.parse_file(cache_path)

        tx_traces = block_data.get_filtered_traces(tx_hash)
        trace_clasifier = TraceClassifier(CLASSIFIER_SPECS)
        classified_traces = trace_clasifier.classify(tx_traces)
        res = inspect_compound_v2_ceth(classified_traces)

        self.assertEqual(res.tx_hash, "0x0")
        self.assertEqual(res.borrower, "0x0")
        self.assertEqual(res.collateral_provided, "0x0")
        self.assertEqual(res.collateral_provided_amount, 0)
        self.assertEqual(res.asset_seized, "0x0")
        self.assertEqual(res.asset_seized_amount, 0)
        self.assertEqual(res.profit_in_eth, 0)
        self.assertEqual(res.tokenflow_estimate_in_eth, 0)
        self.assertEqual(res.tokenflow_diff, 0)
        self.assertEqual(res.status, LiquidationStatus.seized)
        self.assertEqual(res.type, LiquidationType.compound_v2_ceth_liquidation)
        self.assertEqual(res.collateral_source, LiquidationCollateralSource.other)


if __name__ == "__main__":
    unittest.main()
