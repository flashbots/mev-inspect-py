from typing import List

from mev_inspect.schemas.classified_traces import ClassifiedTrace
from mev_inspect.traces import is_child_trace_address, get_child_traces

from .helpers import make_many_unknown_traces


def test_is_child_trace_address():
    assert is_child_trace_address([0], [])
    assert is_child_trace_address([0, 0], [])
    assert is_child_trace_address([0, 0], [0])
    assert is_child_trace_address([100, 1, 10], [100])
    assert is_child_trace_address([100, 1, 10], [100, 1])

    assert not is_child_trace_address([0], [1])
    assert not is_child_trace_address([1], [0])
    assert not is_child_trace_address([1, 0], [0])
    assert not is_child_trace_address([100, 2, 10], [100, 1])


def test_get_child_traces(get_transaction_hashes):
    block_number = 123
    [first_hash, second_hash] = get_transaction_hashes(2)

    traces = []

    first_hash_trace_addresses = [
        [],
        [0],
        [0, 0],
        [1],
        [1, 0],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1],
        [1, 2],
    ]

    second_hash_trace_addresses = [[], [0], [1], [1, 0], [2]]

    traces += make_many_unknown_traces(
        block_number,
        first_hash,
        first_hash_trace_addresses,
    )

    traces += make_many_unknown_traces(
        block_number,
        second_hash,
        second_hash_trace_addresses,
    )

    assert has_expected_child_traces(
        first_hash,
        [],
        traces,
        first_hash_trace_addresses[1:],
    )

    assert has_expected_child_traces(
        first_hash,
        [0],
        traces,
        [
            [0, 0],
        ],
    )

    assert has_expected_child_traces(
        second_hash,
        [2],
        traces,
        [],
    )


def has_expected_child_traces(
    transaction_hash: str,
    parent_trace_address: List[int],
    traces: List[ClassifiedTrace],
    expected_trace_addresses: List[List[int]],
):
    child_traces = get_child_traces(
        transaction_hash,
        parent_trace_address,
        traces,
    )

    distinct_trace_addresses = distinct_lists(expected_trace_addresses)

    if len(child_traces) != len(distinct_trace_addresses):
        return False

    for trace in child_traces:
        if trace.transaction_hash != transaction_hash:
            return False

        if trace.trace_address not in distinct_trace_addresses:
            return False

    return True


def distinct_lists(list_of_lists: List[List[int]]) -> List[List[int]]:
    distinct_so_far = []

    for list_of_values in list_of_lists:
        if list_of_values not in distinct_so_far:
            distinct_so_far.append(list_of_values)

    return distinct_so_far
