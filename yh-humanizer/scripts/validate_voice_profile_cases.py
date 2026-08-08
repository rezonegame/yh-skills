#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ALLOWED = {"quiet-editorial", "plain-technical", "warm-column", "crisp-business", "curated-reading"}

def main() -> int:
    path = Path(__file__).resolve().parents[1] / "evals" / "voice-profile-cases.json"
    try: data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: print(f"ERROR: {exc}"); return 2
    errors=[]
    if data.get("schema") != "yh-humanizer.voice-profile-cases.v1": errors.append("schema")
    for i, case in enumerate(data.get("cases", []), 1):
        if case.get("profile") not in ALLOWED: errors.append(f"case {i}: profile")
        for literal in case.get("required_literals", []):
            if literal not in case.get("candidate", ""): errors.append(f"case {i}: lost {literal}")
    for error in errors: print(f"ERROR: {error}")
    if errors: return 1
    print(f"OK: voice profile fixtures validated ({len(data['cases'])} cases)"); return 0

if __name__ == "__main__": raise SystemExit(main())
