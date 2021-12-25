import json
from typing import List

from mev_inspect.crud.shared import delete_by_block_range
from mev_inspect.models.nft_trades import NftTradeModel
from mev_inspect.schemas.nft_trades import NftTrade


def delete_nft_trades_for_blocks(
    db_session,
    after_block_number: int,
    before_block_number: int,
) -> None:
    delete_by_block_range(
        db_session,
        NftTradeModel,
        after_block_number,
        before_block_number,
    )
    db_session.commit()


def write_nft_trades(
    db_session,
    nft_trades: List[NftTrade],
) -> None:
    models = [NftTradeModel(**json.loads(nft_trade.json())) for nft_trade in nft_trades]

    db_session.bulk_save_objects(models)
    db_session.commit()
