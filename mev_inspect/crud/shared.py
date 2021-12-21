from typing import Type

from mev_inspect.models.base import Base


def delete_by_block_range(
    db_session,
    model_class: Type[Base],
    after_block_number,
    before_block_number,
) -> None:

    (
        db_session.query(model_class)
        .filter(model_class.block_number >= after_block_number)
        .filter(model_class.block_number < before_block_number)
        .delete()
    )

    db_session.commit()
