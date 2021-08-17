from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .blocks import TraceType


class Classification(Enum):
    unknown = "unknown"
    swap = "swap"
    burn = "burn"
    transfer = "transfer"
    liquidate = "liquidate"


class Protocol(Enum):
    uniswap_v2 = "uniswap_v2"
    uniswap_v3 = "uniswap_v3"
    sushiswap = "sushiswap"
    aave = "aave"
    weth = "weth"
    curve = "curve"


class ClassifiedTrace(BaseModel):
    transaction_hash: str
    block_number: int
    trace_type: TraceType
    trace_address: List[int]
    classification: Classification

    class Config:
        json_encoders = {
            # a little lazy but fine for now
            # this is used for bytes value inputs
            bytes: lambda b: b.hex(),
        }


class ClassifiedCall(ClassifiedTrace):
    to_address: str
    from_address: str
    gas: int
    value: int
    gas_used: Optional[int]


class ClassifiedCallData(ClassifiedCall):
    protocol: Optional[Protocol]
    function_name: str
    function_signature: str
    inputs: Dict[str, Any]
    abi_name: str


class ClassifierSpec(BaseModel):
    abi_name: str
    protocol: Optional[Protocol] = None
    valid_contract_addresses: Optional[List[str]] = None
    classifications: Dict[str, Classification] = {}
