#!/usr/bin/env python3
"""yh-local-knowledge bootstrap: detect and optionally install markitdown.

This script keeps the skill folder lightweight. It does NOT bundle markitdown.
Instead it checks whether markitdown is importable, and if not, offers a
one-command install into the user's Python environment.

Usage:
    python scripts/bootstrap.py              # detect + print status
    python scripts/bootstrap.py --install    # detect + auto-install (core)
    python scripts/bootstrap.py --install-all
    python scripts/bootstrap.py --check      # silent check, exit code only

Pure standard library. No pip dependency to run this script itself.
"""
from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import shutil
import subprocess
import sys

# Optional format extras offered by markitdown. Core install already covers
# pdf/docx/pptx/xlsx/html via pure-python parsers. Listed here so the bootstrap
# can recommend them for broader coverage (audio transcription, youtube, etc.).
CORE_EXTRAS = "pdf,docx,pptx,xlsx"
ALL_EXTRAS = "all"
MARKITDOWN_MIN = (0, 1, 7)
MARKITDOWN_SPEC = ">=0.1.7,<0.2"


def _have(module: str) -> bool:
    try:
        importlib.import_module(module)
        return True
    except Exception:
        return False


def _have_markitdown() -> bool:
    return _have("markitdown")


def _markitdown_version() -> str | None:
    try:
        return importlib.metadata.version("markitdown")
    except importlib.metadata.PackageNotFoundError:
        return None


def _supported_markitdown(version: str | None) -> bool:
    if not version:
        return False
    try:
        parts = tuple(int(part) for part in version.split(".")[:3])
    except ValueError:
        return False
    return MARKITDOWN_MIN <= parts < (0, 2)


def _have_ffmpeg() -> bool:
    """ffmpeg is required only for audio transcription. Optional."""
    return shutil.which("ffmpeg") is not None or shutil.which("avconv") is not None


def _pip(args: list[str]) -> int:
    """Run pip as a subprocess (works even if pip is not on PATH via -m)."""
    return subprocess.call([sys.executable, "-m", "pip", *args])


def detect() -> dict:
    """Return a status dict describing what is available."""
    return {
        "markitdown": _have_markitdown(),
        "markitdown_version": _markitdown_version(),
        "markitdown_supported": _supported_markitdown(_markitdown_version()),
        "ffmpeg": _have_ffmpeg(),
        "python": sys.version.split()[0],
    }


def print_status(status: dict) -> None:
    md = "yes" if status["markitdown"] else "NO"
    ff = "yes" if status["ffmpeg"] else "NO (optional, only for audio)"
    print(f"python:      {status['python']}")
    print(f"markitdown:  {md}")
    print(f"version:     {status['markitdown_version'] or 'not installed'} (supported: {status['markitdown_supported']})")
    print(f"ffmpeg:      {ff}")
    print()

    if status["markitdown"] and status["markitdown_supported"]:
        print("Format conversion is fully supported (PDF/Word/Excel/PPT/HTML/images/audio).")
        if not status["ffmpeg"]:
            print("Note: audio transcription needs ffmpeg. Install it separately if needed.")
        return

    print(f"markitdown {MARKITDOWN_SPEC} is not available. Without it the skill falls back to")
    print("system tools (pandoc/pdftotext) or metadata-only indexing.")
    print()
    print("Install options:")
    print(f"  core (PDF/Word/Excel/PPT/HTML):  pip install 'markitdown[{CORE_EXTRAS}]{MARKITDOWN_SPEC}'")
    print(f"  full (adds audio/youtube/etc):   pip install 'markitdown[{ALL_EXTRAS}]{MARKITDOWN_SPEC}'")
    print("  or use this script:")
    print(f"    python scripts/bootstrap.py --install        # core extras")
    print(f"    python scripts/bootstrap.py --install-all    # all extras")


def install(all_extras: bool = False) -> int:
    extra = ALL_EXTRAS if all_extras else CORE_EXTRAS
    print(f"Installing markitdown[{extra}] ...")
    rc = _pip(["install", f"markitdown[{extra}]{MARKITDOWN_SPEC}"])
    if rc == 0:
        print()
        if _have_markitdown() and _supported_markitdown(_markitdown_version()):
            print("OK: markitdown installed successfully.")
        else:
            print("pip reported success but markitdown still not importable.")
            print("Try restarting your shell, or install manually:")
            print(f"  pip install 'markitdown[{extra}]{MARKITDOWN_SPEC}'")
            return 1
    return rc


def main() -> int:
    p = argparse.ArgumentParser(description="yh-local-knowledge format bootstrap")
    p.add_argument("--install", action="store_true", help="install markitdown with core extras")
    p.add_argument("--install-all", action="store_true", help="install markitdown with all extras")
    p.add_argument("--check", action="store_true", help="silent check; exit 0 if ok, 1 if markitdown missing")
    args = p.parse_args()

    if args.check:
        return 0 if _have_markitdown() and _supported_markitdown(_markitdown_version()) else 1

    if args.install or args.install_all:
        return install(all_extras=args.install_all)

    print_status(detect())
    return 0 if _have_markitdown() else 0  # detection mode always exits 0


if __name__ == "__main__":
    raise SystemExit(main())
