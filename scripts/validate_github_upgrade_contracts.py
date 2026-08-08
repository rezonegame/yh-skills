#!/usr/bin/env python3
"""Offline validation of the GitHub-selective upgrade contracts."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "provenance" / "yh-github-adoption-decisions.json"


def main() -> int:
    try:
        data = json.loads(DECISIONS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read decisions: {exc}")
        return 2
    failures: list[str] = []
    if data.get("schema") != "yh-skills.github-adoption-decisions.v1":
        failures.append("unexpected decision schema")
    decisions = data.get("decisions")
    if not isinstance(decisions, list) or len(decisions) < 8:
        failures.append("expected at least eight source decisions")
    else:
        for index, decision in enumerate(decisions, 1):
            if not isinstance(decision, dict):
                failures.append(f"decision {index} is not an object")
                continue
            for field in ("target", "source", "license", "decision", "material", "test", "rollback"):
                if not isinstance(decision.get(field), str) or not decision[field].strip():
                    failures.append(f"decision {index} missing {field}")
            if not re.fullmatch(r"[0-9a-f]{40}", str(decision.get("commit", ""))):
                failures.append(f"decision {index} has invalid commit")
    command = [sys.executable, str(ROOT / "scripts" / "validate_yh_skills.py"), "--provenance"]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, encoding="utf-8")
    if result.returncode:
        failures.append(result.stdout.strip() or result.stderr.strip() or "base validator failed")
    checks = [
        [
            sys.executable,
            "-m",
            "unittest",
            "yh-slides/scripts/tests/test_validate_academic_deck.py",
            "yh-slides/scripts/tests/test_style_profile.py",
            "yh-local-knowledge/scripts/tests/test_input_policy.py",
            "yh-local-knowledge/scripts/tests/test_content_safety.py",
            "yh-image-inspirer/scripts/test_validate_asset_intent.py",
        ],
        [sys.executable, "yh-humanizer/scripts/validate_voice_profile_cases.py"],
        [sys.executable, "yh-document-studio/scripts/check_diagram_contract.py"],
        ["node", "yh-social-visual/scripts/tests/test_social_preset.mjs"],
    ]
    for check in checks:
        run = subprocess.run(check, cwd=ROOT, text=True, capture_output=True, encoding="utf-8")
        if run.returncode:
            failures.append(run.stdout.strip() or run.stderr.strip() or f"contract check failed: {' '.join(check)}")
    for failure in failures:
        print(f"ERROR: {failure}")
    if failures:
        return 1
    print("OK: GitHub adoption decisions and base YH validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
