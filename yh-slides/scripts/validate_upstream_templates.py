#!/usr/bin/env python3
"""Validate imported PPT Master SVG/spec assets without rendering or network access."""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT / "templates" / "upstream" / "ppt-master"
SOCIAL = ROOT.parent / "yh-social-visual" / "assets" / "upstream" / "ppt-master"
SVG_NS = "{http://www.w3.org/2000/svg}"


def number(value: str | None) -> float | None:
    if value is None:
        return None
    match = re.match(r"^\s*(-?\d+(?:\.\d+)?)", value)
    return float(match.group(1)) if match else None


def validate_svg(path: Path, errors: list[str]) -> None:
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        errors.append(f"{path}: invalid SVG: {exc}")
        return
    width, height = number(root.get("width")), number(root.get("height"))
    viewbox = root.get("viewBox", "").split()
    if width is None or height is None or len(viewbox) != 4:
        errors.append(f"{path}: missing numeric canvas dimensions/viewBox")
        return
    try:
        vx, vy, vw, vh = (float(item) for item in viewbox)
    except ValueError:
        errors.append(f"{path}: non-numeric viewBox")
        return
    if abs(width - vw) > 0.1 or abs(height - vh) > 0.1 or vx != 0 or vy != 0:
        errors.append(f"{path}: width/height and viewBox disagree")
    for element in root.iter():
        for key, value in element.attrib.items():
            if key.endswith("href") and re.match(r"^(?:https?:)?//", value, re.I):
                errors.append(f"{path}: external resource {value}")
        if element.tag == f"{SVG_NS}text":
            if not element.get("font-family"):
                errors.append(f"{path}: text element lacks font-family")
            x, y = number(element.get("x")), number(element.get("y"))
            if x is not None and not 0 <= x <= width:
                errors.append(f"{path}: text x={x} outside canvas")
            if y is not None and not 0 <= y <= height:
                errors.append(f"{path}: text y={y} outside canvas")
        bounds = element.get("data-pptx-bounds")
        if bounds:
            try:
                x, y, w, h = (float(item) for item in bounds.split())
            except ValueError:
                errors.append(f"{path}: malformed data-pptx-bounds={bounds!r}")
            else:
                if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > width + 0.1 or y + h > height + 0.1:
                    errors.append(f"{path}: placeholder bounds outside text-safe canvas: {bounds}")


def count_family(base: Path, family: str) -> int:
    return len(list((base / "layouts" / family / "templates").glob("*.svg")))


def main() -> int:
    errors: list[str] = []
    slide_source = json.loads((SLIDES / "SOURCE.json").read_text(encoding="utf-8"))
    social_source = json.loads((SOCIAL / "SOURCE.json").read_text(encoding="utf-8"))
    for family, expected in slide_source["imported"]["layouts"].items():
        actual = count_family(SLIDES, family)
        if actual != expected:
            errors.append(f"{family}: expected {expected} SVGs, found {actual}")
    for family, expected in social_source["imported"]["layouts"].items():
        actual = count_family(SOCIAL, family)
        if actual != expected:
            errors.append(f"{family}: expected {expected} SVGs, found {actual}")
    if len(list((SLIDES / "styles").glob("*/templates/design_spec.md"))) != 12:
        errors.append("expected 12 independent style specs")
    brand_specs = list((SLIDES / "brands").glob("*/templates/design_spec.md"))
    if len(brand_specs) != 15:
        errors.append("expected 15 independent brand specs")
    other_brand_files = [path for path in (SLIDES / "brands").rglob("*") if path.is_file() and path.name != "design_spec.md"]
    if other_brand_files:
        errors.append("brand namespace contains non-spec files (logos/assets are forbidden)")
    fact = set(slide_source["brand_evidence"]["fact_primary_values"])
    approx = set(slide_source["brand_evidence"]["approximate_reference_only"])
    if fact | approx != {path.parents[1].name for path in brand_specs} or fact & approx:
        errors.append("brand fact/approx classification does not cover the 15 specs exactly")
    for path in brand_specs:
        text = path.read_text(encoding="utf-8-sig").lower()
        brand = path.parents[1].name
        primary_row = re.search(r"\|\s*primary\s*\|[^\n]+\|\s*(fact|approx)\s*\|", text)
        expected = "fact" if brand in fact else "approx"
        if not primary_row or primary_row.group(1) != expected:
            errors.append(f"{brand}: primary provenance must be {expected}")
        if re.search(r"official\s+brand\s+(?:manual|guideline|specification)", text) and "not an official" not in text:
            errors.append(f"{brand}: misleading official-brand claim")
    for path in list((SLIDES / "layouts").rglob("*.svg")) + list((SOCIAL / "layouts").rglob("*.svg")):
        validate_svg(path, errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: PPT Master assets validated (39 presentation SVGs, 27 social SVGs, 12 styles, 15 brands, no logos/remotes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
