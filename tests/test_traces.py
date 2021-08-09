from mev_inspect.traces import is_child_trace_address


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
