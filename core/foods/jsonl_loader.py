"""
core.foods.jsonl_loader

Loads Food objects from knowledge/foods/*.jsonl. Falls back to the
Python source in core/foods/data/ when the JSONL is missing.
"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Optional

from .._jsonl import read_jsonl
from ..medications.models import EffectDirection, EffectTargetType
from .models import EffectCertainty, EffectModifier, Food, FoodEffect
from .sources import DataSource


REPO_ROOT = Path(__file__).resolve().parents[2]
FOODS_DIR = REPO_ROOT / "knowledge" / "foods"
FOOD_DATA_PACKAGE = "core.foods.data"


def _enum_or(enum_cls, value, default):
    if value is None:
        return default
    if isinstance(value, enum_cls):
        return value
    try:
        return enum_cls(value)
    except (TypeError, ValueError):
        for member in enum_cls:
            if member.value == value:
                return member
        return default


def _row_to_data_source(row: dict) -> DataSource:
    return DataSource(
        url=row.get("url", ""),
        title=row.get("title", ""),
        source_type=row.get("source_type", "research"),
        access_date=row.get("access_date"),
        doi=row.get("doi"),
    )


def _row_to_effect_modifier(row: dict) -> EffectModifier:
    src = row.get("source")
    return EffectModifier(
        factor=row.get("factor", ""),
        description=row.get("description", ""),
        impact=row.get("impact"),
        direction=row.get("direction", "enhances"),
        source=_row_to_data_source(src) if isinstance(src, dict) else None,
    )


def _row_to_food_effect(row: dict) -> FoodEffect:
    return FoodEffect(
        target_type=_enum_or(EffectTargetType, row.get("target_type"), EffectTargetType.BIOMARKER),
        target_name=row.get("target_name", ""),
        direction=_enum_or(EffectDirection, row.get("direction"), EffectDirection.NONE),
        mechanism=row.get("mechanism", ""),
        sources=[_row_to_data_source(s) for s in (row.get("sources") or [])],
        certainty=_enum_or(EffectCertainty, row.get("certainty"), EffectCertainty.ESTABLISHED),
        per_serving=bool(row.get("per_serving", True)),
        modifiers=[_row_to_effect_modifier(m) for m in (row.get("modifiers") or [])],
        notes=row.get("notes"),
    )


def _row_to_food(row: dict) -> Food:
    return Food(
        name=row.get("name", ""),
        name_de=row.get("name_de", ""),
        nutrition_data=row.get("nutrition_data") or row.get("nutrition_per_100g") or {},
        category=row.get("category"),
        effects=[_row_to_food_effect(e) for e in (row.get("effects") or [])],
        nutrition_sources=[_row_to_data_source(s) for s in (row.get("nutrition_sources") or [])],
        custom_portions=row.get("custom_portions") or {},
        weight=row.get("weight", 0.0) or 0.0,
    )


def load_foods_from_jsonl(directory: Path = None) -> Dict[str, Food]:
    """Load all foods from JSONL files in knowledge/foods/.

    Returns dict keyed by Food.name (lowercased). If the same food name
    appears in multiple files, the last one wins.
    """
    directory = directory or FOODS_DIR
    out: Dict[str, Food] = {}
    if not directory.exists():
        return out
    for path in sorted(directory.glob("*.jsonl")):
        for row in read_jsonl(path):
            food = _row_to_food(row)
            if food.name:
                out[food.name.lower()] = food
    return out


def load_foods_from_python() -> Dict[str, Food]:
    """Load foods by walking core.foods.data and the legacy package."""
    out: Dict[str, Food] = {}
    try:
        main_pkg = importlib.import_module(FOOD_DATA_PACKAGE)
        for _, modname, _ in pkgutil.walk_packages(main_pkg.__path__, main_pkg.__name__ + "."):
            try:
                module = importlib.import_module(modname)
            except Exception:
                continue
            _harvest_module(module, out)
    except ImportError:
        pass
    return out


def _harvest_module(module, out: Dict[str, Food]) -> None:
    for attr_name in dir(module):
        if not attr_name.startswith("create_"):
            continue
        func = getattr(module, attr_name, None)
        if not callable(func):
            continue
        try:
            food = func()
        except Exception:
            continue
        if isinstance(food, Food):
            out[food.name.lower()] = food


def load_foods(source: str = "auto", directory: Path = None) -> Dict[str, Food]:
    """Load foods, preferring JSONL when available.

    source: 'auto' (default) -> JSONL if the directory exists, else Python
            'jsonl'           -> JSONL only
            'python'          -> Python only
    """
    if source == "python":
        return load_foods_from_python()
    if source == "jsonl":
        return load_foods_from_jsonl(directory)
    if FOODS_DIR.exists() and any(FOODS_DIR.glob("*.jsonl")):
        return load_foods_from_jsonl(directory)
    return load_foods_from_python()
