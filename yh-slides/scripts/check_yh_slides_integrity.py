#!/usr/bin/env python3
"""Check yh-slides structural integrity after full upstream absorption."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "references/_INDEX.md",
    "references/meta/upstreams.md",
    "references/meta/second-pass-upstream-audit.md",
    "references/meta/asset-registry.md",
    "references/meta/asset-registry.json",
    "references/meta/upgrade-policy.md",
    "references/constraints/offline-runtime.md",
    "references/integrations/path-s-svg-native-pptx.md",
    "references/integrations/figedit-reconstruction.md",
    "references/integrations/template-fill-pptx.md",
    "references/integrations/presenter-mode.md",
    "references/aesthetics/screenshot-framing.md",
    "references/aesthetics/ian-handdrawn-technical.md",
    "references/aesthetics/swiss/swiss-map-component.md",
    "references/constraints/quality-checklist.md",
    "assets/seeds/path-a-seed.html",
    "assets/seeds/path-c-magazine-seed.html",
    "assets/seeds/path-c-swiss-seed.html",
    "assets/seeds/path-c-minimal-seed.html",
    "assets/seeds/path-d-animated-seed.html",
    "assets/vendor/google-fonts-local.css",
    "assets/vendor/js/lucide.min.js",
    "assets/vendor/js/motion.min.js",
    "templates/html-decks/html-ppt/runtime.js",
    "templates/html-decks/html-ppt/full-decks/presenter-mode-reveal/index.html",
    "templates/html-decks/guizang/template.html",
    "templates/html-decks/guizang/template-swiss.html",
    "scripts/build_asset_registry.py",
    "scripts/check_offline_ready.py",
    "scripts/check_yh_slides_integrity.py",
    "scripts/check_upstream_locks.py",
    "scripts/create_contact_sheet.py",
    "scripts/figedit_batch.py",
    "scripts/skill_creator_self_audit.py",
    "scripts/template_fill_pptx.py",
    "provenance/upstream-locks/ppt-master.source.json",
    "provenance/upstream-locks/guizang-ppt-skill.source.json",
    "provenance/upstream-locks/html-ppt-skill.source.json",
    "provenance/upstream-locks/ian-handdrawn-ppt.source.json",
    "assets/style-samples/ian-handdrawn-technical-anchor.png",
]

REQUIRED_DIRS = [
    "backups",
    "templates/charts",
    "templates/icons",
    "templates/layouts",
    "templates/html-decks",
    "assets/screenshot-backgrounds",
    "scripts/template_fill_pptx",
    "references/provenance",
]

LICENSES = [
    "assets/external-licenses/ppt-master-MIT.txt",
    "assets/external-licenses/html-ppt-skill-MIT.txt",
    "assets/external-licenses/guizang-ppt-skill-AGPL-3.0.txt",
    "assets/external-licenses/ian-handdrawn-ppt-MIT.txt",
    "assets/external-licenses/ian-handdrawn-ppt-NOTICE.md",
    "assets/external-licenses/chartjs-MIT.txt",
    "assets/external-licenses/highlightjs-BSD-3-Clause.txt",
]

SKILL_REQUIRED_TERMS = [
    "2A-S",
    "Path S",
    "2A-T",
    "Template Fill",
    "2D-P",
    "Presenter Mode",
    "FigEdit Reconstruction",
    "asset-registry",
    "Step 0",
]


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED_FILES + LICENSES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing file: {rel}")
    for rel in REQUIRED_DIRS:
        if not (ROOT / rel).is_dir():
            errors.append(f"missing directory: {rel}")

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8", errors="ignore")
    for term in SKILL_REQUIRED_TERMS:
        if term not in skill_text:
            errors.append(f"SKILL.md missing required term: {term}")

    registry_path = ROOT / "references/meta/asset-registry.json"
    if registry_path.exists():
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            if registry.get("asset_count", 0) <= 0:
                errors.append("asset registry has no assets")
            origins = {item.get("source", {}).get("origin") for item in registry.get("assets", [])}
            for source in ("ppt-master", "guizang-ppt-skill", "html-ppt-skill", "ian-handdrawn-ppt", "yh-slides"):
                if source not in origins:
                    errors.append(f"asset registry missing origin: {source}")
        except json.JSONDecodeError as exc:
            errors.append(f"asset registry is invalid JSON: {exc}")

    if errors:
        print("yh-slides integrity check FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("yh-slides integrity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
