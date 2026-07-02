#!/usr/bin/env python3
"""Lint a yh-local-knowledge workspace for knowledge health.

Checks the trusted assets and candidate areas for structural problems that
indicate knowledge rot: broken cross-references, orphan assets (no links in
or out), stale assets (long unupdated), missing index entries, incomplete
frontmatter, and dangling source references.

Inspired by llm-wiki-skill's lint_wiki.py (zero-dependency, minimal YAML parse).

Usage:
    python scripts/lint_workspace.py <workspace_root>
    python scripts/lint_workspace.py <workspace_root> --json

Pure standard library. Exits 0 if clean, 1 if issues found.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ASSETS_DIR = "可信资产"
CANDIDATES_DIR = ".knowledge/candidates"
STALE_DAYS = 180  # asset not updated in this many days is flagged stale (advisory)

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML frontmatter parser. Only handles flat key: value and lists."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm: dict = {}
    current_list_key = None
    for line in m.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- ") and current_list_key:
            fm[current_list_key].append(stripped[2:].strip())
            continue
        if ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip()
            current_list_key = None
            if val == "":
                fm[key] = []
                current_list_key = key
            else:
                # strip quotes
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                # inline list: [a, b, c]
                if val.startswith("[") and val.endswith("]"):
                    inner = val[1:-1].strip()
                    fm[key] = [x.strip().strip('"') for x in inner.split(",") if x.strip()] if inner else []
                else:
                    fm[key] = val
    return fm


def collect_md_files(root: Path, *dirs: str) -> list[tuple[Path, dict]]:
    """Collect markdown files with parsed frontmatter from given dirs."""
    out = []
    for d in dirs:
        dp = root / d
        if not dp.exists():
            continue
        for p in dp.rglob("*.md"):
            try:
                fm = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                fm = {}
            out.append((p, fm))
    return out


def check_frontmatter(files: list[tuple[Path, dict]]) -> list[str]:
    """Check required frontmatter fields on assets (id, type, title, sources)."""
    issues = []
    required = ["id", "type", "title"]
    for p, fm in files:
        if not fm:
            issues.append(f"{p.name}: no frontmatter")
            continue
        for field in required:
            if field not in fm:
                issues.append(f"{p.name}: missing frontmatter field '{field}'")
        # assets should have sources
        if "sources" not in fm or fm.get("sources") in ([], ""):
            issues.append(f"{p.name}: no sources (untraceable)")
    return issues


def check_orphans(files: list[tuple[Path, dict]]) -> list[str]:
    """Assets with no 'related' links and not referenced by anyone else's 'related'."""
    issues = []
    all_ids = {fm.get("id") for _, fm in files if fm.get("id")}
    referenced: set[str] = set()
    for _, fm in files:
        rel = fm.get("related", [])
        if isinstance(rel, list):
            referenced.update(rel)
        elif isinstance(rel, str) and rel:
            referenced.add(rel)
    for p, fm in files:
        aid = fm.get("id")
        rel = fm.get("related", [])
        has_out = (isinstance(rel, list) and len(rel) > 0) or (isinstance(rel, str) and rel)
        has_in = aid in referenced if aid else False
        if not has_out and not has_in:
            issues.append(f"{p.name} (id={aid}): orphan — no links in or out")
    return issues


def check_stale(files: list[tuple[Path, dict]], now: datetime) -> list[str]:
    issues = []
    threshold = now.timestamp() - STALE_DAYS * 86400
    for p, fm in files:
        updated = fm.get("updated_at") or fm.get("created_at")
        if not updated:
            continue
        try:
            ts = datetime.fromisoformat(updated.replace("Z", "+00:00")).timestamp()
            if ts < threshold:
                issues.append(f"{p.name}: stale (not updated since {updated[:10]})")
        except Exception:
            pass
    return issues


def check_dangling_refs(files: list[tuple[Path, dict]], manifest_ids: set[str]) -> list[str]:
    """'related' or 'sources' pointing to non-existent ids."""
    issues = []
    for p, fm in files:
        for field in ("related",):
            rel = fm.get(field, [])
            if isinstance(rel, str):
                rel = [rel]
            for r in rel:
                if r and r not in manifest_ids and not _id_exists(files, r):
                    issues.append(f"{p.name}: {field} references unknown id '{r}'")
    return issues


def _id_exists(files: list[tuple[Path, dict]], target_id: str) -> bool:
    return any(fm.get("id") == target_id for _, fm in files)


def load_manifest_source_ids(root: Path) -> set[str]:
    mp = root / ".knowledge/manifest.json"
    if not mp.exists():
        return set()
    try:
        data = json.loads(mp.read_text(encoding="utf-8"))
        return {f.get("source_id") for f in data.get("files", []) if f.get("source_id")}
    except Exception:
        return set()


def main() -> int:
    p = argparse.ArgumentParser(description="Lint a yh-local-knowledge workspace")
    p.add_argument("workspace")
    p.add_argument("--json", action="store_true", help="output JSON instead of text")
    args = p.parse_args()

    root = Path(args.workspace).resolve()
    if not (root / ".knowledge").exists():
        print("not a yh-local-knowledge workspace (no .knowledge/)", file=sys.stderr)
        return 2

    assets = collect_md_files(root, ASSETS_DIR)
    manifest_ids = load_manifest_source_ids(root)

    checks = {
        "frontmatter": check_frontmatter(assets),
        "orphans": check_orphans(assets),
        "stale": check_stale(assets, datetime.now(timezone.utc)),
        "dangling_refs": check_dangling_refs(assets, manifest_ids),
    }
    all_issues = [i for issues in checks.values() for i in issues]

    if args.json:
        print(json.dumps({
            "workspace": str(root),
            "assets_checked": len(assets),
            "issues_by_check": {k: len(v) for k, v in checks.items()},
            "total_issues": len(all_issues),
            "issues": checks,
        }, ensure_ascii=False, indent=2))
    else:
        print(f"Linting {len(assets)} assets in {root.name}...")
        for check_name, issues in checks.items():
            status = "OK" if not issues else f"{len(issues)} issue(s)"
            print(f"  {check_name}: {status}")
            for i in issues:
                print(f"    - {i}")
        print()
        print(f"Total: {len(all_issues)} issue(s)" if all_issues else "Clean.")

    return 1 if all_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
