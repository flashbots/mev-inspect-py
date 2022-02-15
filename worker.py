import logging
import os
import sys

import dramatiq

from mev_inspect.queue.broker import connect_broker
from mev_inspect.queue.middleware import (
    AsyncMiddleware,
    DbMiddleware,
    InspectorMiddleware,
)
from mev_inspect.queue.tasks import (
    BACKFILL_INSPECT_MANY_BLOCKS_PRIORITY,
    LIVE_EXPORT_BLOCK_PRIORITY,
    export_block_task,
    inspect_many_blocks_task,
)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

broker = connect_broker()
broker.add_middleware(DbMiddleware())
broker.add_middleware(AsyncMiddleware())
broker.add_middleware(InspectorMiddleware(os.environ["RPC_URL"]))
dramatiq.set_broker(broker)

dramatiq.actor(inspect_many_blocks_task, priority=BACKFILL_INSPECT_MANY_BLOCKS_PRIORITY)
dramatiq.actor(export_block_task, priority=LIVE_EXPORT_BLOCK_PRIORITY)
