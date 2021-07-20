from typing import Iterable, List

from mev_inspect.schemas import Trace, NestedTrace


def as_nested_traces(traces: Iterable[Trace]) -> List[NestedTrace]:
    """
    Turns a list of Traces into a a tree of NestedTraces
    using their trace addresses

    Right now this has an exponential (?) runtime because we rescan
    most traces at each level of tree depth

    TODO to write a better implementation if it becomes a bottleneck
    Should be doable in linear time
    """

    nested_traces = []

    parent = None
    children: List[Trace] = []

    sorted_traces = sorted(traces, key=lambda t: t.trace_address)

    for trace in sorted_traces:
        if parent is None:
            parent = trace
            children = []
            continue

        elif not _is_subtrace(trace, parent):
            nested_traces.append(
                NestedTrace(
                    trace=parent,
                    subtraces=as_nested_traces(children),
                )
            )

            parent = trace
            children = []

        else:
            children.append(trace)

    if parent is not None:
        nested_traces.append(
            NestedTrace(
                trace=parent,
                subtraces=as_nested_traces(children),
            )
        )

    return nested_traces


def _is_subtrace(trace: Trace, parent: Trace):
    parent_trace_length = len(parent.trace_address)

    if len(trace.trace_address) > parent_trace_length:
        prefix = trace.trace_address[:parent_trace_length]
        return prefix == parent.trace_address

    return False
