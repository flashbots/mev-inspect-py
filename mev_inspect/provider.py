from web3 import Web3, AsyncHTTPProvider


def get_base_provider(rpc: str, request_timeout: int = 500) -> Web3.AsyncHTTPProvider:
    base_provider = AsyncHTTPProvider(rpc, request_kwargs={"timeout": request_timeout})
    return base_provider
