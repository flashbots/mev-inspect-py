import logging
import signal
import time


logging.basicConfig(filename="app.log", level=logging.DEBUG)
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
    logger.info("Starting...")
    killer = GracefulKiller()

    while not killer.kill_now:
        logger.info("Running...")
        time.sleep(5)

    logger.info("Stopping...")
