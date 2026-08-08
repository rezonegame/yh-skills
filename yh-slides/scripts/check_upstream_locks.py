#!/usr/bin/env python3
"""Verify absorbed upstream provenance locks are present and pinned."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK_DIR = ROOT / "provenance" / "upstream-locks"

EXPECTED = {
    "ppt-master": "328388d4e76778535676056f49be8f28a08e79b2",
    "guizang-ppt-skill": "82fe5ae129e8c2a12e1155fcabed6703342749d6",
    "html-ppt-skill": "f3a8435d3901697d5ac5e64d356c933637e43107",
    "ian-handdrawn-ppt": "b2cc5f303337e5470fd6ac2870d261a43b218439",
    "academic-pptx-skill": "9f2b703ffe8d1449851617665ab1ffb3516d54ac",
    "dashi-ppt-skill": "7cb23347f91cda1a5519eafc8c040704e389535a",
    "bento": "f51795b8e71496b11e13e53ce3f4c8a97a72a699",
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
        if name == "bento":
            artifact = ROOT / data.get("local_artifact", "")
            expected_hash = data.get("patched_sha256")
            if not artifact.is_file():
                errors.append(f"bento: missing pinned local artifact: {artifact}")
            elif not expected_hash:
                errors.append("bento: missing patched_sha256")
            else:
                actual_hash = hashlib.sha256(artifact.read_bytes()).hexdigest().upper()
                if actual_hash != expected_hash.upper():
                    errors.append(f"bento: pinned shell hash differs; expected {expected_hash}, found {actual_hash}")
    if errors:
        print("upstream lock check FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("upstream lock check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
