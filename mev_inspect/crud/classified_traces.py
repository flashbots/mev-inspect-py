import json
from typing import List

from mev_inspect.models.classified_traces import ClassifiedTraceModel
from mev_inspect.schemas.classified_traces import ClassifiedTrace


def write_classified_traces(
    db_connection,
    classified_traces: List[ClassifiedTrace],
) -> None:
    models = [
        ClassifiedTraceModel(**json.loads(trace.json())) for trace in classified_traces
    ]

    db_connection.bulk_save_objects(models)
    db_connection.commit()
