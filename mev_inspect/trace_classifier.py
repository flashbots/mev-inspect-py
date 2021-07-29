from typing import Dict, List, Optional

from mev_inspect.abi import get_abi
from mev_inspect.decode import ABIDecoder
from mev_inspect.schemas.blocks import CallAction, CallResult, Trace, TraceType
from mev_inspect.schemas.classified_traces import (
    Classification,
    ClassifiedTrace,
    ClassifierSpec,
)


class TraceClassifier:
    def __init__(self, classifier_specs: List[ClassifierSpec]) -> None:
        # TODO - index by contract_addresses for speed
        self._classifier_specs = classifier_specs
        self._decoders_by_abi_name: Dict[str, ABIDecoder] = {}

        for spec in self._classifier_specs:
            abi = get_abi(spec.abi_name)

            if abi is None:
                raise ValueError(f"No ABI found for {spec.abi_name}")

            decoder = ABIDecoder(abi)
            self._decoders_by_abi_name[spec.abi_name] = decoder

    def classify(
        self,
        traces: List[Trace],
    ) -> List[ClassifiedTrace]:
        return [
            self._classify_trace(trace)
            for trace in traces
            if trace.type != TraceType.reward
        ]

    def _classify_trace(self, trace: Trace) -> ClassifiedTrace:
        if trace.type == TraceType.call:
            classified_trace = self._classify_call(trace)
            if classified_trace is not None:
                return classified_trace

        return ClassifiedTrace(
            **trace.dict(),
            trace_type=trace.type,
            classification=Classification.unknown,
        )

    def _classify_call(self, trace) -> Optional[ClassifiedTrace]:
        action = CallAction(**trace.action)
        result = CallResult(**trace.result) if trace.result is not None else None

        for spec in self._classifier_specs:
            if spec.valid_contract_addresses is not None:
                if action.to not in spec.valid_contract_addresses:
                    continue

            decoder = self._decoders_by_abi_name[spec.abi_name]
            call_data = decoder.decode(action.input)

            if call_data is not None:
                signature = call_data.function_signature
                classification = spec.classifications.get(
                    signature, Classification.unknown
                )

                return ClassifiedTrace(
                    **trace.dict(),
                    trace_type=trace.type,
                    classification=classification,
                    protocol=spec.protocol,
                    abi_name=spec.abi_name,
                    function_name=call_data.function_name,
                    function_signature=signature,
                    inputs=call_data.inputs,
                    to_address=action.to,
                    from_address=action.from_,
                    value=action.value,
                    gas=action.gas,
                    gas_used=result.gas_used if result is not None else None,
                )

        return ClassifiedTrace(
            **trace.dict(),
            trace_type=trace.type,
            classification=Classification.unknown,
            to_address=action.to,
            from_address=action.from_,
            value=action.value,
            gas=action.gas,
            gas_used=result.gas_used if result is not None else None,
        )
