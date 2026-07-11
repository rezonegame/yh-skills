"""Shared local-path and size guards for SVG image embedding.

SVG files are untrusted input. Referenced images may be loaded only from the
SVG task root (normally the parent of `svg_output`), never from an absolute
path, a URI, or a path that escapes that root.
"""

from __future__ import annotations

import html
import os
from pathlib import Path
from urllib.parse import unquote, urlparse


MAX_EMBED_IMAGE_BYTES = 25 * 1024 * 1024


def resolve_image_path(href: str, svg_dir: Path, asset_root: Path | None = None) -> Path | None:
    """Return a safe local image reference, or `None` when it is unsafe.

    The default asset root is the parent of `svg_dir` so a conventional
    `project/svg_output/slide.svg` may still reference `../images/foo.png`.
    """
    if not href:
        return None
    decoded = html.unescape(unquote(href)).strip()
    parsed = urlparse(decoded)
    if parsed.scheme or decoded.startswith("//") or os.path.isabs(decoded):
        return None

    base = svg_dir.resolve()
    root = (asset_root or base.parent).resolve()
    candidate = (base / decoded).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None

    if not candidate.is_file():
        return None
    try:
        if candidate.stat().st_size > MAX_EMBED_IMAGE_BYTES:
            return None
    except OSError:
        return None
    return candidate
