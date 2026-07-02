# 矛盾专题包（conflict-pack）

**用途**：聚焦资料中的矛盾点、张力、未解问题，做深度研究。比 `debate-pack` 更聚焦——debate-pack 是"不同观点并列"，conflict-pack 是"具体矛盾深挖"。

**启发来源**：karpathy gist（contradictions flagged 是一等维护行为）。

**条目类型**：`synthesis`（矛盾分析是综合产物）

**产出结构**：
```
conflict-pack/
├── USAGE.md
├── INDEX.md
└── conflicts/
    └── [conflict-slug].md
```

**条目结构**：
```markdown
---
id: conflict_001
type: synthesis
title: [矛盾一句话]
citable: false
trust_role: synthesis
sources: [src_001, src_003, src_005]
status: open | partially_resolved | unresolved
---
# [矛盾标题]

## 矛盾描述
[src_001 说 A，src_003 说非 A。具体分歧在……]

## 甲方主张（src_001, src_005）
- 主张：[...]
- 原文：> [...]
- 论据强度：[强/中/弱]（理由）

## 乙方主张（src_003）
- 主张：[...]
- 原文：> [...]
- 论据强度：[强/中/弱]（理由）

## 张力分析
[为什么这个矛盾重要？它折射了什么更深的问题？]

## 可能的调和
- [如果有资料尝试调和，列出]
- [如果纯推断，明确标注"以下为推断，非原文"]

## 待解问题
- [要解决这个矛盾，还需要什么证据/资料？]

## 关联
- related: [其他相关的 conflict 或 concept]
```

**生成逻辑**：
1. 在提取/lint 阶段发现矛盾（同主题、不同结论）。
2. 每个矛盾独立成页，标 `status`。
3. 矛盾不强行裁决——保留双方原文，让读者判断。
4. lint 发现的新矛盾自动归入此包（作为候选，需用户确认）。

**与 debate-pack 的区别**：
- debate-pack：多个观点的并列展示（广度）。
- conflict-pack：单个矛盾点的深度剖析（深度），含张力分析、待解问题。

**USAGE.md 要点**：
- 适合做深度研究/学术/决策的人。
- `citable: false`——矛盾分析是综合判断，引用任何一方都应回原文。
- 矛盾页是"活的"——新资料加入可能 resolve 某个矛盾，lint 会重新评估。
