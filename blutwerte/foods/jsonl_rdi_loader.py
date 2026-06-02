"""
blutwerte.foods.jsonl_rdi_loader

Loads RDI (Recommended Daily Intake) entries from
knowledge/nutrients/nutrients.jsonl. Falls back to the Python
registry in blutwerte/foods/rdi.py when the JSONL is missing.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from .._jsonl import read_jsonl
from .rdi import RDI
from .sources import DataSource


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSONL = REPO_ROOT / "knowledge" / "nutrients" / "nutrients.jsonl"


def _row_to_data_source(row: dict) -> DataSource:
    return DataSource(
        url=row.get("url", ""),
        title=row.get("title", ""),
        source_type=row.get("source_type", "research"),
        access_date=row.get("access_date"),
        doi=row.get("doi"),
    )


def _row_to_rdi(row: dict) -> RDI:
    return RDI(
        minimum=row.get("minimum"),
        reference=row.get("reference"),
        maximum=row.get("maximum"),
        unit=row.get("unit", "g/day"),
        comments=list(row.get("comments") or []),
        sources=[_row_to_data_source(s) for s in (row.get("sources") or [])],
    )


def load_rdis_from_jsonl(path: Path = None) -> Dict[str, RDI]:
    """Load RDI entries from the JSONL knowledge file.

    Returns a dict keyed by lowercased nutrient name.
    """
    path = path or DEFAULT_JSONL
    out: Dict[str, RDI] = {}
    if not path.exists() or path.stat().st_size == 0:
        return out
    for row in read_jsonl(path):
        name = (row.get("name") or "").strip()
        if not name:
            continue
        out[name.lower()] = _row_to_rdi(row)
    return out


def load_rdis_from_python() -> Dict[str, RDI]:
    """Load RDI entries from the Python registry."""
    from .rdi import get_all_rdis
    return get_all_rdis()


def load_rdis(source: str = "auto") -> Dict[str, RDI]:
    """Load RDI entries, preferring JSONL when available."""
    if source == "python":
        return load_rdis_from_python()
    if source == "jsonl":
        return load_rdis_from_jsonl()
    if DEFAULT_JSONL.exists() and DEFAULT_JSONL.stat().st_size > 0:
        return load_rdis_from_jsonl()
    return load_rdis_from_python()
