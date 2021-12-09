import json
from typing import List

from mev_inspect.models.punks import (
    PunkSnipeModel,
    PunkBidModel,
    PunkBidAcceptanceModel,
)
from mev_inspect.schemas.punk_snipe import PunkSnipe
from mev_inspect.schemas.punk_bid import PunkBid
from mev_inspect.schemas.punk_accept_bid import PunkBidAcceptance


def delete_punk_bid_acceptances_for_block(
    db_session,
    block_number: int,
) -> None:
    (
        db_session.query(PunkBidAcceptanceModel)
        .filter(PunkBidAcceptanceModel.block_number == block_number)
        .delete()
    )

    db_session.commit()


def write_punk_bid_acceptances(
    db_session,
    punk_bid_acceptances: List[PunkBidAcceptance],
) -> None:
    models = [
        PunkBidAcceptanceModel(**json.loads(punk_bid_acceptance.json()))
        for punk_bid_acceptance in punk_bid_acceptances
    ]

    db_session.bulk_save_objects(models)
    db_session.commit()


def delete_punk_bids_for_block(
    db_session,
    block_number: int,
) -> None:
    (
        db_session.query(PunkBidModel)
        .filter(PunkBidModel.block_number == block_number)
        .delete()
    )

    db_session.commit()


def write_punk_bids(
    db_session,
    punk_bids: List[PunkBid],
) -> None:
    models = [PunkBidModel(**json.loads(punk_bid.json())) for punk_bid in punk_bids]

    db_session.bulk_save_objects(models)
    db_session.commit()


def delete_punk_snipes_for_block(
    db_session,
    block_number: int,
) -> None:
    (
        db_session.query(PunkSnipeModel)
        .filter(PunkSnipeModel.block_number == block_number)
        .delete()
    )

    db_session.commit()


def write_punk_snipes(
    db_session,
    punk_snipes: List[PunkSnipe],
) -> None:
    models = [
        PunkSnipeModel(**json.loads(punk_snipe.json())) for punk_snipe in punk_snipes
    ]

    db_session.bulk_save_objects(models)
    db_session.commit()
