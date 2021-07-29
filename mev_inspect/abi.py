import json
from pathlib import Path
from typing import Optional

from pydantic import parse_obj_as

from mev_inspect.schemas import ABI


THIS_FILE_DIRECTORY = Path(__file__).parents[0]
ABI_DIRECTORY_PATH = THIS_FILE_DIRECTORY / "abis"


def get_abi(abi_name: str) -> Optional[ABI]:
    abi_path = ABI_DIRECTORY_PATH / f"{abi_name}.json"

    if abi_path.is_file():
        with abi_path.open() as abi_file:
            abi_json = json.load(abi_file)
            return parse_obj_as(ABI, abi_json)

    return None
