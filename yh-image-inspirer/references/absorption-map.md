# Absorption Map

只记录“来源 -> 本地落点”的实际映射，避免空泛叙述。

## `src-awesome-gpt-image-2`

| 来源能力 | 本地落点 | 吸收方式 | 当前状态 |
| --- | --- | --- | --- |
| Prompt-as-Code 模板结构 | `references/structured-templates.md` | 抽取槽位、`useWhen`、`guidance`、`pitfalls` | 已落地 |
| 案例精选思路 | `db/*/prompt.md` 中的精选条目 | 按任务高频度做定向吸收，不做全量镜像 | 已落地 |
| 桌游可迁移案例 | `references/awesome-boardgame-cases.md` | 抽取桌游生产中高价值结构 | 已落地 |
| 海报风格扩展 | `references/poster-artist-styles.md`、`references/poster-composition-patterns.md`、`references/poster-genre-templates.md` | 本地化引用与重组 | 已落地 |
| 模板索引能力 | `references/template-index.md` | 本地轻量索引，不复制上游数据系统 | 本次新增 |
| 精选入口能力 | `references/featured-cases.md` | 用于快速检索，减少翻全库 | 本次新增 |

## `src-yinyo-image2-prompt`

| 来源能力 | 本地落点 | 吸收方式 | 当前状态 |
| --- | --- | --- | --- |
| GPT-Image-2 模型特性总结 | `references/gpt-image2-decision-rules.md` | 提炼为模型专用规则 | 本次新增 |
| 5-Phase 引导思路 | `references/gpt-image2-decision-rules.md`、`references/upgrade-playbook.md`、`SKILL.md` | 压缩为适合本地 workflow 的决策层 | 本次新增 |
| 模板/非模板判断 | `references/gpt-image2-decision-rules.md` | 形成任务分类决策 | 本次新增 |
| A/B 备选策略 | `references/gpt-image2-decision-rules.md` | 作为复杂任务补充策略 | 本次新增 |
| 编辑工作流 `Change / Preserve` | `references/edit-workflows.md`、`references/output-checklists.md` | 形成统一 edit 模板 | 本次新增 |

## `src-user-preferences`

| 来源能力 | 本地落点 | 吸收方式 | 当前状态 |
| --- | --- | --- | --- |
| 用户当前画面语言偏好 | `references/personal-preferences.md` | 作为默认规则 | 已重构 |
| 桌游默认理解方式 | `references/personal-preferences.md`、`recipes/boardgame-*.md` | 作为路由和默认输出形态 | 已落地 |
| 商品与参考图保真偏好 | `references/personal-preferences.md`、`references/edit-workflows.md` | 作为识别锚点规则 | 已落地 |

## `src-continuous-learning`

| 来源能力 | 本地落点 | 吸收方式 | 当前状态 |
| --- | --- | --- | --- |
| 会话模式抽取 | `references/learning-capture-rules.md` | 采用“何时落档、落到哪里”的规则，不依赖全局 Hook | 本次新增 |

## `src-skill-evolution`

| 来源能力 | 本地落点 | 吸收方式 | 当前状态 |
| --- | --- | --- | --- |
| fossil record / archive 思路 | `references/fossil-record.md` | 记录被否决或被替代的策略 | 本次新增 |
| 升级前适配性检查 | `references/upgrade-playbook.md` | 形成统一升级前体检流程 | 本次新增 |

## `src-100-layout-compositions`

| 来源能力 | 本地落点 | 吸收方式 | 当前状态 |
| --- | --- | --- | --- |
| 100 张排版构图高清图 | `references/layout-composition-images/originals/` | 完整本地化保存，离线可用 | 本次新增 |
| 100 张轻量缩略图 | `references/layout-composition-images/thumbnails/` | 用于快速预览和索引，不要求运行时读取高清图 | 本次新增 |
| 图号、构图名、路径索引 | `references/layout-composition-images/INDEX.md` | 手工 OCR / 视觉复核后建立完整本地索引 | 本次新增 |
| 可迁移构图知识 | `references/layout-composition-patterns.md` | 将图片型构图参考转写为 Agent 可调用的文字化构图模式、Prompt 片段和组合建议 | 本次新增 |
| 海报/排版路由 | `SKILL.md` 资源地图与类型路由表 | 在海报、排版、构图、版式场景中加入该库 | 本次新增 |

## Usage Rule

未来升级时，先按来源找到本地落点，再决定是：

- 更新现有文件
- 新增专题文件
- 只更新 `upstream-gap-tracker.md`
- 记入 `fossil-record.md`
