from typing import list

from pydantic import BaseModel

ETH_TOKEN_ADDRESS = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"

class AtomicMatch(BaseModel):
    block_number: int
    transaction_hash: str
    protocol: str
    from_address: str
    to_address: str
    amount: str
    metadata: List[str]
