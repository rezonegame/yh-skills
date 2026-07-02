#!/usr/bin/env python3
"""Anchor-based feedback location for yh-local-knowledge.

Feedback/review on a specific passage should not store line numbers (they
drift on every edit). Instead, store an anchor window: the selected text plus
~80 chars of context before and after. This module computes and resolves such
anchors with a 3-level fallback.

Inspired by llm-wiki-skill's audit-shared anchor.ts. Pure standard library.

Usage as a module:
    from anchor import compute_anchor, resolve_anchor, Anchor

Usage as CLI (for inspection/testing):
    python scripts/anchor.py compute <file> <start_line> <end_line>
    python scripts/anchor.py resolve <file> <anchor_json>
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

CONTEXT_CHARS = 80


@dataclass
class Anchor:
    target_lines: list[int]          # best-effort original line range
    anchor_text: str                 # selected text, verbatim
    anchor_before: str               # ~80 chars before
    anchor_after: str                # ~80 chars after


def compute_anchor(text: str, start_line: int, end_line: int) -> Anchor:
    """Build an anchor from 1-based line numbers."""
    lines = text.splitlines()
    # normalize to file bounds
    s = max(0, start_line - 1)
    e = min(len(lines), end_line)
    selected = "\n".join(lines[s:e])

    # context: flatten surrounding text and grab ~CONTEXT_CHARS on each side
    before_text = "\n".join(lines[:s])
    after_text = "\n".join(lines[e:])
    return Anchor(
        target_lines=[start_line, end_line],
        anchor_text=selected,
        anchor_before=before_text[-CONTEXT_CHARS:] if before_text else "",
        anchor_after=after_text[:CONTEXT_CHARS] if after_text else "",
    )


def resolve_anchor(text: str, anchor: Anchor) -> dict:
    """Resolve an anchor back to a line range. 3-level fallback.

    Returns: {"found": bool, "lines": [s,e]|None, "method": str, "stale": bool}
    """
    lines = text.splitlines()

    # Level 1: try target_lines directly
    s, e = anchor.target_lines[0] - 1, anchor.target_lines[1]
    if 0 <= s < e <= len(lines):
        candidate = "\n".join(lines[s:e])
        if anchor.anchor_text and anchor.anchor_text in candidate:
            return {"found": True, "lines": [s + 1, e], "method": "line_match", "stale": False}

    # Level 2: full-text search for anchor_text, accept if unique
    if anchor.anchor_text:
        idx = text.find(anchor.anchor_text)
        if idx != -1 and text.find(anchor.anchor_text, idx + 1) == -1:
            ls, le = _offset_to_lines(text, idx, idx + len(anchor.anchor_text))
            return {"found": True, "lines": [ls, le], "method": "unique_text", "stale": False}

    # Level 3: context window (before + text + after)
    if anchor.anchor_text and (anchor.anchor_before or anchor.anchor_after):
        window = anchor.anchor_before + anchor.anchor_text + anchor.anchor_after
        idx = text.find(window)
        if idx == -1:
            # try just before+text
            window2 = anchor.anchor_before + anchor.anchor_text
            idx = text.find(window2)
        if idx == -1:
            window3 = anchor.anchor_text + anchor.anchor_after
            idx = text.find(window3)
        if idx != -1:
            ls, le = _offset_to_lines(text, idx, idx + len(anchor.anchor_text) if anchor.anchor_text else idx + len(window))
            return {"found": True, "lines": [ls, le], "method": "context_window", "stale": False}

    # All failed — stale, ask human
    return {"found": False, "lines": None, "method": "none", "stale": True}


def _offset_to_lines(text: str, start_offset: int, end_offset: int) -> tuple[int, int]:
    """Convert char offsets to 1-based line numbers."""
    start_line = text.count("\n", 0, start_offset) + 1
    end_line = text.count("\n", 0, end_offset) + 1
    return start_line, end_line


def main() -> int:
    p = argparse.ArgumentParser(description="anchor compute/resolve")
    sub = p.add_subparsers(dest="cmd", required=True)

    pc = sub.add_parser("compute")
    pc.add_argument("file")
    pc.add_argument("start", type=int)
    pc.add_argument("end", type=int)

    pr = sub.add_parser("resolve")
    pr.add_argument("file")
    pr.add_argument("anchor", help="anchor JSON string")

    args = p.parse_args()
    text = Path(args.file).read_text(encoding="utf-8", errors="replace")

    if args.cmd == "compute":
        a = compute_anchor(text, args.start, args.end)
        print(json.dumps(asdict(a), ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "resolve":
        a = Anchor(**json.loads(args.anchor))
        print(json.dumps(resolve_anchor(text, a), ensure_ascii=False, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
