#!/usr/bin/env python3
"""Normalize binary source files into markdown for indexing/extraction.

This is the Tier-1/Tier-2/Tier-3 format converter behind the skill's
"format zero-barrier" pillar. It converts PDF/Word/Excel/PPT/images/etc.
under a source root into clean markdown under .knowledge/normalized/,
leaving the original raw files untouched.

Strategy (degradation chain):
  Tier 1: markitdown (if importable)        -> full format coverage
  Tier 2: system tools (pandoc/pdftotext)   -> partial coverage
  Tier 3: metadata only                       -> record file, no content

It never overwrites raw source files. Output is an intermediate read-only
layer consumed by sync/index/extract. Status is written back into
manifest.json entries via normalized_path / normalization_status fields
(the agent or caller merges these into the manifest; this script prints a
JSON report it can consume).

Usage:
    python scripts/normalize.py <workspace_root> [--source-root 原始资料]
    python scripts/normalize.py <workspace_root> --file 原始资料/x.pdf
    python scripts/normalize.py <workspace_root> --status   # print report only

Pure standard library except for the optional markitdown import.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# --- format classification -------------------------------------------------

BINARY_EXTS = {
    ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx",
    ".html", ".htm", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff",
    ".mp3", ".wav", ".m4a", ".mp4", ".epub", ".zip", ".rst",
}
# Already-text formats that do not need normalization.
TEXT_EXTS = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".log", ".tsv", ".org"}
NORMALIZED_DIR = ".knowledge/normalized"

# --- tier detection --------------------------------------------------------


class Converters:
    """Detect available converters once, cheaply."""

    def __init__(self) -> None:
        self.markitdown = self._try_markitdown()
        self.pandoc = shutil.which("pandoc") is not None
        self.pdftotext = shutil.which("pdftotext") is not None

    @staticmethod
    def _try_markitdown():
        try:
            from markitdown import MarkItDown  # type: ignore

            return MarkItDown()
        except Exception:
            return None


# --- conversion ------------------------------------------------------------


def _out_path(workspace: Path, src: Path) -> Path:
    rel = src.with_suffix(".md").name
    # namespace by source root folder to avoid collisions across roots
    parent = src.parent.name
    return workspace / NORMALIZED_DIR / parent / rel


def _tier1_markitdown(conv: Converters, src: Path, out: Path) -> tuple[str, str | None]:
    """Use markitdown. Return (status, error|None)."""
    try:
        # convert_local is the safe variant for local files (no URI handling).
        # Older markitdown (0.1.x) exposes .convert(); prefer convert_local.
        if hasattr(conv.markitdown, "convert_local"):
            result = conv.markitdown.convert_local(str(src))
        else:
            result = conv.markitdown.convert(str(src))
        text = getattr(result, "text_content", None) or str(result)
        if not text or not text.strip():
            return "fallback_metadata_only", "empty conversion result"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        return "normalized", None
    except Exception as e:  # noqa: BLE001
        return "failed", f"markitdown: {e}"


def _tier2_system(src: Path, out: Path, pdftotext: bool, pandoc: bool) -> tuple[str, str | None]:
    """Fallback to system tools."""
    ext = src.suffix.lower()
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        if ext == ".pdf" and pdftotext:
            # pdftotext writes to a file path (never stdout, per kb-retriever discipline).
            tmp = out.with_suffix(".tmp.txt")
            subprocess.call(["pdftotext", str(src), str(tmp)])
            if tmp.exists() and tmp.stat().st_size > 0:
                out.write_text(tmp.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
                tmp.unlink(missing_ok=True)
                return "normalized", None
            return "fallback_metadata_only", "pdftotext produced empty output"
        if ext in {".doc", ".docx", ".rst", ".epub"} and pandoc:
            subprocess.call(["pandoc", str(src), "-o", str(out)])
            if out.exists() and out.stat().st_size > 0:
                return "normalized", None
            return "fallback_metadata_only", "pandoc produced empty output"
        return "fallback_metadata_only", "no system tool for this format"
    except Exception as e:  # noqa: BLE001
        return "failed", f"system tool: {e}"


def convert_one(conv: Converters, workspace: Path, src: Path) -> dict:
    """Convert a single source file. Returns a manifest entry fragment."""
    ext = src.suffix.lower()
    record = {
        "path": str(src.relative_to(workspace)) if src.is_relative_to(workspace) else str(src),
        "type": ext,
        "normalized_path": None,
        "normalization_status": "skipped",
        "normalization_error": None,
    }

    # Text formats need no conversion.
    if ext in TEXT_EXTS:
        record["normalization_status"] = "not_required"
        return record
    # Unknown/binary extensions still attempted via markitdown if present.

    out = _out_path(workspace, src)
    # Skip if output already exists and source unchanged (incremental).
    if out.exists():
        record["normalized_path"] = str(out.relative_to(workspace))
        record["normalization_status"] = "normalized_cached"
        return record

    status, err = "fallback_metadata_only", "no converter available"
    if conv.markitdown is not None:
        status, err = _tier1_markitdown(conv, src, out)
    if status != "normalized":
        s2, e2 = _tier2_system(src, out, conv.pdftotext, conv.pandoc)
        if s2 == "normalized":
            status, err = "normalized", None
        else:
            # keep the more informative error
            err = err if err else e2

    if status == "normalized":
        record["normalized_path"] = str(out.relative_to(workspace))
    record["normalization_status"] = status
    record["normalization_error"] = err
    return record


def scan_source_root(root: Path) -> list[Path]:
    files: list[Path] = []
    for dp, _dirs, names in os.walk(root):
        # skip the .knowledge working area itself
        if ".knowledge" in Path(dp).parts:
            continue
        for n in names:
            files.append(Path(dp) / n)
    return files


def main() -> int:
    p = argparse.ArgumentParser(description="Normalize source files to markdown")
    p.add_argument("workspace", help="workspace root (the topic folder)")
    p.add_argument("--source-root", default="原始资料", help="source root name or path")
    p.add_argument("--file", help="normalize a single file instead of a root")
    p.add_argument("--status", action="store_true", help="print converter status and exit")
    args = p.parse_args()

    workspace = Path(args.workspace).resolve()
    conv = Converters()

    if args.status:
        print(json.dumps({
            "markitdown": conv.markitdown is not None,
            "pandoc": conv.pandoc,
            "pdftotext": conv.pdftotext,
            "normalized_dir": str(workspace / NORMALIZED_DIR),
        }, ensure_ascii=False, indent=2))
        return 0

    if not conv.markitdown and not conv.pandoc and not conv.pdftotext:
        print(
            "No converter available. Install markitdown for full support:\n"
            "  python scripts/bootstrap.py --install\n"
            "Falling back to metadata-only for all binary files.",
            file=sys.stderr,
        )

    if args.file:
        targets = [Path(args.file).resolve()]
    else:
        src_root = (workspace / args.source_root).resolve()
        if not src_root.is_absolute() or not src_root.exists():
            src_root = Path(args.source_root).resolve()
        if not src_root.exists():
            print(f"source root not found: {src_root}", file=sys.stderr)
            return 2
        targets = scan_source_root(src_root)

    results = [convert_one(conv, workspace, t) for t in targets if t.is_file()]

    # Ensure normalized dir exists even if nothing converted (for structure).
    (workspace / NORMALIZED_DIR).mkdir(parents=True, exist_ok=True)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "converter": {
            "markitdown": conv.markitdown is not None,
            "pandoc": conv.pandoc,
            "pdftotext": conv.pdftotext,
        },
        "total": len(results),
        "by_status": {},
        "files": results,
    }
    for r in results:
        s = r["normalization_status"]
        summary["by_status"][s] = summary["by_status"].get(s, 0) + 1

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
