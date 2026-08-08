#!/usr/bin/env python3
"""Validate BCP-47, direction, font slots, flow modes, and group consistency."""
from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
from svg_to_pptx.text_contract import text_direction, text_flow_mode, validate_bcp47


XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        return [f"invalid SVG: {exc}"]
    root_lang = root.get("lang") or root.get(XML_LANG) or "zh-CN"
    groups: dict[str, tuple] = {}
    for element in root.iter():
        if not element.tag.endswith("text"):
            continue
        try:
            language = validate_bcp47(element.get("lang") or element.get(XML_LANG) or root_lang)
            direction = text_direction(language, element.get("dir"))
            flow = text_flow_mode(element.get("data-pptx-text-flow"))
        except ValueError as exc:
            errors.append(str(exc))
            continue
        slots = tuple((element.get(name) or "").strip() for name in (
            "data-pptx-font-latin", "data-pptx-font-ea", "data-pptx-font-cs"
        ))
        if any(name in element.attrib and not element.get(name, "").strip() for name in (
            "data-pptx-font-latin", "data-pptx-font-ea", "data-pptx-font-cs"
        )):
            errors.append("declared font slot is empty")
        group = element.get("data-pptx-flow-group")
        signature = (language, direction, flow, slots)
        if group and group in groups and groups[group] != signature:
            errors.append(f"flow group {group!r} has inconsistent language/direction/mode/font slots")
        elif group:
            groups[group] = signature
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    files: list[Path] = []
    for path in args.paths:
        files.extend(sorted(path.rglob("*.svg")) if path.is_dir() else [path])
    errors: list[str] = []
    for path in files:
        errors.extend(f"{path}: {error}" for error in validate_file(path))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: SVG text contracts validated ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
