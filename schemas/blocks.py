import json
from enum import Enum
from typing import Dict, List, Optional

from hexbytes import HexBytes
from pydantic import BaseModel
from web3.datastructures import AttributeDict

from .utils import CamelModel


class BlockCallType(Enum):
    call = "call"
    create = "create"
    delegate_call = "delegateCall"
    reward = "reward"
    suicide = "suicide"


class BlockCall(CamelModel):
    action: dict
    block_hash: str
    block_number: int
    result: Optional[dict]
    subtraces: int
    trace_address: List[int]
    transaction_hash: Optional[str]
    transaction_position: Optional[int]
    type: BlockCallType
    error: Optional[str]


class Block(BaseModel):
    block_number: int
    calls: List[BlockCall]
    data: dict
    logs: List[dict]
    receipts: dict
    transaction_hashes: List[str]
    txs_gas_data: Dict[str, dict]

    class Config:
        json_encoders = {
            AttributeDict: dict,
            HexBytes: lambda h: h.hex(),
        }

    def get_filtered_calls(self, hash: str) -> List[BlockCall]:
        return [
            call for call in self.calls
            if call.transaction_hash == hash
        ]
