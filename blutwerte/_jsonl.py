"""
blutwerte._jsonl

Generic, type-driven deserializer for reconstructing dataclass
instances from JSONL rows written by tools/migrate_to_json.py.

Used by the per-entity JSONL loaders in medications/, bloodtests/,
and foods/. Not a public API.
"""

from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar, Union, get_args, get_origin

T = TypeVar("T")


_PRIMITIVES = (str, int, float, bool, bytes)


def _is_optional(tp: Any) -> bool:
    """True if tp is Optional[X]."""
    if tp is type(None):
        return True
    origin = get_origin(tp)
    if origin is Union:
        return type(None) in get_args(tp)
    return False


def _strip_optional(tp: Any) -> Any:
    """Return the non-None type for Optional[X], else tp unchanged."""
    if tp is type(None):
        return Any
    origin = get_origin(tp)
    if origin is Union:
        non_none = [a for a in get_args(tp) if a is not type(None)]
        if len(non_none) == 1:
            return non_none[0]
    return tp


def _is_list(tp: Any) -> bool:
    origin = get_origin(tp)
    if origin is list:
        return True
    if tp is list:
        return True
    return False


def _is_dict(tp: Any) -> bool:
    origin = get_origin(tp)
    if origin is dict:
        return True
    if tp is dict:
        return True
    return False


def _is_tuple(tp: Any) -> bool:
    origin = get_origin(tp)
    if origin is tuple:
        return True
    if tp is tuple:
        return True
    return False


def _list_item_type(tp: Any) -> Any:
    args = get_args(tp)
    return args[0] if args else Any


def _dict_value_type(tp: Any) -> Any:
    args = get_args(tp)
    return args[1] if len(args) >= 2 else Any


def _is_enum(tp: Any) -> bool:
    return isinstance(tp, type) and issubclass(tp, Enum)


def _coerce_primitive(tp: Any, value: Any) -> Any:
    """Coerce a value to a primitive type if tp is a known primitive."""
    if value is None:
        return None
    if tp in (str, int, float, bool):
        if isinstance(value, tp):
            return value
        if tp is bool and isinstance(value, str):
            return value.lower() in ("true", "1", "yes")
        if tp is float and isinstance(value, int):
            return float(value)
        if tp is int and isinstance(value, float) and value.is_integer():
            return int(value)
        try:
            return tp(value)
        except (TypeError, ValueError):
            return value
    return value


def _convert(value: Any, tp: Any) -> Any:
    """Convert a JSON-decoded value to a Python value matching type hint `tp`."""
    if value is None:
        return None
    if tp is Any or tp is None:
        return value
    if tp in _PRIMITIVES:
        return _coerce_primitive(tp, value)
    if _is_optional(tp):
        if value is None:
            return None
        return _convert(value, _strip_optional(tp))
    if _is_list(tp):
        if not isinstance(value, list):
            return value
        item_tp = _list_item_type(tp)
        return [_convert(v, item_tp) for v in value]
    if _is_dict(tp):
        if not isinstance(value, dict):
            return value
        val_tp = _dict_value_type(tp)
        return {k: _convert(v, val_tp) for k, v in value.items()}
    if _is_tuple(tp):
        if not isinstance(value, list):
            return value
        args = get_args(tp)
        if len(args) == 2 and args[1] is Ellipsis:
            return tuple(_convert(v, args[0]) for v in value)
        if args:
            return tuple(_convert(v, t) for v, t in zip(value, args))
        return tuple(value)
    if _is_enum(tp):
        try:
            return tp(value)
        except (TypeError, ValueError):
            for member in tp:
                if member.value == value:
                    return member
            return value
    if is_dataclass(tp):
        return from_dict(tp, value)
    return value


def from_dict(cls: Type[T], data: Optional[Dict[str, Any]]) -> T:
    """Reconstruct a dataclass instance from a dict.

    Unknown keys in `data` are ignored. Missing keys fall back to the
    dataclass's default. None values become None.
    """
    if data is None:
        return None  # type: ignore[return-value]
    if not is_dataclass(cls):
        if isinstance(data, cls):
            return data
        return data  # type: ignore[return-value]
    kwargs: Dict[str, Any] = {}
    for f in fields(cls):
        if f.name not in data:
            continue
        kwargs[f.name] = _convert(data[f.name], f.type)
    return cls(**kwargs)


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    """Yield each non-empty line of a JSONL file as a dict."""
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def load_jsonl_objects(path: Path, cls: Type[T]) -> List[T]:
    """Load a JSONL file into a list of dataclass instances."""
    return [from_dict(cls, row) for row in read_jsonl(path)]
