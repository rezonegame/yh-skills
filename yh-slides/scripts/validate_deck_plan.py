#!/usr/bin/env python3
"""Validate a path-neutral yh-slides deck plan without third-party dependencies."""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath

DEFAULT_TEMPLATE_MARKERS = ("ai capital", "soundwave", "key metrics", "end of report", "请输入文本", "lorem ipsum")
ALLOWED_ROUTES = {"2A", "2A-S", "2A-T", "2B", "2C", "2B-R", "2D"}
COMPOSITION_FAMILIES = {
    "hero", "split", "metric-spotlight", "chart-led", "timeline", "matrix",
    "editorial", "comparison", "process", "custom",
}


def safe_relative_path(value: str) -> bool:
    candidate = PurePosixPath(value.replace("\\", "/"))
    return bool(value) and not candidate.is_absolute() and ".." not in candidate.parts


def validate(data: object, project_root: Path | None) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["plan must be a JSON object"]
    for field in ("title", "goal", "audience", "route", "pages"):
        if field not in data:
            errors.append(f"missing top-level field: {field}")
    for field in ("title", "goal", "audience"):
        if not isinstance(data.get(field), str) or not data.get(field, "").strip():
            errors.append(f"{field} must be a non-empty string")
    if data.get("route") not in ALLOWED_ROUTES:
        errors.append(f"route must be one of {', '.join(sorted(ALLOWED_ROUTES))}")
    pages = data.get("pages")
    if not isinstance(pages, list) or not pages:
        return errors + ["pages must be a non-empty list"]
    markers = [marker.lower() for marker in DEFAULT_TEMPLATE_MARKERS]
    markers.extend(str(value).lower() for value in data.get("forbidden_copy", []) if isinstance(value, str))
    seen_ids: set[str] = set()
    seen_layouts: set[str] = set()
    seen_media: set[str] = set()
    previous_family: str | None = None
    family_run = 0
    for number, page in enumerate(pages, start=1):
        prefix = f"pages[{number}]"
        if not isinstance(page, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in ("id", "role", "title", "copy"):
            if not isinstance(page.get(field), str) or not page.get(field, "").strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")
        page_id = page.get("id")
        if isinstance(page_id, str):
            if page_id in seen_ids:
                errors.append(f"{prefix}.id duplicates {page_id}")
            seen_ids.add(page_id)
        layout = page.get("layout_id")
        if layout is not None:
            if not isinstance(layout, str) or not layout.strip():
                errors.append(f"{prefix}.layout_id must be a non-empty string when supplied")
            elif layout in seen_layouts and not page.get("allow_layout_reuse", False):
                errors.append(f"{prefix}.layout_id duplicates {layout}")
            else:
                seen_layouts.add(layout)
        candidates = page.get("layout_candidates")
        selected_family = page.get("composition_family")
        if candidates is not None:
            if not isinstance(candidates, list) or not 2 <= len(candidates) <= 4:
                errors.append(f"{prefix}.layout_candidates must contain 2 to 4 candidates")
            else:
                candidate_ids: set[str] = set()
                candidate_families: set[str] = set()
                for candidate_number, candidate in enumerate(candidates, start=1):
                    key = f"{prefix}.layout_candidates[{candidate_number}]"
                    if not isinstance(candidate, dict):
                        errors.append(f"{key} must be an object")
                        continue
                    candidate_id = candidate.get("id")
                    family = candidate.get("family")
                    if not isinstance(candidate_id, str) or not candidate_id.strip():
                        errors.append(f"{key}.id must be a non-empty string")
                    elif candidate_id in candidate_ids:
                        errors.append(f"{key}.id duplicates {candidate_id}")
                    else:
                        candidate_ids.add(candidate_id)
                    if family not in COMPOSITION_FAMILIES:
                        errors.append(f"{key}.family is not a supported composition family")
                    else:
                        candidate_families.add(family)
                    if candidate_id == layout:
                        selected_family = family
                if len(candidate_families) < 2:
                    errors.append(f"{prefix}.layout_candidates must span at least two composition families")
                if isinstance(layout, str) and layout not in candidate_ids:
                    errors.append(f"{prefix}.layout_id must be one of layout_candidates")
            package = page.get("content_package")
            if not isinstance(package, dict):
                errors.append(f"{prefix}.content_package is required with layout_candidates")
            else:
                facts = package.get("required_facts")
                if not isinstance(facts, list) or not all(isinstance(item, str) and item.strip() for item in facts):
                    errors.append(f"{prefix}.content_package.required_facts must be a string list")
        if selected_family is not None and selected_family not in COMPOSITION_FAMILIES:
            errors.append(f"{prefix}.composition_family is not supported")
        elif selected_family:
            family_run = family_run + 1 if selected_family == previous_family else 1
            previous_family = selected_family
            if family_run > 2 and not page.get("allow_family_run", False):
                errors.append(f"{prefix}.composition_family repeats more than twice consecutively")
        copy = page.get("copy")
        if isinstance(copy, str):
            for marker in markers:
                if marker and marker in copy.lower():
                    errors.append(f"{prefix}.copy contains template marker: {marker}")
            budget = page.get("copy_budget")
            if budget is not None and (not isinstance(budget, int) or budget < 1 or len(copy) > budget):
                errors.append(f"{prefix}.copy exceeds copy_budget")
        if page.get("chart_data") is not None and (not isinstance(page.get("insight"), str) or not page["insight"].strip()):
            errors.append(f"{prefix} has chart_data but no insight")
        media = page.get("media", [])
        if not isinstance(media, list):
            errors.append(f"{prefix}.media must be a list")
            continue
        for media_number, item in enumerate(media, start=1):
            key = f"{prefix}.media[{media_number}]"
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                errors.append(f"{key} must contain a string path")
                continue
            path = item["path"]
            if not safe_relative_path(path):
                errors.append(f"{key}.path must be a safe relative path")
            elif project_root and not (project_root / path).is_file():
                errors.append(f"{key}.path does not exist under project root: {path}")
            if path in seen_media and not item.get("allow_reuse", False):
                errors.append(f"{key}.path reuses media without allow_reuse: {path}")
            seen_media.add(path)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="validate yh-slides deck-plan.json")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--project-root", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read plan: {exc}")
        return 2
    errors = validate(data, args.project_root.resolve() if args.project_root else None)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: deck plan validated ({len(data['pages'])} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
