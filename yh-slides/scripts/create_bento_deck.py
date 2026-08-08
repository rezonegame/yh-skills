#!/usr/bin/env python3
"""Assemble an offline editable .bento.html file from a yh-slides plan."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from validate_bento_deck import validate


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SHELL = ROOT / "templates" / "html-decks" / "bento" / "Bento_Slides.bento.html"
DOC_RE = re.compile(r'(<script[^>]+id="bento-doc"[^>]*>)(.*?)(</script>)', re.IGNORECASE | re.DOTALL)
REMOTE_RUNTIME_RE = re.compile(r'''(?:src|href)\s*=\s*["']https?://''', re.IGNORECASE)


def to_bento_document(plan: dict) -> dict:
    size = plan.get("size", {"width": 1280, "height": 720})
    return {
        "format": "bento/slides",
        "version": 1,
        "title": plan["title"],
        "size": size,
        "theme": plan.get("theme", {}),
        "assets": plan.get("assets", {}),
        "slides": [
            {
                "id": slide["id"],
                "name": slide["name"],
                "background": slide.get("background", "#FFFFFF"),
                "transition": slide.get("transition", "none"),
                "notes": slide["notes"],
                **({"stateOf": slide["state_of"]} if slide.get("state_of") else {}),
                "elements": slide["elements"],
            }
            for slide in plan["slides"]
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--shell", type=Path, default=DEFAULT_SHELL)
    parser.add_argument("--deck-plan", type=Path)
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        deck_plan = json.loads(args.deck_plan.read_text(encoding="utf-8")) if args.deck_plan else None
        shell = args.shell.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Bento deck assembly failed: {exc}")
        return 1
    errors = validate(plan, deck_plan)
    if errors:
        print("Bento deck assembly blocked by validation:")
        for error in errors:
            print(f"  - {error}")
        return 1
    if REMOTE_RUNTIME_RE.search(shell):
        print("Bento deck assembly blocked: shell has a remote runtime dependency")
        return 1
    document_json = json.dumps(to_bento_document(plan), ensure_ascii=False, separators=(",", ":"))
    document_json = document_json.replace("<", "\\u003c")
    result, count = DOC_RE.subn(lambda match: f"{match.group(1)}{document_json}{match.group(3)}", shell, count=1)
    if count != 1:
        print('Bento deck assembly failed: shell must contain exactly one id="bento-doc" script block')
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result, encoding="utf-8")
    print(f"Wrote offline editable Bento deck: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
