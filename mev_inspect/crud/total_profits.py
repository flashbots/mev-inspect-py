from typing import List

from mev_inspect.db import write_as_csv
from mev_inspect.schemas.total_profits import TotalProfits


def write_total_profits_for_blocks(
    inspect_db_session,
    total_profits_for_blocks: List[TotalProfits],
) -> None:
    items_generator = (
        (
            total_profits_for_unique_block.block_number,
            total_profits_for_unique_block.transaction_hash,
            total_profits_for_unique_block.token_debt,
            total_profits_for_unique_block.amount_debt,
            total_profits_for_unique_block.token_received,
            total_profits_for_unique_block.amount_received,
        )
        for total_profits_for_unique_block in total_profits_for_blocks
    )
    write_as_csv(inspect_db_session, "total_profit_by_block", items_generator)
