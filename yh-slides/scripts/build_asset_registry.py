#!/usr/bin/env python3
"""Build the yh-slides local asset registry.

This registry is the native, post-vendor-absorption discovery layer. It indexes
assets by how yh-slides uses them, not by the upstream repository layout.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "references" / "meta" / "asset-registry.json"

SOURCE_LOCK_DIR = ROOT / "provenance" / "upstream-locks"

ASSET_ROOTS = [
    ("assets/seeds", "seed", "core"),
    ("assets/style-samples", "style-sample", "2A/2B/2C style selection"),
    ("assets/vendor", "runtime", "core"),
    ("assets/screenshot-backgrounds", "screenshot-background", "2D screenshot framing"),
    ("templates/charts", "chart-template", "2A-S Path S"),
    ("templates/icons", "icon", "2A-S Path S"),
    ("templates/layouts", "pptx-layout-template", "2A-S Path S"),
    ("templates/html-decks/html-ppt/themes", "html-theme", "2D HTML"),
    ("templates/html-decks/html-ppt/animations", "html-animation", "2D HTML"),
    ("templates/html-decks/html-ppt/single-page", "html-page-template", "2D HTML"),
    ("templates/html-decks/html-ppt/full-decks", "html-full-deck", "2D HTML / 2D-P"),
    ("templates/html-decks/html-ppt", "html-runtime", "2D HTML"),
    ("templates/html-decks/guizang", "html-seed", "2D Path C magazine/swiss"),
    ("scripts/template_fill_pptx", "python-package", "2A-T Template Fill"),
    ("scripts/template_fill_pptx.py", "script", "2A-T Template Fill"),
]

EXT_TAGS = {
    ".html": ["html", "template"],
    ".css": ["css", "theme"],
    ".js": ["javascript", "runtime"],
    ".mjs": ["javascript", "validator"],
    ".py": ["python", "tool"],
    ".md": ["reference"],
    ".json": ["index", "data"],
    ".svg": ["vector"],
    ".pptx": ["pptx", "template"],
    ".webp": ["image", "background"],
    ".png": ["image"],
    ".jpg": ["image"],
    ".jpeg": ["image"],
    ".woff2": ["font"],
}


def read_locks() -> dict:
    locks: dict[str, dict] = {}
    if not SOURCE_LOCK_DIR.exists():
        return locks
    for path in SOURCE_LOCK_DIR.glob("*.source.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        name = data.get("name") or path.name.removesuffix(".source.json")
        locks[name] = data
    return locks


def infer_origin(rel: str) -> str:
    rel = rel.replace("\\", "/")
    if rel == "assets/style-samples/ian-handdrawn-technical-anchor.png":
        return "ian-handdrawn-ppt"
    if rel.startswith("templates/html-decks/html-ppt/"):
        return "html-ppt-skill"
    if rel.startswith("templates/html-decks/guizang/") or rel.startswith("assets/screenshot-backgrounds/guizang/"):
        return "guizang-ppt-skill"
    if rel.startswith("scripts/template_fill_pptx") or rel.startswith("templates/charts/") or rel.startswith("templates/icons/") or rel.startswith("templates/layouts/"):
        return "ppt-master"
    return "yh-slides"


def should_index(path: Path) -> bool:
    if "__pycache__" in path.parts or "node_modules" in path.parts:
        return False
    return path.is_file() and path.suffix.lower() in EXT_TAGS


def stable_id(rel: str, asset_type: str) -> str:
    stem = rel.replace("\\", "/").replace("/", ".")
    for suffix in EXT_TAGS:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    return f"{asset_type}.{stem}".lower().replace(" ", "-")


def main() -> int:
    locks = read_locks()
    assets = []
    seen: set[str] = set()
    for root_rel, asset_type, route_hint in ASSET_ROOTS:
        root = ROOT / root_rel
        if not root.exists():
            continue
        candidates = [root] if root.is_file() else root.rglob("*")
        for path in candidates:
            if not should_index(path):
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel in seen:
                continue
            seen.add(rel)
            origin = infer_origin(rel)
            lock = locks.get(origin, {})
            tags = list(dict.fromkeys(EXT_TAGS.get(path.suffix.lower(), []) + [asset_type]))
            assets.append(
                {
                    "id": stable_id(rel, asset_type),
                    "type": asset_type,
                    "path": rel,
                    "route_hint": route_hint,
                    "tags": tags,
                    "source": {
                        "origin": origin,
                        "repo": lock.get("url", ""),
                        "commit": lock.get("commit", ""),
                        "license": {
                            "ppt-master": "MIT",
                            "html-ppt-skill": "MIT",
                            "guizang-ppt-skill": "AGPL-3.0",
                            "ian-handdrawn-ppt": "MIT",
                            "yh-slides": "local",
                        }.get(origin, ""),
                    },
                }
            )

    registry = {
        "schema": "yh_slides_asset_registry.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "asset_count": len(assets),
        "source_locks": locks,
        "assets": sorted(assets, key=lambda item: (item["route_hint"], item["type"], item["path"])),
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_JSON} with {len(assets)} assets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
