import json

from hexbytes import HexBytes
from pydantic import BaseModel
from web3.datastructures import AttributeDict


def to_camel(string: str) -> str:
    return "".join(
        word.capitalize() if i > 0 else word for i, word in enumerate(string.split("_"))
    )


def to_original_json_dict(model: BaseModel) -> dict:
    return json.loads(model.json(by_alias=True, exclude_unset=True))


class Web3Model(BaseModel):
    """BaseModel that handles web3's unserializable objects"""

    class Config:
        json_encoders = {
            AttributeDict: dict,
            HexBytes: lambda h: h.hex(),
        }


class CamelModel(BaseModel):
    """BaseModel that translates from snake_case to camelCase"""

    class Config(Web3Model.Config):
        alias_generator = to_camel
        allow_population_by_field_name = True
