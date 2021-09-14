from web3 import Web3

from mev_inspect.retry import http_retry_with_backoff_request_middleware


def get_base_provider(rpc: str) -> Web3.HTTPProvider:
    base_provider = Web3.HTTPProvider(rpc)
    base_provider.middlewares.remove("http_retry_request")
    base_provider.middlewares.add(
        http_retry_with_backoff_request_middleware,
        "http_retry_with_backoff",
    )

    return base_provider
