#!/usr/bin/env python3
"""Fail-closed delivery checks and last-known-good artifact promotion."""
from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Callable, Iterable, Mapping


REQUIRED_BRIEF_FIELDS = ("audience", "language", "template", "output_format", "acceptance_check")


def contained_path(root: Path, candidate: Path) -> Path:
    root = root.resolve()
    candidate = candidate.resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes delivery root: {candidate}") from exc
    return candidate


def validate_delivery_brief(brief: Mapping[str, object]) -> list[str]:
    errors = []
    for field in REQUIRED_BRIEF_FIELDS:
        value = brief.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"delivery brief missing {field}")
    capabilities = brief.get("capabilities", {})
    if not isinstance(capabilities, Mapping):
        errors.append("delivery brief capabilities must be an object")
    else:
        for name, available in capabilities.items():
            if available is not True:
                errors.append(f"required capability unavailable: {name}")
    return errors


def validate_required_files(root: Path, paths: Iterable[str], *, label: str = "asset") -> list[str]:
    errors: list[str] = []
    for relative in paths:
        try:
            path = contained_path(root, root / relative)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not path.is_file():
            errors.append(f"missing required {label}: {relative}")
        elif path.stat().st_size == 0:
            errors.append(f"empty required {label}: {relative}")
    return errors


def candidate_path(final_path: Path) -> Path:
    """Return a same-directory path so os.replace remains atomic."""
    final_path = final_path.resolve()
    final_path.parent.mkdir(parents=True, exist_ok=True)
    return final_path.with_name(f".{final_path.stem}.{uuid.uuid4().hex}.candidate{final_path.suffix}")


def discard_candidate(candidate: Path) -> None:
    candidate.unlink(missing_ok=True)


def promote_candidate(
    candidate: Path,
    final_path: Path,
    *,
    validator: Callable[[Path], Iterable[str]] | None = None,
) -> None:
    """Atomically promote a validated candidate, preserving the last good file on failure."""
    candidate = candidate.resolve()
    final_path = final_path.resolve()
    if candidate.parent != final_path.parent:
        raise ValueError("candidate and final artifact must share a directory")
    if not candidate.is_file() or candidate.stat().st_size == 0:
        raise ValueError("candidate artifact is missing or empty")
    errors = list(validator(candidate)) if validator else []
    if errors:
        raise ValueError("candidate validation failed: " + "; ".join(errors))
    os.replace(candidate, final_path)
