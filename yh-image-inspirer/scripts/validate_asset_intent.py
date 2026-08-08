#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath


def _safe(value: object) -> bool:
    return isinstance(value, str) and bool(value) and not PurePosixPath(value.replace("\\", "/")).is_absolute() and ".." not in PurePosixPath(value.replace("\\", "/")).parts


def validate(data: object, project_root: Path | None = None) -> list[str]:
    if not isinstance(data, dict): return ["intent must be an object"]
    errors = []
    operation = data.get("operation")
    if operation not in {"generate", "edit"}: errors.append("operation must be generate or edit")
    if not isinstance(data.get("consumer"), str) or not data["consumer"].strip(): errors.append("consumer is required")
    destination = data.get("destination")
    if not _safe(destination): errors.append("destination must be a safe relative path")
    elif project_root and (project_root / destination).exists() and not data.get("replace_explicitly", False): errors.append("destination exists; use a versioned sibling or replace_explicitly")
    if operation == "edit":
        if not isinstance(data.get("inputs"), list) or not data["inputs"]: errors.append("edit requires inputs")
        if not isinstance(data.get("immutable_constraints"), list) or not data["immutable_constraints"]: errors.append("edit requires immutable_constraints")
    return errors


def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("intent", type=Path); p.add_argument("--project-root", type=Path); a = p.parse_args()
    try: errors = validate(json.loads(a.intent.read_text(encoding="utf-8")), a.project_root.resolve() if a.project_root else None)
    except (OSError, json.JSONDecodeError) as exc: print(f"ERROR: {exc}"); return 2
    for error in errors: print(f"ERROR: {error}")
    if errors: return 1
    print("OK: asset intent validated"); return 0


if __name__ == "__main__": raise SystemExit(main())
