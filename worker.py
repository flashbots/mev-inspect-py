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
    LOW_PRIORITY,
    LOW_PRIORITY_QUEUE,
    export_block_task,
    inspect_many_blocks_task,
)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

broker = connect_broker()
broker.add_middleware(DbMiddleware())
broker.add_middleware(AsyncMiddleware())
broker.add_middleware(InspectorMiddleware(os.environ["RPC_URL"]))
dramatiq.set_broker(broker)

dramatiq.actor(
    inspect_many_blocks_task, queue_name=LOW_PRIORITY_QUEUE, priority=LOW_PRIORITY
)
dramatiq.actor(export_block_task)
