#!/usr/bin/env python3
"""Validate the recorded isolated MarkItDown 0.1.7 regression evidence offline."""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "provenance" / "markitdown-0.1.7-validation.json"
TEST = ROOT / "yh-local-knowledge" / "scripts" / "tests" / "test_markitdown_017.py"
EXPECTED_COMMIT = "fd239d5d2be43d9b68329730206b9312c7d5a388"


def main() -> int:
    failures: list[str] = []
    try:
        data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: invalid MarkItDown evidence: {exc}")
        return 1

    expected = {
        "schema": "yh-skills.upstream-validation.v1",
        "tag": "v0.1.7",
        "commit": EXPECTED_COMMIT,
        "package_version": "0.1.7",
        "result": "passed: 2 tests",
    }
    for field, value in expected.items():
        if data.get(field) != value:
            failures.append(f"{field} mismatch: expected {value!r}, got {data.get(field)!r}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(data.get("validated_at", ""))):
        failures.append("validated_at is not an ISO date")
    if "isolated" not in str(data.get("environment", "")).lower() and "temporary" not in str(data.get("environment", "")).lower():
        failures.append("environment does not record isolation")
    fixtures = data.get("fixtures", [])
    if not isinstance(fixtures, list) or not any("OMML" in str(item) for item in fixtures):
        failures.append("OMML fixture evidence is missing")
    try:
        test_source = TEST.read_text(encoding="utf-8")
    except OSError as exc:
        failures.append(f"regression test missing: {exc}")
    else:
        for marker in ("m:oMath", "test_plain_docx_heading_table_body", "test_omml_formula_heading_table_body"):
            if marker not in test_source:
                failures.append(f"regression test is missing marker: {marker}")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1
    print(f"OK: MarkItDown 0.1.7 isolated evidence verified at {EXPECTED_COMMIT[:8]} (plain + OMML DOCX)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
