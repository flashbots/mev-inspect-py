import json
from typing import Dict, List, Optional

from hexbytes import HexBytes
from pydantic import BaseModel
from web3.datastructures import AttributeDict


class Block(BaseModel):
    block_number: int
    calls: List[dict]
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

    def get_filtered_calls(self, hash: str) -> List[dict]:
        return [
            call for call in self.calls
            if call["transactionHash"] == hash
        ]
