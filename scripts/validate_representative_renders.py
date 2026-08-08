#!/usr/bin/env python3
"""Validate the six offline representative render dimensions."""
from __future__ import annotations

import json
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "output" / "playwright" / "template-representatives" / "render-manifest.json"


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = []
    cases = data.get("cases", [])
    if len(cases) != 6 or data.get("network") is not False:
        errors.append("manifest must contain six offline cases")
    for case in cases:
        output = ROOT / case["output"]
        actual = png_size(output) if output.is_file() else None
        expected = (case["width"], case["height"])
        if actual != expected:
            errors.append(f"{case['name']}: expected {expected}, found {actual}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: six representative renders have exact 4:3, 16:9, 3:4, 9:16, and 1:1 canvases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
