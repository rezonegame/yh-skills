#!/usr/bin/env python3
"""Validate local diagram primitives for accessibility and offline rendering."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = (
    ROOT / "assets/diagrams/timeline.html",
    ROOT / "assets/diagrams/flowchart.html",
    ROOT / "assets/diagrams/comparison.html",
    ROOT / "assets/diagrams/timeline.svg",
    ROOT / "assets/diagrams/comparison.svg",
    ROOT / "assets/diagrams/process.svg",
)
REMOTE_REF = re.compile(r"(?:src|href|xlink:href)\s*=\s*['\"]https?://", re.I)


def validate_html(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    if not any(token in text.lower() for token in ("<svg", "<figure", "<table")):
        errors.append("missing diagram structure")
    if REMOTE_REF.search(text) or "@import url(" in text.lower():
        errors.append("remote resource reference")
    if not any(token in text.lower() for token in ("<title", "aria-label", "aria-labelledby")):
        errors.append("missing accessible label")
    if path.stat().st_size > 250 * 1024:
        errors.append("HTML primitive exceeds 250 KB")
    return errors


def validate_svg(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    if path.stat().st_size > 50 * 1024:
        errors.append("SVG primitive exceeds 50 KB")
    if REMOTE_REF.search(text):
        errors.append("remote resource reference")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return [f"invalid XML: {exc}"]
    local = lambda tag: tag.rsplit("}", 1)[-1].lower()
    tags = [local(node.tag) for node in root.iter()]
    if local(root.tag) != "svg":
        errors.append("root element is not <svg>")
    if "title" not in tags:
        errors.append("missing <title>")
    if "desc" not in tags:
        errors.append("missing <desc>")
    if not root.attrib.get("viewBox"):
        errors.append("missing viewBox")
    if "script" in tags or "foreignobject" in tags:
        errors.append("script/foreignObject is not print-safe")
    return errors


def validate(path: Path) -> list[str]:
    if not path.is_file():
        return ["file not found"]
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".svg":
        return validate_svg(path, text)
    if path.suffix.lower() == ".html":
        return validate_html(path, text)
    return ["unsupported file type (expected .html or .svg)"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    paths = [p.resolve() for p in args.paths] or list(DEFAULTS)
    failures = 0
    for path in paths:
        errors = validate(path)
        label = path.name if path.parent == ROOT / "assets/diagrams" else str(path)
        if errors:
            failures += 1
            print(f"ERROR: {label}: {'; '.join(errors)}")
        else:
            print(f"OK: {label}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
