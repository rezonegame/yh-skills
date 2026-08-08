#!/usr/bin/env python3
"""Fail-closed output containment and SVG/image provenance manifests."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote


XLINK = "{http://www.w3.org/1999/xlink}href"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contained(root: Path, candidate: Path) -> Path:
    root = root.resolve()
    candidate = candidate.resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path escapes project root: {candidate}") from exc
    return candidate


def resolve_output(project_root: Path, value: str | Path) -> Path:
    raw = Path(value)
    candidate = raw if raw.is_absolute() else project_root / raw
    return contained(project_root, candidate)


def inspect_svg_sources(project_root: Path, svg_files: list[Path]) -> list[dict]:
    records: list[dict] = []
    for svg in svg_files:
        svg = contained(project_root, svg)
        item = {"path": svg.relative_to(project_root).as_posix(), "sha256": sha256(svg), "images": []}
        root = ET.parse(svg).getroot()
        for image in root.iter():
            if not image.tag.endswith("image"):
                continue
            href = image.get("href") or image.get(XLINK) or ""
            if href.startswith("data:"):
                item["images"].append({"source": "embedded-data", "sha256": hashlib.sha256(href.encode("utf-8")).hexdigest()})
                continue
            if href.startswith(("http://", "https://", "//")):
                raise ValueError(f"remote image is forbidden at export: {svg}: {href}")
            local = contained(project_root, svg.parent / unquote(href))
            if not local.is_file():
                raise ValueError(f"image source missing: {svg}: {href}")
            item["images"].append({"source": local.relative_to(project_root).as_posix(), "sha256": sha256(local)})
        records.append(item)
    return records


def write_source_manifest(output_path: Path, project_root: Path, records: list[dict]) -> Path:
    output_path = contained(project_root, output_path)
    manifest_path = output_path.with_suffix(output_path.suffix + ".sources.json")
    payload = {
        "schema": "yh-slides.export-sources.v1",
        "output": output_path.relative_to(project_root).as_posix(),
        "output_sha256": sha256(output_path),
        "sources": records,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{manifest_path.name}.", dir=manifest_path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(tmp_name, manifest_path)
    except Exception:
        Path(tmp_name).unlink(missing_ok=True)
        raise
    return manifest_path


def write_template_fill_manifest(output_path: Path, project_root: Path, template: Path, plan: Path) -> Path:
    """Write a bounded manifest for a template-fill export."""
    plan = contained(project_root, plan)
    records = [
        {"role": "source-template", "name": template.name, "sha256": sha256(template)},
        {"role": "fill-plan", "path": plan.relative_to(project_root).as_posix(), "sha256": sha256(plan)},
    ]
    return write_source_manifest(output_path, project_root, records)


def promote_export(candidate: Path, output_path: Path) -> None:
    """Validate and atomically promote a same-directory export candidate."""
    candidate = candidate.resolve()
    output_path = output_path.resolve()
    try:
        candidate.relative_to(output_path.parent)
    except ValueError as exc:
        raise ValueError("candidate must remain inside the output directory") from exc
    if not candidate.is_file() or candidate.stat().st_size == 0:
        raise ValueError("export candidate is missing or empty")
    if output_path.suffix.lower() == ".pptx":
        try:
            with zipfile.ZipFile(candidate) as archive:
                names = set(archive.namelist())
        except zipfile.BadZipFile as exc:
            raise ValueError("PPTX candidate is not a valid ZIP package") from exc
        if "[Content_Types].xml" not in names or "ppt/presentation.xml" not in names:
            raise ValueError("PPTX candidate lacks required package parts")
    os.replace(candidate, output_path)
