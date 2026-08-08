#!/usr/bin/env python3
"""Skill-creator style self-audit for the absorbed yh-slides skill."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="ignore")


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def check(name: str, passed: bool, evidence: str, failures: list[str]) -> None:
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}: {evidence}")
    if not passed:
        failures.append(f"{name}: {evidence}")


def main() -> int:
    failures: list[str] = []
    skill = read("SKILL.md")
    lines = skill.splitlines()

    check(
        "frontmatter has name and description",
        skill.startswith("---") and "name: yh-slides" in skill and "description:" in skill,
        "SKILL.md frontmatter present",
        failures,
    )
    check(
        "progressive disclosure keeps SKILL body navigable",
        len(lines) < 700 and "内置能力与参考索引" in skill and "references/" in skill,
        f"SKILL.md has {len(lines)} lines and links references",
        failures,
    )
    check(
        "strong guidance preserved",
        all(term in skill for term in ["Step 0", "意图启动面板", "推荐项", "备选项", "风险提示", "样稿"]),
        "Step 0 / recommendation / risk / sample checkpoints present",
        failures,
    )
    check(
        "new paths exposed without replacing originals",
        all(term in skill for term in ["2A-S", "2A-T", "2D-P", "2D-B", "2A 通用可编辑", "2B 整图", "2C 视觉底图", "2D 多功能"]),
        "old and new path labels coexist",
        failures,
    )
    check(
        "local assets are discoverable via registry",
        exists("references/meta/asset-registry.json") and exists("references/meta/asset-registry.md"),
        "asset registry doc and JSON exist",
        failures,
    )
    if exists("references/meta/asset-registry.json"):
        registry = json.loads(read("references/meta/asset-registry.json"))
        origins = {item.get("source", {}).get("origin") for item in registry.get("assets", [])}
        check(
            "asset registry covers local and absorbed sources",
            registry.get("asset_count", 0) > 1000
            and all(src in origins for src in ["ppt-master", "guizang-ppt-skill", "html-ppt-skill", "bento", "yh-slides"]),
            f"asset_count={registry.get('asset_count')}, origins={sorted(origins)}",
            failures,
        )
    check(
        "provenance and license records exist",
        all(
            exists(path)
            for path in [
                "references/meta/upstreams.md",
                "provenance/upstream-locks/ppt-master.source.json",
                "provenance/upstream-locks/html-ppt-skill.source.json",
                "provenance/upstream-locks/guizang-ppt-skill.source.json",
                "provenance/upstream-locks/ian-handdrawn-ppt.source.json",
                "provenance/upstream-locks/academic-pptx-skill.source.json",
                "provenance/upstream-locks/dashi-ppt-skill.source.json",
                "provenance/upstream-locks/bento.source.json",
                "assets/external-licenses/ppt-master-MIT.txt",
                "assets/external-licenses/html-ppt-skill-MIT.txt",
                "assets/external-licenses/guizang-ppt-skill-AGPL-3.0.txt",
                "assets/external-licenses/ian-handdrawn-ppt-MIT.txt",
                "assets/external-licenses/ian-handdrawn-ppt-NOTICE.md",
                "assets/external-licenses/academic-pptx-skill-MIT.txt",
                "assets/external-licenses/dashi-ppt-skill-AGPL-3.0-method-only.md",
                "assets/external-licenses/bento-MIT.txt",
            ]
        ),
        "upstream locks and required licenses present",
        failures,
    )
    check(
        "offline gates are scripted",
        all(
            exists(path)
            for path in [
                "scripts/check_offline_ready.py",
                "scripts/check_yh_slides_integrity.py",
                "scripts/build_asset_registry.py",
            "scripts/check_upstream_locks.py",
            "scripts/create_contact_sheet.py",
            ]
        ),
        "offline/integrity/registry scripts present",
        failures,
    )
    q = read("references/constraints/quality-checklist.md")
    check(
        "quality checklist covers new paths",
        all(term in q for term in ["2A-S / Path S", "2A-T / Template Fill", "2D-P / Presenter Mode", "2D-B / Bento Deck"]),
        "quality-checklist has dedicated sections for 2A-S, 2A-T, 2D-P, 2D-B",
        failures,
    )
    workflows = read("references/paths/path-workflows.md")
    check(
        "workflow docs cover new execution paths",
        all(term in workflows for term in ["Path S / 2A-S", "Template Fill / 2A-T", "Presenter Mode / 2D-P", "Bento Adapter / 2D-B"]),
        "path-workflows includes new execution chains",
        failures,
    )
    check(
        "migration safety backup exists",
        any((ROOT / "backups").glob("pre-absorb-vendors-*")),
        "timestamped pre-absorption backup found",
        failures,
    )
    runtime_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in [
            ROOT / "templates/html-decks/guizang/template.html",
            ROOT / "templates/html-decks/guizang/template-swiss.html",
            ROOT / "templates/html-decks/html-ppt/fonts.css",
        ]
        if path.exists()
    )
    check(
        "critical absorbed runtime uses local assets",
        "fonts.googleapis" not in runtime_text
        and "unpkg.com" not in runtime_text
        and "cdn.jsdelivr.net" not in runtime_text
        and "google-fonts-local.css" in runtime_text,
        "guizang/html-ppt critical runtime patched to local font/js paths",
        failures,
    )
    check(
        "references avoid deep hidden dependencies",
        all(
            exists(path)
            for path in [
                "references/integrations/template-fill-pptx.md",
                "references/integrations/presenter-mode.md",
                "references/aesthetics/screenshot-framing.md",
                "references/aesthetics/swiss/swiss-map-component.md",
            ]
        )
        and "asset-registry.json" in skill,
        "new references are directly reachable from SKILL/INDEX",
        failures,
    )
    ian_reference = read("references/aesthetics/ian-handdrawn-technical.md")
    check(
        "Ian hand-drawn style is routed without a new path",
        all(term in ian_reference for term in ["2B / Path B", "2C / Path H", "Required text only", "不新增模式或路径"])
        and exists("assets/style-samples/ian-handdrawn-technical-anchor.png"),
        "Ian style contract and attributed visual anchor are present",
        failures,
    )
    academic_reference = read("references/contracts/academic-deck.md")
    candidate_reference = read("references/aesthetics/content-layout-candidates.md")
    check(
        "academic and layout-method integrations stay path-neutral",
        all(term in academic_reference for term in ["structured_argument", "visual_narrative", "references", "appendix"])
        and all(term in candidate_reference for term in ["canonical content", "capacity", "composition family"])
        and exists("references/meta/academic-and-dashi-integration.md"),
        "academic v2 and Dashi-derived method layer are documented without a new runtime path",
        failures,
    )
    bento_reference = read("references/contracts/bento-deck.md")
    bento_shell = ROOT / "templates/html-decks/bento/Bento_Slides.bento.html"
    check(
        "Bento adapter remains local and explicitly scoped",
        all(term in bento_reference for term in ["yh_slides_bento_deck.v1", "allow_external_media", "collaboration"])
        and exists("references/integrations/bento-deck-adapter.md")
        and bento_shell.exists(),
        "Bento contract, adapter guide and pinned local shell present",
        failures,
    )
    remote_runtime = re.compile(
        r"""(?:src|href)\s*=\s*["']https?://|@import\s+url\(["']?https?://|import\(["']https?://|url\(["']https?://""",
        re.IGNORECASE,
    )
    scan_files = list((ROOT / "assets/seeds").rglob("*.html")) + list((ROOT / "templates/html-decks").rglob("*.html"))
    offenders = []
    for path in scan_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if remote_runtime.search(text):
            offenders.append(path.relative_to(ROOT).as_posix())
    check(
        "no remote runtime in seed/template HTML",
        not offenders,
        "no offenders" if not offenders else ", ".join(offenders[:10]),
        failures,
    )
    removed_upstream_dir = "vendor" + "_sources"
    check(
        "no live upstream source-tree dependency",
        removed_upstream_dir not in skill and not (ROOT / removed_upstream_dir).exists(),
        "SKILL.md and filesystem do not require the removed upstream source-tree layer",
        failures,
    )

    if failures:
        print("\nSkill self-audit FAILED:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("\nSkill self-audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
