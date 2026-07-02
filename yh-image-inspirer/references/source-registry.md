# Source Registry

`yh-image-inspirer` 的知识来源主表。未来升级前，先读本文件，再读 `absorption-map.md` 与 `upstream-gap-tracker.md`。

## Status 枚举

- `planned`: 已识别为潜在来源，但尚未正式吸收。
- `partially_absorbed`: 已吸收部分结构、规则或案例，但仍有明确 gap。
- `absorbed`: 当前阶段已吸收到足以支持主要工作流。
- `superseded`: 曾经有用，但已被新的本地结构取代。
- `rejected`: 评估过但不适合当前 skill 的维护边界。

## Type 枚举

- `template-library`
- `workflow-skill`
- `case-library`
- `user-preference`
- `internal-learning`

## Source Table

| source_id | name | type | upstream_url | local_scope | first_absorbed_at | last_reviewed_at | last_online_reviewed_at | upstream_version_note | review_method | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `src-awesome-gpt-image-2` | `freestylefly/awesome-gpt-image-2` | `template-library` | `https://github.com/freestylefly/awesome-gpt-image-2` | `structured templates`, `featured cases`, `boardgame picks`, `部分 db 精选案例`, `海报题材模板（旅行/国潮/奢品/食品饮料）`, `3 个新增结构化模板（美妆报告/研发拆解/古风题材）` | `2026-05-07` | `2026-05-25` | `2026-05-25` | `上游 466 案例、22 模板；本地采用 28 模板策略（新增 3 个模板 + 4 个海报题材）。` | `manual-local-led` | `partially_absorbed` |
| `src-gpt-image2-ecommerce` | `buluslan/gpt-image2-ecommerce` | `template-library` | `https://github.com/buluslan/gpt-image2-ecommerce` | `25 个电商场景结构化 prompt 模板`, `触发词`, `变量槽位`, `风格变体`, `品类适配`, `Anti-AI 处理`, `Prompt 写法五原则`, `桌游文创品类适配` | `2026-05-25` | `2026-05-26` | `2026-05-26` | `25 个结构化 JSON 场景模板已吸收为 ecommerce-scene-templates.md；SKILL.md 工作流、Prompt 写法指南、Anti-AI 防坑规则、桌游文创品类适配已吸收为 ecommerce-prompt-methodology.md。` | `manual-local-led` | `absorbed` |
| `src-yinyo-image2-prompt` | `xiaoshiyilangzhao1996-droid/yinyo-image2-prompt` | `workflow-skill` | `https://github.com/xiaoshiyilangzhao1996-droid/yinyo-image2-prompt` | `GPT-Image-2 决策规则`, `edit workflow`, `模板适配判断`, `提问策略` | `2026-05-16` | `2026-05-16` | `2026-05-16` | `v1.6.0；重点吸收 5-Phase、编辑规则、A/B 策略与模板/非模板判断。` | `manual-local-led` | `partially_absorbed` |
| `src-local-db-14` | `yh-image-inspirer local db` | `case-library` | `local://db` | `14 类案例库与本地图像参考` | `2026-05-07` | `2026-05-16` | `n/a` | `本地自有案例资产，持续增量沉淀。` | `local-review` | `absorbed` |
| `src-user-preferences` | `User workflow preferences` | `user-preference` | `conversation://user-corrections` | `语言偏好`, `桌游默认规则`, `电商与参考图保真`, `默认确认策略` | `2026-05-07` | `2026-05-16` | `n/a` | `以本地规则优先，不绑定单一上游。` | `session-derived` | `absorbed` |
| `src-continuous-learning` | `continuous-learning` | `internal-learning` | `local://C:/Users/wudao/.codex/skills/continuous-learning/SKILL.md` | `会话后学习归档思路` | `2026-05-16` | `2026-05-16` | `n/a` | `借用其模式抽取思路，不依赖其全局 Hook。` | `local-review` | `partially_absorbed` |
| `src-skill-evolution` | `skill-evolution` | `internal-learning` | `local://C:/Users/wudao/.codex/skills/skill-evolution/SKILL.md` | `archive/fossil`, `升级适配性`, `维护边界` | `2026-05-16` | `2026-05-16` | `n/a` | `借用 fossil record 与升级前检查思路。` | `local-review` | `partially_absorbed` |
| `src-native-image-runtime` | `Codex native image runtime` | `workflow-skill` | `runtime://image_gen` | `最终出图默认通道` | `2026-05-07` | `2026-06-19` | `n/a` | `作为唯一默认生图通道；不可用时保留 prompt 并明确报告，不静默回退外部 provider。` | `runtime-review` | `absorbed` |
| `src-poster-design` | `poster-design` | `workflow-skill` | `local://C:/Users/wudao/.codex/skills/poster-design/SKILL.md` | `海报设计底层原理：视觉层级、网格系统、排版规范、色彩策略、印刷制作` | `2026-05-25` | `2026-05-25` | `n/a` | `已整合为 references/poster-design-fundamentals.md，独立技能已删除。` | `local-review` | `absorbed` |
| `src-open-design` | `nexu-io/open-design` | `template-library` | `https://github.com/nexu-io/open-design` | `43 个 image prompt-templates`, `GST+NP 模式`, `HUD 叠加规范`, `拆解图结构`, `pose grid`, `storyboard 序列`, `相机参数`, `Anti-AI-Slop 清单`, `22 张精选参考图` | `2026-05-26` | `2026-05-26` | `2026-05-26` | `Apache-2.0 / CC-BY-4.0；精选 10 种高级模式吸收为 gpt-image2-advanced-patterns.md，22 张参考图下载到 awesome-images/open-design/。` | `manual-local-led` | `partially_absorbed` |
| `src-100-layout-compositions` | `nevertoday/100-layout-compositions` | `case-library` | `https://github.com/nevertoday/100-layout-compositions` | `100 种中文排版构图词汇`, `100 张高清构图参考图`, `100 张缩略图`, `Agent 可调用构图模式库` | `2026-05-26` | `2026-05-26` | `2026-05-26` | `CC BY 4.0；完整图片本地化到 references/layout-composition-images/，文字化吸收为 layout-composition-patterns.md。` | `manual-online-led` | `absorbed` |

## Maintenance Notes

- 新增来源时，先补本表，再决定是否需要新增 `absorption-map.md` 与 `upstream-gap-tracker.md` 条目。
- `last_reviewed_at` 表示本地结构最近一次人工复核时间。
- `last_online_reviewed_at` 仅为二阶段“本地+在线比对”预留；本地来源统一写 `n/a`。
