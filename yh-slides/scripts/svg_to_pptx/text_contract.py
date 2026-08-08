"""BCP-47, font-slot, direction, and editable text-flow contracts."""
from __future__ import annotations

import re


TEXT_FLOW_MODES = ("preserve", "reflow", "split")
_BCP47 = re.compile(r"^(?:[A-Za-z]{2,3}|[A-Za-z]{4}|[A-Za-z]{5,8})(?:-[A-Za-z0-9]{1,8})*$")
RTL_LANGUAGES = {"ar", "fa", "he", "ps", "ur"}


def validate_bcp47(value: str) -> str:
    value = value.strip()
    if not _BCP47.fullmatch(value):
        raise ValueError(f"invalid BCP-47 language tag: {value!r}")
    parts = value.split("-")
    normalized = [parts[0].lower()]
    for part in parts[1:]:
        if len(part) == 4 and part.isalpha():
            normalized.append(part.title())
        elif len(part) == 2 and part.isalpha() or len(part) == 3 and part.isdigit():
            normalized.append(part.upper())
        else:
            normalized.append(part.lower())
    return "-".join(normalized)


def text_direction(language: str, explicit: str | None = None) -> str:
    if explicit:
        value = explicit.lower()
        if value not in {"ltr", "rtl"}:
            raise ValueError(f"invalid text direction: {explicit!r}")
        return value
    return "rtl" if validate_bcp47(language).split("-", 1)[0] in RTL_LANGUAGES else "ltr"


def text_flow_mode(value: str | None) -> str:
    mode = (value or "preserve").lower()
    if mode not in TEXT_FLOW_MODES:
        raise ValueError(f"invalid text-flow mode: {value!r}; expected preserve, reflow, or split")
    return mode
