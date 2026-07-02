# 治理协议（Governance Protocol）

本协议定义 yh-local-knowledge 的长期治理能力：主动维护（lint）、反馈纠错（锚点）、复利闭环。它让知识库从"一次性产物"变成"可自检、可纠错、可复利"的活资产。

核心理念（吸收自 karpathy + llm-wiki）：**知识库会腐烂，除非有人/agent 主动维护。LLM 适合做维护劳动（不嫌烦、不忘更新交叉引用、能一次碰 15 个文件）。**

## 一、Lint：主动健康检查

Lint 是工作流的一等公民。生命周期加入 lint 相位：

```
... → asset_verified → lint → export → 增量同步
```

### 何时跑 lint

- **导出前**：必须跑一次，导出包不应带着已知问题。
- **增量同步后**：源变更可能引入不一致，lint 复查。
- **用户主动要求**："检查一下知识库健康"。
- **定期**：长期维护的工作区，建议每隔一段时间 lint 一次。

### lint 检查项（scripts/lint_workspace.py）

1. **frontmatter 完整性**：每个资产有 id/type/title/sources。
2. **孤儿资产**：没有任何 related 链接（出链）且不被任何其他资产引用（入链）。
3. **陈旧资产**：updated_at 超过阈值（默认 180 天）未更新（提示性，非错误）。
4. **悬空引用**：related 指向不存在的 id。
5. **无溯源资产**：没有 sources 的资产（下游无法验证）。

### lint 产出的处理

- lint 发现的问题**作为候选提交**（不是直接改资产）——守信任闸门。
- 矛盾类问题 → 归入"矛盾专题包"候选。
- 孤儿/陈旧 → 提示用户"这些资产可能需要补充关联或重新审视"。
- 悬空引用 → 提示用户"这些链接断了，要修复还是删除"。

lint 结果写入 `.knowledge/logs/` 并在交付时简报给用户。

## 二、锚点反馈：跨编辑稳定定位

借鉴 llm-wiki-skill 的 anchor 设计。用户或下游对某条资产有反馈时，反馈不存行号（会漂移），存锚点窗口。

### 锚点结构（scripts/anchor.py）

```json
{
  "target_lines": [12, 14],
  "anchor_text": "选中区的逐字文本",
  "anchor_before": "选中前约80字符上下文",
  "anchor_after": "选中后约80字符上下文"
}
```

### 3 级解析降级

1. **Level 1 行号匹配**：target_lines 范围内含 anchor_text → 命中。
2. **Level 2 唯一文本**：全文搜 anchor_text，唯一匹配 → 命中。
3. **Level 3 上下文窗口**：before+text+after 组合搜 → 命中。
4. **都失败 → stale**：标记陈旧，不静默丢弃，问人（re-anchor / reject / archive）。

### 反馈文件（.knowledge/feedback/）

```
.knowledge/feedback/
├── [timestamp]-[slug].md     # open 状态
└── resolved/                 # resolved 状态（含 rejected，永不删）
```

反馈文件结构：
```markdown
---
id: fb_001
target_asset: asset_003
anchor: {target_lines, anchor_text, anchor_before, anchor_after}
severity: info | suggest | warn | error
status: open | resolved
created_at: [ISO-8601]
---

# [反馈标题]

## Comment
[反馈内容]

## Resolution
[accept / partial / reject + 理由]  (resolved 时填)
```

### 反馈闭环

反馈**触发候选**（不直接改资产）：
1. 用户/下游选中资产文本提反馈 → 写 feedback 文件（open）。
2. agent 处理反馈：accept（改资产）/ partial（部分改）/ reject（写理由，移 resolved）/ defer（挪开放问题）。
3. **rejected 也留存**（移 resolved/，不删）——保留"为什么否"的信号。
4. accept/partial 的改动走候选→确认闸门，确认后才改资产。

## 三、复利闭环：探索也能生产知识

借鉴 karpathy 的"好答案归档回 wiki"。查询/分析的优质产出不丢弃，作为新候选回流。

### 复利场景

- 用户问了一个问题，agent 基于可信资产综合出一个好答案 → 答案作为 `synthesis` 候选。
- 用户做了一次对比/分析 → 分析作为候选。
- 导出过程中产生的新洞察 → 作为候选。

### 复利纪律

- 复利产出**必须走候选→确认闸门**——不能因为是 agent 产的就直接进可信资产。
- 标 `trust_role: synthesis`（综合产物），`citable` 默认 false（需用户确认且明确支撑后才 true）。
- 带溯源（综合自哪些可信资产/原始资料）。
- 用户可以选择"不归档"——复利是机会，不是义务。

## 四、与现有信任边界的关系

本协议**不削弱**任何现有规则：
- lint 发现的问题 → 候选（不直接改）。
- 反馈触发的改动 → 候选（不直接改）。
- 复利产出 → 候选（不直接进可信资产）。
- 所有治理动作都走 `.knowledge/candidates/` → 用户确认 → `可信资产/` 的标准闸门。

治理是"主动发现问题并提交候选"，不是"绕过用户自动修改"。这条是治理协议的红线。

