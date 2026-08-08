#!/usr/bin/env python3
"""Validate a self-contained yh-slides design brief without third-party deps."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(data: object, deck_plan: object | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["brief must be a JSON object"]
    for field in ("title", "objective", "audience", "speaker_notes_strategy"):
        if not _nonempty(data.get(field)):
            errors.append(f"{field} must be a non-empty string")
    canvas = data.get("canvas")
    if not isinstance(canvas, dict) or not _nonempty(canvas.get("aspect_ratio")):
        errors.append("canvas.aspect_ratio must be a non-empty string")
    visual = data.get("visual_system")
    if not isinstance(visual, dict):
        errors.append("visual_system must be an object")
    else:
        for field in ("mood", "typography", "colour_roles"):
            value = visual.get(field)
            if field == "colour_roles":
                ok = isinstance(value, dict) and bool(value) and all(_nonempty(k) and _nonempty(v) for k, v in value.items())
            else:
                ok = _nonempty(value)
            if not ok:
                errors.append(f"visual_system.{field} must be specified")
    principles = data.get("layout_principles")
    if not isinstance(principles, list) or not principles or not all(_nonempty(item) for item in principles):
        errors.append("layout_principles must be a non-empty list of strings")
    pages = data.get("pages")
    if not isinstance(pages, list) or not pages:
        return errors + ["pages must be a non-empty list"]
    ids: list[str] = []
    has_ai_images = False
    for index, page in enumerate(pages, start=1):
        prefix = f"pages[{index}]"
        if not isinstance(page, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in ("id", "purpose", "audience_move"):
            if not _nonempty(page.get(field)):
                errors.append(f"{prefix}.{field} must be a non-empty string")
        page_id = page.get("id")
        if isinstance(page_id, str):
            if page_id in ids:
                errors.append(f"{prefix}.id duplicates {page_id}")
            ids.append(page_id)
        has_ai_images = has_ai_images or page.get("has_ai_images") is True
    if has_ai_images and (not isinstance(visual, dict) or not _nonempty(visual.get("ai_image_strategy"))):
        errors.append("visual_system.ai_image_strategy is required when a page has_ai_images")
    if deck_plan is not None:
        plan_pages = deck_plan.get("pages") if isinstance(deck_plan, dict) else None
        plan_ids = [page.get("id") for page in plan_pages if isinstance(page, dict) and isinstance(page.get("id"), str)] if isinstance(plan_pages, list) else []
        if ids != plan_ids:
            errors.append("brief page IDs must exactly match deck-plan page IDs and order")
    return errors


def _load(path: Path, label: str) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {label}: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="validate yh-slides design-brief.json")
    parser.add_argument("brief", type=Path)
    parser.add_argument("--deck-plan", type=Path)
    args = parser.parse_args()
    try:
        data = _load(args.brief, "brief")
        plan = _load(args.deck_plan, "deck plan") if args.deck_plan else None
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2
    errors = validate(data, plan)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: design brief validated ({len(data['pages'])} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
