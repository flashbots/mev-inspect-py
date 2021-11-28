from typing import List

from sqlalchemy.dialects.postgresql import insert

from mev_inspect.models.prices import PriceModel
from mev_inspect.schemas.prices import Price


def write_prices(db_session, prices: List[Price]) -> None:
    insert_statement = (
        insert(PriceModel.__table__)
        .values([price.dict() for price in prices])
        .on_conflict_do_nothing()
    )

    db_session.execute(insert_statement)
    db_session.commit()