## 五、不要做的事

- 不要让 lint 自动改资产（只提候选）。
- 不要静默丢弃 stale 锚点（要问人）。
- 不要把复利产出直接当可信资产（要过闸门）。
- 不要把 rejected 反馈删掉（要留痕）。
- 不要让治理变成负担——lint 是建议性（除导出前必须跑），不是每次操作都跑。

## 六、资产版本化

可信资产会随时间被修正、补充、推翻。版本化让历史可追溯，不会因一次修改丢失之前的判断。

### 版本规则（激活 asset.schema 的 version 字段）

- 每次用户确认修改一个已存在的可信资产 → 版本号 +1，不覆盖旧版。
- 旧版标 `status: deprecated`，保留在原位或挪到 `可信资产/.archive/`。
- 新版 `status: verified`，`version` 递增，`updated_at` 刷新。
- 借鉴 SurfSense 的 isLatest 思路：同一 id 的多个版本里，只有一个是当前可信版。

### 什么时候触发版本化

- 用户基于反馈/复利/lint 修正了资产内容。
- 源资料变更导致资产需要重审后改写。
- 用户主动"推翻"某个资产（旧版 deprecated，不一定有新版）。

### 版本化产出

```
可信资产/
├── [slug].md              # 当前版（version: 3, status: verified）
└── .archive/
    └── [slug]/
        ├── v1.md          # version: 1, status: deprecated
        └── v2.md          # version: 2, status: deprecated
```

archive 永不自动删（保留判断演变史）。

## 七、源变更影响分析

增量同步检测到原始资料变更（hash/mtime 变化）时，要追溯到引用该源的候选/资产，标记需要重审。

### 流程（激活 state.schema 的 affected_assets 字段）

1. 增量同步发现 src_001 的 hash 变了。
2. 扫描所有候选/资产的 `sources` 字段，找出引用 src_001 的条目。
3. 这些条目标 `status: needs_review`（资产）或保持 `candidate`（候选）。
4. 在 `state.json` 的 `affected_assets` 数组记录受影响的 id。
5. 下次简报/交互时告诉用户："这些资产引用了变更的源，建议重审"。

### 重审后的处理

- 源变更后内容仍一致 → 清除 needs_review，资产不变。
- 源变更后内容矛盾 → 触发版本化（旧版 deprecated）+ 新候选。
- 源被删除 → 引用它的资产标 needs_review，提示用户"源已不存在，是否保留/废弃该资产"。

这是"知识库随源演变"的关键——不让可信资产和原始资料脱节。

## 八、跨工作区 Projects（Phase 4）

design-history 第7节规划了跨工作区 Projects：一个临时任务可以引用多个 Workspace 的资产，产出一个跨主题导出包。

### Projects 不破坏工作区隔离

关键约束（守 design-history"防止语义污染"原则）：
- Project **只引用**多个 Workspace 的资产，**不移动**它们。
- 资产仍归原 Workspace 所有。
- Project 是短期目标容器，不是新的知识库。

### Project 结构

Projects 放在工作区之外的统一位置（如用户根目录的 `~/yh-projects/`），或在一个专门的 Projects 工作区：

```
yh-projects/
└── [project-slug]/
    ├── project.md         # 项目说明：目标、引用的 workspace、产出
    ├── refs/              # 软引用（指向各 workspace 的资产 id，不复制内容）
    │   └── refs.json
    └── 导出结果/           # 跨主题导出包（带 USAGE/INDEX/可信标签）
```

### refs.json 结构

```json
{
  "project_id": "proj_001",
  "title": "AI Agent 如何改变桌游设计",
  "goal": "写一篇跨主题文章",
  "workspace_refs": [
    {"workspace": "/path/to/桌游设计", "assets": ["asset_001", "asset_003"]},
    {"workspace": "/path/to/AI-Agent", "assets": ["asset_002", "asset_005"]}
  ],
  "created_at": "ISO-8601",
  "status": "active | completed | archived"
}
```

### Project 生命周期

- 创建：用户说"我想结合 A 和 B 两个主题做 X"。
- 引用：agent 从两个 Workspace 挑相关资产，写入 refs.json（不复制内容）。
- 产出：基于引用的资产生成跨主题导出包（如写作素材包）。
- 完成：Project 标 completed，导出包归档；原 Workspace 资产不动。

### Projects 与信任闸门

- Project 引用的是**已确认的可信资产**（不引用候选）。
- 跨主题综合产出仍是候选 → 用户确认 → Project 的导出包。
- Project 不创建新的可信资产回到原 Workspace（除非用户明确要）。

## 九、治理的节制原则

治理能力很容易过度工程。守以下节制：

- **lint 是建议性的**，只有导出前是必须的。不要每次操作都 lint。
- **版本化只在内容真正改变时**触发，不要因为格式微调就升版本。
- **Projects 是可选的**，单工作区用户完全不需要它。
- **复利是机会不是义务**，用户可以拒绝归档。
- **治理服务于"知识长期可用"**，不是为了让系统看起来复杂。
