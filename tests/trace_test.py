import unittest
from typing import List

from mev_inspect.schemas import Trace, TraceType, NestedTrace
from mev_inspect.traces import as_nested_traces


DEFAULT_BLOCK_NUMBER = 123


class TestTraces(unittest.TestCase):
    def test_nested_traces(self):
        trace_hash_address_pairs = [
            ("abc", [0, 2]),
            ("abc", []),
            ("abc", [2]),
            ("abc", [0]),
            ("abc", [0, 0]),
            ("abc", [0, 1]),
            ("abc", [1]),
            ("efg", []),
            ("abc", [1, 0]),
            ("abc", [0, 1, 0]),
            ("efg", [0]),
        ]

        traces = [
            build_trace_at_address(hash, address)
            for (hash, address) in trace_hash_address_pairs
        ]

        nested_traces = as_nested_traces(traces)

        assert len(nested_traces) == 2

        abc_trace = nested_traces[0]
        efg_trace = nested_traces[1]

        # abc
        assert abc_trace.trace.transaction_hash == "abc"
        assert_trace_address(abc_trace, [])
        assert len(abc_trace.subtraces) == 3

        [trace_0, trace_1, trace_2] = abc_trace.subtraces

        assert_trace_address(trace_0, [0])
        assert_trace_address(trace_1, [1])
        assert_trace_address(trace_2, [2])

        assert len(trace_0.subtraces) == 3
        assert len(trace_1.subtraces) == 1
        assert len(trace_2.subtraces) == 0

        [trace_0_0, trace_0_1, trace_0_2] = trace_0.subtraces
        [trace_1_0] = trace_1.subtraces

        assert_trace_address(trace_0_0, [0, 0])
        assert_trace_address(trace_0_1, [0, 1])
        assert_trace_address(trace_0_2, [0, 2])
        assert_trace_address(trace_1_0, [1, 0])

        assert len(trace_0_0.subtraces) == 0
        assert len(trace_0_1.subtraces) == 1
        assert len(trace_0_2.subtraces) == 0
        assert len(trace_1_0.subtraces) == 0

        [trace_0_1_0] = trace_0_1.subtraces
        assert_trace_address(trace_0_1_0, [0, 1, 0])
        assert len(trace_0_1_0.subtraces) == 0

        # efg
        assert efg_trace.trace.transaction_hash == "efg"
        assert_trace_address(efg_trace, [])
        assert len(efg_trace.subtraces) == 1

        [efg_subtrace] = efg_trace.subtraces

        assert_trace_address(efg_subtrace, [0])
        assert len(efg_subtrace.subtraces) == 0


def build_trace_at_address(
    transaction_hash: str,
    trace_address: List[int],
) -> Trace:
    return Trace(
        # real values
        transaction_hash=transaction_hash,
        trace_address=trace_address,
        # placeholders
        action={},
        block_hash="",
        block_number=DEFAULT_BLOCK_NUMBER,
        result=None,
        subtraces=0,
        transaction_position=None,
        type=TraceType.call,
        error=None,
    )


def assert_trace_address(nested_trace: NestedTrace, trace_address: List[int]):
    assert nested_trace.trace.trace_address == trace_address
