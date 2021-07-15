import json
from typing import Optional

from pydantic import parse_obj_as

from mev_inspect.config import load_config
from mev_inspect.schemas import ABI


ABI_CONFIG_KEY = "ABI"

config = load_config()


def get_abi(abi_name: str) -> Optional[ABI]:
    if abi_name in config[ABI_CONFIG_KEY]:
        abi_json = json.loads(config[ABI_CONFIG_KEY][abi_name])
        return parse_obj_as(ABI, abi_json)

    return None
