# 互链 wiki 包（wiki-pack）

**用途**：把可信资产编织成可浏览、互链的 wiki（类似 Obsidian vault）。

**启发来源**：LLM-wiki-system-skill（字段化双链）+ llm-wiki-skill（folder-split + index MOC）+ karpathy（cross-references）。

**条目类型**：`concept` / `entity` / `synthesis`

**产出结构**：
```
wiki-pack/
├── USAGE.md
├── INDEX.md            # 导航索引（也是 MOC 入口）
├── index.md            # wiki 内容目录（Map of Content）
├── concepts/           # 概念页
│   ├── [slug].md
│   └── [big-topic]/    # folder-split：大概念拆子页
│       ├── index.md
│       └── [subslug].md
├── entities/           # 人/工具/机构/项目
│   └── [slug].md
└── synthesis/          # 综述/对比/综合判断
    └── [slug].md
```

**字段化双链**（关键设计，借鉴 LLM-wiki-system）：

不用 `[[wikilink]]` 文本（脆弱、易断链），用 frontmatter `related` 字段：
```yaml
---
id: concept_001
type: concept
title: 核心概念A
citable: true
trust_role: source_evidence
sources: [src_001]
related: [concept_002, entity_x]   # 出链，指向其他条目的 id/slug
aliases: [别名1, 别名2]             # 用于实体解析/去重
tags: [领域]
---
```

生成 wiki 时，agent 负责**同步维护对端的入链**（如果 A 的 related 含 B，则在 B 的 related 里也加 A），保持图连通。

**index.md（MOC）**：
```markdown
# [主题] Wiki 目录

## 概念
- [[核心概念A]]：一句话
- [[核心概念B]]：一句话

## 实体
- [[实体X]]：一句话

## 综述
- [[综述1]]：一句话

## 待办/开放问题
- [ ] 还没建页但被多次提及的：[概念C]
```

**folder-split 规则**（借鉴 llm-wiki）：
- 单页 > 1200 词 → 拆成 `[slug]/index.md` + 子页。
- index.md 是该概念的概述 + 子页导航。
- 子页每页 400-1200 词。
- 拆分前先和用户确认拆分计划（哪些子主题）。

**USAGE.md 要点 + 联动**：
- 适合想长期沉淀、可浏览知识库的人。
- 可直接导入 Obsidian 作为 vault（frontmatter 兼容 Dataview）。
- `related` 字段化双链可在 Obsidian graph view 显示。
- 导入后可用 qmd 等工具做向量检索（>100 页时）。
