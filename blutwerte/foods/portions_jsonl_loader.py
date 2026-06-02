"""
blutwerte.foods.portions_jsonl_loader

Loads the predefined Portion objects from
knowledge/units/portions.jsonl. Used to audit and verify the
27 portion definitions that blutwerte/foods/portions.py registers
at import time.

This loader is read-only: portions.py is still the live registry
that constructs the Portion objects. The JSONL is the formal data
representation; the round-trip test compares the two.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from .._jsonl import read_jsonl


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSONL = REPO_ROOT / "knowledge" / "units" / "portions.jsonl"


def load_portions_from_jsonl(path: Path = None) -> Dict[str, dict]:
    """Load portion definitions from the JSONL knowledge file.

    Returns a dict keyed by portion name (lowercased). Each value
    is a dict with keys: id, name, weight_grams.
    """
    path = path or DEFAULT_JSONL
    out: Dict[str, dict] = {}
    if not path.exists() or path.stat().st_size == 0:
        return out
    for row in read_jsonl(path):
        name = (row.get("name") or "").strip()
        if not name:
            continue
        out[name.lower()] = {
            "id": row.get("id"),
            "name": name,
            "weight_grams": row.get("weight_grams"),
        }
    return out


def load_portions_from_python() -> Dict[str, dict]:
    """Audit the live Portion registry built by portions.py."""
    from .portions import Registry
    return {
        name.lower(): {
            "id": f"n1:{name.lower()}",
            "name": name,
            "weight_grams": portion.weight,
        }
        for name, portion in Registry.portions.items()
    }


def load_portions(source: str = "auto") -> Dict[str, dict]:
    """Load portion definitions, preferring JSONL when available."""
    if source == "python":
        return load_portions_from_python()
    if source == "jsonl":
        return load_portions_from_jsonl()
    if DEFAULT_JSONL.exists() and DEFAULT_JSONL.stat().st_size > 0:
        return load_portions_from_jsonl()
    return load_portions_from_python()
