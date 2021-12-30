from typing import Callable, List

from web3._utils.rpc_abi import RPC
from web3.method import Method, default_root_munger
from web3.types import BlockIdentifier, ParityBlockTrace, RPCEndpoint

trace_block: Method[Callable[[BlockIdentifier], List[ParityBlockTrace]]] = Method(
    RPC.trace_block,
    mungers=[default_root_munger],
)


get_block_receipts: Method[Callable[[BlockIdentifier], List[dict]]] = Method(
    RPCEndpoint("eth_getBlockReceipts"),
    mungers=[default_root_munger],
)
