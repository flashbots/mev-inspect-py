import asyncio
import logging
import random
import sys
from typing import (
    Any,
    Callable,
    Collection,
    Type,
    Coroutine,
)
from asyncio.exceptions import TimeoutError

from requests.exceptions import (
    ConnectionError,
    HTTPError,
    Timeout,
    TooManyRedirects,
)
from web3 import Web3
from web3.middleware.exception_retry_request import check_if_retry_on_failure
from web3.types import (
    RPCEndpoint,
    RPCResponse,
)


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


async def exception_retry_with_backoff_middleware(
    make_request: Callable[[RPCEndpoint, Any], Any],
    web3: Web3,  # pylint: disable=unused-argument
    errors: Collection[Type[BaseException]],
    retries: int = 5,
    backoff_time_seconds: float = 0.1,
) -> Callable[[RPCEndpoint, Any], Coroutine[Any, Any, RPCResponse]]:
    """
    Creates middleware that retries failed HTTP requests. Is a default
    middleware for HTTPProvider.
    """

    async def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:

        if check_if_retry_on_failure(method):
            for i in range(retries):
                try:
                    return await make_request(method, params)
                # https://github.com/python/mypy/issues/5349
                except errors:  # type: ignore
                    logger.error(
                        f"Request for method {method}, block: {int(params[0], 16)}, retrying: {i}/{retries}"
                    )
                    if i < retries - 1:
                        backoff_time = backoff_time_seconds * (
                            random.uniform(5, 10) ** i
                        )
                        await asyncio.sleep(backoff_time)
                        continue

                    else:
                        raise
            return None
        else:
            return await make_request(method, params)

    return middleware


async def http_retry_with_backoff_request_middleware(
    make_request: Callable[[RPCEndpoint, Any], Any], web3: Web3
) -> Callable[[RPCEndpoint, Any], Coroutine[Any, Any, RPCResponse]]:
    return await exception_retry_with_backoff_middleware(
        make_request,
        web3,
        (ConnectionError, HTTPError, Timeout, TooManyRedirects, TimeoutError),
    )
