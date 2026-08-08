#!/usr/bin/env python3
"""Validate opt-in yh-slides personal style profiles."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROUTES = {"2A", "2A-S", "2A-T", "2B", "2C", "2B-R", "2D"}
FORBIDDEN = {"api_key", "token", "secret", "model", "provider", "script", "command", "env_file"}


def validate(data: object, explicit_route: str | None = None) -> list[str]:
    if not isinstance(data, dict):
        return ["style profile must be a JSON object"]
    errors: list[str] = []
    if set(data).intersection(FORBIDDEN):
        errors.append("style profile contains forbidden execution or secret fields")
    palette = data.get("palette")
    if not isinstance(palette, dict) or not palette or not all(isinstance(k, str) and isinstance(v, str) and v.strip() for k, v in palette.items()):
        errors.append("palette must be a non-empty string map")
    for field in ("typography", "density"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{field} must be a non-empty string")
    route = data.get("preferred_route")
    if route not in ROUTES:
        errors.append("preferred_route is not a supported route")
    if explicit_route and route != explicit_route:
        errors.append("explicit project route conflicts with profile preferred_route")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="validate yh-slides style profile")
    parser.add_argument("profile", type=Path)
    parser.add_argument("--explicit-route")
    args = parser.parse_args()
    if not args.profile.is_absolute():
        print("ERROR: profile path must be explicit and absolute")
        return 2
    try:
        data = json.loads(args.profile.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read profile: {exc}")
        return 2
    errors = validate(data, args.explicit_route)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: style profile validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
