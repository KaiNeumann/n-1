"""
blutwerte.bloodtests.jsonl_loader

Loads Biomarker objects from knowledge/biomarkers/biomarkers.jsonl.
Falls back to the Python source in blutwerte/bloodtests/biomarkers_db.py
when the JSONL is missing.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Dict, List

from .._jsonl import read_jsonl
from .models import Biomarker, Category, Interpretation, Quote, RangeCondition, ReferenceRange


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSONL = REPO_ROOT / "knowledge" / "biomarkers" / "biomarkers.jsonl"


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


def _row_to_quote(row: dict) -> Quote:
    return Quote(text=row.get("text", ""), source=row.get("source", ""))


def _row_to_range_condition(row: Optional[dict]) -> Optional[RangeCondition]:
    if not row:
        return None
    return RangeCondition(
        gender=row.get("gender"),
        age_min=row.get("age_min"),
        age_max=row.get("age_max"),
        pregnant=row.get("pregnant"),
        notes=row.get("notes", ""),
    )


def _row_to_reference_range(row: dict) -> ReferenceRange:
    return ReferenceRange(
        label=row.get("label", "normal"),
        min_value=row.get("min_value"),
        max_value=row.get("max_value"),
        unit=row.get("unit", ""),
        conditions=_row_to_range_condition(row.get("conditions")),
        range_func=None,  # functions cannot round-trip through JSON
        remarks=[_row_to_quote(q) for q in (row.get("remarks") or [])],
    )


def _row_to_interpretation(row: dict) -> Interpretation:
    if not row:
        row = {}
    return Interpretation(
        low=[_row_to_quote(q) for q in (row.get("low") or [])],
        high=[_row_to_quote(q) for q in (row.get("high") or [])],
        normal=[_row_to_quote(q) for q in (row.get("normal") or [])],
    )


def _row_to_biomarker(row: dict) -> Biomarker:
    categories_raw = row.get("categories", []) or []
    categories: List[Category] = []
    for c in categories_raw:
        if isinstance(c, Category):
            categories.append(c)
        else:
            v = _enum_or(Category, c, None)
            if v is not None:
                categories.append(v)
    ranges: Dict[str, List[ReferenceRange]] = {}
    for unit, rlist in (row.get("ranges") or {}).items():
        ranges[unit] = [_row_to_reference_range(rr) for rr in (rlist or [])]
    return Biomarker(
        name=row.get("name", ""),
        name_de=row.get("name_de", ""),
        synonyms=row.get("synonyms", []) or [],
        categories=categories,
        ranges=ranges,
        description=[_row_to_quote(q) for q in (row.get("description") or [])],
        interpretation=_row_to_interpretation(row.get("interpretation")),
        organs=row.get("organs", []) or [],
        diet=[_row_to_quote(q) for q in (row.get("diet") or [])],
        wikipedia_url=row.get("wikipedia_url", ""),
    )


def load_biomarkers_from_jsonl(path: Path = None) -> Dict[str, Biomarker]:
    """Load biomarkers from the JSONL knowledge file.

    Returns a dict keyed by biomarker name.
    """
    path = path or DEFAULT_JSONL
    out: Dict[str, Biomarker] = {}
    if not path.exists() or path.stat().st_size == 0:
        return out
    for row in read_jsonl(path):
        bm = _row_to_biomarker(row)
        if bm.name:
            out[bm.name] = bm
    return out


def load_biomarkers_from_python() -> Dict[str, Biomarker]:
    """Load biomarkers by instantiating BiomarkerDatabase."""
    from .biomarkers_db import BiomarkerDatabase
    db = BiomarkerDatabase()
    return dict(db._biomarkers)


def load_biomarkers(source: str = "auto") -> Dict[str, Biomarker]:
    """Load biomarkers, preferring JSONL when available."""
    if source == "python":
        return load_biomarkers_from_python()
    if source == "jsonl":
        return load_biomarkers_from_jsonl()
    if DEFAULT_JSONL.exists() and DEFAULT_JSONL.stat().st_size > 0:
        return load_biomarkers_from_jsonl()
    return load_biomarkers_from_python()
