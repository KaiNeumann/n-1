"""
tools/validate_schemas.py

Validates every JSONL file under knowledge/ against its corresponding
JSON Schema in docs/schemas/. Resolves $ref to _common.json in the same
directory.

Usage:
    python tools/validate_schemas.py
    python tools/validate_schemas.py --strict   # exit non-zero on any error

Run before committing a change to the knowledge base, and as part of
the round-trip test.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = REPO_ROOT / "docs" / "schemas"
KNOWLEDGE_DIR = REPO_ROOT / "knowledge"

# Map entity name -> (schema file, list of JSONL paths)
ENTITY_TARGETS: List[Tuple[str, Path, List[Path]]] = [
    ("medication", SCHEMAS_DIR / "medication.schema.json",
     [KNOWLEDGE_DIR / "medications" / "medications.jsonl"]),
    ("biomarker", SCHEMAS_DIR / "biomarker.schema.json",
     [KNOWLEDGE_DIR / "biomarkers" / "biomarkers.jsonl"]),
    ("nutrient", SCHEMAS_DIR / "nutrient.schema.json",
     [KNOWLEDGE_DIR / "nutrients" / "nutrients.jsonl"]),
    ("activity", SCHEMAS_DIR / "activity.schema.json",
     [KNOWLEDGE_DIR / "activities" / "activities.jsonl"]),
    ("unit", SCHEMAS_DIR / "unit.schema.json",
     [KNOWLEDGE_DIR / "units" / "portions.jsonl"]),
    ("portion_default", SCHEMAS_DIR / "portion_default.schema.json",
     [KNOWLEDGE_DIR / "units" / "portion_category_defaults.jsonl"]),
    # Foods: one schema covers all 15 source files under knowledge/foods/
    ("food", SCHEMAS_DIR / "food.schema.json",
     sorted((KNOWLEDGE_DIR / "foods").glob("*.jsonl"))),
]


def _build_registry() -> Registry:
    """Build a referencing.Registry with all schema files under docs/schemas/."""
    pairs = []
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as f:
            contents = json.load(f)
        uri = contents.get("$id", f"file://{path.as_posix()}")
        resource = Resource.from_contents(contents, default_specification=DRAFT202012)
        pairs.append((uri, resource))
    return Registry().with_resources(pairs)


def _load_schema(path: Path, registry: Registry) -> Draft202012Validator:
    with path.open(encoding="utf-8") as f:
        contents = json.load(f)
    return Draft202012Validator(contents, registry=registry)


def _validate_file(validator: Draft202012Validator, path: Path) -> List[str]:
    errs: List[str] = []
    if not path.exists():
        return [f"missing: {path}"]
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                errs.append(f"{path.name}:{line_no} JSON parse error: {e}")
                continue
            for err in validator.iter_errors(row):
                errs.append(f"{path.name}:{line_no} {err.message} at {'/'.join(str(x) for x in err.absolute_path) or '<root>'}")
    return errs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--strict", action="store_true",
                        help="Exit non-zero on any error (default: report only).")
    args = parser.parse_args()

    print("=== schema validation ===")
    registry = _build_registry()

    total_errs = 0
    total_rows = 0
    summary: Dict[str, int] = {}
    for entity, schema_path, jsonl_paths in ENTITY_TARGETS:
        if not schema_path.exists():
            print(f"  --- {entity}: SKIP (schema not found at {schema_path})")
            summary[entity] = 0
            continue
        validator = _load_schema(schema_path, registry)
        entity_rows = 0
        entity_errs: List[str] = []
        for path in jsonl_paths:
            if not path.exists():
                continue
            rows_in_file = sum(1 for l in path.read_text(encoding="utf-8").splitlines() if l.strip())
            entity_rows += rows_in_file
            file_errs = _validate_file(validator, path)
            entity_errs.extend(file_errs)
        total_rows += entity_rows
        total_errs += len(entity_errs)
        summary[entity] = entity_rows
        status = "OK" if not entity_errs else f"{len(entity_errs)} errors"
        print(f"  --- {entity}: {entity_rows} rows, {status}")
        for e in entity_errs[:5]:
            print(f"      {e}")
        if len(entity_errs) > 5:
            print(f"      ... and {len(entity_errs) - 5} more")

    print("=== summary ===")
    for k, v in summary.items():
        print(f"  {k:12} {v:>6}")
    print(f"  {'total':12} {total_rows:>6} rows, {total_errs} errors")
    if total_errs:
        print("FAIL")
        return 1 if args.strict else 0
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
