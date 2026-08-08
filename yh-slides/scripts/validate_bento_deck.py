#!/usr/bin/env python3
"""Validate a local yh-slides Bento deck plan before it is assembled.

The validator deliberately checks the portable planning subset rather than the
vendored Bento runtime.  This keeps the generated deck offline by default and
makes slide IDs stable enough for morph/state transitions and review comments.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SCHEMA = "yh_slides_bento_deck.v1"
ALLOWED_TRANSITIONS = {"none", "fade", "slide", "zoom", "morph"}
ALLOWED_TYPES = {"text", "shape", "image", "svg", "chart", "table", "media"}
REMOTE_RE = re.compile(r"^https?://", re.IGNORECASE)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _bounds(element: dict[str, Any], width: int, height: int, label: str, errors: list[str]) -> None:
    for key in ("x", "y", "w", "h"):
        if not _is_number(element.get(key)):
            errors.append(f"{label}: {key} must be a number")
    if any(not _is_number(element.get(key)) for key in ("x", "y", "w", "h")):
        return
    if element["x"] < 0 or element["y"] < 0 or element["w"] <= 0 or element["h"] <= 0:
        errors.append(f"{label}: x/y must be non-negative and w/h positive")
    if element["x"] + element["w"] > width or element["y"] + element["h"] > height:
        errors.append(f"{label}: bounds exceed the {width}x{height} canvas")


def _check_source(src: Any, assets: dict[str, Any], allow_external_media: bool, label: str, errors: list[str]) -> None:
    if not _nonempty(src):
        errors.append(f"{label}: src is required")
        return
    if src.startswith("asset:"):
        key = src.removeprefix("asset:")
        if key not in assets:
            errors.append(f"{label}: asset '{key}' is not declared")
    elif REMOTE_RE.match(src) and not allow_external_media:
        errors.append(f"{label}: remote src is disabled; use a data URI or declared asset")
    elif not (src.startswith("data:") or REMOTE_RE.match(src)):
        errors.append(f"{label}: src must be data:, asset:, or an explicitly allowed https URL")


def validate(plan: dict[str, Any], deck_plan: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if plan.get("schema") != SCHEMA:
        errors.append(f"schema must be '{SCHEMA}'")
    if not _nonempty(plan.get("title")):
        errors.append("title is required")
    size = plan.get("size", {"width": 1280, "height": 720})
    if not isinstance(size, dict) or not all(isinstance(size.get(key), int) and size[key] > 0 for key in ("width", "height")):
        errors.append("size must contain positive integer width and height")
        width, height = 1280, 720
    else:
        width, height = size["width"], size["height"]
    assets = plan.get("assets", {})
    if not isinstance(assets, dict):
        errors.append("assets must be an object keyed by asset ID")
        assets = {}
    for key, value in assets.items():
        if not _nonempty(key) or not _nonempty(value):
            errors.append("assets must contain non-empty keys and values")
        elif REMOTE_RE.match(value):
            errors.append(f"asset '{key}' is remote; Bento decks are offline by default")
    slides = plan.get("slides")
    if not isinstance(slides, list) or not slides:
        return errors + ["slides must be a non-empty list"]
    allow_external_media = plan.get("allow_external_media") is True
    slide_ids: set[str] = set()
    element_ids_by_slide: list[set[str]] = []
    all_slide_ids = {slide.get("id") for slide in slides if isinstance(slide, dict)}
    for slide_index, slide in enumerate(slides, start=1):
        label = f"slide {slide_index}"
        if not isinstance(slide, dict):
            errors.append(f"{label}: must be an object")
            element_ids_by_slide.append(set())
            continue
        slide_id = slide.get("id")
        if not _nonempty(slide_id):
            errors.append(f"{label}: id is required")
        elif slide_id in slide_ids:
            errors.append(f"{label}: duplicate slide id '{slide_id}'")
        else:
            slide_ids.add(slide_id)
        if not _nonempty(slide.get("name")):
            errors.append(f"{label}: name is required")
        if not _nonempty(slide.get("notes")):
            errors.append(f"{label}: notes are required for the review/presenter loop")
        transition = slide.get("transition", "none")
        if transition not in ALLOWED_TRANSITIONS:
            errors.append(f"{label}: unsupported transition '{transition}'")
        if slide.get("state_of") and slide["state_of"] not in all_slide_ids:
            errors.append(f"{label}: state_of must reference a slide id")
        elements = slide.get("elements")
        if not isinstance(elements, list) or not elements:
            errors.append(f"{label}: elements must be a non-empty list")
            element_ids_by_slide.append(set())
            continue
        element_ids: set[str] = set()
        for element_index, element in enumerate(elements, start=1):
            element_label = f"{label} element {element_index}"
            if not isinstance(element, dict):
                errors.append(f"{element_label}: must be an object")
                continue
            if not _nonempty(element.get("id")):
                errors.append(f"{element_label}: stable id is required")
            elif element["id"] in element_ids:
                errors.append(f"{element_label}: duplicate element id '{element['id']}'")
            else:
                element_ids.add(element["id"])
            kind = element.get("type")
            if kind not in ALLOWED_TYPES:
                errors.append(f"{element_label}: unsupported type '{kind}'")
            _bounds(element, width, height, element_label, errors)
            if kind == "text" and not _nonempty(element.get("html")):
                errors.append(f"{element_label}: text html is required")
            if kind in {"image", "svg", "media"}:
                _check_source(element.get("src"), assets, allow_external_media and kind == "media", element_label, errors)
            if kind == "chart" and not isinstance(element.get("option"), dict):
                errors.append(f"{element_label}: chart option must be an object")
            if kind == "table" and (not isinstance(element.get("columns"), list) or not isinstance(element.get("rows"), list)):
                errors.append(f"{element_label}: table needs columns and rows lists")
        element_ids_by_slide.append(element_ids)
    for index, slide in enumerate(slides):
        if not isinstance(slide, dict) or slide.get("transition") != "morph" or index == 0:
            continue
        if not (element_ids_by_slide[index] & element_ids_by_slide[index - 1]):
            errors.append(f"slide {index + 1}: morph transition needs a stable element id shared with the prior slide")
    if deck_plan is not None:
        planned_ids = [page.get("id") for page in deck_plan.get("pages", []) if isinstance(page, dict)]
        bento_ids = [slide.get("id") for slide in slides if isinstance(slide, dict)]
        if planned_ids and planned_ids != bento_ids:
            errors.append("Bento slide ids/order must match deck-plan.json pages")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--deck-plan", type=Path)
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        deck_plan = json.loads(args.deck_plan.read_text(encoding="utf-8")) if args.deck_plan else None
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Bento plan read failed: {exc}")
        return 1
    errors = validate(plan, deck_plan)
    if errors:
        print("Bento deck validation FAILED:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Bento deck validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
