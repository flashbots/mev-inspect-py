from enum import Enum
from typing import List

from pydantic import BaseModel

from .blocks import TraceType


class ClassificationType(Enum):
    unknown = "unknown"


class Classification(BaseModel):
    transaction_hash: str
    block_number: int
    trace_type: TraceType
    trace_address: List[int]
    classification_type: ClassificationType
