import asyncio
import os
from contextlib import contextmanager

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.cli import main as dramatiq_worker
from dramatiq.middleware import Middleware

from mev_inspect.db import get_inspect_sessionmaker, get_trace_sessionmaker
from mev_inspect.inspector import MEVInspector

InspectSession = get_inspect_sessionmaker()
TraceSession = get_trace_sessionmaker()


class AsyncMiddleware(Middleware):
    def before_process_message(
        self, _broker, message
    ):  # pylint: disable=unused-argument
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def after_process_message(
        self, _broker, message, *, result=None, exception=None
    ):  # pylint: disable=unused-argument
        self.loop.close()


rpc = os.environ["RPC_URL"]
broker = RedisBroker(host="redis-master", password=os.environ["REDIS_PASSWORD"])
broker.add_middleware(AsyncMiddleware())
dramatiq.set_broker(broker)


@contextmanager
def session_scope(Session=None):
    if Session is None:
        return None

    with Session() as session:
        yield session


@dramatiq.actor
def inspect_many_blocks_task(
    after_block: int,
    before_block: int,
):
    with session_scope(InspectSession) as inspect_db_session:
        with session_scope(TraceSession) as trace_db_session:
            inspector = MEVInspector(
                rpc,
                inspect_db_session,
                trace_db_session,
                max_concurrency=5,
                request_timeout=300,
            )

            asyncio.run(
                inspector.inspect_many_blocks(
                    after_block=after_block, before_block=before_block
                )
            )


if __name__ == "__main__":
    dramatiq_worker(processes=1, threads=1)
