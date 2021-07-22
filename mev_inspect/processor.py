from typing import List

from mev_inspect.inspectors import Inspector
from mev_inspect.schemas.blocks import Block, NestedTrace, TraceType
from mev_inspect.schemas.classifications import (
    Classification,
    UnknownClassification,
)
from mev_inspect.traces import as_nested_traces


class Processor:
    def __init__(self, inspectors: List[Inspector]) -> None:
        self._inspectors = inspectors

    def get_transaction_evaluations(
        self,
        block: Block,
    ) -> List[Classification]:
        transaction_traces = (
            trace for trace in block.traces if trace.type != TraceType.reward
        )

        return [
            self._run_inspectors(nested_trace)
            for nested_trace in as_nested_traces(transaction_traces)
        ]

    def _run_inspectors(self, nested_trace: NestedTrace) -> Classification:
        for inspector in self._inspectors:
            classification = inspector.inspect(nested_trace)

            if classification is not None:
                return classification

        internal_classifications = [
            self._run_inspectors(subtrace) for subtrace in nested_trace.subtraces
        ]

        return UnknownClassification(
            trace=nested_trace.trace,
            internal_classifications=internal_classifications,
        )
