from web3 import AsyncHTTPProvider, Web3

from mev_inspect.retry import http_retry_with_backoff_request_middleware


def get_base_provider(rpc: str, request_timeout: int = 500) -> Web3.AsyncHTTPProvider:
    base_provider = AsyncHTTPProvider(rpc, request_kwargs={"timeout": request_timeout})
    base_provider.middlewares += (http_retry_with_backoff_request_middleware,)
    return base_provider
