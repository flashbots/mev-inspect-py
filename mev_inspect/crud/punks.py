import json
from typing import List

from mev_inspect.models.punk_snipes import PunkSnipeModel
from mev_inspect.schemas.punk_snipe import PunkSnipe


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
