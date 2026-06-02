# Migration Plan: Python-Authored Knowledge → JSONL

This document is the concrete plan for moving the n=1 knowledge base
from Python-authored modules to JSONL files under `knowledge/`. It is
executed by `tools/migrate_to_json.py`.

## Status

| Entity      | Source                                  | Count | Target                                        | Done |
|-------------|-----------------------------------------|------:|-----------------------------------------------|------|
| Medications | `core/medications/data/*.py`       |    13 | `knowledge/medications/medications.jsonl`     | ✓    |
| Biomarkers  | `core/bloodtests/biomarkers_db.py` |    99 | `knowledge/biomarkers/biomarkers.jsonl`       | ✓    |
| Foods (BLS curated) | `core/foods/data/legacy/food_bls_migrated.py` | 74 | `knowledge/foods/bls_curated.jsonl`  | ✓    |
| Foods (BLS full)    | `core/foods/data/legacy/food_bls_german_migrated.py` | 7,140 | `knowledge/foods/bls.jsonl` | ✓    |
| Foods (Swiss)       | `core/foods/data/legacy/food_naehrwertdaten_ch_migrated.py` | 1,092 | `knowledge/foods/swiss.jsonl` | ✓    |
| Foods (OFF)         | `core/foods/data/legacy/food_openfoodfacts_manual_migrated.py` | 74 | `knowledge/foods/openfoodfacts.jsonl` | ✓    |
| Foods (Yazio)       | `core/foods/data/legacy/food_yazio_migrated.py` | 8 | `knowledge/foods/yazio.jsonl`         | ✓    |
| Foods (manual)      | `core/foods/data/legacy/food_other_manual_migrated.py` | 31 | `knowledge/foods/manual.jsonl`     | ✓    |
| Foods (priority)    | `core/foods/data/{vegetables,fruits,dairy,grains,proteins/*}.py` | 22 | `knowledge/foods/priority_*.jsonl` | ✓    |
| Nutrients   | `core/foods/rdi.py`                |    10 | `knowledge/nutrients/nutrients.jsonl`         | ✓    |
| Activities  | `core/activities/data/common_activities.py` |    58 | `knowledge/activities/activities.jsonl` | ✓    |
| Units       | `core/foods/portions.py`           |    27 | `knowledge/units/portions.jsonl`              | ✓    |

### Wired up (JSONL preferred, Python fallback)

- `core/medications/jsonl_loader.py` + `_load_all_medications` prefers JSONL.
- `core/bloodtests/jsonl_loader.py` + `_initialize_biomarkers` prefers JSONL.
- `core/foods/jsonl_loader.py` + `FoodDatabase.load_all` prefers JSONL.
- `core/foods/jsonl_rdi_loader.py` + `_load_rdi_registry` prefers JSONL.
- `core/activities/jsonl_loader.py` + `load_activities(source='auto')` prefers JSONL.
- `core/foods/portions_jsonl_loader.py` + `_initialize_predefined_portions()`
  loads the 27 Portion objects from JSONL and registers them as module
  globals at import time.

### Legacy Python data — removed

- `core/medications/data/` (14 files) — removed in `8d07d9f`.
- `core/bloodtests/biomarkers_db.py` Python fallback (8,303 lines) — removed in `a090e2e`.
- `core/foods/data/` (18 files, 11.6 MB) — removed in `eef8fde`.
- `core/foods/data/legacy/MIGRATION_SUMMARY.md` — removed in `eef8fde`.
- `core/foods/rdi.py` (10 RDI_* constants + 3 default sources) — removed in `e7b63db`.
- `enrich_foods_with_foodb.py`, `add_biomarker_effects.py` — obsolete one-off scripts, removed in `431a656`.
- `core/activities/data/` (2 files, 55 KB) — removed in `2f70313`.
- `core/foods/portions.py` hard-coded portion definitions (27 calls) — replaced by JSONL loader in `3129725`.

### Open follow-ups

- **Portion category defaults** (the 26 `CategoryPortionDefaults.set(...)`
  calls in portions.py) are mutable runtime state, not static knowledge.
  They were deliberately left in Python and not migrated.

JSONL everywhere (one object per line), for uniform tooling and
append-friendly edits. The principles doc is the source of truth on
this choice; if you disagree, change it there first.

## ID scheme

- **External IDs preferred**: when a food/biomarker/medication has a
  canonical upstream ID, use `<source>:<id>` (e.g. `bls:BLS_0123`,
  `off:4053400205298`, `loinc:718-7`, `rxcui:29046`).
