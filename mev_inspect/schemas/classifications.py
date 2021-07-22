from typing import List

from pydantic import BaseModel

from .blocks import Trace


class Classification(BaseModel):
    pass


class UnknownClassification(Classification):
    trace: Trace
    internal_classifications: List[Classification]
