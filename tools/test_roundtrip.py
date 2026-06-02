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

from blutwerte.medications.models import Medication            # noqa: E402
from blutwerte.bloodtests.models import Biomarker              # noqa: E402
from blutwerte.foods.models import Food                         # noqa: E402


REQUIRED_FIELDS = {"id", "schema_version", "source", "name"}


def _check_required_fields(entity: str, row: dict, line_no: int, path: Path) -> List[str]:
    errs = []
    missing = REQUIRED_FIELDS - set(row.keys())
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
    from blutwerte.medications.database import MedicationDatabase
    db = MedicationDatabase()
    return {m.name.lower(): m for m in db._medications.values()}


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

    # Summary
    print("=== summary ===")
    print(f"  medications: {len(meds)}")
    print(f"  biomarkers:  {len(bms)}")
    print(f"  foods:       {total_foods}")
    print(f"  errors:      {len(errs)}")
    if errs:
        print()
        print("FAILURES:")
        for e in errs[:50]:
            print(f"  {e}")
        if len(errs) > 50:
            print(f"  ... and {len(errs) - 50} more")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
