#!/usr/bin/env python3
"""Audit image assets before a public skill release.

The local library may contain learning/reference images. A public package
requires a separate JSONL manifest with per-asset origin, license, hash, and
redistribution approval. This script is read-only by default; use `--strict`
as a release gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references" / "assets-manifest.jsonl"
ASSET_ROOTS = [
    ROOT / "db",
    ROOT / "references" / "layout-composition-images",
    ROOT / "references" / "awesome-images",
]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
REQUIRED_FIELDS = {"path", "sha256", "source_url", "license_spdx", "redistributable"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> tuple[dict[str, dict], list[str]]:
    entries: dict[str, dict] = {}
    errors: list[str] = []
    if not MANIFEST.exists():
        return entries, [f"missing manifest: {MANIFEST.relative_to(ROOT)}"]
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"line {number}: invalid JSON ({error.msg})")
            continue
        path = entry.get("path")
        if not isinstance(path, str):
            errors.append(f"line {number}: missing string path")
            continue
        entries[path.replace("\\", "/")] = entry
    return entries, errors


def image_files() -> list[Path]:
    return sorted(
        path for root in ASSET_ROOTS if root.exists() for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def initialize_manifest(files: list[Path]) -> None:
    if MANIFEST.exists():
        raise FileExistsError(f"manifest already exists: {MANIFEST}")
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    temporary = MANIFEST.with_name(f".{MANIFEST.name}.{os.getpid()}.tmp")
    reviewed_at = datetime.now(timezone.utc).isoformat()
    try:
        with temporary.open("w", encoding="utf-8", newline="\n") as handle:
            for path in files:
                entry = {
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": sha256(path),
                    "source_url": None,
                    "license_spdx": "NOASSERTION",
                    "redistributable": False,
                    "reviewed_at": reviewed_at,
                    "review_status": "unreviewed",
                }
                handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, MANIFEST)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit yh-image-inspirer image provenance")
    parser.add_argument("--strict", action="store_true", help="fail when any publishable image lacks approved provenance")
    parser.add_argument("--initialize-manifest", action="store_true", help="create a conservative hash inventory when no manifest exists")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    files = image_files()
    if args.initialize_manifest:
        try:
            initialize_manifest(files)
        except FileExistsError as error:
            print(f"ERROR: {error}", file=sys.stderr)
            return 2
        print(f"Initialized {MANIFEST.relative_to(ROOT)} with {len(files)} unreviewed assets.")
        return 0

    manifest, errors = load_manifest()
    unreviewed: list[str] = []
    mismatched_hashes: list[str] = []
    nonredistributable: list[str] = []
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        entry = manifest.get(relative)
        if not entry or not REQUIRED_FIELDS.issubset(entry):
            unreviewed.append(relative)
            continue
        if entry["sha256"] != sha256(path):
            mismatched_hashes.append(relative)
        if entry.get("redistributable") is not True:
            nonredistributable.append(relative)

    report = {
        "schema": "yh-image-inspirer.asset-audit.v1",
        "asset_count": len(files),
        "manifest_entries": len(manifest),
        "manifest_errors": errors,
        "unreviewed_count": len(unreviewed),
        "hash_mismatch_count": len(mismatched_hashes),
        "nonredistributable_count": len(nonredistributable),
        "samples": {
            "unreviewed": unreviewed[:20],
            "hash_mismatch": mismatched_hashes[:20],
            "nonredistributable": nonredistributable[:20],
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    blocked = bool(errors or unreviewed or mismatched_hashes or nonredistributable)
    return 1 if args.strict and blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
