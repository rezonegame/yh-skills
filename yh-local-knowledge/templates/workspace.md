# [Topic] Knowledge Workspace

## Purpose

This folder is a local knowledge workspace. Put raw source files in `原始资料/`. The agent maintains internal state in `.knowledge/`, drafts candidates in `.knowledge/candidates/`, saves user-approved knowledge in `可信资产/`, and writes final deliverables to `导出结果/`.

## User-Facing Folders

- `原始资料/`: raw files collected by the user.
- `可信资产/`: knowledge approved by the user.
- `导出结果/`: generated packages, reports, specs, or agent workspaces.

## Current Goals

- [ ] Normalize binary sources to markdown (scripts/normalize.py)
- [ ] Sync source files
- [ ] Generate source map
- [ ] Generate extraction menu
- [ ] Extract candidate package
- [ ] Review candidates
- [ ] Export deliverable

## Notes

Do not edit raw source files unless explicitly requested. Binary sources (PDF/Word/Excel/etc.) are converted to read-only markdown under `.knowledge/normalized/` — sync/index/extract operate on that layer, not the raw binaries.
