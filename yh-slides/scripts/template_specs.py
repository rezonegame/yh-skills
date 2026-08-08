#!/usr/bin/env python3
"""Resolve independent template specs without destructively merging installed files."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


PRIORITY_LOW_TO_HIGH = ("upstream-default", "style", "layout", "brand", "project-explicit")


@dataclass(frozen=True)
class SpecLayer:
    role: str
    path: Path


def build_spec_stack(
    *,
    upstream_default: Path | None = None,
    style: Path | None = None,
    layout: Path | None = None,
    brand: Path | None = None,
    project_explicit: Path | None = None,
) -> tuple[SpecLayer, ...]:
    """Return existing specs in deterministic low-to-high precedence order."""
    requested = {
        "upstream-default": upstream_default,
        "style": style,
        "layout": layout,
        "brand": brand,
        "project-explicit": project_explicit,
    }
    layers: list[SpecLayer] = []
    for role in PRIORITY_LOW_TO_HIGH:
        path = requested[role]
        if path is None:
            continue
        resolved = path.resolve()
        if not resolved.is_file():
            raise FileNotFoundError(f"{role} spec does not exist: {path}")
        layers.append(SpecLayer(role, resolved))
    return tuple(layers)


def effective_text(stack: tuple[SpecLayer, ...]) -> str:
    """Create a reviewable composite while preserving every source boundary."""
    chunks = []
    for layer in stack:
        chunks.append(f"<!-- spec-layer:{layer.role} source:{layer.path.as_posix()} -->")
        chunks.append(layer.path.read_text(encoding="utf-8-sig").rstrip())
    return "\n\n".join(chunks) + ("\n" if chunks else "")
