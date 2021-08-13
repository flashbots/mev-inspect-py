import unittest

from mev_inspect import tokenflow

from .utils import load_test_block


class TestTokenFlow(unittest.TestCase):
    def test_simple_arb(self):
        tx_hash = "0x4121ce805d33e952b2e6103a5024f70c118432fd0370128d6d7845f9b2987922"
        block_no = 11930296

        block = load_test_block(block_no)
        res = tokenflow.run_tokenflow(tx_hash, block)
        self.assertEqual(res["ether_flows"], [3547869861992962562, 3499859860420296704])
        self.assertEqual(res["dollar_flows"], [0, 0])

    def test_arb_with_stable_flow(self):
        tx_hash = "0x496836e0bd1520388e36c79d587a31d4b3306e4f25352164178ca0667c7f9c29"
        block_no = 11935012

        block = load_test_block(block_no)
        res = tokenflow.run_tokenflow(tx_hash, block)
        self.assertEqual(res["ether_flows"], [597044987302243493, 562445964778930176])
        self.assertEqual(res["dollar_flows"], [871839781, 871839781])

    def test_complex_cross_arb(self):
        tx_hash = "0x5ab21bfba50ad3993528c2828c63e311aafe93b40ee934790e545e150cb6ca73"
        block_no = 11931272
        block = load_test_block(block_no)
        res = tokenflow.run_tokenflow(tx_hash, block)
        self.assertEqual(res["ether_flows"], [3636400213125714803, 3559576672903063566])
        self.assertEqual(res["dollar_flows"], [0, 0])


if __name__ == "__main__":
    unittest.main()
