"""
core.activities.jsonl_loader

Loads Activity objects from knowledge/activities/activities.jsonl.
Falls back to the Python source in
core/activities/data/common_activities.py when the JSONL is
missing.
"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Optional

from .._jsonl import read_jsonl
from ..medications.models import EffectDirection, EffectTargetType
from .models import Activity, ActivityCategory, ActivityEffect, IntensityLevel
from core.foods.sources import DataSource


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSONL = REPO_ROOT / "knowledge" / "activities" / "activities.jsonl"


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


def _row_to_data_source(row: Optional[dict]) -> Optional[DataSource]:
    if not row:
        return None
    return DataSource(
        url=row.get("url", ""),
        title=row.get("title", ""),
        source_type=row.get("source_type", "research"),
        access_date=row.get("access_date"),
        doi=row.get("doi"),
    )


def _row_to_activity_effect(row: dict) -> ActivityEffect:
    return ActivityEffect(
        target_type=_enum_or(EffectTargetType, row.get("target_type"), EffectTargetType.BIOMARKER),
        target_name=row.get("target_name", ""),
        direction=_enum_or(EffectDirection, row.get("direction"), EffectDirection.NONE),
        mechanism=row.get("mechanism", ""),
        duration_dependent=bool(row.get("duration_dependent", True)),
        intensity_dependent=bool(row.get("intensity_dependent", True)),
        acute_effect=row.get("acute_effect"),
        chronic_effect=row.get("chronic_effect"),
        sources=[s for s in (_row_to_data_source(s) for s in (row.get("sources") or [])) if s is not None],
    )


def _row_to_activity(row: dict) -> Activity:
    intensities: list = []
    for i in (row.get("intensity_range") or []):
        v = _enum_or(IntensityLevel, i, None)
        if v is not None:
            intensities.append(v)
    return Activity(
        name=row.get("name", ""),
        name_de=row.get("name_de", ""),
        category=_enum_or(ActivityCategory, row.get("category"), ActivityCategory.DAILY_LIVING),
        description=row.get("description", ""),
        calories_per_hour=float(row.get("calories_per_hour", 0) or 0),
        effects=[_row_to_activity_effect(e) for e in (row.get("effects") or [])],
        intensity_range=intensities,
        sources=[s for s in (_row_to_data_source(s) for s in (row.get("sources") or [])) if s is not None],
    )


def load_activities_from_jsonl(path: Path = None) -> Dict[str, Activity]:
    """Load activities from the JSONL knowledge file.

    Returns a dict keyed by Activity.name (lowercased).
    """
    path = path or DEFAULT_JSONL
    out: Dict[str, Activity] = {}
    if not path.exists() or path.stat().st_size == 0:
        return out
    for row in read_jsonl(path):
        act = _row_to_activity(row)
        if act.name:
            out[act.name.lower()] = act
    return out


def load_activities_from_python() -> Dict[str, Activity]:
    """Load activities by walking common_activities.py for create_* functions."""
    out: Dict[str, Activity] = {}
    try:
        module = importlib.import_module("core.activities.data.common_activities")
    except Exception:
        return out
    for attr_name in dir(module):
        if not attr_name.startswith("create_") or attr_name == "create_source":
            continue
        func = getattr(module, attr_name, None)
        if not callable(func):
            continue
        try:
            act = func()
        except Exception:
            continue
        if isinstance(act, Activity):
            out[act.name.lower()] = act
    return out


def load_activities(source: str = "auto") -> Dict[str, Activity]:
    """Load activities, preferring JSONL when available."""
    if source == "python":
        return load_activities_from_python()
    if source == "jsonl":
        return load_activities_from_jsonl()
    if DEFAULT_JSONL.exists() and DEFAULT_JSONL.stat().st_size > 0:
        return load_activities_from_jsonl()
    return load_activities_from_python()
