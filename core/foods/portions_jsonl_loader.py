"""
core.foods.portions_jsonl_loader

Loads the predefined Portion objects from
knowledge/units/portions.jsonl. Used to audit and verify the
27 portion definitions that core/foods/portions.py registers
at import time.

This loader is read-only: portions.py is still the live registry
that constructs the Portion objects. The JSONL is the formal data
representation; the round-trip test compares the two.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

from .._jsonl import read_jsonl


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSONL = REPO_ROOT / "knowledge" / "units" / "portions.jsonl"
DEFAULT_DEFAULTS_JSONL = REPO_ROOT / "knowledge" / "units" / "portion_category_defaults.jsonl"


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


def load_category_defaults_from_jsonl(path: Path = None) -> List[Tuple[str, str, float]]:
    """Load category-default portion amounts from the JSONL knowledge file.

    Returns a list of (category, portion_name, amount_grams) tuples.
    One row per (category, portion_name) combination.
    """
    path = path or DEFAULT_DEFAULTS_JSONL
    out: List[Tuple[str, str, float]] = []
    if not path.exists() or path.stat().st_size == 0:
        return out
    for row in read_jsonl(path):
        category = (row.get("category") or "").strip()
        portion_name = (row.get("portion_name") or "").strip()
        amount = row.get("amount_grams")
        if not category or not portion_name or amount is None:
            continue
        out.append((category, portion_name, float(amount)))
    return out


def load_category_defaults_from_python() -> List[Tuple[str, str, float]]:
    """Audit the live CategoryPortionDefaults registry built by portions.py."""
    from .portions import CategoryPortionDefaults
    out: List[Tuple[str, str, float]] = []
    for category in CategoryPortionDefaults.list_categories():
        for portion_name, amount in CategoryPortionDefaults.get_category_defaults(category).items():
            out.append((category, portion_name, float(amount)))
    return out


def load_category_defaults(source: str = "auto") -> List[Tuple[str, str, float]]:
    """Load category-default portion amounts, preferring JSONL when available."""
    if source == "python":
        return load_category_defaults_from_python()
    if source == "jsonl":
        return load_category_defaults_from_jsonl()
    if DEFAULT_DEFAULTS_JSONL.exists() and DEFAULT_DEFAULTS_JSONL.stat().st_size > 0:
        return load_category_defaults_from_jsonl()
    return load_category_defaults_from_python()
