from abc import ABC, abstractmethod
from typing import Optional

from mev_inspect.schemas.blocks import NestedTrace
from mev_inspect.schemas.classifications import Classification


class Inspector(ABC):
    @abstractmethod
    def inspect(self, nested_trace: NestedTrace) -> Optional[Classification]:
        pass
