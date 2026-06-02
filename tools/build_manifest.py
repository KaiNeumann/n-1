"""
tools/build_manifest.py

Generates MANIFEST.json with SHA256 of every file under knowledge/.
Idempotent; re-run after any knowledge/ change.

Run:
    python tools/build_manifest.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = REPO_ROOT / "knowledge"
MANIFEST_PATH = REPO_ROOT / "MANIFEST.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not KNOWLEDGE_DIR.exists():
        print(f"ERROR: {KNOWLEDGE_DIR} does not exist", file=sys.stderr)
        return 1

    files: dict = {}
    for path in sorted(KNOWLEDGE_DIR.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        files[rel] = {
            "sha256": sha256_file(path),
            "size": path.stat().st_size,
        }

    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "knowledge_root": "knowledge/",
        "file_count": len(files),
        "files": files,
    }

    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {MANIFEST_PATH} ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
