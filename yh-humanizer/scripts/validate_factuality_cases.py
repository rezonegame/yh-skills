#!/usr/bin/env python3
"""Validate factuality regression fixtures for yh-humanizer output reviews."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate(data: object) -> list[str]:
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        return ["cases file must contain a cases array"]
    errors: list[str] = []
    ids: set[str] = set()
    for number, case in enumerate(data["cases"], start=1):
        prefix = f"cases[{number}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{prefix}.id must be a non-empty string")
        elif case_id in ids:
            errors.append(f"{prefix}.id duplicates {case_id}")
        else:
            ids.add(case_id)
        candidate = case.get("candidate")
        if not isinstance(candidate, str) or not candidate.strip():
            errors.append(f"{prefix}.candidate must be a non-empty string")
            continue
        for literal in case.get("required_literals", []):
            if not isinstance(literal, str) or not literal:
                errors.append(f"{prefix}.required_literals contains an invalid literal")
            elif literal not in candidate:
                errors.append(f"{prefix}: candidate lost required fact: {literal}")
        for literal in case.get("forbidden_literals", []):
            if not isinstance(literal, str) or not literal:
                errors.append(f"{prefix}.forbidden_literals contains an invalid literal")
            elif literal in candidate:
                errors.append(f"{prefix}: candidate invents or asserts forbidden text: {literal}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="validate yh-humanizer factuality regression cases")
    parser.add_argument("cases", type=Path, nargs="?", default=Path(__file__).resolve().parents[1] / "evals" / "factuality-cases.json")
    args = parser.parse_args()
    try:
        data = json.loads(args.cases.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read cases: {exc}")
        return 2
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: factuality fixtures validated ({len(data['cases'])} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