- **Project-local IDs** use the `n1:` prefix (e.g. `n1:bendroflumethiazide`,
  `n1:potassium`, `n1:running_moderate`). Slug = lowercase ASCII, words
  joined by `_`. Accents and umlauts are stripped to ASCII.

The converter generates `n1:` IDs from the English `name` (slugified)
when no upstream ID is available.

## Schema versioning

Every JSONL row carries a top-level `schema_version` (integer). The
current schema is version `1`. Breaking changes bump the version and
require a converter.

Schema files live in `docs/schemas/`:

- `medication.schema.json` — JSON Schema for one medication row
- `biomarker.schema.json`  — JSON Schema for one biomarker row
- `food.schema.json`       — JSON Schema for one food row
- `nutrient.schema.json`   — JSON Schema for one nutrient row
- `activity.schema.json`   — JSON Schema for one activity row
- `unit.schema.json`       — JSON Schema for one unit row

(These are written alongside the JSONL files; converters write
schema-bearing rows so validation is possible from day one.)

## Converter design

`tools/migrate_to_json.py` is a single Python module that:

1. **Imports** the current Python data as-is (no model changes
   required).
2. **Instantiates** every `Medication`, `Biomarker`, `Food`.
3. **Serializes** each instance to a JSONL row using
   `dataclasses.as_dict()`-style flattening.
4. **Writes** to the target JSONL file with stable ordering and a
   trailing newline.

Key design points:

- The converter is **idempotent**: re-running it produces the same
  output (modulo timestamps and reordering of internal sets).
- The converter is **non-destructive**: it writes to `knowledge/` and
  does not touch the Python source.
- The converter uses the *existing* dataclasses as the source of
  truth for the JSON shape. Renaming a field in the dataclass will
  change the JSON output; that is intentional.
- Enum values are written as their `.value` (string), not the enum
  name.
- Empty lists and dicts are written as `[]` / `{}`, not omitted, so
  round-trip works without inference.

## Round-trip test

`tools/test_roundtrip.py` reads the JSONL back, reconstructs
equivalent Python objects, and asserts structural equality on a
sample (or all) of the rows. It catches:

- Missing fields after deserialization
- Type errors (e.g. `None` where a number was expected)
- Enum mismatches
- Source list corruption

The test is run before the Python source is deleted, so any
divergence is caught early.

## Transition

During the transition (after JSONL is written, before Python source
is deleted):

- `core/foods/database.py`, `core/bloodtests/biomarkers_db.py`,
  `core/medications/database.py` are updated to **prefer JSONL**
  if it exists, falling back to Python on missing files. This lets us
  migrate one entity type at a time.
- Each migrated entity gets a new top-level loader module
  (`core/foods/jsonl_loader.py`, etc.) that is the path forward.
- The Python source files stay in tree for at least one release, marked
  as legacy in their docstrings, and are deleted once the round-trip
  test passes for every entity.

## Deletion policy

The Python data files are deleted only when:

1. JSONL exists and is non-empty for the entity.
2. The round-trip test passes for the entity.
3. `MANIFEST.json` includes the JSONL file with a fresh SHA256.

Deletion happens in a single commit per entity, with a clear message
(`refactor: remove legacy Python data for <entity>`), so git history
always shows the Python file before its JSONL replacement.

## Risks and open questions

- **Encoding bugs in source**: the `archive/food_legacy/.../BLS_4_0_2025_DE.zip`
  path had UTF-8 mojibake (`BundeslebensmittelschlǬssel`). The
  converter normalizes to NFC and strips non-ASCII to ASCII where
  safe, but German food names may lose umlauts. We accept this for
  the slug, keep the original name with the umlaut in the `name_de`
  field.
- **Nutrition units**: the current Python `nutrition_data` is
  heterogeneous — sometimes per-100g, sometimes per-serving, sometimes
  with mixed units. The converter assumes per-100g and logs a
  warning on suspect values (e.g. calories > 900 kcal/100g).
- **RDI personalization**: `core/foods/rdi.py` mixes static data
  and personalizing functions. Only the static data goes into
  `knowledge/nutrients.json`; the functions stay in
  `core/foods/rdi.py` as the consumer.
- **Cooklang recipes**: deferred; current `receipts.py` is in
  `archive/food_legacy/` and will be re-encoded as Cooklang files
  under `knowledge/recipes/` as a separate step.

## Order of execution

1. **Migrations** (this PR): medications → biomarkers → foods → RDI → activities → units.
2. **JSONL loaders** in `core/` (separate commits).
3. **Database modules** updated to prefer JSONL (separate commits).
4. **Deletion** of Python data (one commit per entity, gated on
   round-trip + MANIFEST).
5. **Schema files** under `docs/schemas/` (one per entity, written
   alongside the JSONL).
