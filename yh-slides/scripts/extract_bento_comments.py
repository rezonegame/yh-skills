#!/usr/bin/env python3
"""Extract Bento review comments into JSON for the yh-slides revision loop."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DOC_RE = re.compile(r'<script[^>]+id="bento-doc"[^>]*>(.*?)</script>', re.IGNORECASE | re.DOTALL)


def extract(deck: Path) -> dict:
    text = deck.read_text(encoding="utf-8")
    match = DOC_RE.search(text)
    if not match:
        raise ValueError('missing id="bento-doc" script block')
    doc = json.loads(match.group(1).strip())
    comments = []
    for index, slide in enumerate(doc.get("slides", []), start=1):
        for comment in slide.get("comments", []):
            comments.append({"slide_id": slide.get("id"), "slide_name": slide.get("name"), "slide_index": index, "comment": comment})
    return {"schema": "yh_slides_bento_comments.v1", "deck_title": doc.get("title", ""), "slide_count": len(doc.get("slides", [])), "comments": comments}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = extract(args.deck)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Bento comment extraction failed: {exc}")
        return 1
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
