import asyncio
import logging
from threading import local

from dramatiq.middleware import Middleware

from mev_inspect.db import get_inspect_sessionmaker, get_trace_sessionmaker
from mev_inspect.inspector import MEVInspector

logger = logging.getLogger(__name__)


class DbMiddleware(Middleware):
    STATE = local()
    INSPECT_SESSION_STATE_KEY = "InspectSession"
    TRACE_SESSION_STATE_KEY = "TraceSession"

    @classmethod
    def get_inspect_sessionmaker(cls):
        return getattr(cls.STATE, cls.INSPECT_SESSION_STATE_KEY, None)

    @classmethod
    def get_trace_sessionmaker(cls):
        return getattr(cls.STATE, cls.TRACE_SESSION_STATE_KEY, None)

    def before_process_message(self, _broker, message):
        if not hasattr(self.STATE, self.INSPECT_SESSION_STATE_KEY):
            logger.info("Building sessionmakers")
            setattr(
                self.STATE, self.INSPECT_SESSION_STATE_KEY, get_inspect_sessionmaker()
            )
            setattr(self.STATE, self.TRACE_SESSION_STATE_KEY, get_trace_sessionmaker())
        else:
            logger.info("Sessionmakers already set")


class InspectorMiddleware(Middleware):
    STATE = local()
    INSPECT_STATE_KEY = "inspector"

    def __init__(self, rpc_url):
        self._rpc_url = rpc_url

    @classmethod
    def get_inspector(cls):
        return getattr(cls.STATE, cls.INSPECT_STATE_KEY, None)

    def before_process_message(
        self, _broker, worker
    ):  # pylint: disable=unused-argument
        if not hasattr(self.STATE, self.INSPECT_STATE_KEY):
            logger.info("Building inspector")
            inspector = MEVInspector(
                self._rpc_url,
                max_concurrency=5,
                request_timeout=300,
            )

            setattr(self.STATE, self.INSPECT_STATE_KEY, inspector)
        else:
            logger.info("Inspector already exists")


class AsyncMiddleware(Middleware):
    def before_process_message(
        self, _broker, message
    ):  # pylint: disable=unused-argument
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def after_process_message(
        self, _broker, message, *, result=None, exception=None
    ):  # pylint: disable=unused-argument
        if hasattr(self, "loop"):
            self.loop.close()
