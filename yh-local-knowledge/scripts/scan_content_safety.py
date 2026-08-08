#!/usr/bin/env python3
"""Advisory content-safety scan for normalized knowledge and skill packs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from content_safety import scan_text


MAX_FILES = 2_000
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 30 * 1024 * 1024
TEXT_SUFFIXES = {".md", ".txt", ".rst", ".adoc", ".html", ".htm"}


def collect(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(
        (candidate for candidate in path.rglob("*") if candidate.is_file() and candidate.suffix.lower() in TEXT_SUFFIXES),
        key=lambda candidate: candidate.as_posix().lower(),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    requested = args.path.resolve()
    if not requested.exists() or requested.is_symlink():
        print(json.dumps({"error": "path must exist and must not be a symbolic link"}))
        return 2

    files = collect(requested)
    if len(files) > MAX_FILES:
        print(json.dumps({"error": f"more than {MAX_FILES} text files"}))
        return 2

    total = 0
    results: list[dict[str, object]] = []
    root = requested if requested.is_dir() else requested.parent
    for path in files:
        if path.is_symlink():
            results.append({"path": str(path.relative_to(root)), "rule_id": "path.symlink", "line": 0})
            continue
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            results.append({"path": str(path.relative_to(root)), "rule_id": "size.file_limit", "line": 0})
            continue
        total += size
        if total > MAX_TOTAL_BYTES:
            print(json.dumps({"error": f"text exceeds {MAX_TOTAL_BYTES} bytes"}))
            return 2
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError):
            results.append({"path": str(path.relative_to(root)), "rule_id": "encoding.invalid_utf8", "line": 0})
            continue
        for finding in scan_text(text):
            results.append(
                {
                    "path": str(path.relative_to(root)),
                    "line": finding.line,
                    "rule_id": finding.rule_id,
                    "message": finding.message,
                }
            )

    print(json.dumps({"path": str(requested), "files_scanned": len(files), "findings": results}, ensure_ascii=False, indent=2))
    return 1 if results else 0


if __name__ == "__main__":
    raise SystemExit(main())
