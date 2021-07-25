from typing import List

from mev_inspect.schemas.blocks import Block, TraceType
from mev_inspect.schemas.classifications import (
    Classification,
    ClassificationType,
)


class Processor:
    def __init__(self) -> None:
        pass

    def process(
        self,
        block: Block,
    ) -> List[Classification]:
        return [
            Classification(
                transaction_hash=trace.transaction_hash,
                block_number=trace.block_number,
                trace_type=trace.type,
                trace_address=trace.trace_address,
                classification_type=ClassificationType.unknown,
            )
            for trace in block.traces
            if trace.type != TraceType.reward
        ]
