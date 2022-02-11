import asyncio
import logging
from contextlib import contextmanager

from mev_inspect.s3_export import export_block

from .middleware import DbMiddleware, InspectorMiddleware

logger = logging.getLogger(__name__)


def inspect_many_blocks_task(
    after_block: int,
    before_block: int,
):
    with _session_scope(DbMiddleware.get_inspect_sessionmaker()) as inspect_db_session:
        with _session_scope(DbMiddleware.get_trace_sessionmaker()) as trace_db_session:
            asyncio.run(
                InspectorMiddleware.get_inspector().inspect_many_blocks(
                    inspect_db_session=inspect_db_session,
                    trace_db_session=trace_db_session,
                    after_block=after_block,
                    before_block=before_block,
                )
            )


def export_block_task(block_number: int):
    with _session_scope(DbMiddleware.get_inspect_sessionmaker()) as inspect_db_session:
        export_block(inspect_db_session, block_number)


@contextmanager
def _session_scope(Session=None):
    if Session is None:
        yield None
    else:
        with Session() as session:
            yield session
