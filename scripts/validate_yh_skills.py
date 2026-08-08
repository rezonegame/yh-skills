#!/usr/bin/env python3
"""UTF-8-safe validation for the maintained YH skills."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "skills-manifest.json"
PROVENANCE = ROOT / "provenance" / "yh-source-locks.json"
RELEASE_MANIFEST = ROOT / "release-manifest.json"
ADOPTION_DECISIONS = ROOT / "provenance" / "yh-github-adoption-decisions.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_provenance(skills: list[dict[str, str]]) -> list[str]:
    failures: list[str] = []
    if not PROVENANCE.is_file():
        return [f"missing provenance registry: {PROVENANCE.relative_to(ROOT)}"]
    try:
        data = json.loads(read(PROVENANCE))
    except json.JSONDecodeError as exc:
        return [f"invalid provenance registry JSON: {exc}"]
    if data.get("schema") != "yh-skills.provenance.v1":
        failures.append("provenance registry: unexpected schema")
    records = data.get("skills")
    if not isinstance(records, dict):
        return failures + ["provenance registry: missing skills object"]
    for skill in skills:
        name = skill["name"]
        entries = records.get(name)
        if not isinstance(entries, list):
            failures.append(f"provenance registry: {name} must have a source list")
            continue
        for index, entry in enumerate(entries, start=1):
            if not isinstance(entry, dict):
                failures.append(f"provenance registry: {name}[{index}] is not an object")
                continue
            for field in ("name", "url", "license", "role", "distribution"):
                if not isinstance(entry.get(field), str) or not entry[field].strip():
                    failures.append(f"provenance registry: {name}[{index}] missing {field}")
            for field in ("absorbed_commit", "reviewed_commit"):
                value = entry.get(field)
                if value is not None and (not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value)):
                    failures.append(f"provenance registry: {name}[{index}] invalid {field}")
            if entry.get("role") != "local-only" and entry.get("reviewed_commit") is None:
                failures.append(f"provenance registry: {name}[{index}] needs reviewed_commit")
    return failures


def validate_release_manifest() -> list[str]:
    if not RELEASE_MANIFEST.is_file():
        return [f"missing release manifest: {RELEASE_MANIFEST.relative_to(ROOT)}"]
    try:
        data = json.loads(read(RELEASE_MANIFEST))
    except json.JSONDecodeError as exc:
        return [f"invalid release manifest JSON: {exc}"]
    failures: list[str] = []
    if data.get("schema") != "yh-skills.release-manifest.v1":
        failures.append("release manifest: unexpected schema")
    if data.get("release_track") not in {"private-only", "public"}:
        failures.append("release manifest: invalid release_track")
    if data.get("provenance") != "provenance/yh-source-locks.json":
        failures.append("release manifest: provenance reference mismatch")
    return failures


def validate_adoption_decisions() -> list[str]:
    if not ADOPTION_DECISIONS.is_file():
        return [f"missing GitHub adoption decisions: {ADOPTION_DECISIONS.relative_to(ROOT)}"]
    try:
        data = json.loads(read(ADOPTION_DECISIONS))
    except json.JSONDecodeError as exc:
        return [f"invalid adoption decisions JSON: {exc}"]
    failures: list[str] = []
    if data.get("schema") != "yh-skills.github-adoption-decisions.v1":
        failures.append("adoption decisions: unexpected schema")
    decisions = data.get("decisions")
    if not isinstance(decisions, list) or len(decisions) < 8:
        failures.append("adoption decisions: expected at least eight decisions")
        return failures
    for index, decision in enumerate(decisions, 1):
        if not isinstance(decision, dict):
            failures.append(f"adoption decisions: item {index} is not an object")
            continue
        for field in ("target", "source", "license", "decision", "material", "test", "rollback"):
            if not isinstance(decision.get(field), str) or not decision[field].strip():
                failures.append(f"adoption decisions: item {index} missing {field}")
        if not re.fullmatch(r"[0-9a-f]{40}", str(decision.get("commit", ""))):
            failures.append(f"adoption decisions: item {index} invalid commit")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="treat SKILL.md length warnings as errors")
    parser.add_argument("--provenance", action="store_true", help="validate shared upstream-source records")
    args = parser.parse_args()
    manifest = json.loads(read(MANIFEST))
    failures: list[str] = []
    warnings: list[str] = []
    skills = manifest["skills"]
    if args.provenance:
        failures.extend(validate_provenance(skills))
        failures.extend(validate_release_manifest())
        failures.extend(validate_adoption_decisions())
    for item in skills:
        skill_dir = ROOT / item["path"]
        skill_md = skill_dir / "SKILL.md"
        agents = skill_dir / "agents" / "openai.yaml"
        if not skill_md.is_file():
            failures.append(f"{item['name']}: missing SKILL.md")
            continue
        text = read(skill_md)
        if not re.search(r"(?m)^name:\s*" + re.escape(item["name"]) + r"\s*$", text):
            failures.append(f"{item['name']}: frontmatter name mismatch")
        if not re.search(r"(?m)^description:\s*", text):
            failures.append(f"{item['name']}: missing description")
        if not agents.is_file():
            failures.append(f"{item['name']}: missing agents/openai.yaml")
        if len(text.splitlines()) > 500:
            warnings.append(f"{item['name']}: SKILL.md exceeds 500 lines")

    slides = ROOT / "yh-slides"
    image_tool = read(slides / "scripts" / "generate_image.py")
    if "?key=" in image_tool or "current_dir.parents" in image_tool:
        failures.append("yh-slides: API key transport or config discovery is unsafe")
    for source in ["scripts/browser_safety.mjs", "scripts/export_deck_pdf.mjs", "scripts/export_deck_stage_pdf.mjs", "scripts/gen_deck_thumbs.mjs"]:
        if "restrictContextToLocalRoots" not in read(slides / source):
            failures.append(f"yh-slides: missing local-only browser guard in {source}")

    social = ROOT / "yh-social-visual"
    for source in ["scripts/render-social-deck.mjs", "scripts/validate-social-deck.mjs"]:
        if "restrictContextToLocalRoots" not in read(social / source):
            failures.append(f"yh-social-visual: missing local-only browser guard in {source}")
    if "enable-unsafe-swiftshader" in read(social / "scripts/lib/browser-options.mjs"):
        failures.append("yh-social-visual: unsafe browser flag remains enabled")

    local = read(ROOT / "yh-local-knowledge/scripts/normalize.py")
    if "_file_sha256" not in local or "_atomic_write_text" not in local:
        failures.append("yh-local-knowledge: hash cache or atomic output guard is missing")
    humanizer = read(ROOT / "yh-humanizer/SKILL.md")
    if "不杜撰叙述者" not in humanizer:
        failures.append("yh-humanizer: factual narrator guard is missing")
    document = read(ROOT / "yh-document-studio/SKILL.md")
    if "scripts/check-update.sh" in document or "slides-weasy-ko.html" in document:
        failures.append("yh-document-studio: stale update/template contract remains")
    if not (ROOT / "yh-image-inspirer/scripts/audit_assets.py").is_file():
        failures.append("yh-image-inspirer: asset release audit is missing")
    profiler = ROOT / "yh-style-profiler"
    if profiler.exists():
        for source in ["scripts/analyze-samples.py", "scripts/self-check.py"]:
            if not (profiler / source).is_file():
                failures.append(f"yh-style-profiler: missing {source}")

    registry = subprocess.run(
        [sys.executable, str(ROOT / "scripts/generate_skill_registry.py"), "--check"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if registry.returncode:
        failures.append(registry.stdout.strip() or registry.stderr.strip() or "registry check failed")

    for warning in warnings:
        print(f"WARN: {warning}")
    for failure in failures:
        print(f"ERROR: {failure}")
    if failures or (args.strict and warnings):
        return 1
    print(f"OK: validated {len(skills)} YH skills with UTF-8-safe checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
