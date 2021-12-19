import json
from typing import List

from mev_inspect.models.nft_trades import NftTradeModel
from mev_inspect.schemas.nft_trades import NftTrade


def delete_nft_trades_for_block(
    db_session,
    block_number: int,
) -> None:
    (
        db_session.query(NftTradeModel)
        .filter(NftTradeModel.block_number == block_number)
        .delete()
    )

    db_session.commit()


def write_nft_trades(
    db_session,
    nft_trades: List[NftTrade],
) -> None:
    models = [NftTradeModel(**json.loads(nft_trade.json())) for nft_trade in nft_trades]

    db_session.bulk_save_objects(models)
    db_session.commit()
