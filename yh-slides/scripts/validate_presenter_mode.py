#!/usr/bin/env python3
"""Self-authored presenter-mode contract validator; contains no Guizang runtime code."""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
NOTE_FIELDS = ("id", "title", "purpose", "talking_points", "transition", "talk_seconds", "interaction", "fallback", "pronunciation")
RUNTIME_FEATURES = {"audience-connection", "heartbeat-timeout", "recovery", "end-mask", "notes-persistence"}


class PresenterHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.slide_ids: list[str] = []
        self._capture_notes = False
        self._notes_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if "data-slide-id" in values:
            self.slide_ids.append(values.get("data-slide-id") or "")
        if tag == "script" and values.get("id") == "speaker-notes" and values.get("type") == "application/json":
            self._capture_notes = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._capture_notes:
            self._capture_notes = False

    def handle_data(self, data: str) -> None:
        if self._capture_notes:
            self._notes_parts.append(data)

    @property
    def notes_json(self) -> str:
        return "".join(self._notes_parts)


def validate_presenter(html_text: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    parser = PresenterHTML()
    parser.feed(html_text)
    ids = parser.slide_ids
    if not ids:
        errors.append("no data-slide-id values found")
    if len(ids) != len(set(ids)):
        errors.append("duplicate data-slide-id")
    for slide_id in ids:
        if not ID_RE.fullmatch(slide_id):
            errors.append(f"non-semantic slide id: {slide_id!r}")
    try:
        contract = json.loads(parser.notes_json)
    except json.JSONDecodeError as exc:
        errors.append(f"speaker-notes JSON missing or invalid: {exc}")
        return errors, warnings
    notes = contract.get("notes")
    if not isinstance(notes, list):
        errors.append("speaker-notes notes must be an array")
        return errors, warnings
    note_ids = [note.get("id") for note in notes if isinstance(note, dict)]
    if note_ids != ids:
        errors.append("speaker notes count/order/id must exactly match slide order")
    talk_total = 0.0
    for index, note in enumerate(notes):
        if not isinstance(note, dict):
            errors.append(f"note {index + 1} must be an object")
            continue
        for field in NOTE_FIELDS:
            if field not in note:
                errors.append(f"note {note.get('id', index + 1)} missing {field}")
        if "duration" in note:
            errors.append(f"note {note.get('id')} uses ambiguous duration; use talk_seconds and auto_advance_seconds")
        talking_points = note.get("talking_points")
        if not isinstance(talking_points, list) or not talking_points:
            errors.append(f"note {note.get('id')} talking_points must be non-empty")
        for field in ("interaction", "pronunciation"):
            if field in note and not isinstance(note[field], list):
                errors.append(f"note {note.get('id')} {field} must be an array")
        try:
            talk = float(note.get("talk_seconds", 0))
            if talk <= 0:
                raise ValueError
            talk_total += talk
        except (TypeError, ValueError):
            errors.append(f"note {note.get('id')} talk_seconds must be positive")
        if "auto_advance_seconds" in note:
            try:
                if float(note["auto_advance_seconds"]) <= 0:
                    raise ValueError
            except (TypeError, ValueError):
                errors.append(f"note {note.get('id')} auto_advance_seconds must be positive when present")
    try:
        budget = float(contract.get("talk_budget_seconds", 0))
    except (TypeError, ValueError):
        budget = 0
    if budget <= 0:
        errors.append("talk_budget_seconds must be positive")
    elif talk_total > budget:
        errors.append(f"talk time {talk_total:g}s exceeds budget {budget:g}s")
    elif talk_total < budget * 0.55:
        warnings.append(f"talk time {talk_total:g}s uses less than 55% of budget {budget:g}s")
    features = set(contract.get("runtime_features", []))
    missing = sorted(RUNTIME_FEATURES - features)
    if missing:
        errors.append("presenter runtime contract missing: " + ", ".join(missing))
    recovery = contract.get("recovery", {})
    if not isinstance(recovery, dict) or not all(recovery.get(key) for key in ("heartbeat_seconds", "timeout_seconds", "resume_token")):
        errors.append("recovery must declare heartbeat_seconds, timeout_seconds, and resume_token")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    args = parser.parse_args()
    errors, warnings = validate_presenter(args.html.read_text(encoding="utf-8-sig"))
    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: presenter contract validated (stable IDs, structured notes, timing, audience recovery)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
