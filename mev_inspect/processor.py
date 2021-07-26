from typing import Dict, List, Optional

from mev_inspect.abi import get_abi
from mev_inspect.decode import ABIDecoder
from mev_inspect.schemas.blocks import Block, Trace, TraceType
from mev_inspect.schemas.classifications import (
    Classification,
    ClassifiedTrace,
    DecodeSpec,
)


class Processor:
    def __init__(self, decode_specs: List[DecodeSpec]) -> None:
        # TODO - index by contract_addresses for speed
        self._decode_specs = decode_specs
        self._decoders_by_abi_name: Dict[str, ABIDecoder] = {}

        for spec in self._decode_specs:
            abi = get_abi(spec.abi_name)

            if abi is None:
                raise ValueError(f"No ABI found for {spec.abi_name}")

            decoder = ABIDecoder(abi)
            self._decoders_by_abi_name[spec.abi_name] = decoder

    def process(
        self,
        block: Block,
    ) -> List[ClassifiedTrace]:
        return [
            self._classify(trace)
            for trace in block.traces
            if trace.type != TraceType.reward
        ]

    def _classify(self, trace: Trace) -> ClassifiedTrace:
        if trace.type == TraceType.call:
            classified_trace = self._classify_call(trace)
            if classified_trace is not None:
                return classified_trace

        return self._build_unknown_classified_trace(trace)

    def _classify_call(self, trace) -> Optional[ClassifiedTrace]:
        to_address = trace.action["to"]

        for spec in self._decode_specs:
            if spec.valid_contract_addresses is not None:
                if to_address is None:
                    continue

                if to_address not in spec.valid_contract_addresses:
                    continue

            decoder = self._decoders_by_abi_name[spec.abi_name]
            call_data = decoder.decode(trace.action["input"])

            if call_data is not None:
                return ClassifiedTrace(
                    transaction_hash=trace.transaction_hash,
                    block_number=trace.block_number,
                    trace_type=trace.type,
                    trace_address=trace.trace_address,
                    classification=Classification.unknown,
                    protocol=spec.protocol,
                    function_name=call_data.function_name,
                    function_signature=call_data.function_signature,
                    intputs=call_data.inputs,
                )

        return None

    @staticmethod
    def _build_unknown_classified_trace(trace):
        return ClassifiedTrace(
            transaction_hash=trace.transaction_hash,
            block_number=trace.block_number,
            trace_type=trace.type,
            trace_address=trace.trace_address,
            classification=Classification.unknown,
            protocol=None,
            function_name=None,
            function_signature=None,
            intputs=None,
        )
