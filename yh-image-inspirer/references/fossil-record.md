# Fossil Record

记录曾经考虑、测试、否决、替换或降级的结构与规则。目的不是追责，而是防止未来升级时重复引回已证明不合适的方案。

## Record Template

| fossil_id | date | topic | previous_idea | outcome | why_not_kept | replacement | revisit_condition |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Records

| fossil_id | date | topic | previous_idea | outcome | why_not_kept | replacement | revisit_condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `fos-001` | `2026-05-16` | 全量上游镜像 | 将 `awesome-gpt-image-2` 的全量案例与结构整体复制到本地 | 否决 | 案例噪音高、维护成本大、来源治理复杂，不符合当前 markdown-first 自包含边界 | 采用 `template-index.md` + `featured-cases.md` + 定向精选吸收 | 只有当本 skill 明确要发展成独立案例检索产品时再重审 |
| `fos-002` | `2026-05-16` | 完整照搬 `yinyo` | 将 `yinyo-image2-prompt` 整份 skill 作为本地子技能依赖 | 否决 | 会把通用视觉工作流过度绑定到 GPT-Image-2 单模型，且说明冗长 | 抽取为 `gpt-image2-decision-rules.md` 与 `edit-workflows.md` | 若未来出现明确的模型专属子技能分层方案，可再评估 |
| `fos-003` | `2026-05-16` | 绑定全局学习 Hook | 直接复用 `continuous-learning` 的自动 Stop hook | 暂不采用 | 与当前本 skill 的本地维护边界不一致，且会引入外部路径依赖 | 采用 `learning-capture-rules.md` 的手工显式落档 | 当你确认全局 Hook 稳定且愿意统一全技能维护策略时再开启 |
| `fos-004` | `2026-06-19` | 外部生图后端回退 | 原生图像生成不可用时自动回退到已删除的 `yh-image` provider 后端 | 移除 | 造成技能边界重复、依赖失效，并可能在未获用户同意时切换执行通道 | 仅使用 runtime-native image generation；不可用时保留 prompt 并明确失败 | 只有用户明确要求且系统重新定义统一执行层时再评估 |

## When To Write Here

把内容写进本文件，而不是 `evolution-log.md` 的场景：

- 某个想法已经试过，且明确不想按原方案继续。
- 某个结构被新的本地方案替换。
- 某个上游能力被评估为不值得吸收。
- 某个失败模式值得被未来升级前再次看到。

## Relationship To Other Files

- `evolution-log.md`: 记录发生了什么。
- `fossil-record.md`: 记录哪些思路不要再无条件重复。
- `upstream-gap-tracker.md`: 记录还有哪些没补。
