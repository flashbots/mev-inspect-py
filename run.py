import logging
import os
import signal
import time

from web3 import Web3

from mev_inspect.block import get_latest_block_number
from mev_inspect.crud.latest_block_update import (
    find_latest_block_update,
    update_latest_block,
)
from mev_inspect.db import get_session
from mev_inspect.inspect_block import inspect_block
from mev_inspect.provider import get_base_provider


logging.basicConfig(filename="app.log", level=logging.INFO)
logger = logging.getLogger(__name__)


class GracefulKiller:
    """
    handle sigint / sigterm gracefully
    taken from https://stackoverflow.com/a/31464349
    """

    signal_names = {signal.SIGINT: "SIGINT", signal.SIGTERM: "SIGTERM"}

    def __init__(self):
        self.kill_now = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):  # pylint: disable=unused-argument
        signal_name = self.signal_names[signum]
        logger.info(f"Received {signal_name} signal")
        logger.info("Cleaning up resources. End of process")
        self.kill_now = True


def run():
    rpc = os.getenv("RPC_URL")
    if rpc is None:
        raise RuntimeError("Missing environment variable RPC_URL")

    logger.info("Starting...")

    killer = GracefulKiller()

    db_session = get_session()
    base_provider = get_base_provider(rpc)
    w3 = Web3(base_provider)

    latest_block_number = get_latest_block_number(w3)

    while not killer.kill_now:
        last_written_block = find_latest_block_update(db_session)
        logger.info(f"Latest block: {latest_block_number}")
        logger.info(f"Last written block: {last_written_block}")

        if last_written_block is None or last_written_block < latest_block_number:
            block_number = (
                latest_block_number
                if last_written_block is None
                else last_written_block + 1
            )

            logger.info(f"Writing block: {block_number}")

            inspect_block(
                db_session,
                base_provider,
                w3,
                block_number,
                should_write_classified_traces=False,
                should_cache=False,
            )
            update_latest_block(db_session, block_number)
        else:
            latest_block_number = get_latest_block_number(w3)
            time.sleep(5)

    logger.info("Stopping...")


if __name__ == "__main__":
    run()
