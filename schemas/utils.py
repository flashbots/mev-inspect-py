import json

from pydantic import BaseModel


def to_camel(string: str) -> str:
    return ''.join(
        word.capitalize() if i > 0 else word
        for i, word in enumerate(string.split('_'))
    )


class CamelModel(BaseModel):
    """BaseModel that translates from camelCase to snake_case"""

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


def to_original_json_dict(model: BaseModel) -> dict:
    return json.loads(model.json(by_alias=True, exclude_unset=True))
