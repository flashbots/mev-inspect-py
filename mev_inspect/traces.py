from typing import List


def is_child_trace_address(
    child_trace_address: List[int],
    parent_trace_address: List[int],
) -> bool:
    parent_trace_length = len(parent_trace_address)

    return (
        len(child_trace_address) > parent_trace_length
        and child_trace_address[:parent_trace_length] == parent_trace_address
    )
