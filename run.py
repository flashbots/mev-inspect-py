import logging
import os
import signal
import time

from web3 import Web3

from mev_inspect.block import get_latest_block_number
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


if __name__ == "__main__":
    rpc = os.getenv("RPC_URL")
    if rpc is None:
        raise RuntimeError("Missing environment variable RPC_URL")

    logger.info("Starting...")

    killer = GracefulKiller()
    base_provider = get_base_provider(rpc)
    w3 = Web3(base_provider)

    while not killer.kill_now:
        latest_block_number = get_latest_block_number(w3)
        logger.info(f"Latest block: {latest_block_number}")
        time.sleep(5)

    logger.info("Stopping...")
