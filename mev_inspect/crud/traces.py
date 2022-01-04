import json
from datetime import datetime, timezone
from typing import List

from mev_inspect.db import to_postgres_list, write_as_csv
from mev_inspect.models.traces import ClassifiedTraceModel
from mev_inspect.schemas.traces import ClassifiedTrace

from .shared import delete_by_block_range


def delete_classified_traces_for_blocks(
    db_session,
    after_block_number: int,
    before_block_number: int,
) -> None:
    delete_by_block_range(
        db_session,
        ClassifiedTraceModel,
        after_block_number,
        before_block_number,
    )

    db_session.commit()


def write_classified_traces(
    db_session,
    classified_traces: List[ClassifiedTrace],
) -> None:
    classified_at = datetime.now(timezone.utc)
    items = (
        (
            classified_at,
            trace.transaction_hash,
            trace.block_number,
            trace.classification.value,
            trace.type.value,
            str(trace.protocol),
            trace.abi_name,
            trace.function_name,
            trace.function_signature,
            _inputs_as_json(trace),
            trace.from_address,
            trace.to_address,
            trace.gas,
            trace.value,
            trace.gas_used,
            trace.error,
            to_postgres_list(trace.trace_address),
            trace.transaction_position,
        )
        for trace in classified_traces
    )

    write_as_csv(db_session, "classified_traces", items)


def _inputs_as_json(trace) -> str:
    inputs = json.dumps(json.loads(trace.json(include={"inputs"}))["inputs"])
    inputs_with_array = f"[{inputs}]"
    return inputs_with_array
