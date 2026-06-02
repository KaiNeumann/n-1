"""
tools/test_roundtrip.py

Structural and round-trip tests for the migrated JSONL knowledge base.

Run:
    python tools/test_roundtrip.py

Exits non-zero on any failure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from core.medications.models import Medication            # noqa: E402
from core.bloodtests.models import Biomarker              # noqa: E402
from core.foods.models import Food                         # noqa: E402
from core.foods.rdi import RDI                            # noqa: E402
from core.activities.models import Activity               # noqa: E402


REQUIRED_FIELDS_BY_ENTITY: Dict[str, set] = {
    "medication":      {"id", "schema_version", "source", "name"},
    "biomarker":       {"id", "schema_version", "source", "name"},
    "food":            {"id", "schema_version", "source", "name"},
    "nutrient":        {"id", "schema_version", "source", "name"},
    "activity":        {"id", "schema_version", "source", "name"},
    "unit":            {"id", "schema_version", "source", "name"},
    "portion_default": {"id", "schema_version", "source", "category", "portion_name", "amount_grams"},
}


def _check_required_fields(entity: str, row: dict, line_no: int, path: Path) -> List[str]:
    errs = []
    required = REQUIRED_FIELDS_BY_ENTITY.get(entity, {"id", "schema_version", "source", "name"})
    missing = required - set(row.keys())
    if missing:
        errs.append(f"{entity} {path.name}:{line_no} missing {sorted(missing)}")
    if row.get("schema_version") != 1:
        errs.append(f"{entity} {path.name}:{line_no} schema_version={row.get('schema_version')} (expected 1)")
    if not row.get("id"):
        errs.append(f"{entity} {path.name}:{line_no} empty id")
    return errs


def _check_unique_ids(entity: str, rows: List[dict], path: Path) -> List[str]:
    errs = []
    seen: Dict[str, int] = {}
    for i, r in enumerate(rows, 1):
        rid = r.get("id")
        if rid in seen:
            errs.append(f"{entity} {path.name}:{i} duplicate id={rid!r} (first seen at line {seen[rid]})")
        else:
            seen[rid] = i
    return errs


def _check_medications(meds: List[dict], originals: Dict[str, Medication]) -> List[str]:
    errs = []
    by_id = {m["id"]: m for m in meds}
    for orig in originals.values():
        oid = f"n1:{orig.name.lower().replace(' ', '_').replace('-', '_')}"
        if oid not in by_id:
            errs.append(f"medication original {orig.name!r} not found in JSONL (expected id {oid!r})")
            continue
        jm = by_id[oid]
        if jm.get("name") != orig.name:
            errs.append(f"medication {oid}: name mismatch json={jm.get('name')!r} orig={orig.name!r}")
        if orig.drug_class and jm.get("drug_class") != orig.drug_class:
            errs.append(f"medication {oid}: drug_class mismatch")
        if jm.get("id") != oid:
            errs.append(f"medication {oid}: id mismatch")
    return errs


def _check_biomarkers(rows: List[dict]) -> List[str]:
    errs = []
    for r in rows:
        if not r.get("ranges"):
            errs.append(f"biomarker {r.get('id')}: no ranges")
    return errs


def _check_food_nutrition(rows: List[dict], path: Path) -> List[str]:
    errs = []
    for i, r in enumerate(rows, 1):
        n = r.get("nutrition_per_100g") or r.get("nutrition_data") or {}
        cal = n.get("calories")
        if cal is not None and cal > 900:
            errs.append(f"{path.name}:{i} id={r.get('id')!r} suspicious calories={cal}")
    return errs


def _gather_original_medications() -> Dict[str, Medication]:
    from core.medications.database import MedicationDatabase
    db = MedicationDatabase()
    return {m.name.lower(): m for m in db._medications.values()}


def _gather_original_rdis() -> Dict[str, RDI]:
    from core.foods.rdi import get_all_rdis
    return get_all_rdis()


def _gather_original_activities() -> Dict[str, Activity]:
    from core.activities import load_activities
    return load_activities()


def _check_nutrients(rows: List[dict], originals: Dict[str, RDI]) -> List[str]:
    errs = []
    for r in rows:
        name = (r.get("name") or "").lower()
        if name and name not in originals:
            errs.append(f"nutrient {r.get('id')!r} original {name!r} not in registry")
    return errs


def _check_activities(rows: List[dict], originals: Dict[str, Activity]) -> List[str]:
    errs = []
    for r in rows:
        name = (r.get("name") or "").lower()
        if name and name not in originals:
            errs.append(f"activity {r.get('id')!r} original {name!r} not in registry")
        if r.get("calories_per_hour") is None:
            errs.append(f"activity {r.get('id')!r}: missing calories_per_hour")
    return errs


def main() -> int:
    print("=== round-trip test ===")
    errs: List[str] = []

    # Medications
    print("--- medications ---")
    med_path = REPO_ROOT / "knowledge" / "medications" / "medications.jsonl"
    meds = [json.loads(l) for l in med_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"  loaded {len(meds)} rows")
    for i, m in enumerate(meds, 1):
        errs.extend(_check_required_fields("medication", m, i, med_path))
    errs.extend(_check_unique_ids("medication", meds, med_path))
    originals = _gather_original_medications()
    errs.extend(_check_medications(meds, originals))

    # Biomarkers
    print("--- biomarkers ---")
    bm_path = REPO_ROOT / "knowledge" / "biomarkers" / "biomarkers.jsonl"
    bms = [json.loads(l) for l in bm_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"  loaded {len(bms)} rows")
    for i, b in enumerate(bms, 1):
        errs.extend(_check_required_fields("biomarker", b, i, bm_path))
    errs.extend(_check_unique_ids("biomarker", bms, bm_path))
    errs.extend(_check_biomarkers(bms))

    # Foods
    print("--- foods ---")
    food_dir = REPO_ROOT / "knowledge" / "foods"
    food_files = sorted(food_dir.glob("*.jsonl"))
    total_foods = 0
    for fp in food_files:
        rows = [json.loads(l) for l in fp.read_text(encoding="utf-8").splitlines() if l.strip()]
        total_foods += len(rows)
        print(f"  {fp.name}: {len(rows)} rows")
        for i, f in enumerate(rows, 1):
            errs.extend(_check_required_fields("food", f, i, fp))
        errs.extend(_check_unique_ids("food", rows, fp))
        errs.extend(_check_food_nutrition(rows, fp))
    print(f"  total foods: {total_foods}")

    # Nutrients
    print("--- nutrients ---")
    nut_path = REPO_ROOT / "knowledge" / "nutrients" / "nutrients.jsonl"
    nuts = [json.loads(l) for l in nut_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"  loaded {len(nuts)} rows")
    for i, n in enumerate(nuts, 1):
        errs.extend(_check_required_fields("nutrient", n, i, nut_path))
    errs.extend(_check_unique_ids("nutrient", nuts, nut_path))
    orig_nuts = _gather_original_rdis()
    errs.extend(_check_nutrients(nuts, orig_nuts))

    # Activities
    print("--- activities ---")
    act_path = REPO_ROOT / "knowledge" / "activities" / "activities.jsonl"
    acts = [json.loads(l) for l in act_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"  loaded {len(acts)} rows")
    for i, a in enumerate(acts, 1):
        errs.extend(_check_required_fields("activity", a, i, act_path))
    errs.extend(_check_unique_ids("activity", acts, act_path))
    orig_acts = _gather_original_activities()
    errs.extend(_check_activities(acts, orig_acts))

    # Units (portions)
    print("--- units (portions) ---")
    unit_path = REPO_ROOT / "knowledge" / "units" / "portions.jsonl"
    units = [json.loads(l) for l in unit_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"  loaded {len(units)} rows")
    for i, u in enumerate(units, 1):
        errs.extend(_check_required_fields("unit", u, i, unit_path))
    errs.extend(_check_unique_ids("unit", units, unit_path))
    # Cross-check: every portion in JSONL must exist in the live Python registry
    from core.foods.portions_jsonl_loader import load_portions_from_python
    live = load_portions_from_python()
    for u in units:
        n = (u.get("name") or "").lower()
        if n not in live:
            errs.append(f"unit {u.get('id')!r} name={n!r} not in live Python registry")
        elif live[n]["weight_grams"] != u.get("weight_grams"):
            errs.append(f"unit {u.get('id')!r} weight mismatch jsonl={u.get('weight_grams')} python={live[n]['weight_grams']}")

    # Portion category defaults
    print("--- portion category defaults ---")
    pcd_path = REPO_ROOT / "knowledge" / "units" / "portion_category_defaults.jsonl"
    pcds = [json.loads(l) for l in pcd_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"  loaded {len(pcds)} rows")
    for i, p in enumerate(pcds, 1):
        errs.extend(_check_required_fields("portion_default", p, i, pcd_path))
    errs.extend(_check_unique_ids("portion_default", pcds, pcd_path))
    # Cross-check: every (category, portion_name) in JSONL must match the live registry
    from core.foods.portions_jsonl_loader import load_category_defaults_from_python
    live_defaults = {
        (cat, pn): amt
        for cat, pn, amt in load_category_defaults_from_python()
    }
    for p in pcds:
        key = ((p.get("category") or "").strip(), (p.get("portion_name") or "").strip())
        amt = p.get("amount_grams")
        if key not in live_defaults:
            errs.append(f"portion_default {p.get('id')!r} {key} not in live registry")
        elif float(live_defaults[key]) != float(amt):
            errs.append(f"portion_default {p.get('id')!r} amount mismatch jsonl={amt} python={live_defaults[key]}")

    # Summary
    print("=== summary ===")
    print(f"  medications:    {len(meds)}")
    print(f"  biomarkers:     {len(bms)}")
    print(f"  foods:          {total_foods}")
    print(f"  nutrients:      {len(nuts)}")
    print(f"  activities:     {len(acts)}")
    print(f"  units:          {len(units)}")
    print(f"  portion_defaults: {len(pcds)}")
    print(f"  errors:         {len(errs)}")
    if errs:
        print()
        print("FAILURES:")
        for e in errs[:50]:
            print(f"  {e}")
        if len(errs) > 50:
            print(f"  ... and {len(errs) - 50} more")
        return 1

    # Schema validation (delegates to tools/validate_schemas.py)
    print("--- schema validation ---")
    import subprocess
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "validate_schemas.py")],
        capture_output=True, text=True,
    )
    print(r.stdout.rstrip())
    if r.returncode != 0:
        print(r.stderr.rstrip())
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
