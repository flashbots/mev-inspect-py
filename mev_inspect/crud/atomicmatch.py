import json
from typing import list

from mev_inspect.models.atomicmatch import AtomicMatchModel
from mev_inspect.schemas.atomicmatch import AtomicMatch

def delete_atomicmatch_for_block(
    db_session,
    block_number: int,
) -> None:
    (
        db_session.query(AtomicMatchModel)
        .filter(AtomicMatchModel.block_number == block_number)
        .delete()
    )

    db_session.commit()

def write_atomicmatch(
    db_session,
    atomicmatches: List[AtomicMatch],
) -> None:
    models = [AtomicMatchModel(**json.loads(atomicmatch.json())) for atomicmatch in atomicmatches]

    db_session.bulk_save_objects(models)
    db_session.commit()
