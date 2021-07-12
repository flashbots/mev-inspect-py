from typing import List, Optional

from pydantic import BaseModel


class Block(BaseModel):
    block_number: int
    calls: List[dict]
    data: dict
    logs: List[dict]
    receipts: dict
    transaction_hashes: List[str]
