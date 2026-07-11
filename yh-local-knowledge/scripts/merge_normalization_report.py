#!/usr/bin/env python3
"""Atomically merge normalization results into a workspace manifest."""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def atomic_write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    workspace = Path(args.workspace).resolve()
    knowledge = workspace / ".knowledge"
    manifest_path = knowledge / "manifest.json"
    report_path = knowledge / "normalization-report.json"
    if not manifest_path.is_file() or not report_path.is_file():
        print("ERROR: run workspace initialization and normalize.py --write-report first")
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    by_path = {item.get("path"): item for item in report.get("files", []) if item.get("path")}
    updated = 0
    for entry in manifest.get("files", []):
        item = by_path.pop(entry.get("path"), None)
        if item is None:
            continue
        entry["normalized_path"] = item.get("normalized_path")
        entry["normalization_status"] = item.get("normalization_status")
        entry["normalization_error"] = item.get("normalization_error")
        if item.get("source_sha256"):
            entry["hash"] = item["source_sha256"]
        updated += 1
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    summary = {"updated": updated, "unmatched_report_entries": sorted(by_path)}
    if args.dry_run:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    atomic_write_json(manifest_path, manifest)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
