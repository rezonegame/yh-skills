#!/usr/bin/env python3
"""Build structural indexes for a yh-local-knowledge workspace.

Generates three JSON indexes under .knowledge/indexes/, inspired by knowhere's
structural retrieval (path navigation + multi-channel search + lightweight graph).
All pure standard library; keyword extraction itself is done by the LLM during
extraction — this script only does path parsing, RRF index generation, keyword
overlap graph computation, and importance stats.

Outputs:
  .knowledge/indexes/nav.json      — hierarchical navigation tree per source
  .knowledge/indexes/search.json   — three-channel (path/content/term) index text
  .knowledge/indexes/graph.json    — keyword-overlap graph + importance (hit counts)

Usage:
    python scripts/build_index.py <workspace>
    python scripts/build_index.py <workspace> --rebuild   # ignore mtime, full rebuild

Pure standard library.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

NORMALIZED_DIR = ".knowledge/normalized"
ASSETS_DIR = "可信资产"
INDEX_DIR = ".knowledge/indexes"
GRAPH_OVERLAP_THRESHOLD = 0.15  # Jaccard; lowered so opposing views sharing one core term still link
SHARED_KEYWORD_MIN = 2  # or at least this many shared keywords
SHARED_CORE_MIN_JACCARD = 0.1  # if only 1 shared keyword, still link if Jaccard >= this

HEADER_RE = re.compile(r"^(#{1,6})\s+(.*)$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_minimal_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm: dict = {}
    current_key = None
    for line in m.group(1).splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("- ") and current_key:
            fm.setdefault(current_key, []).append(s[2:].strip().strip('"'))
            continue
        if ":" in s:
            k, _, v = s.partition(":")
            k, v = k.strip(), v.strip()
            current_key = None
            if v == "":
                fm[k] = []
                current_key = k
            else:
                if v.startswith("[") and v.endswith("]"):
                    inner = v[1:-1].strip()
                    fm[k] = [x.strip().strip('"') for x in inner.split(",") if x.strip()] if inner else []
                elif v.startswith('"') and v.endswith('"'):
                    fm[k] = v[1:-1]
                else:
                    fm[k] = v
    return fm


def extract_outline(text: str, file_label: str, workspace: str) -> dict:
    """Build a nav-tree node from markdown headers. Returns the root node.

    The first H1 (if present) is promoted to the root's title; subsequent
    headers build the children hierarchy.
    """
    lines = text.splitlines()
    root = {"title": file_label, "path": f"{workspace}/{file_label}", "summary": "", "children": []}
    stack = [(0, root)]  # (level, node)
    # first non-empty, non-header line as summary
    for ln in lines:
        stripped = ln.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("---"):
            root["summary"] = stripped[:120]
            break

    promoted_h1 = False
    for ln in lines:
        m = HEADER_RE.match(ln)
        if not m:
            continue
        level = len(m.group(1))
        title = m.group(2).strip()
        # Promote the first H1 to be the root's title (avoid a redundant wrapper node).
        if level == 1 and not promoted_h1:
            root["title"] = title
            root["path"] = f"{workspace}/{file_label}"
            promoted_h1 = True
            continue
        node = {"title": title, "path": "", "summary": "", "children": []}
        # pop stack to parent (headers below H1 use level-1 so H2 is depth 1)
        effective_level = level - 1 if promoted_h1 else level
        while stack and stack[-1][0] >= effective_level:
            stack.pop()
        if not stack:
            stack.append((0, root))
        parent = stack[-1][1]
        node["path"] = f"{parent['path']}/{title}"
        parent["children"].append(node)
        stack.append((effective_level, node))
    return root


def build_nav(workspace: Path, ws_name: str) -> dict:
    """Build nav.json from normalized markdown files."""
    nav = {"workspace": ws_name, "trees": {}, "generated_at": _now()}
    norm = workspace / NORMALIZED_DIR
    if not norm.exists():
        return nav
    for src_root in norm.iterdir():
        if not src_root.is_dir():
            continue
        for md in src_root.glob("**/*.md"):
            try:
                text = md.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            label = md.name
            nav["trees"][f"{src_root.name}/{label}"] = extract_outline(text, label, ws_name)
    return nav


def tokenize(text: str) -> list[str]:
    """Simple tokenizer for CJK + ascii. Splits on non-alphanumeric/CJK."""
    # keep CJK runs and ascii words
    tokens = re.findall(r"[\u4e00-\u9fff]+|[a-zA-Z0-9]+", text.lower())
    # further split CJK runs into chars for coarse matching (no jieba dependency)
    out = []
    for t in tokens:
        if re.fullmatch(r"[\u4e00-\u9fff]+", t):
            out.extend(list(t))
        else:
            out.append(t)
    return out


def build_search_index(workspace: Path, nav: dict) -> dict:
    """Build search.json with path/content/term channels. term channel uses nav summaries."""
    items = []
    # add normalized sections from nav
    def walk(node: dict, root_text_acc=""):
        if node.get("path"):
            path_tokens = " ".join(re.split(r"[/\s]", node["path"]))
            content = node.get("summary", "")
            items.append({
                "ref": node["path"],
                "path_text": path_tokens,
                "content_text": content,
                "term_text": content,
                "path": node["path"],
            })
        for c in node.get("children", []):
            walk(c)

    for _, tree in nav.get("trees", {}).items():
        walk(tree)

    # add trusted assets as searchable items
    assets_dir = workspace / ASSETS_DIR
    if assets_dir.exists():
        for md in assets_dir.glob("**/*.md"):
            try:
                text = md.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            fm = parse_minimal_frontmatter(text)
            body = FRONTMATTER_RE.sub("", text)
            aid = fm.get("id", md.stem)
            title = fm.get("title", md.stem)
            path = f"{aid}/{title}"
            items.append({
                "ref": aid,
                "path_text": f"{aid} {title} {' '.join(fm.get('tags', [])) if isinstance(fm.get('tags'), list) else ''}",
                "content_text": (title + " " + body[:500]).strip(),
                "term_text": " ".join(fm.get("tags", []) if isinstance(fm.get("tags"), list) else []) or title,
                "path": path,
            })

    return {"generated_at": _now(), "item_count": len(items), "items": items}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def build_graph(workspace: Path, prev_graph: dict | None) -> dict:
    """Build graph.json from asset keywords (LLM-provided in frontmatter)."""
    assets_dir = workspace / ASSETS_DIR
    nodes = []
    if assets_dir.exists():
        for md in assets_dir.glob("**/*.md"):
            try:
                text = md.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            fm = parse_minimal_frontmatter(text)
            aid = fm.get("id", md.stem)
            kws = fm.get("keywords", fm.get("tags", []))
            if isinstance(kws, str):
                kws = [k.strip() for k in kws.split(",") if k.strip()]
            # merge prev hit_count for compounding
            prev_node = next((n for n in (prev_graph or {}).get("nodes", []) if n["id"] == aid), None)
            nodes.append({
                "id": aid,
                "title": fm.get("title", md.stem),
                "keywords": list(kws),
                "importance": (prev_node or {}).get("importance", 0.0),
                "hit_count": (prev_node or {}).get("hit_count", 0),
                "last_hit_at": (prev_node or {}).get("last_hit_at"),
            })

    edges = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            ka, kb = set(nodes[i]["keywords"]), set(nodes[j]["keywords"])
            if not ka or not kb:
                continue
            shared = ka & kb
            jac = jaccard(ka, kb)
            # Link when: strong overlap, or multiple shared terms, or one shared core
            # term with non-trivial Jaccard (so opposing views on the same topic link).
            if jac >= GRAPH_OVERLAP_THRESHOLD or len(shared) >= SHARED_KEYWORD_MIN \
                    or (len(shared) >= 1 and jac >= SHARED_CORE_MIN_JACCARD):
                edges.append({
                    "from": nodes[i]["id"],
                    "to": nodes[j]["id"],
                    "weight": round(jac, 3),
                    "shared_keywords": sorted(shared),
                })

    # normalize importance by hit_count
    max_hits = max((n["hit_count"] for n in nodes), default=0) or 1
    for n in nodes:
        n["importance"] = round(n["hit_count"] / max_hits, 3)

    return {"generated_at": _now(), "nodes": nodes, "edges": edges, "overlap_threshold": GRAPH_OVERLAP_THRESHOLD}


def record_hit(workspace: Path, asset_id: str) -> int:
    """Increment hit_count for an asset (called when asset is used in retrieval/export)."""
    gpath = workspace / INDEX_DIR / "graph.json"
    g = json.loads(gpath.read_text(encoding="utf-8")) if gpath.exists() else {"nodes": [], "edges": []}
    now = _now()
    found = False
    for n in g["nodes"]:
        if n["id"] == asset_id:
            n["hit_count"] += 1
            n["last_hit_at"] = now
            found = True
            break
    if found:
        max_hits = max((n.get("hit_count", 0) for n in g["nodes"]), default=0) or 1
        for n in g["nodes"]:
            n["importance"] = round(n.get("hit_count", 0) / max_hits, 3)
        gpath.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0
    print(f"asset {asset_id} not found in graph", file=sys.stderr)
    return 1


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    p = argparse.ArgumentParser(description="Build nav/search/graph indexes")
    p.add_argument("workspace")
    p.add_argument("--rebuild", action="store_true")
    p.add_argument("--hit", help="record a usage hit for an asset id (compounding)")
    args = p.parse_args()

    workspace = Path(args.workspace).resolve()
    if args.hit:
        return record_hit(workspace, args.hit)

    if not (workspace / ".knowledge").exists():
        print("not a yh workspace (no .knowledge/)", file=sys.stderr)
        return 2

    ws_name = workspace.name
    idx_dir = workspace / INDEX_DIR
    idx_dir.mkdir(parents=True, exist_ok=True)

    prev_graph = None
    gp = idx_dir / "graph.json"
    if gp.exists() and not args.rebuild:
        try:
            prev_graph = json.loads(gp.read_text(encoding="utf-8"))
        except Exception:
            prev_graph = None

    nav = build_nav(workspace, ws_name)
    search = build_search_index(workspace, nav)
    graph = build_graph(workspace, prev_graph)

    (idx_dir / "nav.json").write_text(json.dumps(nav, ensure_ascii=False, indent=2), encoding="utf-8")
    (idx_dir / "search.json").write_text(json.dumps(search, ensure_ascii=False, indent=2), encoding="utf-8")
    (idx_dir / "graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({
        "workspace": ws_name,
        "nav_trees": len(nav["trees"]),
        "search_items": search["item_count"],
        "graph_nodes": len(graph["nodes"]),
        "graph_edges": len(graph["edges"]),
        "generated_at": _now(),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
