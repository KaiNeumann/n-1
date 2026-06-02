# N=1 — Principles

The n-of-1 project: a personal health analysis system applying n-of-1
trial discipline to nutrition, fitness and health for a single subject — you.

This document is the project's *constitution*. Concrete file formats and
schemas live in sibling documents; this one defines the rules those
formats must obey.

---

## 1. The data is the project. The code is replaceable.

The dataset is the artifact. The Python package is a *consumer* of that
data, never its owner. If the Python code is deleted, the dataset is
still self-describing, complete, and useful. If the dataset is deleted,
the Python code is empty.

This means:

- The canonical data lives in plain-text, open-standard files.
- Schemas are documented in plain Markdown and versioned.
- Every fact has exactly one source of truth, identified by a stable ID.
- The Python code is a *projection* of the data, not the data itself.
- Migration between tools, languages, or storage backends is a consumer
  change, not a data change.

## 2. Plain text, git-friendly, hand-editable.

The first-class editor is `git`. Files must be:

- **Diffable** — a change to one fact shows up as a minimal diff.
- **Mergeable** — small additions to different rows don't conflict.
- **Hand-editable** — small fixes don't require running a script.
- **Grep-able** — any single value is findable with `grep` in seconds.

Concretely:

- UTF-8 everywhere.
- ISO 8601 for every date and timestamp.
- LF line endings; CRLF tolerated on read, normalized on write.
- No binary blobs in the dataset. No SQLite, no pickle, no proprietary.
- Trailing newline on every file.

## 3. One source of truth per fact.

If the same fact appears in two places, one of them is wrong. The
project's directory layout encodes what lives where:

| Path                          | Contents                                       | Mutable by        | In git |
|-------------------------------|------------------------------------------------|-------------------|--------|
| `data/profile.md`             | Personal profile, goals, conditions            | You               | Yes    |
| `data/diary/YYYY/YYYY-MM-DD.md` | Daily logs (sleep, vitals, intake, activity)  | You               | Yes    |
| `data/notes/`                 | Free-form notes, hypotheses                    | You               | Yes    |
| `data/reports/`               | Generated analyses                             | Tool              | No (regenerable) |
| `data/cache/external/`        | Cached external lookups (devices, OFF, ...)    | Tool              | No (regenerable) |
| `knowledge/foods/*.jsonl`     | Food database rows                             | Tool + curation   | Yes    |
| `knowledge/biomarkers/*.jsonl`| Biomarker reference rows                       | Tool + curation   | Yes    |
| `knowledge/medications/*.jsonl` | Medication rows                              | Tool + curation   | Yes    |
| `knowledge/nutrients.json`    | Nutrient definitions, RDI helpers, citations   | Tool              | Yes    |
| `knowledge/activities.json`   | Activity MET values, biomarker effects         | Tool              | Yes    |
| `knowledge/units.json`        | Unit / portion definitions                     | Tool              | Yes    |
| `knowledge/recipes/`          | Cooklang recipes                               | You               | Yes    |
| `MANIFEST.json`               | SHA256 of every `knowledge/` file              | Tool              | Yes    |
| `lib/`                        | Python tool (consumer)                         | Maintainer        | Yes    |
| `.n1/config.toml`             | Tool config (paths, credentials)               | You               | No (private) |
| `.n1/cache/`                  | Tool runtime cache                             | Tool              | No     |

The diary references foods, medications, activities, biomarkers, and
patients *by ID*, never by display name. If a name changes in the
knowledge base, no diary entry changes.

## 4. Stable IDs everywhere.

Every entity that can be referenced has a stable, opaque ID:

| Entity       | ID format                                   | Example                          |
|--------------|---------------------------------------------|----------------------------------|
| Food         | `<source>:<id>`                             | `bls:BLS_0123`, `off:4053400205298`, `swiss:banane` |
| Biomarker    | `<source>:<id>` or `n1:<slug>`              | `loinc:718-7`, `n1:homocysteine` |
| Medication   | `<source>:<id>` or `n1:<slug>`              | `rxcui:29046`, `n1:telmisartan`  |
| Activity     | `n1:<slug>`                                 | `n1:running_moderate`            |
| Patient      | `n1:<id>`                                   | `n1:p001`                        |
| Unit         | `n1:<slug>`                                 | `n1:scheibe`                     |
| Nutrient     | `n1:<slug>` or external                     | `n1:vitamin_k`, `usda:1110`      |
| Diary entry  | ISO 8601 date (the date *is* the ID)        | `2024-01-15`                     |

External IDs (LOINC, RxNorm, BLS, Open Food Facts, USDA) are preferred.
Project-local IDs (`n1:` prefix) are added when no upstream ID exists.
The two are syntactically distinguishable. The ID, not the display name,
is what gets referenced in diary entries and reports.

## 5. The tool is a consumer, not the source.

