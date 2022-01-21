INSERT_ARBITRAGE_SUMMARY_QUERY = """
INSERT INTO mev_summary (
    SELECT
        NULL,
        a.block_number,
        b.block_timestamp,
        NULL AS protocol,
        a.transaction_hash,
        'arbitrage' AS type,
        (
            (
                SELECT usd_price
                FROM prices
                WHERE
                    token_address = a.profit_token_address
                    AND timestamp <= b.block_timestamp
                ORDER BY timestamp DESC
                LIMIT 1
            ) * a.profit_amount / POWER(10, profit_token.decimals)
        ) AS gross_profit_usd,
        (
            (
                ((mp.gas_used * mp.gas_price) + mp.coinbase_transfer) /
                POWER(10, 18)
            ) * 
            (
                SELECT usd_price
                FROM prices p
                WHERE
                    p.timestamp <= b.block_timestamp
                    AND p.token_address = '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
                ORDER BY p.timestamp DESC
                LIMIT 1
            )
        ) AS miner_payment_usd,
        mp.gas_used,
        mp.gas_price,
        mp.coinbase_transfer,
        mp.gas_price_with_coinbase_transfer,
        mp.miner_address,
        mp.base_fee_per_gas,
        ct.error as error,
        a.protocols
    FROM arbitrages a
    JOIN blocks b ON b.block_number = a.block_number
    JOIN tokens profit_token ON profit_token.token_address = a.profit_token_address
    JOIN classified_traces ct ON
        ct.block_number = a.block_number AND
        ct.transaction_hash = a.transaction_hash
    JOIN miner_payments mp ON
        mp.block_number = a.block_number AND
        mp.transaction_hash = a.transaction_hash
    WHERE
        b.block_number >= :after_block_number
        AND b.block_number < :before_block_number
        AND ct.trace_address = '{}'
        AND NOT EXISTS (
            SELECT 1
            FROM sandwiches front_sandwich
            WHERE 
                front_sandwich.block_number = a.block_number AND
                front_sandwich.frontrun_swap_transaction_hash = a.transaction_hash
        )
        AND NOT EXISTS (
            SELECT 1
            FROM sandwiches back_sandwich
            WHERE
                back_sandwich.block_number = a.block_number AND
                back_sandwich.backrun_swap_transaction_hash = a.transaction_hash
        )
)
"""

INSERT_LIQUIDATIONS_SUMMARY_QUERY = """
INSERT INTO mev_summary (
    SELECT
        NULL,
        l.block_number,
        b.block_timestamp,
        l.protocol as protocol,
        l.transaction_hash,
        'liquidation' as type,
        l.received_amount*
        (
            SELECT usd_price
            FROM prices
            WHERE token_address = l.received_token_address
            AND timestamp <= b.block_timestamp
            ORDER BY timestamp DESC
            LIMIT 1
        )
        /POWER(10, received_token.decimals) 
        
        - 

        l.debt_purchase_amount*
        (
            SELECT usd_price
            FROM prices
            WHERE token_address = l.debt_token_address
            AND timestamp <= b.block_timestamp
            ORDER BY timestamp DESC
            LIMIT 1
        )
        /POWER(10, debt_token.decimals) as gross_profit_usd,
        (
            (
                ((mp.gas_used * mp.gas_price) + mp.coinbase_transfer) /
                POWER(10, 18)
            ) * 
            (
                SELECT usd_price
                FROM prices p
                WHERE
                    p.timestamp <= b.block_timestamp
                    AND p.token_address = '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
                ORDER BY p.timestamp DESC
                LIMIT 1
            )
        ) AS miner_payment_usd,
        mp.gas_used,
        mp.gas_price,
        mp.coinbase_transfer,
        mp.gas_price_with_coinbase_transfer,
        mp.miner_address,
        mp.base_fee_per_gas,
        ct.error as error,
        ARRAY[l.protocol]
    FROM liquidations l
    JOIN blocks b ON b.block_number = l.block_number
    JOIN tokens received_token ON received_token.token_address = l.received_token_address
    JOIN tokens debt_token ON debt_token.token_address = l.debt_token_address
    JOIN miner_payments mp ON
        mp.block_number = l.block_number AND
        mp.transaction_hash = l.transaction_hash
    JOIN classified_traces ct ON
        ct.block_number = l.block_number AND
        ct.transaction_hash = l.transaction_hash
    WHERE
        b.block_number >= :after_block_number AND 
        b.block_number < :before_block_number AND
        ct.trace_address = '{}' AND
        l.debt_purchase_amount > 0 AND
        l.received_amount > 0 AND
        l.debt_purchase_amount < 115792089237316195423570985008687907853269984665640564039457584007913129639935
)
"""


def update_summary_for_block_range(
    db_session,
    after_block_number: int,
    before_block_number: int,
) -> None:
    _delete_summary_for_block_range(db_session, after_block_number, before_block_number)
    _insert_into_summary_for_block_range(
        db_session, after_block_number, before_block_number
    )


def _delete_summary_for_block_range(
    db_session,
    after_block_number: int,
    before_block_number: int,
) -> None:
    db_session.execute(
        """
        DELETE FROM mev_summary
        WHERE
            block_number >= :after_block_number AND
            block_number < :before_block_number
        """,
        params={
            "after_block_number": after_block_number,
            "before_block_number": before_block_number,
        },
    )

    db_session.commit()


def _insert_into_summary_for_block_range(
    db_session,
    after_block_number: int,
    before_block_number: int,
) -> None:
    db_session.execute(
        INSERT_ARBITRAGE_SUMMARY_QUERY,
        params={
            "after_block_number": after_block_number,
            "before_block_number": before_block_number,
        },
    )

    db_session.execute(
        INSERT_LIQUIDATIONS_SUMMARY_QUERY,
        params={
            "after_block_number": after_block_number,
            "before_block_number": before_block_number,
        },
    )

    db_session.commit()
