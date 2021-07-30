import json
from pathlib import Path
from typing import Optional

from pydantic import parse_obj_as

from mev_inspect.schemas import ABI
from mev_inspect.schemas.classified_traces import Protocol


THIS_FILE_DIRECTORY = Path(__file__).parents[0]
ABI_DIRECTORY_PATH = THIS_FILE_DIRECTORY / "abis"


def get_abi(abi_name: str, protocol: Optional[Protocol]) -> Optional[ABI]:
    abi_filename = f"{abi_name}.json"
    abi_path = (
        ABI_DIRECTORY_PATH / abi_filename
        if protocol is None
        else ABI_DIRECTORY_PATH / protocol.value / abi_filename
    )

    if abi_path.is_file():
        with abi_path.open() as abi_file:
            abi_json = json.load(abi_file)
            return parse_obj_as(ABI, abi_json)

    return None
