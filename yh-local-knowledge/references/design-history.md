# YH Local Knowledge Design History

This document records the discussion and reasoning that led to `yh-local-knowledge`. Use it as background for future upgrades, product planning, architecture decisions, and comparisons with Anything2Ontology.

## 1. Starting Point: Anything2Ontology

The discussion began with `rezonegame/Anything2Ontology`, a pipeline that converts many input formats into an `ontology/` workspace for coding agents.

The project's core flow was understood as:

```text
Input files / URLs
  -> Anything2Markdown
  -> Markdown2Chunks
  -> Chunks2SKUs
  -> SKUs2Ontology
  -> ontology/
```

Its output is designed for an AI coding agent:

```text
ontology/
├── spec.md
├── mapping.md
├── eureka.md
├── README.md
└── skus/
```

The key interpretation was:

> Anything2Ontology is less a traditional OWL/RDF ontology system and more an agent-oriented knowledge workspace compiler.

It turns messy source material into structured, navigable, reusable files that an agent can consume.

## 2. Strengths Identified

Anything2Ontology has several strong ideas:

- It recognizes that raw files are too large and noisy for direct LLM context.
- It creates an intermediate workspace instead of relying only on one-shot prompting.
- It separates knowledge into useful categories: factual, relational, procedural, and meta.
- It tries to generate agent-consumable outputs such as `mapping.md`, `spec.md`, and `SKILL.md`.
- It is more than a prompt demo: it has CLI modules, schemas, logging, post-processing, deduplication, and confidence scoring.

The most valuable conceptual insight:

> Agent work benefits from a persistent knowledge workspace, not just ephemeral context.

## 3. Problems Found Through Use

After repeated use, several practical issues appeared:

1. Long-running data processing is slow and fragile.
2. When a run fails, recovery can be painful or require starting over.
3. The process is mostly black-box; progress is inferred from folder changes.
4. Configuration is hard for ordinary users.
5. The exported material often still requires another compilation or cleanup step.
6. Long-term evolution is weak.
7. The system feels like a one-time full compilation rather than a living knowledge asset system.

The core product concern:

> To make agents work better, the user first has to wait for another complicated agent-like pipeline to finish.

This can undermine practical value.

## 4. Key Question Raised

A central doubt emerged:

> How much value does this pipeline really add if stronger LLMs, larger context windows, and better constraints can already cover much of the same work?

The answer developed during discussion:

- For single tasks, strong models plus good prompts can cover much of the summarization/extraction/spec-generation work.
- For long-term, multi-source, multi-version, multi-project knowledge reuse, a persistent system still matters.
- The missing layer is not just extraction; it is lifecycle, traceability, confirmation, versioning, and export.

This led to a shift in framing:

```text
Not "Anything to Ontology"
but "Source folder to evolving knowledge assets"
```

## 5. Revised Direction

The proposed alternative became:

> A local-first, incremental personal knowledge asset system.

Instead of:

```text
Raw sources -> full ontology compilation
```

Use:

```text
Local folder
  -> incremental index
  -> source map
  -> extractable package menu
  -> user-selected extraction
  -> candidate knowledge
  -> user review
  -> trusted assets
  -> export targets
```

Core principle:

> First index, then extract. First generate candidates, then ask the user to confirm.

## 6. Why User Confirmation Matters

LLM output should not be treated as a trusted knowledge asset.

The system should distinguish:

```text
Source: original material, preserved as evidence.
Candidate: agent-generated knowledge, not yet trusted.
Asset: user-confirmed knowledge, versioned and reusable.
```

Candidate knowledge becomes trusted only after:

- user confirms it;
- user edits and confirms it;
- user marks it as acceptable for the intended purpose.

This review gate is the line between "LLM output" and "knowledge asset."

## 7. Multi-Workspace Requirement

The user may have many folders and many topics.

The system therefore should not be a single folder tool only. It should support:

```text
Workspace: 桌游设计
Workspace: AI Agent
Workspace: 营销案例
Workspace: 写作素材
Workspace: 客户项目
```

Each topic folder is a separate Workspace with its own:

- sources;
- manifest;
- index;
- candidates;
- assets;
- exports.

