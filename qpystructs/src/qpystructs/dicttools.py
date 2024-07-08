#!/usr/bin/env python
from __future__ import annotations

from typing import Any, Callable
from typing import Dict
from typing import List

__all__ = ["deep_update", "merge_dicts", "pick_value", "pick_by_keys", "pick_values", "merge_dicts"]


def deep_update(base_dict: dict, update_dict: dict):
    """
    Works like update, but recursively on each level
    """
    res = base_dict.copy()
    for key, val in update_dict.items():
        c = isinstance(res.get(key), dict) and isinstance(val, dict)
        res[key] = deep_update(res[key], val) if c else val
    return res


def merge_dicts(*dicts: dict) -> dict:
    """依次合并多个字典。merge multiple dict one by one.

    Examples::

        offset_limit_schema = {'offset': Validation(...), 'limit': Validation(...)}
        ...
        schema = merge_dicts(offset_limit_schema, from_to_schema, payment_schema)
    """
    dict_merged = {}
    for d in dicts:
        dict_merged.update(d)
    return dict_merged


def pick_by_keys(base: dict[Any, Any], *keys: str) -> dict[Any, Any]:
    result = {}
    for key in keys:
        if key in base and base[key] is not None:
            result[key] = base[key]
    return result


def pick_values(base: dict[Any, Any], *keys: str) -> list[Any]:
    result = []
    for key in keys:
        if key in base and base[key] is not None:
            result.append(base[key])
    return result


def pick_value(base: dict[Any, Any], *keys: str) -> Any | None:
    for key in keys:
        if key in base and base[key] is not None:
            return base[key]
    return None


# def map_list_keys(objs: List, func: Callable):
#     new_objs = []
#     for obj in objs:
#         if isinstance(obj, dict):
#             new_objs.append(map_dict_keys(func, obj))
#         else:
#             new_objs.append(obj)
#     return new_objs


# def map_dict_keys(func, obj: Dict):
#     new_obj = {}
#     for key, value in obj.items():
#         func_key = func(key)
#         if isinstance(value, dict):
#             new_obj[func_key] = func(value)
#         if isinstance(value, list):
#             new_obj[func_key] = map_list_keys(func, value)
#         else:
#             new_obj[func_key] = value
#     return new_obj
