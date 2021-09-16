import time
from typing import (
    Any,
    Callable,
    Collection,
    Type,
)

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


def exception_retry_with_backoff_middleware(
    make_request: Callable[[RPCEndpoint, Any], RPCResponse],
    web3: Web3,  # pylint: disable=unused-argument
    errors: Collection[Type[BaseException]],
    retries: int = 5,
    backoff_time_seconds: float = 0.1,
) -> Callable[[RPCEndpoint, Any], RPCResponse]:
    """
    Creates middleware that retries failed HTTP requests. Is a default
    middleware for HTTPProvider.
    """

    def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        if check_if_retry_on_failure(method):
            for i in range(retries):
                try:
                    return make_request(method, params)
                # https://github.com/python/mypy/issues/5349
                except errors:  # type: ignore
                    if i < retries - 1:
                        time.sleep(backoff_time_seconds)
                        continue
                    else:
                        raise
            return None
        else:
            return make_request(method, params)

    return middleware


def http_retry_with_backoff_request_middleware(
    make_request: Callable[[RPCEndpoint, Any], Any], web3: Web3
) -> Callable[[RPCEndpoint, Any], Any]:
    return exception_retry_with_backoff_middleware(
        make_request, web3, (ConnectionError, HTTPError, Timeout, TooManyRedirects)
    )
