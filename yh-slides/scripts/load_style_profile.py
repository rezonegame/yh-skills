#!/usr/bin/env python3
"""Load an explicitly named slides style profile; never search for one."""
from __future__ import annotations

import json
import os
from pathlib import Path

from validate_style_profile import validate


def load(explicit_route: str | None = None) -> dict | None:
    raw = os.environ.get("YH_SLIDES_STYLE_PROFILE")
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        raise ValueError("YH_SLIDES_STYLE_PROFILE must be an absolute path")
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(data, explicit_route)
    if errors:
        raise ValueError("; ".join(errors))
    return data


if __name__ == "__main__":
    try:
        profile = load()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1)
    print(json.dumps(profile or {}, ensure_ascii=False, sort_keys=True))
