#!/usr/bin/env python3
"""Rebuild and validate the local Tosea preview catalog from files on disk."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOSEA = ROOT / "templates" / "tosea"
OUT = TOSEA / "metadata.json"
ASSET_NAMES = ("preview.webp", "cover_page.webp", "content_page.webp", "table_page.webp")
CATEGORY_TERMS = {
    "pitch_investment": {"pitch", "invest", "capital", "venture", "startup", "fund", "finance", "financial", "bp"},
    "education_academic": {"academic", "thesis", "education", "course", "class", "university", "research", "science", "medical", "biotech"},
    "company_marketing": {"company", "marketing", "sales", "product", "launch", "business", "corporate", "brand"},
    "consulting_research": {"consulting", "strategy", "report", "analysis", "mckinsey", "bain", "deloitte", "bcg"},
    "personal_career": {"resume", "career", "portfolio", "personal", "job"},
    "life_events": {"wedding", "festival", "ceremony", "travel", "food", "life"},
    "creative_brand": {"creative", "editorial", "fashion", "art", "design", "magazine", "mono", "minimal", "folio"},
    "workplace": {"work", "qbr", "annual", "summary", "training", "meeting"},
}


def tokens(name: str) -> list[str]:
    clean = re.sub(r"^(?:gi2|ref)_d\d+_?", "", name.lower())
    return [part for part in re.split(r"[^a-z0-9]+", clean) if part]


def category(parts: list[str]) -> str:
    values = set(parts)
    for name, terms in CATEGORY_TERMS.items():
        if values & terms:
            return name
    return "industry_or_other"


def record(path: Path, family: str) -> dict:
    rel = path.relative_to(TOSEA).as_posix()
    parts = tokens(path.name)
    return {
        "name": path.name,
        "family": family,
        "path": rel,
        "category": category(parts),
        "tokens": parts,
        "assets": [name for name in ASSET_NAMES if (path / name).is_file()],
    }


def main() -> int:
    if not TOSEA.is_dir():
        raise SystemExit(f"missing Tosea root: {TOSEA}")
    originals = sorted(p for p in TOSEA.iterdir() if p.is_dir() and p.name not in {"gi2", "originals"})
    gi2_root = TOSEA / "gi2"
    gi2 = sorted(p for p in gi2_root.iterdir() if p.is_dir()) if gi2_root.is_dir() else []
    catalog = [record(p, "original") for p in originals] + [record(p, "gi2") for p in gi2]
    missing_preview = [item["path"] for item in catalog if "preview.webp" not in item["assets"]]
    if missing_preview:
        print(f"WARN: {len(missing_preview)} template directories have no preview.webp")

    old_sample: list[str] = []
    if OUT.is_file():
        try:
            old_sample = json.loads(OUT.read_text(encoding="utf-8")).get("gi2_sample", [])
        except (json.JSONDecodeError, AttributeError):
            pass
    actual_names = {p.name for p in gi2}
    sample = [name for name in old_sample if name in actual_names]
    for name in sorted(actual_names):
        if len(sample) >= 50:
            break
        if name not in sample:
            sample.append(name)

    counts = Counter(item["category"] for item in catalog)
    data = {
        "schema": "yh-slides.tosea-preview-index.v2",
        "generated_at": date.today().isoformat(),
        "description": "Local preview-only catalog rebuilt from actual directories; no remote runtime dependency.",
        "total": len(catalog),
        "originals_count": len(originals),
        "gi2_count": len(gi2),
        "originals": [p.name for p in originals],
        "gi2_sample": sample,
        "gi2_full": [p.name for p in gi2],
        "categories": dict(sorted(counts.items())),
        "missing_preview_count": len(missing_preview),
        "catalog": catalog,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} with {len(catalog)} template records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
