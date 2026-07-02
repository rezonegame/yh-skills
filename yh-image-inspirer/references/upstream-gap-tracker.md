# Upstream Gap Tracker

升级前先读本文件。它回答三件事：

1. 这个来源已经吸收到哪一步？
2. 还缺什么？
3. 缺的东西为什么还没补？

## 目录

- Awesome GPT Image 2 与 Yinyo 来源
- 用户偏好、学习与演化来源
- 100 Layout Compositions
- Upgrade Checklist

## `src-awesome-gpt-image-2`

### 已有

- 已有 25 个结构化模板，且每个模板都带 `useWhen` / `guidance` / `pitfalls`。
- 已有按任务类型划分的本地 `db/` 案例库。
- 已有桌游精选迁移文件。
- 已有海报风格扩展与 Mondo 相关专题资源。

### 仍缺

- 没有上游 style-library 的统一标签体系。
- 没有全量案例图库索引入口。
- 没有对“新模板 / 新案例”的标准化增量复核流程。
- 没有轻量统一的“高复用精选案例入口”。

### 本次处理

- 新增 `template-index.md` 补模板元信息。
- 新增 `featured-cases.md` 作为精选入口。
- 保持 markdown-first，不引入完整 JSON 数据系统。

### 继续不吸收的内容

- 不做上游仓库的全量镜像。
- 不引入其网站、数据库或在线检索结构。

### 原因

- 当前目标是提升 skill 的可执行性与维护性，而不是复制一个站点产品。
- 全量镜像会显著增加维护成本和版权/来源管理噪音。

## `src-yinyo-image2-prompt`

### 已有

- 当前 skill 已有强确认 brief、任务路由、参考图保真规则。
- 已有结构化模板与工作流门禁。

### 仍缺

- 缺少显式 GPT-Image-2 专项规则文件。
- 缺少“模板化 vs 非模板化”的硬判断框架。
- 缺少统一 edit workflow。
- 缺少 A/B 备选策略的触发条件。

### 本次处理

- 新增 `gpt-image2-decision-rules.md`。
- 新增 `edit-workflows.md`。
- 在 `SKILL.md` 中明确 GPT-Image-2 与 edit 决策入口。

### 暂不吸收

- 不照搬完整 5-Phase 长篇文案。
- 不把 `yinyo` 变成新的主 skill 或子 skill 依赖。

### 原因

- `yh-image-inspirer` 是通用视觉工作流，不应被单模型单仓库绑死。
- 本地实现更需要“决策层”，而不是另一份超长说明书。

## `src-user-preferences`

### 已有

- 已经有偏好规则，但结构偏平铺。

### 仍缺

- 缺少标准章节。
- 缺少“默认确认策略”条目。
- 缺少与学习归档规则的衔接说明。

### 本次处理

- 重构 `personal-preferences.md` 为固定章节。

## `src-continuous-learning`

### 已有

- 仅借用了“从会话抽取可复用模式”的理念。

### 仍缺

- 没有面向 `yh-image-inspirer` 的专属落档规则。

### 本次处理

- 新增 `learning-capture-rules.md`。

### 暂不吸收

- 不绑定全局 Stop hook。

### 原因

- 当前更适合把经验显式写入本 skill，而不是依赖外部自动化流程。

## `src-skill-evolution`

### 已有

- 仅借用了“fossil record / archive / evolution pressure”的方法论。

### 仍缺

- 没有专门记录被放弃策略的地方。
- 升级前没有固定体检流程。

### 本次处理

- 新增 `fossil-record.md`。
- 新增 `upgrade-playbook.md`。

## `src-100-layout-compositions`

### 已有

- 上游提供 100 张排版构图图片，含高清原图与缩略图。
- 上游 README 说明其用途是排版构图交流与参考。
- 上游授权为 CC BY 4.0。

### 本次处理

- 完整下载 100 张高清原图到 `references/layout-composition-images/originals/`。
- 完整下载 100 张缩略图到 `references/layout-composition-images/thumbnails/`。
- 新增 `references/layout-composition-images/INDEX.md`，记录 100 个图号、构图名和本地路径。
- 新增 `references/layout-composition-patterns.md`，将图片型知识转写成构图词表、任务路由、高频模式卡、Prompt 片段和组合建议。
- 更新 `SKILL.md`，将该库接入资源地图和海报/排版/构图路由。

### 仍缺

- 尚未为 100 个构图逐一写长篇案例说明；当前只对高频构图写了完整模式卡，其余通过完整词表和图片索引保留。
- 尚未建立自动图像识别/标签检索脚本。

### 暂不吸收

- 不把 100 张图片全部塞入 `db/海报与排版/images/`，避免案例库膨胀并干扰海报风格案例检索。
- 不把图片作为唯一知识入口；必须以文字化规则优先。

### 原因

- 该来源是构图语法库，不是具体风格案例库。
- 通用 Agent 不应依赖每次现场读图才能使用；文字化模式更稳定、更便宜、更可迁移。

## Upgrade Checklist

未来升级前，至少回答以下问题：

- 这次要吸收的知识来源是否已经在 `source-registry.md` 登记？
- 是否已有对应本地落点？
- 这次是补 gap，还是重复表达？
- 新知识最小应落在哪个文件？
- 如果暂时不吸收，原因是否应该写进本文件或 `fossil-record.md`？
