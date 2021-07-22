from typing import Any, Dict

from pydantic import BaseModel


class CallData(BaseModel):
    function_name: str
    function_signature: str
    inputs: Dict[str, Any]
