# 下游消费契约（Downstream Contract）

本契约定义 yh-local-knowledge 的导出内容如何被下游 agent 或人有效消费。它是"下游可用性"支柱的核心，直接服务于用户的北极星需求：**后续 agent 或人怎么使用导出内容**。

核心理念：**导出包不是"生成完就结束"，而是带着使用说明、导航索引、可信标签一起交付。** 下游拿到一个导出包，应该立刻知道：这是什么、适合谁用、怎么用、哪些能直接引用、哪些需要复核。

## 一、每个导出包的三件套

每个导出包产出时，必须在包根目录生成三个文件：

### 1. `USAGE.md` — 消费指南

告诉下游"这是什么、怎么用"。模板：

```markdown
# [导出包名] 使用指南

## 这是什么
[一句话说明这个包的内容和来源]

## 适合谁用
- [人群1]：[场景1]
- [人群2]：[场景2]

## 怎么用
1. 先读 INDEX.md 了解包内有什么
2. [针对该包类型的典型使用流程]

## 可信度说明
本包内的条目带有 `citable` 和 `trust_role` 标签：
- `citable: true` + `trust_role: source_evidence`：可直接引用，源自原始资料
- `citable: false`：是推导/综合产物，引用前建议回原始资料核对
详见下方"可信标签"。

## 联动的下游技能
- 写作素材包 → 可喂给 boardgame-writer / yh-humanizer
- 产品 Spec 包 → 可喂给 yh-slides 做演示
- [本包对应的联动]
```

### 2. `INDEX.md` — 导航索引

让下游 agent **先读索引再下钻，不用全读**。借鉴 kb-retriever 的 data_structure.md。模板：

```markdown
# [导出包名] 导航索引

## 概览
本包共 N 个条目，覆盖[主题范围]。

## 条目清单

| 文件 | 标题 | 类型 | 可引用 | 覆盖 |
|------|------|------|--------|------|
| concepts/xxx.md | XXX概念 | concept | ✅ | [一句话] |
| entities/yyy.md | YYY | entity | ✅ | [一句话] |
| synthesis/zzz.md | ZZZ综合判断 | synthesis | ⚠️需复核 | [一句话] |

## 怎么找
- 想找概念定义 → concepts/ 目录
- 想找人/工具/机构 → entities/ 目录
- 想找综合判断 → synthesis/ 目录
- [本包特有的导航逻辑]
```

### 3. 可信标签（每个条目的 frontmatter）

每个导出条目（以及可信资产）的 frontmatter 带：

```yaml
---
id: concept_001
type: concept
title: XXX
citable: true                    # 是否可直接被下游引用
trust_role: source_evidence      # 信任角色（见下方）
sources: [src_001, src_003]
---
```

## 二、可信标签规范（借鉴 SourceWeft 的 evidenceRole + citable）

### `citable`（布尔）

- `true`：下游 agent 可以直接引用这个条目作为事实依据，不需要回原始资料核对。
- `false`：这个条目是推导、综合、猜测或低置信度产物，下游引用前应该回原始资料核对，或标注"此为推断"。

### `trust_role`（信任角色）

| 值 | 含义 | 典型来源 | citable 通常 |
|----|------|---------|-------------|
| `source_evidence` | 直接源自原始资料的事实/引用 | 从原始资料提取的原文、定义、数据 | `true` |
| `working_memory` | 推导过程中的中间产物 | agent 分析时产生的中间判断、未确认的关联 | `false` |
| `synthesis` | 综合多个来源的判断 | 跨源综合的结论、对比、争议总结 | 视情况（单一来源支撑则 true，跨源综合需标注来源数） |

设计目的：让下游 agent 一眼区分"这是原文事实"和"这是 AI 综合"，避免把综合判断当成原文事实引用。

### 全局可信声明

`manifest.json` 在工作区根加一个全局声明（向前兼容字段）：

```json
{
  "trust_policy": {
    "default_citable": false,
    "verified_assets_citable": true,
    "note": "未标 citable 的条目默认不可直接引用；可信资产区(可信资产/)的条目默认可引用。"
  }
}
```

## 三、下游 agent 如何解读（消费契约）

下游 agent（无论是另一个 skill 还是人）消费 yh 的导出包时，遵循：

1. **先读 `USAGE.md`**：了解这是什么、怎么用。
2. **再读 `INDEX.md`**：找到需要的条目，不要全读。
3. **读条目时检查 `citable` 和 `trust_role`**：
   - `citable: true` → 可直接用，引用时标注来源 `sources`。
   - `citable: false` → 当成参考，引用前回原始资料核对，或明确标注"此为推断/综合"。
4. **引用时带溯源**：引用任何条目，都要带上它的 `sources`（指向 manifest 里的 source_id），让读者能追到原始资料。

## 四、与现有信任边界的关系

本契约**不削弱**现有的"候选→可信"闸门：
- 候选阶段的条目 `citable` 必须为 `false`（它们还没被用户确认）。
- 只有用户确认成可信资产后，`citable` 才可能为 `true`（且仅当 `trust_role` 是 `source_evidence` 时）。
- 导出包里的条目如果来自候选（未经确认），`citable` 必须为 `false`，并在 USAGE.md 里标注"本包含未确认内容"。

## 五、典型下游联动（给出阶段性建议）

针对你关心的"下游怎么用"，这里给出具体联动方向（在阶段3 的导出包成品里会细化）：

| 导出包 | 典型下游 | 怎么联动 |
|--------|---------|---------|
| 写作素材包 | boardgame-writer / yh-humanizer / 通用写作 | 把论点+证据+引用喂给写作技能，作为文章素材 |
| 学习路径包 | 学习者直接用 / 课程设计 | 按阶段路径学习，做练习 |
| 产品/Agent Spec 包 | yh-slides / 开发 agent | spec.md 喂给开发或演示技能 |
| 概念术语包 | Obsidian 笔记 / 知识库 | 导入 vault 做术语索引 |
| 流程技能包 | 操作指南 / SOP | 直接作为操作手册用 |
| 争议观点包 | 决策 / 深度分析 | 看正反方证据做判断 |
| 互链 wiki 包 | Obsidian / 浏览 | 双链浏览、graph view |
| 思维导图/图谱包 | 可视化 / 演示 | mermaid 渲染、嵌入演示 |
| 矛盾专题包 | 深度研究 | 聚焦矛盾点深挖 |
| 播客脚本包 | 音频制作 / 传播 | TTS 合成或人录 |

## 六、不要做的事

- 不要让导出包"裸奔"——每个包必须有 USAGE.md + INDEX.md。
- 不要把候选内容标成 `citable: true`（绕过信任闸门）。
- 不要在 INDEX.md 里堆砌全部内容（它是导航，不是正文）。
- 不要省略 `sources`——没有溯源的条目，下游无法验证。
- 不要假设下游 agent 知道 yh 的内部结构——USAGE.md 要用下游能懂的话写。
