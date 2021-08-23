from typing import List

from pydantic import BaseModel

from .classified_traces import Classification, ClassifiedTrace, Protocol


class ERC20Transfer(BaseModel):
    transaction_hash: str
    trace_address: List[int]
    from_address: str
    to_address: str
    amount: int
    token_address: str

    @classmethod
    def from_trace(cls, trace: ClassifiedTrace) -> "ERC20Transfer":
        if trace.classification != Classification.transfer or trace.inputs is None:
            raise ValueError("Invalid transfer")

        if trace.protocol == Protocol.weth:
            return cls(
                transaction_hash=trace.transaction_hash,
                trace_address=trace.trace_address,
                amount=trace.inputs["wad"],
                to_address=trace.inputs["dst"],
                from_address=trace.from_address,
                token_address=trace.to_address,
            )
        else:
            return cls(
                transaction_hash=trace.transaction_hash,
                trace_address=trace.trace_address,
                amount=trace.inputs["amount"],
                to_address=trace.inputs["recipient"],
                from_address=trace.inputs.get("sender", trace.from_address),
                token_address=trace.to_address,
            )
