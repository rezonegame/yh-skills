#!/usr/bin/env python3
"""Report the optional runtime capabilities required by yh-document-studio.

This is deliberately read-only: it helps a maintainer distinguish a missing
Python package from a missing native WeasyPrint runtime before attempting a
full PDF build.
"""
from __future__ import annotations

import importlib.metadata
import importlib.util
import platform
import sys


DEPENDENCIES = {
    "weasyprint": "weasyprint",
    "pypdf": "pypdf",
    "PyMuPDF": "fitz",
    "python-pptx": "pptx",
    "Pygments": "pygments",
}


def main() -> int:
    print(f"Python: {sys.version.split()[0]} ({platform.platform()})")
    missing = []
    for package, module in DEPENDENCIES.items():
        available = importlib.util.find_spec(module) is not None
        version = ""
        if available:
            try:
                version = f" {importlib.metadata.version(package)}"
            except importlib.metadata.PackageNotFoundError:
                version = " (version unknown)"
        else:
            missing.append(package)
        print(f"{'OK ' if available else 'MISS'} {package}{version}")

    if importlib.util.find_spec("weasyprint") is not None:
        try:
            from optional_deps import require_weasyprint_html

            require_weasyprint_html()
            print("OK  WeasyPrint native runtime")
        except Exception as exc:  # noqa: BLE001 - diagnostics must report any native failure
            missing.append("WeasyPrint native runtime")
            print(f"MISS WeasyPrint native runtime: {exc}")

    if missing:
        print("Missing capabilities: " + ", ".join(missing))
        return 1
    print("Environment is ready for optional PDF/PPTX enhancements.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
