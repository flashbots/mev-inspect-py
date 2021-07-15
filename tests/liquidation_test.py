import unittest

from mev_inspect import inspector_compound
from mev_inspect import inspector_aave

class TestLiquidations (unittest.TestCase):
    def test_compound_liquidation(self):
        tx_hash = "0x0ec6d5044a47feb3ceb647bf7ea4ffc87d09244d629eeced82ba17ec66605012"
        block_no = 11338848
        res = inspector_compound.get_profit(tx_hash, block_no)
        # self.assertEqual(res['profit'], 0)
    def test_aave_liquidation(self):
        tx_hash = "0xc8d2501d28800b1557eb64c5d0e08fd6070c15b6c04c39ca05631f641d19ffb2"
        block_no = 10803840
        res = inspector_aave.get_profit(tx_hash, block_no)
        # self.assertEqual(res['profit'], 0)


if __name__ == '__main__':
    unittest.main()
