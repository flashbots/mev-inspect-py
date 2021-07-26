from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .blocks import TraceType


class ClassificationType(Enum):
    unknown = "unknown"
    swap = "swap"


class Protocol(Enum):
    uniswap_v2 = "uniswap_v2"
    sushiswap = "sushiswap"


class Classification(BaseModel):
    transaction_hash: str
    block_number: int
    trace_type: TraceType
    trace_address: List[int]
    classification_type: ClassificationType
    protocol: Optional[Protocol]
    function_name: Optional[str]
    function_signature: Optional[str]
    inputs: Optional[Dict[str, Any]]


class DecodeSpec(BaseModel):
    abi_name: str
    protocol: Optional[Protocol] = None
    valid_contract_addresses: Optional[List[str]] = None
