"""
Modified asynchronous geth_poa_middleware which mirrors functionality of
https://github.com/ethereum/web3.py/blob/master/web3/middleware/geth_poa.py
"""
from typing import (
    Any,
    Callable,
)

from hexbytes import (
    HexBytes,
)

from eth_utils.curried import (
    apply_formatter_if,
    apply_formatters_to_dict,
    apply_key_map,
    is_null,
)
from eth_utils.toolz import (
    complement,
    compose,
    assoc,
)

from web3._utils.rpc_abi import (
    RPC,
)

from web3.types import (
    Formatters,
    RPCEndpoint,
    RPCResponse,
)

from web3 import Web3  # noqa: F401


async def get_geth_poa_middleware(
    make_request: Callable[[RPCEndpoint, Any], RPCResponse],
    request_formatters: Formatters = {},
    result_formatters: Formatters = {},
    error_formatters: Formatters = {},
) -> RPCResponse:
    async def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        if method in request_formatters:
            formatter = request_formatters[method]
            formatted_params = formatter(params)
            response = await make_request(method, formatted_params)
        else:
            response = await make_request(method, params)

        if "result" in response and method in result_formatters:
            formatter = result_formatters[method]
            formatted_response = assoc(
                response,
                "result",
                formatter(response["result"]),
            )
            return formatted_response
        elif "error" in response and method in error_formatters:
            formatter = error_formatters[method]
            formatted_response = assoc(
                response,
                "error",
                formatter(response["error"]),
            )
            return formatted_response
        else:
            return response

    return middleware


is_not_null = complement(is_null)

remap_geth_poa_fields = apply_key_map(
    {
        "extraData": "proofOfAuthorityData",
    }
)

pythonic_geth_poa = apply_formatters_to_dict(
    {
        "proofOfAuthorityData": HexBytes,
    }
)

geth_poa_cleanup = compose(pythonic_geth_poa, remap_geth_poa_fields)


async def geth_poa_middleware(make_request: Callable[[RPCEndpoint, Any], Any], _: Web3):
    return await get_geth_poa_middleware(
        make_request=make_request,
        request_formatters={},
        result_formatters={
            RPC.eth_getBlockByHash: apply_formatter_if(is_not_null, geth_poa_cleanup),
            RPC.eth_getBlockByNumber: apply_formatter_if(is_not_null, geth_poa_cleanup),
        },
        error_formatters={},
    )
