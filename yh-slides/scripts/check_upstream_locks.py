#!/usr/bin/env python3
"""Verify absorbed upstream provenance locks are present and pinned."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK_DIR = ROOT / "provenance" / "upstream-locks"

EXPECTED = {
    "ppt-master": "328388d4e76778535676056f49be8f28a08e79b2",
    "guizang-ppt-skill": "82fe5ae129e8c2a12e1155fcabed6703342749d6",
    "html-ppt-skill": "f3a8435d3901697d5ac5e64d356c933637e43107",
    "ian-handdrawn-ppt": "b2cc5f303337e5470fd6ac2870d261a43b218439",
}


def main() -> int:
    errors: list[str] = []
    for name, commit in EXPECTED.items():
        path = LOCK_DIR / f"{name}.source.json"
        if not path.exists():
            errors.append(f"missing lock: {path}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid lock JSON for {name}: {exc}")
            continue
        if data.get("commit") != commit:
            errors.append(f"{name}: expected {commit}, found {data.get('commit')}")
    if errors:
        print("upstream lock check FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("upstream lock check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
