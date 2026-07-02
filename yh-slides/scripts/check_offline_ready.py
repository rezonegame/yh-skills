#!/usr/bin/env python3
"""Scan yh-slides native assets for hard online runtime dependencies."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SCAN_DIRS = [
    "assets/seeds",
    "assets/vendor",
    "assets/screenshot-backgrounds",
    "templates/html-decks",
]

REMOTE_RUNTIME_RE = re.compile(
    r"""(?:src|href)\s*=\s*["']https?://|@import\s+url\(["']?https?://|import\(["']https?://|url\(["']https?://""",
    re.IGNORECASE,
)

TEXT_SUFFIXES = {".html", ".css", ".js", ".mjs", ".json", ".md"}


def iter_files():
    for rel_dir in SCAN_DIRS:
        root = ROOT / rel_dir
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if "__pycache__" in path.parts or "node_modules" in path.parts:
                continue
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                yield path


def main() -> int:
    issues: list[str] = []
    for path in iter_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if REMOTE_RUNTIME_RE.search(line):
                rel = path.relative_to(ROOT)
                issues.append(f"{rel}:{line_no}: {line.strip()[:180]}")

    required_local = [
        "assets/vendor/google-fonts-local.css",
        "assets/vendor/js/lucide.min.js",
        "assets/vendor/js/motion.min.js",
        "references/meta/asset-registry.json",
    ]
    for rel in required_local:
        if not (ROOT / rel).exists():
            issues.append(f"missing offline runtime file: {rel}")

    if issues:
        print("offline readiness check FAILED:")
        for issue in issues[:200]:
            print(f"  - {issue}")
        if len(issues) > 200:
            print(f"  ... {len(issues) - 200} more")
        return 1
    print("offline readiness check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
