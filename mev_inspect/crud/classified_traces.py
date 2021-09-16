import json
from typing import List

from mev_inspect.models.classified_traces import ClassifiedTraceModel
from mev_inspect.schemas.classified_traces import ClassifiedTrace


def delete_classified_traces_for_block(
    db_session,
    block_number: int,
) -> None:
    (
        db_session.query(ClassifiedTraceModel)
        .filter(ClassifiedTraceModel.block_number == block_number)
        .delete()
    )

    db_session.commit()


def write_classified_traces(
    db_session,
    classified_traces: List[ClassifiedTrace],
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

    db_session.bulk_save_objects(models)
    db_session.commit()
