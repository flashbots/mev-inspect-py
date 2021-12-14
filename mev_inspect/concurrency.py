import asyncio
import signal
from functools import wraps


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()

        def cancel_task_callback():
            for task in asyncio.all_tasks():
                task.cancel()

        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, cancel_task_callback)
        try:
            loop.run_until_complete(f(*args, **kwargs))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())

    return wrapper
