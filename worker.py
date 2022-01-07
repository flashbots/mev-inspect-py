import asyncio
import logging
import os
import sys
import threading
from contextlib import contextmanager

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.cli import main as dramatiq_worker
from dramatiq.middleware import Middleware

from mev_inspect.db import get_inspect_sessionmaker, get_trace_sessionmaker
from mev_inspect.inspector import MEVInspector

InspectSession = get_inspect_sessionmaker()
TraceSession = get_trace_sessionmaker()

thread_local = threading.local()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


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


class InspectorMiddleware(Middleware):
    def before_process_message(
        self, _broker, worker
    ):  # pylint: disable=unused-argument
        rpc = os.environ["RPC_URL"]

        if not hasattr(thread_local, "inspector"):
            logger.info("Building inspector")
            thread_local.inspector = MEVInspector(
                rpc,
                max_concurrency=5,
                request_timeout=300,
            )
        else:
            logger.info("Inspector already exists")


broker = RedisBroker(host="redis-master", password=os.environ["REDIS_PASSWORD"])
broker.add_middleware(AsyncMiddleware())
broker.add_middleware(InspectorMiddleware())
dramatiq.set_broker(broker)


@contextmanager
def session_scope(Session=None):
    if Session is None:
        yield None
    else:
        with Session() as session:
            yield session


@dramatiq.actor
def inspect_many_blocks_task(
    after_block: int,
    before_block: int,
):
    with session_scope(InspectSession) as inspect_db_session:
        with session_scope(TraceSession) as trace_db_session:
            asyncio.run(
                thread_local.inspector.inspect_many_blocks(
                    inspect_db_session=inspect_db_session,
                    trace_db_session=trace_db_session,
                    after_block=after_block,
                    before_block=before_block,
                )
            )


if __name__ == "__main__":
    dramatiq_worker(processes=1, threads=1)
