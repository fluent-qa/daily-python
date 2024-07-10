from __future__ import annotations

from typing import TypeVar, Any, Type
from typing import Union

import re

import inflection
import pydantic

from pydantic import BaseModel
from pydantic import ConfigDict

T = TypeVar("T")  # Declare type variable


def to_camel(s: str) -> str:
    s = re.sub("_(url)$", lambda m: f"_{m.group(1).upper()}", s)
    return inflection.camelize(s, uppercase_first_letter=False)


class CamelModel(BaseModel):
    def __init__(self, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        super().__init__(**kwargs)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        alias_generator=to_camel,
        populate_by_name=True,
        use_enum_values=True,
    )

    def to_json(self, by_alias=True):
        return self.model_dump_json(by_alias=by_alias, exclude_none=True)

    def to_dict(self, by_alias=True):
        return self.dict(by_alias=by_alias, exclude_none=True)


class GenericDataModel(CamelModel, BaseModel):
    pass


class BaseDataModel(GenericDataModel):
    pass


def parse_as(
        json_or_dict: str | dict, to_type: Type[GenericDataModel, BaseDataModel, BaseModel]
) -> Union[GenericDataModel, BaseDataModel, BaseModel, Any]:
    if isinstance(json_or_dict, str):
        return to_type.parse_raw(json_or_dict)
    else:
        return to_type.parse_obj(json_or_dict)


def to_json(obj: Union[GenericDataModel, BaseDataModel, BaseModel]) -> str:
    if isinstance(obj, GenericDataModel) or isinstance(obj, BaseDataModel):
        return obj.to_json()
    else:
        return obj.model_dump_json(by_alias=True, exclude_none=True)
