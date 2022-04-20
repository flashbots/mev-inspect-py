from mev_inspect.schemas.jit_liquidity import JITLiquidity
from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.traces import Protocol
from mev_inspect.swaps import get_swaps
from mev_inspect.jit_liquidity import get_jit_liquidity

from mev_inspect.classifiers.trace import TraceClassifier

from .utils import load_test_block


def test_single_sandwich_jit_liquidity(trace_classifier: TraceClassifier):
    print("\n")
    test_block = load_test_block(13601096)

    classified_traces = trace_classifier.classify(test_block.traces)
    swaps = get_swaps(classified_traces)
    jit_liquidity_instances = get_jit_liquidity(classified_traces, swaps)

    # Assert Section

    jit_swap = Swap(  # Double check these values
        abi_name="UniswapV3Pool",
        transaction_hash="0x943131400defa5db902b1df4ab5108b58527e525da3d507bd6e6465d88fa079c".lower(),
        transaction_position=1,
        block_number=13601096,
        trace_address=[7, 0, 12, 1, 0],
        contract_address="0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8".lower(),
        from_address="0xE592427A0AEce92De3Edee1F18E0157C05861564".lower(),
        to_address="0xAa6E8127831c9DE45ae56bB1b0d4D4Da6e5665BD".lower(),
        token_in_address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48".lower(),  # USDC Contract
        token_in_amount=1896817745609,
        token_out_address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower(),
        token_out_amount=408818202022592862626,
        protocol=Protocol.uniswap_v3
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
            token0_address="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            token1_address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            mint_token0_amount=10864608891029,
            mint_token1_amount=8281712219747858010668,
            burn_token0_amount=12634177387879,
            burn_token1_amount=7900319851971188832064,
            token0_swap_volume=1896817745609,
            token1_swap_volume=0,
        )
    ]

    # Might be super janky but this could be done with assert jit_liquidity_instances == expected_jit_liquidity
    assert len(jit_liquidity_instances) == 1
    assert len(jit_liquidity_instances[0].swaps) == 1
    assert jit_liquidity_instances[0].burn_transaction_hash == expected_jit_liquidity[0].burn_transaction_hash
    assert jit_liquidity_instances[0].mint_transaction_hash == expected_jit_liquidity[0].mint_transaction_hash
    assert jit_liquidity_instances[0].burn_token0_amount == expected_jit_liquidity[0].burn_token0_amount
    assert jit_liquidity_instances[0].burn_token1_amount == expected_jit_liquidity[0].burn_token1_amount
    assert jit_liquidity_instances[0].mint_token0_amount == expected_jit_liquidity[0].mint_token0_amount
    assert jit_liquidity_instances[0].mint_token1_amount == expected_jit_liquidity[0].mint_token1_amount
    assert jit_liquidity_instances[0].bot_address == expected_jit_liquidity[0].bot_address
    assert jit_liquidity_instances[0].token0_swap_volume == expected_jit_liquidity[0].token0_swap_volume
    assert jit_liquidity_instances[0].token1_swap_volume == expected_jit_liquidity[0].token1_swap_volume

    # Swap Checks
    assert jit_liquidity_instances[0].swaps[0].transaction_hash == jit_swap.transaction_hash
    assert jit_liquidity_instances[0].swaps[0].trace_address == jit_swap.trace_address




