#!/usr/bin/env python3
"""Verify release identity, package contents, required files, and evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

from artifact_contract import validate_required_files


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_sha(root: Path) -> str | None:
    result = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def validate_manifest(manifest: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    identity = manifest.get("identity", {})
    for field in ("name", "version", "git_sha"):
        if not identity.get(field):
            errors.append(f"missing release identity field: {field}")
    if identity.get("name") != "yh-document-studio":
        errors.append("package identity name mismatch")
    actual_git = git_sha(root)
    if actual_git != identity.get("git_sha"):
        errors.append(f"Git SHA mismatch: expected {identity.get('git_sha')}, actual {actual_git}")

    package = manifest.get("package", {})
    package_path = root / str(package.get("path", ""))
    if not package_path.is_file():
        errors.append(f"package missing: {package.get('path')}")
    else:
        expected_hash = str(package.get("sha256", "")).lower()
        if not expected_hash or sha256(package_path) != expected_hash:
            errors.append("package SHA-256 mismatch")
        if package_path.suffix.lower() == ".zip":
            try:
                with zipfile.ZipFile(package_path) as archive:
                    members = set(archive.namelist())
            except zipfile.BadZipFile:
                errors.append("package is not a valid ZIP")
            else:
                for member in package.get("required_members", []):
                    if member not in members:
                        errors.append(f"package member missing: {member}")

    errors.extend(validate_required_files(root, manifest.get("required_files", []), label="release file"))
    evidence = manifest.get("validation_evidence", [])
    if not evidence:
        errors.append("validation evidence list is empty")
    else:
        errors.extend(validate_required_files(root, evidence, label="validation evidence"))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    errors = validate_manifest(data, ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: release gate passed for {data['identity']['name']} {data['identity']['version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
