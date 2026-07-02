# 现有 6 类导出包模板

本文件给出概念术语包、学习路径包、流程技能包、写作素材包、产品/Agent Spec 包、争议观点包的精炼模板。每个包产出时参照对应章节，并配 USAGE.md + INDEX.md（见 downstream-contract.md）。

---

## 1. 概念术语包（concept-pack）

**用途**：建术语表、做 Obsidian 笔记、建立领域共识。

**条目类型**：`concept` / `entity`

**条目结构**：
```markdown
---
id: concept_001
type: concept
title: [术语]
citable: true
trust_role: source_evidence
sources: [src_001]
tags: [领域, 类别]
---
# [术语]

## 定义
[一句话定义，源自原始资料]

## 来源原文
> [原始资料的原文片段]

## 相关术语
- [[相关术语1]]
- [[相关术语2]]

## 备注
[歧义、不同流派用法、注意事项]
```

**USAGE.md 要点**：适合想建立术语表/做笔记/学基础概念的人；可导入 Obsidian 做双链。

---

## 2. 学习路径包（learning-path-pack）

**用途**：系统学习这批资料覆盖的主题。

**条目类型**：`path`

**条目结构**：
```markdown
---
id: path_001
type: path
title: [主题] 学习路径
citable: false
trust_role: synthesis
sources: [src_001, src_002, src_005]
---
# [主题] 学习路径

## 学习目标
学完后能[具体能力]

## 前置知识
- [需要先掌握的概念]

## 阶段路径
### 阶段1：[名称]（约X小时）
- 目标：[...]
- 读：[具体资料 + 章节]
- 练习：[...]
### 阶段2：...

## 每日任务建议
- Day1：[...]
- Day2：[...]

## 检验
- [能回答什么问题算学完]
```

**USAGE.md 要点**：适合想系统学习的人；`citable: false` 因为路径是综合设计，非原文事实。

---

## 3. 流程技能包（process-pack）

**用途**：资料中的操作方法、工作流、SOP。

**条目类型**：`process`

**条目结构**：
```markdown
---
id: process_001
type: process
title: [流程名]
citable: true
trust_role: source_evidence
sources: [src_003]
---
# [流程名]

## 适用场景
[什么时候用]

## 前置条件
- [需要的工具/权限/状态]

## 步骤
1. [步骤1：动作 + 预期结果]
2. [步骤2：...]

## 注意事项
- [常见坑、边界情况]

## 验证
- [如何确认做对了]
```

**USAGE.md 要点**：适合需要操作指南/SOP 的人；直接作为操作手册用。

---

## 4. 写作素材包（writing-pack）

**用途**：写文章/报告/公众号长文的素材。

**条目类型**：`claim`（论点）/ `case`（案例）

**条目结构**（论点）：
```markdown
---
id: claim_001
type: claim
title: [论点一句话]
citable: true
trust_role: source_evidence
sources: [src_002, src_004]
---
# [论点]

## 论点
[完整表述]

## 支撑证据
- [证据1，来自 src_002]
- [证据2，来自 src_004]

## 原文引用
> [可直接引用的原文]

## 反面观点
- [如有，来自争议资料]

## 可用场景
[这个论点适合写什么类型的文章]
```

**INDEX.md 额外列**：建议加"立场"列（支持/反对/中立），方便写作时挑素材。

**USAGE.md 要点 + 联动**：适合写作者；论点+证据+引用可直接喂给 boardgame-writer / yh-humanizer / 通用写作技能。

---

## 5. 产品/Agent Spec 包（spec-pack）

**用途**：从资料生成产品规格、Agent 工作区。

**条目类型**：`spec`

**条目结构**：
```markdown
---
id: spec_001
type: spec
title: [产品/Agent 名] Spec
citable: false
trust_role: synthesis
sources: [src_001, src_002, src_006]
---
# [产品/Agent 名] Spec

## 问题定义
[要解决什么问题]

## 目标用户
- [用户画像]

## 功能清单
| 功能 | 优先级 | 来源 |
|------|--------|------|
| [功能1] | P0 | src_001 |

## 数据模型
[实体、字段、关系]

## 非功能需求
- [性能/安全/合规]

## 风险与未决
- [风险1]

## 参考
- mapping.md（资料→功能的映射）
```

**USAGE.md 要点 + 联动**：适合做产品/agent 的人；spec.md 可喂给 yh-slides 做演示、喂给开发 agent。

---

## 6. 争议观点包（debate-pack）

**用途**：资料中不同流派、冲突观点、证据强弱差异。

**条目类型**：`claim`（带立场标注）

**条目结构**：
```markdown
---
id: debate_001
type: claim
title: [争议议题]
citable: false
trust_role: synthesis
sources: [src_002, src_005, src_007]
---
# [争议议题]

## 议题
[一句话描述争议什么]

## 观点A：[立场]
- 主张：[...]
- 支持来源：src_002, src_007
- 关键论据：[...]

## 观点B：[立场]
- 主张：[...]
- 支持来源：src_005
- 关键论据：[...]

## 证据强弱对比
| 维度 | 观点A | 观点B |
|------|-------|-------|
| 来源数 | 2 | 1 |
| 证据类型 | [实验/案例/推理] | [实验/案例/推理] |

## 待核验问题
- [还没定论的关键点]

## 中立观察
[如果资料里有第三方视角]
```

**USAGE.md 要点**：适合需要做判断/决策的人；`citable: false` 因为综合判断需读者自行裁决。矛盾更聚焦的版本见 `conflict-pack.md`。
