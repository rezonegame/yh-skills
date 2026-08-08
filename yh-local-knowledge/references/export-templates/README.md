# 导出包模板总览（Export Templates）

本目录定义 yh-local-knowledge 的 11 类导出包成品规范。每个导出包产出时，参照对应模板，并遵守 `references/downstream-contract.md` 的三件套要求（USAGE.md + INDEX.md + 可信标签）。

## 11 类导出包

### 现有 6 类（已强化，配模板）

| 包 | 模板文件 | 用途 |
|----|---------|------|
| 概念术语包 | `concept-pack.md` | 建术语表、Obsidian 笔记 |
| 学习路径包 | `learning-path-pack.md` | 系统学习这批资料 |
| 流程技能包 | `process-pack.md` | 资料>中的操作方法/SOP |
| 写作素材包 | `writing-pack.md` | 写文章/报告的素材 |
| 产品/Agent Spec 包 | `spec-pack.md` | 生成 spec/功能清单/数据模型 |
| 争议观点包 | `debate-pack.md` | 不同流派/冲突观点 |

### 扩展 5 类

| 包 | 模板文件 | 用途 | 来源启发 |
|----|---------|------|---------|
| 思维导图/知识图谱包 | `graph-pack.md` | 可视化、mermaid、演示 | notebookllama |
| 互链 wiki 包 | `wiki-pack.md` | 双链浏览、MOC、Obsidian | LLM-wiki-system + llm-wiki |
| 矛盾专题包 | `conflict-pack.md` | 聚焦矛盾点深挖 | karpathy |
| 播客脚本包（可选） | `podcast-pack.md` | 双人对话脚本、TTS | notebookllama |
| 知识技能包 | `skill-pack.md` | 按主题加载的 Agent Skill | book-to-skill 方法，经本地信任模型改造 |

## 通用规范（所有包共享）

### 每个包的标准结构

```
[export-target]/
├── USAGE.md          # 消费指南（必需）
├── INDEX.md          # 导航索引（必需）
├── manifest.ref.md   # 引用的 source_id 清单（可选，便于溯源）
└── [条目文件...]
```

### 每个条目的 frontmatter

```yaml
---
id: [type]_001
type: concept | path | process | claim | case | spec | entity | synthesis | other
title: [标题]
citable: true | false
trust_role: source_evidence | working_memory | synthesis
sources: [src_001, src_003]
tags: [可选标签]
created_at: [ISO-8601]
updated_at: [ISO-8601]
---
```

### folder-split 原则（借鉴 llm-wiki）

任何单个条目超过 ~1200 词时，拆成 index + 子页：
```
concepts/
└── big-topic/
    ├── index.md          # 概述 + 子页导航
    ├── subtopic-a.md     # 400-1200 词
    └── subtopic-b.md
```
拆分理由：让下游 agent 能选择性读取（只读 index 或某个子页），不用整篇加载。

## 如何新增下一类包（可扩展性）

导出包不锁死为 11 类。新增包时：
1. 在本目录加一个 `[name]-pack.md` 模板。
2. 在本 README 的表格里登记。
3. 在 `references/engagement-protocol.md` 的"推荐方向"表里按需加入。
4. 新包仍必须遵守三件套（USAGE/INDEX/可信标签）。

## 提取纪律（所有包共享）

- **先归一化再提取**：从 `.knowledge/normalized/` 提取，不直接读二进制。
- **渐进式检索**：grep + offset/limit，不整文件加载（见 normalization.md）。
- **候选先行**：提取产物先放 `.knowledge/candidates/`，用户确认后才进导出包。
- **溯源必带**：每个条目带 `sources`，没溯源的条目下游无法验证。
- **不编造**：资料里没有的，不要硬凑。缺口在 USAGE.md 里如实说明。

## 包之间的组合

用户可以一次选多个包。组合时：
- 共享的候选/资产只确认一次，多包复用。
- INDEX.md 在各包独立，但可在 USAGE.md 里互相引用（如"本写作素材包的概念定义见概念术语包"）。
- 典型组合：概念术语包 + 学习路径包（学习场景）、写作素材包 + 争议观点包（深度写作）、产品 Spec 包 + 思维导图包（产品设计）。
