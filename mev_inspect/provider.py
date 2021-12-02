from web3 import Web3, AsyncHTTPProvider

from mev_inspect.retry import http_retry_with_backoff_request_middleware
from mev_inspect.geth_poa_middleware import geth_poa_middleware


def get_base_provider(
    rpc: str, request_timeout: int = 500, geth: bool = False
) -> Web3.AsyncHTTPProvider:
    base_provider = AsyncHTTPProvider(rpc, request_kwargs={"timeout": request_timeout})
    if geth:
        base_provider.middlewares += (
            geth_poa_middleware,
            http_retry_with_backoff_request_middleware,
        )
    else:
        base_provider.middlewares += (http_retry_with_backoff_request_middleware,)
    return base_provider
