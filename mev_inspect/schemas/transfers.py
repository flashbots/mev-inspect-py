from typing import List, TypeVar

from pydantic import BaseModel

from .classified_traces import Classification, ClassifiedTrace, Protocol


class Transfer(BaseModel):
    block_number: int
    transaction_hash: str
    trace_address: List[int]
    from_address: str
    to_address: str
    amount: int


# To preserve the specific Transfer type
TransferGeneric = TypeVar("TransferGeneric", bound="Transfer")


class EthTransfer(Transfer):
    @classmethod
    def from_trace(cls, trace: ClassifiedTrace) -> "EthTransfer":
        return cls(
            block_number=trace.block_number,
            transaction_hash=trace.transaction_hash,
            trace_address=trace.trace_address,
            amount=trace.value,
            to_address=trace.to_address,
            from_address=trace.from_address,
        )


class ERC20Transfer(Transfer):
    token_address: str

    @classmethod
    def from_trace(cls, trace: ClassifiedTrace) -> "ERC20Transfer":
        if trace.classification != Classification.transfer or trace.inputs is None:
            raise ValueError("Invalid transfer")

        if trace.protocol == Protocol.weth:
            return cls(
                block_number=trace.block_number,
                transaction_hash=trace.transaction_hash,
                trace_address=trace.trace_address,
                amount=trace.inputs["wad"],
                to_address=trace.inputs["dst"],
                from_address=trace.from_address,
                token_address=trace.to_address,
            )
        else:
            return cls(
                block_number=trace.block_number,
                transaction_hash=trace.transaction_hash,
                trace_address=trace.trace_address,
                amount=trace.inputs["amount"],
                to_address=trace.inputs["recipient"],
                from_address=trace.inputs.get("sender", trace.from_address),
                token_address=trace.to_address,
            )
