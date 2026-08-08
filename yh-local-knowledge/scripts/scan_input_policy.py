#!/usr/bin/env python3
"""Scan a source root against the untrusted-input policy without converting."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from input_policy import reject_reason


def main() -> int:
    parser = argparse.ArgumentParser(description="scan untrusted knowledge inputs")
    parser.add_argument("source_root", type=Path)
    args = parser.parse_args()
    root = args.source_root.resolve()
    if not root.is_dir():
        print("ERROR: source_root must be an existing directory")
        return 2
    rejected = []
    for path in root.rglob("*"):
        if path.is_file() or path.is_symlink():
            reason = reject_reason(path, root)
            if reason:
                rejected.append({"path": str(path.relative_to(root)), "reason": reason})
    print(json.dumps({"source_root": str(root), "rejected": rejected}, ensure_ascii=False, indent=2))
    return 1 if rejected else 0


if __name__ == "__main__":
    raise SystemExit(main())
