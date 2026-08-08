#!/usr/bin/env python3
"""Validate a delivery brief and every declared material, asset, and screenshot."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from artifact_contract import validate_delivery_brief, validate_required_files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path)
    args = parser.parse_args()
    brief_path = args.brief.resolve()
    data = json.loads(brief_path.read_text(encoding="utf-8-sig"))
    root = brief_path.parent
    errors = validate_delivery_brief(data)
    for field, label in (("materials", "material"), ("assets", "asset"), ("screenshots", "screenshot")):
        values = data.get(field, [])
        if not isinstance(values, list):
            errors.append(f"delivery brief {field} must be an array")
        else:
            errors.extend(validate_required_files(root, values, label=label))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: delivery contract is closed (brief, capabilities, materials, assets, screenshots)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
