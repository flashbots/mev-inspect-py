from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .blocks import TraceType


class Classification(Enum):
    unknown = "unknown"
    swap = "swap"
    burn = "burn"
    transfer = "transfer"


class Protocol(Enum):
    uniswap_v2 = "uniswap_v2"
    sushiswap = "sushiswap"


class ClassifiedTrace(BaseModel):
    transaction_hash: str
    block_number: int
    trace_type: TraceType
    trace_address: List[int]
    classification: Classification
    protocol: Optional[Protocol]
    function_name: Optional[str]
    function_signature: Optional[str]
    inputs: Optional[Dict[str, Any]]


class DecodeSpec(BaseModel):
    abi_name: str
    protocol: Optional[Protocol] = None
    valid_contract_addresses: Optional[List[str]] = None
    classifications: Dict[str, Classification] = {}
