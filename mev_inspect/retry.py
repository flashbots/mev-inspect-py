import asyncio
import logging
import random
from asyncio.exceptions import TimeoutError
from typing import Any, Callable, Collection, Coroutine, Type

from aiohttp.client_exceptions import (
    ClientConnectorError,
    ClientOSError,
    ClientResponseError,
    ServerDisconnectedError,
    ServerTimeoutError,
)
from requests.exceptions import ConnectionError, HTTPError, Timeout, TooManyRedirects
from web3 import Web3
from web3.middleware.exception_retry_request import whitelist
from web3.types import RPCEndpoint, RPCResponse

request_exceptions = (ConnectionError, HTTPError, Timeout, TooManyRedirects)
aiohttp_exceptions = (
    ClientOSError,
    ClientResponseError,
    ClientConnectorError,
    ServerDisconnectedError,
    ServerTimeoutError,
)

whitelist_additions = ["eth_getBlockReceipts", "trace_block", "eth_feeHistory"]

logger = logging.getLogger(__name__)


def check_if_retry_on_failure(method: RPCEndpoint) -> bool:
    root = method.split("_")[0]
    if root in (whitelist + whitelist_additions):
        return True
    elif method in (whitelist + whitelist_additions):
        return True
    else:
        return False


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
                        f"Request for method {method}, params: {params}, retrying: {i}/{retries}"
                    )
                    if i < (retries - 1):
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
        (
            request_exceptions
            + aiohttp_exceptions
            + (TimeoutError, ConnectionRefusedError)
        ),
    )
