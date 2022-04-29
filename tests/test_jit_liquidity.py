from mev_inspect.classifiers.trace import TraceClassifier
from mev_inspect.jit_liquidity import get_jit_liquidity
from mev_inspect.schemas.jit_liquidity import JITLiquidity
from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.traces import Protocol
from mev_inspect.swaps import get_swaps

from .utils import load_test_block


def test_single_sandwich_jit_liquidity_WETH_USDC(trace_classifier: TraceClassifier):
    test_block = load_test_block(13601096)
    classified_traces = trace_classifier.classify(test_block.traces)
    swaps = get_swaps(classified_traces)
    jit_liquidity_instances = get_jit_liquidity(classified_traces, swaps)

    jit_swap = Swap(  # Double check these values
        abi_name="UniswapV3Pool",
        transaction_hash="0x943131400defa5db902b1df4ab5108b58527e525da3d507bd6e6465d88fa079c".lower(),
        transaction_position=1,
        block_number=13601096,
        trace_address=[7, 0, 12, 1, 0],
        contract_address="0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8".lower(),
        from_address="0xAa6E8127831c9DE45ae56bB1b0d4D4Da6e5665BD".lower(),
        to_address="0xAa6E8127831c9DE45ae56bB1b0d4D4Da6e5665BD".lower(),
        token_in_address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48".lower(),  # USDC Contract
        token_in_amount=1896817745609,
        token_out_address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower(),
        token_out_amount=408818202022592862626,
        protocol=Protocol.uniswap_v3,
    )
    expected_jit_liquidity = [
        JITLiquidity(
            block_number=13601096,
            bot_address="0xa57Bd00134B2850B2a1c55860c9e9ea100fDd6CF".lower(),
            pool_address="0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8".lower(),
            mint_transaction_hash="0x80e4abcb0b701e9d2c0d0fd216ef22eca5fc13904e8c7b3967bcad997480d638".lower(),
            mint_trace=[0, 9, 1],
            burn_transaction_hash="0x12b3d1f0e29d9093d8f3c7cce2da95edbef01aaab3794237f263da85c37c7d27".lower(),
            burn_trace=[0, 1, 0],
            swaps=[jit_swap],
            token0_address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48".lower(),
            token1_address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower(),
            mint_token0_amount=10864608891029,
            mint_token1_amount=8281712219747858010668,
            burn_token0_amount=12634177387879,
            burn_token1_amount=7900319851971188832064,
            token0_swap_volume=1896817745609,
            token1_swap_volume=0,
        )
    ]

    assert expected_jit_liquidity == jit_liquidity_instances


def test_single_sandwich_jit_liquidity_CRV_WETH(trace_classifier: TraceClassifier):
    test_block = load_test_block(14621812)
    classified_traces = trace_classifier.classify(test_block.traces)
    swaps = get_swaps(classified_traces)
    jit_liquidity_instances = get_jit_liquidity(classified_traces, swaps)

    jit_swap = Swap(  # Double check these values
        abi_name="UniswapV3Pool",
        transaction_hash="0x37e84f64698fe1a4852370b4d043491d5f96078d7c69e52f973932bc15ce8617".lower(),
        transaction_position=5,
        block_number=14621812,
        trace_address=[0, 1],
        contract_address="0x4c83A7f819A5c37D64B4c5A2f8238Ea082fA1f4e".lower(),
        from_address="0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45".lower(),
        to_address="0x1d9d04bf507b86fea6c13a412f3bff40eeb64e96".lower(),
        token_in_address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower(),  # USDC Contract
        token_in_amount=6206673612383009024,
        token_out_address="0xD533a949740bb3306d119CC777fa900bA034cd52".lower(),
        token_out_amount=8111771836975942396605,
        protocol=Protocol.uniswap_v3,
    )
    expected_jit_liquidity = [
        JITLiquidity(
            block_number=14621812,
            bot_address="0xa57Bd00134B2850B2a1c55860c9e9ea100fDd6CF".lower(),
            pool_address="0x4c83A7f819A5c37D64B4c5A2f8238Ea082fA1f4e".lower(),
            mint_transaction_hash="0xdcb5eac97a6bcade485ee3dc8be0f7d8722e6ebacb3910fb31dea30ff40e694e".lower(),
            mint_trace=[0, 9, 1],
            burn_transaction_hash="0x499021c4f87facfffc08d143539019d8638c924a4786de15be99567ab6026b98".lower(),
            burn_trace=[0, 1, 0],
            swaps=[jit_swap],
            token0_address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower(),
            token1_address="0xD533a949740bb3306d119CC777fa900bA034cd52".lower(),
            mint_token0_amount=324305525132652136497,
            mint_token1_amount=182991368595201974557004,
            burn_token0_amount=330104892856183548121,
            burn_token1_amount=175411922548908668697796,
            token0_swap_volume=6206673612383009024,
            token1_swap_volume=0,
        )
    ]

    assert jit_liquidity_instances == expected_jit_liquidity