This prevents semantic contamination. For example, the word "机制" may mean different things in tabletop game design, education, software architecture, or policy analysis.

At the same time, future versions should support cross-workspace Projects:

```text
Project: 写一篇“AI Agent 如何改变桌游设计”的文章
  -> uses Workspace: 桌游设计
  -> uses Workspace: AI Agent
  -> exports writing package
```

Long-term assets live in Workspaces. Short-term goals live in Projects.

## 8. Simplified User Entry

A major design realization:

> Ordinary users should not need to design a knowledge directory structure.

The simplest real user behavior is:

```text
1. Create a topic folder.
2. Create `原始资料/`.
3. Drop all files into it.
4. Ask the agent to take over.
```

Therefore, the user-facing folder structure should be minimal:

```text
[主题文件夹]/
├── 原始资料/
├── 可信资产/
└── 导出结果/
```

The system can add:

```text
.knowledge/
```

as an internal working folder.

Ordinary users only need to understand:

```text
原始资料：我丢资料的地方
可信资产：我确认后的知识
导出结果：我要拿去用的产物
```

The agent should provide virtual classification views instead of forcing users to manually organize files.

## 9. Skill-First Strategy

The recommended implementation path became:

```text
1. Skill / protocol
2. Lightweight CLI
3. GUI
```

Why start with a Skill:

- The first thing to validate is the agent behavior protocol.
- A Skill can stabilize the workflow before building a product shell.
- Users can run it directly inside any topic folder.
- It avoids prematurely investing in GUI before the workflow is proven.

The Skill is not the final product, but it is the portable operational protocol.

## 10. GUI Later

A GUI is still valuable, but later.

Its primary value should be observability, not just chat:

- which files are indexed;
- which files failed;
- which candidates await review;
- which assets are verified;
- which assets need re-review because sources changed;
- what export packages exist;
- what the agent is currently doing.

Recommended GUI layout:

```text
Left: Workspace list
Center: source map / candidates / assets / exports
Right: agent panel + source preview + review controls
Top: sync / extract / review / export
```

## 11. Why The Skill Must Be Portable

The user requested that this Skill should not depend on a single agent implementation.

Therefore, `yh-local-knowledge` should behave as a cross-agent execution protocol:

- fixed directory structure;
- fixed state machine;
- fixed file schemas;
- fixed review gates;
- fixed export locations;
- fixed degradation rules;
- fixed completion report.

This led to adding:

```text
references/agent-contract.md
references/workspace-protocol.md
references/schemas/
templates/
```

The goal:

> Any agent that reads the Skill package should initialize, sync, map, extract, review, and export in the same way.

## 12. Core Architecture

The current architecture is:

```text
[Topic Folder]/
├── 原始资料/
├── 可信资产/
├── 导出结果/
└── .knowledge/
    ├── workspace.md
    ├── manifest.json
    ├── state.json
    ├── source-map.md
    ├── extraction-menu.md
    ├── candidates/
    ├── maps/
    ├── indexes/
    └── logs/
```

Key files:

- `manifest.json`: durable inventory of source files.
- `state.json`: workflow state and next actions.
- `source-map.md`: human-readable overview of the workspace.
- `extraction-menu.md`: recommended candidate packages.
- `.knowledge/candidates/`: unverified agent outputs.
- `可信资产/`: user-approved assets.
- `导出结果/`: deliverables.

## 13. Extraction Packages

The first package menu includes:

1. 概念术语包
2. 学习路径包
3. 流程技能包
4. 写作素材包
5. 产品 / Agent Spec 包
6. 争议观点包

These are not all generated by default. The user chooses based on their goal.

This avoids wasteful full extraction and makes the process more transparent.

## 14. Export Targets

The export layer is essential. Without it, the system risks becoming only a high-end file indexer.

Planned export targets:

- learning pack;
- writing pack;
- product pack;
- agent workspace;
- Obsidian vault;
- skill pack.

Agent Workspace export may include:

```text
agent-workspace/
├── README.md
├── spec.md
├── mapping.md
├── assets/
└── sources.md
```

This absorbs the most useful part of Anything2Ontology as one export target, not the whole system's default behavior.

## 15. MVP Scope

