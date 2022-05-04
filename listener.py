import asyncio
import logging
import os
from collections import deque
from typing import Dict, Optional

import dramatiq
from aiohttp_retry import ExponentialRetry, RetryClient

from mev_inspect.block import get_latest_block_number
from mev_inspect.concurrency import coro
from mev_inspect.crud.latest_block_update import (
    find_latest_block_update,
    update_latest_block,
)
from mev_inspect.db import get_inspect_session, get_trace_session
from mev_inspect.inspector import MEVInspector
from mev_inspect.provider import get_base_provider
from mev_inspect.queue.broker import connect_broker
from mev_inspect.queue.tasks import (
    HIGH_PRIORITY,
    HIGH_PRIORITY_QUEUE,
    realtime_export_task,
)
from mev_inspect.signal_handler import GracefulKiller

logging.basicConfig(filename="listener.log", filemode="a", level=logging.INFO)
logger = logging.getLogger(__name__)

# lag to make sure the blocks we see are settled
BLOCK_NUMBER_LAG = 5

primary_rpc = os.getenv("RPC_URL")
secondary_rpc = os.getenv("SECONDARY_RPC_URL")

if os.getenv("RPC_URL") is None:
    raise RuntimeError("Missing primary RPC environment variable: RPC_URL. ")

rpc_queue = deque([primary_rpc, secondary_rpc])


@coro
async def run():

    logger.info("Starting...")

    if _get_inspector_params(rpc_queue[0]) is None and secondary_rpc is not None:
        rpc_queue.reverse()

    inspect_params: Optional[Dict] = _get_inspector_params(rpc_queue[0])

    killer = inspect_params["killer"]

    while not killer.kill_now:
        await inspect_next_block(
            inspect_params["inspector"],
            inspect_params["inspect_db_session"],
            inspect_params["trace_db_session"],
            inspect_params["base_provider"],
            inspect_params["healthcheck_url"],
            inspect_params["export_actor"],
        )

    logger.info("Stopping...")


async def inspect_next_block(
    inspector: MEVInspector,
    inspect_db_session,
    trace_db_session,
    base_provider,
    healthcheck_url,
    export_actor,
):

    latest_block_number = await get_latest_block_number(base_provider)
    last_written_block = find_latest_block_update(inspect_db_session)

    logger.info(f"Latest block: {latest_block_number}")
    logger.info(f"Last written block: {last_written_block}")

    if last_written_block is None:
        # maintain lag if no blocks written yet
        last_written_block = latest_block_number - BLOCK_NUMBER_LAG - 1

    if last_written_block < (latest_block_number - BLOCK_NUMBER_LAG):
        block_number = last_written_block + 1

        logger.info(f"Writing block: {block_number}")

        await inspector.inspect_single_block(
            inspect_db_session=inspect_db_session,
            trace_db_session=trace_db_session,
            block=block_number,
        )

        update_latest_block(inspect_db_session, block_number)

        logger.info(f"Sending block {block_number} for export")
        export_actor.send(block_number)

        if healthcheck_url:
            await ping_healthcheck_url(healthcheck_url)
    else:
        await asyncio.sleep(5)


async def ping_healthcheck_url(url):
    retry_options = ExponentialRetry(attempts=3)

    async with RetryClient(
        raise_for_status=False, retry_options=retry_options
    ) as client:
        async with client.get(url) as _response:
            pass


def _get_inspector_params(rpc: str) -> Optional[Dict]:
    try:
        healthcheck_url = os.getenv("LISTENER_HEALTHCHECK_URL")

        broker = connect_broker()
        export_actor = dramatiq.actor(
            realtime_export_task,
            broker=broker,
            queue_name=HIGH_PRIORITY_QUEUE,
            priority=HIGH_PRIORITY,
        )

        killer = GracefulKiller()

        inspect_db_session = get_inspect_session()
        trace_db_session = get_trace_session()

        inspector = MEVInspector(rpc)
        base_provider = get_base_provider(rpc)

        return {
            "inspector": inspector,
            "base_provider": base_provider,
            "killer": killer,
            "healthcheck_url": healthcheck_url,
            "inspect_db_session": inspect_db_session,
            "trace_db_session": trace_db_session,
            "export_actor": export_actor,
        }
    except Exception:
        return None


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logger.error(e)
