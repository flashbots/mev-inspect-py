import asyncio
import logging
import os

from aiohttp_retry import ExponentialRetry, RetryClient

from mev_inspect.block import get_latest_block_number
from mev_inspect.concurrency import coro
from mev_inspect.crud.latest_block_update import find_latest_block_update
from mev_inspect.db import get_inspect_session
from mev_inspect.inspector import MEVInspector
from mev_inspect.signal_handler import GracefulKiller

logging.basicConfig(filename="listener.log", filemode="a", level=logging.INFO)
logger = logging.getLogger(__name__)

# lag to make sure the blocks we see are settled
BLOCK_NUMBER_LAG = 5
SLEEP_TIME = 24 * 60 * 60
STRIDE_SIZE = 500000


@coro
async def run():
    rpc = os.getenv("RPC_URL")
    if rpc is None:
        raise RuntimeError("Missing environment variable RPC_URL")

    logger.info("Starting...")

    killer = GracefulKiller()

    inspector = MEVInspector(rpc)
    while not killer.kill_now:
        await asyncio.gather(
            inspect_next_many_blocks(
                inspector,
            ),
            asyncio.sleep(SLEEP_TIME),
        )
    logger.info("Stopping...")


async def inspect_next_many_blocks(
    inspector: MEVInspector,
):
    with get_inspect_session() as inspect_db_session:
        latest_block_number = await get_latest_block_number(inspector.w3)
        last_written_block = find_latest_block_update(inspect_db_session)

    logger.info(f"Latest block: {latest_block_number}")
    logger.info(f"Last written block: {last_written_block}")

    if last_written_block is None:
        # maintain lag if no blocks written yet
        last_written_block = latest_block_number - BLOCK_NUMBER_LAG - 1

    for start_block_number in range(
        last_written_block + 1, latest_block_number, STRIDE_SIZE
    ):
        end_block_number = start_block_number + STRIDE_SIZE
        end_block_number = (
            end_block_number
            if end_block_number <= latest_block_number
            else latest_block_number
        )
        logger.info(
            f"Inpecting blocks started: {start_block_number} to {end_block_number}"
        )
        with get_inspect_session() as inspect_db_session:
            await inspector.inspect_many_blocks(
                inspect_db_session=inspect_db_session,
                trace_db_session=None,
                after_block=start_block_number,
                before_block=end_block_number,
            )
        logger.info(
            f"Inpecting blocks ended: {start_block_number} to {end_block_number}"
        )


async def ping_healthcheck_url(url):
    retry_options = ExponentialRetry(attempts=3)

    async with RetryClient(
        raise_for_status=False, retry_options=retry_options
    ) as client:
        async with client.get(url) as _response:
            pass


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logger.error(e)
