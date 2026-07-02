# Agent Contract

This file is the cross-agent execution contract for `yh-local-knowledge`. Any agent, framework, or GUI wrapper that claims to run this skill should obey this contract so that the workspace behaves consistently.

## 1. Invocation

The skill may be invoked by natural language, command palette, CLI wrapper, or GUI button. Regardless of invocation method, the agent must treat the current folder as the candidate workspace root unless the user explicitly provides another path.

Canonical user phrases:

```text
启动 yh-local-knowledge
初始化这个知识工作区
同步这个资料文件夹
帮我整理这个本地知识库
把这个文件夹变成知识资产系统
```

## 2. Required Inputs

The only required input is a local folder path.

If the folder has `原始资料/`, use it as the primary source root.

If the folder does not have `原始资料/` but contains source files, ask the user whether to:

1. Create `原始资料/` and leave existing files in place as an additional source root.
2. Create `原始资料/` and move/copy files there.

Default to option 1 if the user asks for the simplest path.

## 3. Required Output Structure

After initialization, the workspace root must contain:

```text
原始资料/
可信资产/
导出结果/
.knowledge/
```

`.knowledge/` must contain:

```text
workspace.md
manifest.json
state.json
source-map.md
extraction-menu.md
candidates/
maps/
indexes/
logs/
```

## 4. Canonical Action State Machine

Agents must follow this state machine:

```text
uninitialized
  -> initialized
  -> synced
  -> mapped
  -> menu_ready
  -> extracting
  -> candidate_ready
  -> review_pending
  -> asset_verified
  -> linted
  -> exported
```

Allowed shortcuts:

- `initialized -> synced -> mapped -> menu_ready` may happen in one run.
- `candidate_ready -> exported` is not allowed unless the export is explicitly marked as draft/candidate.
- `candidate_ready -> asset_verified` requires user approval.
- `asset_verified -> exported` must pass through `linted` (lint is required before export).

## 5. Required Action Definitions

### init

Create required folders and starter files. Do not parse deeply.

Completion criteria:

- Required directories exist.
- `.knowledge/workspace.md` exists.
- `.knowledge/manifest.json` exists.
- `.knowledge/state.json` exists.

### sync

Scan source roots, update metadata, hash files if possible, and update `manifest.json`.

Completion criteria:

- `manifest.json` lists every discovered source file.
- Each file has `source_id`, `path`, `type`, `status`, and available metadata.
- `state.json.last_sync_at` is updated.

### map

Generate or update `.knowledge/source-map.md`.

Completion criteria:

- Includes overview, file inventory, virtual categories, possible themes, limitations, and next actions.
- Does not claim content from unparsed files.

### menu

Generate `.knowledge/extraction-menu.md`.

Completion criteria:

- Lists recommended extractable packages.
- Explains expected output and when to use each package.
- Recommends one next package based on available sources.

### extract

Generate candidate knowledge under `.knowledge/candidates/`.

Completion criteria:

- Candidate files include frontmatter.
- Candidate files include source references.
- Candidate files remain outside `可信资产/`.

### review

Present candidates for user decision.

Completion criteria:

- User can choose confirm, edit-confirm, reject, uncertain, split, or merge.
- Confirmed or edited-confirmed items are saved to `可信资产/`.

### export

Generate deliverables under `导出结果/`.

Completion criteria:

- Export target folder exists.
- Export includes source/asset references.
- Draft exports based on unverified candidates are labeled as draft.

### lint

Run `scripts/lint_workspace.py` to check trusted-asset health (orphans, stale, dangling refs, incomplete frontmatter, missing sources).

Completion criteria:

- Lint has run and its report is available.
- Findings are filed as candidates (not auto-applied to assets).
- Blocking findings (broken sources, missing required frontmatter) are surfaced to the user before export.

### feedback

Process anchor-based feedback under `.knowledge/feedback/`. See `references/governance.md`.

Completion criteria:

- Each open feedback gets one of: accept / partial / reject (with reason) / defer.
- Accepted/partial changes become candidates and go through the review gate before touching assets.
- Rejected feedback moves to `resolved/` and is never deleted.

## 6. Required User Approval Gates

Agents must not:

- Write unreviewed candidates into `可信资产/`.
- Mark a candidate as `verified` without user approval.
- Delete raw source files.
- Move raw source files unless the user explicitly approves.
- Overwrite an existing asset without versioning or asking.

## 7. Degradation Rules

Agents have different tool access. Use these rules:

- If hashing is unavailable, use path + size + modified time and note `hash_unavailable`.
- If content extraction is unavailable, index metadata only.
- If embedding/vector search is unavailable, use filename, headings, file snippets, and user-provided context.
- If a file cannot be read, mark it as `failed` and record the error.
- Never invent content to compensate for missing tools.

## 8. Determinism Rules

To keep behavior consistent across agents:

- Use stable IDs sorted by normalized relative path.
- Preserve existing IDs across syncs.
- Use ISO-8601 timestamps.
- Use UTF-8 files.
- Use Markdown for human-readable artifacts.
- Use JSON for state and manifests.
- Keep user-facing folder names in Chinese by default: `原始资料`, `可信资产`, `导出结果`.
- Keep internal folder name `.knowledge`.

## 9. Required Final Response Pattern

After a run, summarize in this order:

```text
完成状态：
- 初始化：
- 同步：
- 资料地图：
- 候选菜单：
- 候选资产：
- 可信资产：
- 导出：

关键文件：
- [path]

下一步建议：
1. ...
```

If blocked, explain the exact missing input or unavailable capability and state what was still completed.

## 10. Compliance Checklist

Before finishing, verify:

- Required folders exist.
- `manifest.json` is valid JSON.
- `state.json` is valid JSON.
- `source-map.md` exists.
- `extraction-menu.md` exists or the reason for not generating it is stated.
- No unverified knowledge was saved into `可信资产/`.
- No raw files were deleted or moved without approval.
