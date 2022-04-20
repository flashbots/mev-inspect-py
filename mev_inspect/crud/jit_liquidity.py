from typing import List
from uuid import uuid4

from mev_inspect.schemas.jit_liquidity import JITLiquidity
from mev_inspect.models.jit_liquidity import JITLiquidityModel

from .shared import delete_by_block_range


def delete_jit_liquidity_for_blocks(
        db_session,
        after_block_number: int,
        before_block_number: int,
) -> None:
    delete_by_block_range(
        db_session,
        JITLiquidityModel,
        after_block_number,
        before_block_number,
    )
    db_session.commit()


def write_jit_liquidity(
        db_session,
        jit_liquidity_instances: List[JITLiquidity]
) -> None:
    jit_liquidity_models = []
    swap_jit_liquidity_ids = []
    for jit_liquidity in jit_liquidity_instances:
        jit_liquidity_id = str(uuid4())
        jit_liquidity_models.append(JITLiquidityModel(
            id=jit_liquidity_id,
            block_number=jit_liquidity.block_number,
            bot_address=jit_liquidity.bot_address,
            pool_address=jit_liquidity.pool_address,
            token0_address=jit_liquidity.token0_address,
            token1_address=jit_liquidity.token1_address,
            mint_transaction_hash=jit_liquidity.mint_transaction_hash,
            mint_transaction_trace=jit_liquidity.mint_trace,
            burn_transaction_hash=jit_liquidity.burn_transaction_hash,
            burn_transaction_trace=jit_liquidity.burn_trace,
            mint_token0_amount=jit_liquidity.mint_token0_amount,
            mint_token1_amount=jit_liquidity.mint_token1_amount,
            burn_token0_amoun=jit_liquidity.burn_token0_amount,
            burn_token1_amount=jit_liquidity.burn_token1_amount,
            token0_swap_volume=jit_liquidity.token0_swap_volume,
            token1_swap_volume=jit_liquidity.token1_swap_volume
        ))

        for swap in jit_liquidity.swaps:
            swap_jit_liquidity_ids.append({
                "jit_liquidity_id": jit_liquidity_id,
                "swap_transaction_hash": swap.transaction_hash,
                "swap_trace_address": swap.trace_address
            })

    if len(jit_liquidity_models) > 0:
        db_session.bulk_save_objects(jit_liquidity_models)
        db_session.execute(
            """
            INSERT INTO jit_liquidity_swaps
            (jit_liquidity_id, swap_transaction_hash, swap_trace_address)
            VALUES
            (:jit_liquidity_id, :swap_transaction_hash, :swap_trace_address)
            """,
            params=swap_jit_liquidity_ids
        )

        db_session.commit()
