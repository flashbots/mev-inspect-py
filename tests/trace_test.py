import unittest
from typing import List

from mev_inspect.schemas import Trace, TraceType, NestedTrace
from mev_inspect.traces import as_nested_traces


DEFAULT_BLOCK_NUMBER = 123


class TestTraces(unittest.TestCase):
    def test_nested_traces(self):
        trace_addresses = [
            [0, 2],
            [],
            [2],
            [0],
            [0, 0],
            [0, 1],
            [1],
            [1, 0],
            [0, 1, 0],
        ]

        traces = [build_trace_at_address(address) for address in trace_addresses]

        nested_traces = as_nested_traces(traces)

        assert len(nested_traces) == 1
        root_trace = nested_traces[0]

        assert_trace_address(root_trace, [])
        assert len(root_trace.subtraces) == 3

        [trace_0, trace_1, trace_2] = root_trace.subtraces

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


def build_trace_at_address(
    trace_address: List[int],
) -> Trace:
    return Trace(
        # real values
        trace_address=trace_address,
        # placeholders
        transaction_hash="",
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
