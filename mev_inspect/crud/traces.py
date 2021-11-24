import json
from typing import List

from mev_inspect.crud.generic import delete_by_block_number
from mev_inspect.models.traces import ClassifiedTraceModel
from mev_inspect.schemas.traces import ClassifiedTrace


async def delete_classified_traces_for_block(db_session, block_number: int) -> None:
    await delete_by_block_number(
        db_session=db_session, block_number=block_number, model=ClassifiedTraceModel
    )


async def write_classified_traces(
    db_session, classified_traces: List[ClassifiedTrace]
) -> None:
    models = []
    for trace in classified_traces:
        inputs_json = (json.loads(trace.json(include={"inputs"}))["inputs"],)
        models.append(
            ClassifiedTraceModel(
                transaction_hash=trace.transaction_hash,
                block_number=trace.block_number,
                classification=trace.classification.value,
                trace_type=trace.type.value,
                trace_address=trace.trace_address,
                protocol=str(trace.protocol),
                abi_name=trace.abi_name,
                function_name=trace.function_name,
                function_signature=trace.function_signature,
                inputs=inputs_json,
                from_address=trace.from_address,
                to_address=trace.to_address,
                gas=trace.gas,
                value=trace.value,
                gas_used=trace.gas_used,
                error=trace.error,
            )
        )
    db_session.add_all(models)
    await db_session.commit()
    await db_session.flush()
