"""
tools/migrate_to_json.py

Migrates the n-1 knowledge base from Python-authored modules to JSONL
files under knowledge/. Idempotent, non-destructive.

Usage:
    python tools/migrate_to_json.py medications
    python tools/migrate_to_json.py biomarkers
    python tools/migrate_to_json.py foods
    python tools/migrate_to_json.py all
    python tools/migrate_to_json.py all --dry-run

See docs/MIGRATION_TO_JSON.md for the plan.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import pkgutil
import re
import sys
import unicodedata
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from uuid import UUID


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from blutwerte.medications.models import Medication            # noqa: E402
from blutwerte.medications.effects.dose_models import DoseEffectModel  # noqa: E402
from blutwerte.bloodtests.models import Biomarker              # noqa: E402
from blutwerte.foods.models import Food                         # noqa: E402
from blutwerte.foods.rdi import RDI                            # noqa: E402
from blutwerte.activities.models import Activity               # noqa: E402

SCHEMA_VERSION = 1


def to_jsonable(obj: Any) -> Any:
    """Recursively convert Python objects to JSON-serializable form."""
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj)
    if is_dataclass(obj):
        d = asdict(obj)
        return {k: to_jsonable(v) for k, v in d.items()}
    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set, frozenset)):
        return [to_jsonable(v) for v in obj]
    return str(obj)


def slugify(text: str) -> str:
    """ASCII slug from arbitrary text. Lowercase, words joined by _."""
    if not text:
        return ""
    nfc = unicodedata.normalize("NFKC", text)
    ascii_text = nfc.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower()
    ascii_text = re.sub(r"[^a-z0-9]+", "_", ascii_text)
    return ascii_text.strip("_")


def n1_id(name: str) -> str:
    """Project-local ID from a name."""
    slug = slugify(name)
    return f"n1:{slug}" if slug else "n1:unnamed"


def _sanitize_value(v: Any) -> Any:
    """Strip a value the JSON encoder hates (inf, nan, very large ints)."""
    if isinstance(v, float):
        if v != v or v in (float("inf"), float("-inf")):
            return None
    return v


def _clean_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize all values in a dict."""
    return {k: _sanitize_value(v) for k, v in d.items()}


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    """Write rows as JSONL (one object per line). Returns count written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            clean = _clean_dict(row)
            f.write(json.dumps(clean, ensure_ascii=False, sort_keys=True))
            f.write("\n")
            n += 1
    return n


# ---------------------------------------------------------------------------
# Medications
# ---------------------------------------------------------------------------

def _collect_medication_modules() -> List[Tuple[str, Any]]:
    """Find every module in blutwerte.medications.data that creates medications."""
    modules: List[Tuple[str, Any]] = []
    try:
        from blutwerte.medications import data as meds_data
    except ImportError:
        print("  WARN  blutwerte.medications.data not present (already deleted)")
        return modules

    for _, modname, _ in pkgutil.iter_modules(meds_data.__path__, meds_data.__name__ + "."):
        try:
            modules.append((modname, importlib.import_module(modname)))
        except Exception as exc:
            print(f"  WARN  could not import {modname}: {exc}")

    try:
        from blutwerte.medications.data import vitamins
        for _, modname, _ in pkgutil.iter_modules(vitamins.__path__, vitamins.__name__ + "."):
            try:
                modules.append((modname, importlib.import_module(modname)))
            except Exception as exc:
                print(f"  WARN  could not import {modname}: {exc}")
    except ImportError:
        pass

    return modules


def _medication_to_row(med: Medication) -> Dict[str, Any]:
    raw = to_jsonable(med)
    raw["id"] = n1_id(med.name)
    raw["schema_version"] = SCHEMA_VERSION
    raw["source"] = "n1"
    return raw


def migrate_medications(out_dir: Path, dry_run: bool = False) -> int:
    print("=== medications ===")
    modules = _collect_medication_modules()
    print(f"  found {len(modules)} medication modules")

    medications: List[Medication] = []
    seen: set = set()
    for _, module in modules:
        for attr_name in dir(module):
            if not attr_name.startswith("create_"):
                continue
            func = getattr(module, attr_name, None)
            if not callable(func):
                continue
            try:
                med = func()
            except Exception as exc:
                print(f"  WARN  {attr_name} failed: {exc}")
                continue
            if not isinstance(med, Medication):
                continue
            if med.name.lower() in seen:
                continue
            seen.add(med.name.lower())
            medications.append(med)

    print(f"  collected {len(medications)} medications")

    target = out_dir / "knowledge" / "medications" / "medications.jsonl"
    if dry_run:
        print(f"  DRY  would write {target} ({len(medications)} rows)")
        return len(medications)

    rows = [_medication_to_row(m) for m in sorted(medications, key=lambda m: m.name.lower())]
    n = write_jsonl(target, rows)
    print(f"  wrote {n} rows to {target}")
    return n


# ---------------------------------------------------------------------------
# Biomarkers
# ---------------------------------------------------------------------------

def migrate_biomarkers(out_dir: Path, dry_run: bool = False) -> int:
    print("=== biomarkers ===")
    from blutwerte.bloodtests.biomarkers_db import BiomarkerDatabase

    db = BiomarkerDatabase()
    biomarkers: List[Biomarker] = list(db._biomarkers.values())
    print(f"  collected {len(biomarkers)} biomarkers")

    target = out_dir / "knowledge" / "biomarkers" / "biomarkers.jsonl"
    if dry_run:
        print(f"  DRY  would write {target} ({len(biomarkers)} rows)")
        return len(biomarkers)

    def _biomarker_to_row(b: Biomarker) -> Dict[str, Any]:
        raw = to_jsonable(b)
        raw["id"] = n1_id(b.name)
        raw["schema_version"] = SCHEMA_VERSION
        raw["source"] = "n1"
        return raw

    rows = [_biomarker_to_row(b) for b in sorted(biomarkers, key=lambda x: x.name.lower())]
    n = write_jsonl(target, rows)
    print(f"  wrote {n} rows to {target}")
    return n


# ---------------------------------------------------------------------------
# Foods
# ---------------------------------------------------------------------------

FOOD_SOURCES = [
    ("bls_curated", "blutwerte.foods.data.legacy.food_bls_migrated"),
    ("bls",         "blutwerte.foods.data.legacy.food_bls_german_migrated"),
    ("swiss",       "blutwerte.foods.data.legacy.food_naehrwertdaten_ch_migrated"),
    ("openfoodfacts", "blutwerte.foods.data.legacy.food_openfoodfacts_manual_migrated"),
    ("yazio",       "blutwerte.foods.data.legacy.food_yazio_manual_migrated"),
    ("manual",      "blutwerte.foods.data.legacy.food_other_manual_migrated"),
    ("priority_vegetables", "blutwerte.foods.data.vegetables"),
    ("priority_fruits",     "blutwerte.foods.data.fruits"),
    ("priority_dairy",      "blutwerte.foods.data.dairy"),
    ("priority_grains",     "blutwerte.foods.data.grains"),
    ("priority_proteins_meat",    "blutwerte.foods.data.proteins.meat"),
    ("priority_proteins_fish",    "blutwerte.foods.data.proteins.fish"),
    ("priority_proteins_eggs",    "blutwerte.foods.data.proteins.eggs"),
    ("priority_proteins_legumes", "blutwerte.foods.data.proteins.legumes"),
    ("priority_proteins_plant",   "blutwerte.foods.data.proteins.plant"),
]


def _food_to_row(food: Food, source: str, upstream_id: Optional[str]) -> Dict[str, Any]:
    raw = to_jsonable(food)
    raw["schema_version"] = SCHEMA_VERSION
    if upstream_id:
        raw["id"] = f"{source}:{upstream_id}"
        raw["upstream_id"] = upstream_id
    else:
        raw["id"] = n1_id(food.name)
        raw["upstream_id"] = None
    raw["source"] = source
    return raw


def _extract_upstream_id(attr_name: str) -> Optional[str]:
    """Best-effort upstream id from the create_<name> function name."""
    m = re.match(r"^create_(.+)$", attr_name)
    if not m:
        return None
    slug = m.group(1)
    if slug.startswith("BLS_") or re.match(r"^BLS\d+", slug):
        return slug
    return None


def _walk_food_module(module_name: str, source: str) -> List[Dict[str, Any]]:
    try:
        module = importlib.import_module(module_name)
    except (ImportError, ModuleNotFoundError) as exc:
        print(f"  WARN  could not import {module_name}: {exc}")
        return []
    except Exception as exc:
        print(f"  WARN  error importing {module_name}: {exc}")
        return []

    rows: List[Dict[str, Any]] = []
    for attr_name in dir(module):
        if not attr_name.startswith("create_"):
            continue
        func = getattr(module, attr_name, None)
        if not callable(func):
            continue
        try:
            food = func()
        except Exception as exc:
            print(f"  WARN  {module_name}.{attr_name} failed: {exc}")
            continue
        if not isinstance(food, Food):
            continue
        upstream_id = _extract_upstream_id(attr_name)
        rows.append(_food_to_row(food, source, upstream_id))
    return rows


def migrate_foods(out_dir: Path, dry_run: bool = False) -> int:
    print("=== foods ===")
    total = 0
    for source, module_name in FOOD_SOURCES:
        print(f"  --- {source} ({module_name}) ---")
        rows = _walk_food_module(module_name, source)
        print(f"      collected {len(rows)} foods")
        total += len(rows)
        if dry_run:
            continue
        target = out_dir / "knowledge" / "foods" / f"{source}.jsonl"
        n = write_jsonl(target, rows)
        print(f"      wrote {n} rows to {target.relative_to(out_dir)}")
    print(f"  total foods: {total}")
    return total


# ---------------------------------------------------------------------------
# Nutrients (RDI)
# ---------------------------------------------------------------------------

def migrate_nutrients(out_dir: Path, dry_run: bool = False) -> int:
    print("=== nutrients ===")
    from blutwerte.foods.rdi import get_all_rdis

    registry = get_all_rdis()
    print(f"  collected {len(registry)} RDI entries")

    def _rdi_to_row(name: str, rdi: "RDI") -> Dict[str, Any]:
        raw = to_jsonable(rdi)
        raw["id"] = n1_id(name)
        raw["name"] = name
        raw["schema_version"] = SCHEMA_VERSION
        raw["source"] = "n1"
        return raw

    target = out_dir / "knowledge" / "nutrients" / "nutrients.jsonl"
    if dry_run:
        print(f"  DRY  would write {target} ({len(registry)} rows)")
        return len(registry)

    rows = [_rdi_to_row(name, rdi) for name, rdi in sorted(registry.items())]
    n = write_jsonl(target, rows)
    print(f"  wrote {n} rows to {target}")
    return n


# ---------------------------------------------------------------------------
# Activities
# ---------------------------------------------------------------------------

def _activity_to_row(act: Activity) -> Dict[str, Any]:
    raw = to_jsonable(act)
    raw["id"] = n1_id(act.name)
    raw["schema_version"] = SCHEMA_VERSION
    raw["source"] = "n1"
    return raw


def migrate_activities(out_dir: Path, dry_run: bool = False) -> int:
    print("=== activities ===")
    try:
        module = importlib.import_module("blutwerte.activities.data.common_activities")
    except Exception as exc:
        print(f"  WARN  could not import activities module: {exc}")
        return 0

    activities: List[Activity] = []
    for attr_name in dir(module):
        if not attr_name.startswith("create_"):
            continue
        func = getattr(module, attr_name, None)
        if not callable(func):
            continue
        try:
            act = func()
        except Exception as exc:
            print(f"  WARN  {attr_name} failed: {exc}")
            continue
        if isinstance(act, Activity):
            activities.append(act)

    print(f"  collected {len(activities)} activities")

    target = out_dir / "knowledge" / "activities" / "activities.jsonl"
    if dry_run:
        print(f"  DRY  would write {target} ({len(activities)} rows)")
        return len(activities)

    rows = [_activity_to_row(a) for a in sorted(activities, key=lambda a: a.name.lower())]
    n = write_jsonl(target, rows)
    print(f"  wrote {n} rows to {target}")
    return n


# ---------------------------------------------------------------------------
# Units (portions)
# ---------------------------------------------------------------------------

def migrate_units(out_dir: Path, dry_run: bool = False) -> int:
    """Audit the predefined Portion objects in blutwerte.foods.portions and
    write them to JSONL. This is a data audit, not a code rewire: portions.py
    remains the live registry; the JSONL is the formal data so the
    round-trip test can verify the names/weights.
    """
    print("=== units (portions) ===")
    from blutwerte.foods.portions import Registry as PortionsRegistry

    portions = list(PortionsRegistry.portions.values())
    print(f"  collected {len(portions)} Portion objects")

    target = out_dir / "knowledge" / "units" / "portions.jsonl"
    if dry_run:
        print(f"  DRY  would write {target} ({len(portions)} rows)")
        return len(portions)

    def _portion_to_row(p) -> Dict[str, Any]:
        return {
            "id": n1_id(p.name),
            "name": p.name,
            "weight_grams": p.weight,
            "schema_version": SCHEMA_VERSION,
            "source": "n1",
        }

    rows = [_portion_to_row(p) for p in sorted(portions, key=lambda p: p.name)]
    n = write_jsonl(target, rows)
    print(f"  wrote {n} rows to {target}")
    return n


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument(
        "what",
        choices=["medications", "biomarkers", "foods", "nutrients", "activities", "units", "all"],
    )
    parser.add_argument("--out", type=Path, default=REPO_ROOT,
                        help="Output directory (default: repo root)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        print("(dry run; no files written)")

    counts: Dict[str, int] = {}
    if args.what in ("medications", "all"):
        counts["medications"] = migrate_medications(args.out, args.dry_run)
    if args.what in ("biomarkers", "all"):
        counts["biomarkers"] = migrate_biomarkers(args.out, args.dry_run)
    if args.what in ("foods", "all"):
        counts["foods"] = migrate_foods(args.out, args.dry_run)
    if args.what in ("nutrients", "all"):
        counts["nutrients"] = migrate_nutrients(args.out, args.dry_run)
    if args.what in ("activities", "all"):
        counts["activities"] = migrate_activities(args.out, args.dry_run)
    if args.what in ("units", "all"):
        counts["units"] = migrate_units(args.out, args.dry_run)

    print("=== summary ===")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
