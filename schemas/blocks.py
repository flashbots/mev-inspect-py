import json
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel

from .utils import CamelModel, Web3Model


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


class Block(Web3Model):
    block_number: int
    calls: List[BlockCall]
    data: dict
    logs: List[dict]
    receipts: dict
    transaction_hashes: List[str]
    txs_gas_data: Dict[str, dict]

    def get_filtered_calls(self, hash: str) -> List[BlockCall]:
        return [
            call for call in self.calls
            if call.transaction_hash == hash
        ]