Initial MVP should focus on:

1. folder initialization;
2. manifest and state files;
3. metadata-first sync;
4. Markdown/TXT/JSON/CSV reading;
5. source map generation;
6. extraction menu generation;
7. concept package, learning path package, and agent spec package;
8. candidate review;
9. trusted asset saving;
10. Markdown export.

Defer:

- complex vector databases;
- real-time file watching;
- multi-user collaboration;
- video transcription;
- full GUI;
- automatic graph reasoning;
- full SKILL.md generation from arbitrary sources.

## 16. Development Roadmap

### Phase 1: Portable Skill

Deliver:

- `SKILL.md`
- cross-agent contract
- workspace protocol
- schemas
- templates

### Phase 2: Lightweight CLI

Potential commands:

```text
knowledge init
knowledge sync
knowledge map
knowledge menu
knowledge extract
knowledge review
knowledge export
```

### Phase 3: Local GUI

Focus on observability and review.

### Phase 4: Cross-Workspace Projects

Allow temporary tasks that combine assets from multiple Workspaces.

### Phase 5: Trusted Asset System

Add:

- asset versioning;
- source-change impact analysis;
- conflict detection;
- re-review reminders;
- multi-model validation;
- export templates.

## 17. Design Summary

The final direction is:

> A local-first, multi-workspace, incremental, review-gated knowledge asset system that uses agents as operators and exports trusted knowledge into learning, writing, product, Obsidian, Skill, or Agent Workspace formats.

Its advantage over a one-shot ontology pipeline is not that it summarizes better. Its advantage is:

- persistence;
- traceability;
- incrementality;
- reviewability;
- reuse;
- cross-topic composition;
- export flexibility.

The most important product sentence:

> User collects sources. Agent proposes candidates. User confirms assets. The system exports usable results.

## 18. v2 Upgrade: Format Zero-Barrier + Guided Engagement (2026)

The first version worked but hit a real-world wall: users drop messy folders of PDF/Word/Excel/images, and the skill could "index but not extract" binary content (it marked them `indexed_metadata_only` and stopped). This made the skill feel useless for exactly the scenario it was built for — a folder full of mixed-format material.

Two upgrades were added, informed by studying kb-retriever (progressive retrieval discipline), SourceWeft (evidence roles), notebookllama (verify step), SurfSense (ETL/Indexing separation), the LLM-wiki lineage (karpathy gist, llm-wiki-skill, LLM-wiki-system-skill), and the user's own usage path.

### 18.1 Format Zero-Barrier (markitdown as the conversion base)

Instead of writing fragile per-format parsers, the skill adopted `markitdown` (microsoft/markitdown) as the primary converter, with a three-tier degradation chain: markitdown → system tools (pandoc/pdftotext) → metadata-only. The skill does **not bundle** markitdown — it ships a `scripts/bootstrap.py` that detects and optionally installs it, keeping the skill folder lightweight and portable.

A read-only intermediate layer `.knowledge/normalized/` holds the converted markdown. Sync/index/extract operate on this layer; raw binaries are never modified. The manifest gained `normalized_path` / `normalization_status` / `normalization_error` fields (forward-compatible additions).

Key constraint preserved: **never fake extraction.** If a file cannot be converted, it is honestly marked `fallback_metadata_only` and the user is told.

### 18.2 Guided Engagement (active briefing, at most 2 questions)

The old Startup Routine was mechanical: detect → build structure → scan → report status → suggest next step. It waited for the user to drive.

The new engagement protocol (`references/engagement-protocol.md`) makes the skill take initiative: after normalizing and scanning, it actively briefes the user ("here is what I see"), asks at most 2 questions (primarily "what do you want to use this for"), recommends directions, and proceeds on a one-line confirmation.

This matches the user's real path: open a messy folder, start the agent, and let it guide. The guided mode does not weaken the review gate — generated knowledge is still a candidate until the user confirms it.

### 18.3 What was deliberately kept out

Consistent with Section 15's deferral list and the constraint to stay a prompt skill: no vector database, no daemon, no GUI, no network fetching of raw sources. markitdown is an optional install, not a bundled dependency. The progressive retrieval discipline (grep + local reads) replaces vector search.
