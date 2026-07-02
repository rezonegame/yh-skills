# Upgrade Playbook

`yh-image-inspirer` 的升级前自动体检流程。任何新增模板、案例、规则或来源吸收动作，都先走本流程。

## Step 0. 定义升级目标

先明确本次升级属于哪类：

- 模板扩充
- 路由优化
- 案例补充
- GPT-Image-2 专项增强
- 桌游专项增强
- 输出检查增强
- 偏好规则沉淀
- 来源治理或维护结构增强

## Step 1. 读取来源治理文件

按顺序阅读：

1. `source-registry.md`
2. `absorption-map.md`
3. `upstream-gap-tracker.md`
4. `fossil-record.md`

如果升级目标在这些文件里已经有结论，优先沿用已有结论，而不是重开一条新分支。

## Step 2. 做“已吸收检查”

至少确认：

- 该来源是否已有 `source_id`
- 该来源是否已有本地落点
- 该主题是否已经有历史 gap 说明
- 是否已经有被否决的旧方案

如果以上至少三项里已有两项命中，默认视为“不是从零开始”，应增量修改。

## Step 3. 做“重复吸收拦截”

出现以下情况时，优先更新索引或 gap 状态，而不是新增文件：

- 新知识只是上游旧知识的另一种说法
- 本地已有同类模板，只是缺元信息
- 本地已有相同工作流，只是缺触发规则
- 本地已有案例，只是缺精选入口

## Step 4. 做“最小修改落点决策”

根据知识类型，优先落到以下文件：

| 知识类型 | 首选落点 |
| --- | --- |
| 模型专用 prompt 规则 | `gpt-image2-decision-rules.md` |
| 参考图编辑流程 | `edit-workflows.md` |
| 模板元信息 | `template-index.md` |
| 快速复用案例入口 | `featured-cases.md` |
| 用户长期偏好 | `personal-preferences.md` |
| 翻车规避与质检 | `output-checklists.md` |
| 主流程门禁或路由 | `SKILL.md` |
| 固定产物类型流程 | `recipes/` |
| 结构化来源台账 | `source-registry.md` / `absorption-map.md` / `upstream-gap-tracker.md` |
| 已否决思路 | `fossil-record.md` |

## Step 5. 变更后自检

至少做以下 5 项自检：

1. 新知识是否有来源归属
2. 新知识是否知道应该落在哪类文件
3. 是否与已有规则冲突
4. 是否让未来维护者更容易升级，而不是更难
5. 是否需要把“暂不吸收原因”写进 `upstream-gap-tracker.md` 或 `fossil-record.md`

## Step 6. 升级后演练

至少模拟一次：

- 如果下次上游再新增类似内容，未来维护者是否能先查到这次吸收结果？

如果答案是否定的，说明本次升级仍然缺少索引或来源记录。

## Optional Step 7. 在线补检

本阶段默认不启用。若未来进入“本地+在线比对”模式，再追加：

- 检查上游仓库最新模板、案例、版本说明
- 将差异写回 `upstream-gap-tracker.md`
- 更新 `last_online_reviewed_at`、`upstream_version_note`、`review_method`

## Hard Rule

未来维护者升级本 skill 时，默认先查看：

`source-registry.md + absorption-map.md + upstream-gap-tracker.md`

再决定改什么。
