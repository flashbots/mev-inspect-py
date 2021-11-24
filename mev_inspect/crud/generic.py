import json
from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import delete

from mev_inspect.models.base import Base


async def delete_by_block_number(db_session, block_number: int, model: Base):
    statement = delete(model).where(model.block_number == block_number)
    await db_session.execute(statement)
    await db_session.commit()
    await db_session.flush()


async def write_models(db_session, models: Sequence[BaseModel], db_model: Base):
    models = [db_model(**json.loads(model.json())) for model in models]
    db_session.add_all(models)
    await db_session.commit()
    await db_session.flush()