The Python package (currently `core/`, on its way to `lib/n1/`)
reads the data, runs analysis, generates reports. It does not own the
data. It does not hold the only copy of the data. It does not define
the schema by class shape.

Adding a new food, biomarker, medication, or unit should not require
writing a Python class. It should require creating a JSON file (or
editing one) and re-running the validator.

## 6. Open standards only.

| Concept                 | Standard                                            |
|-------------------------|-----------------------------------------------------|
| Object data             | JSON (RFC 8259)                                     |
| Large tabular data      | JSON Lines (`.jsonl`) — one object per line         |
| Diary entries           | Markdown (CommonMark) + YAML frontmatter            |
| Patient data            | YAML or Markdown + YAML frontmatter                 |
| Dates and times         | ISO 8601                                            |
| Identifiers             | External systems (LOINC, RxNorm, BLS, OFF, ...) where available; `n1:` prefix for local |
| Recipes                 | Cooklang                                            |
| Config                  | TOML                                                |
| Manifest / checksum     | JSON                                                |
| Export (optional)       | CSV (RFC 4180) — *export only*, never canonical     |
| Encoding                | UTF-8                                               |

`.xlsx`, `.pdf`, `.zip` downloads are converted to JSON / CSV on import
and never committed as binary. The original downloads may live in
`data/cache/external/` (gitignored) for reproducibility.

## 7. Knowledge base versioning.

Reference data has *editions*: `bls-2025.1`, `dge-2024`,
`openfoodfacts-2024-10`. An edition is a tagged snapshot of the
knowledge base, frozen at a specific upstream release.

Diary entries and reports can record which edition they were analyzed
against:

```yaml
---
date: 2024-01-15
analyzed_with:
  foods: bls-2025.1
  biomarkers: loinc-2024-q4
  nutrients: dge-2024
---
```

When a new edition lands, old diary entries can be re-analyzed and the
diff (calorie total, biomarker interpretation, ...) is visible in git.

`MANIFEST.json` at the repo root records the SHA256 of every file
under `knowledge/`. If a file changes unexpectedly — corrupted,
silently edited, swapped — the manifest flags it.

## 8. Caching is not data.

External lookups (food databases, device APIs) are cached under
`data/cache/external/`. Cache is *regenerable* and is gitignored. If
the cache disappears, the tool re-fetches. The data that survives a
cache wipe is the data that matters; everything else is convenience.

## 9. Schema is documented next to the data.

Every data file lives next to a `*.schema.md` (or shares a single
schema file in the same directory) that documents:

- The columns / keys, with units and types.
- The valid value ranges and enums.
- One worked example.
- The edition the schema applies to.

Schemas are versioned with the data. A breaking schema change is a
major version bump; a new optional field is a minor bump.

## 10. Personal data stays personal.

The dataset belongs to the subject. Backups of `data/` are a few KB per
day, perfect for `rsync`, USB sticks, or `rclone`. Sensitive fields
(medical conditions, exact medication doses) live only in the local
repo unless explicitly exported.

The tool will never phone home. Network calls go only to the
user-configured endpoints (food databases, device APIs) and the
results are cached locally.

---

## What this document is NOT

This document does not define the concrete JSON schema for foods,
biomarkers, medications, diary entries, or units. Those are in:

- `docs/DATA_FORMAT.md` — JSON schema for each knowledge file
- `docs/DIARY_FORMAT.md` — Markdown + frontmatter schema for `data/diary/`
- `docs/MIGRATION_TO_JSON.md` — concrete plan and scripts for moving the
  current Python-authored data to JSON

This document does not define what analysis the tool does. That's in
the README and module docstrings.

This document is allowed to be opinionated. If a future feature
conflicts with these principles, the principles win and the feature
either bends or doesn't ship.

---

## Current state (honest)

The project is in transition. As of the N=1 rebrand:

- ✅ Principles written (this document).
- ✅ Directory layout: `core/` for the Python tool, `data/`,
  `patients/`, `archive/` present.
- ⚠️ Knowledge data is still Python-authored under
  `core/foods/data/legacy/*.py`, `core/bloodtests/biomarkers_db.py`,
  `core/medications/data/*.py`. This violates principle 5 today.
  The migration to JSON is planned and scripted; see
  `docs/MIGRATION_TO_JSON.md` (TODO).
- ⚠️ Diary format not yet specified beyond this document. See
  `docs/DIARY_FORMAT.md` (TODO).
- ⚠️ `MANIFEST.json` not yet generated. Will land with the first JSON
  knowledge file.
- ⚠️ `lib/` vs `core/` rename: the Python package is still
  `core` for backward compatibility. The `lib/n1/` rename is
  tracked in the migration doc.

The goal is for this "Current state" section to shrink to empty over
the next few releases. Until it does, this document is aspirational
guidance, not a description of present reality.
