import logging
import time

from mev_inspect.signal_handler import GracefulKiller

logging.basicConfig(filename="loop.log", level=logging.INFO)
logger = logging.getLogger(__name__)


def run():
    logger.info("Starting...")

    killer = GracefulKiller()
    while not killer.kill_now:
        time.sleep(1)

    logger.info("Stopping...")


if __name__ == "__main__":
    run()
