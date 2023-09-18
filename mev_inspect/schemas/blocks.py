from typing import List

from pydantic import validator

from mev_inspect.utils import hex_to_int

from .receipts import Receipt
from .traces import Trace
from .utils import CamelModel, Web3Model


class CallResult(CamelModel):
    gas_used: int

    @validator("gas_used", pre=True)
    def maybe_hex_to_int(cls, v):
        if isinstance(v, str):
            return hex_to_int(v)
        return v


class CallAction(Web3Model):
    to: str
    from_: str
    input: str
    value: int
    gas: int

    @validator("value", "gas", pre=True)
    def maybe_hex_to_int(cls, v):
        if isinstance(v, str):
            return hex_to_int(v)
        return v

    class Config:
        fields = {"from_": "from"}


class Block(Web3Model):
    block_number: int
    block_timestamp: int
    miner: str
    base_fee_per_gas: int
    traces: List[Trace]
    receipts: List[Receipt]

    def get_filtered_traces(self, hash: str) -> List[Trace]:
        return [trace for trace in self.traces if trace.transaction_hash == hash]
