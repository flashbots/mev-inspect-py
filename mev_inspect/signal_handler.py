import logging
import signal

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
