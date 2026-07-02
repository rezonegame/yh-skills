# Source Attribution

`yh-image-inspirer` 是一个可独立运行的通用视觉生成工作流 skill。它运行时依赖当前目录内置资源，不依赖外部 `image-inspirer` skill 或 `awesome-gpt-image-2` 仓库。

## 内置本地案例库

当前 `db/` 目录包含 14 个图片提示词案例分类：

- UI与界面
- 人物与角色
- 其他应用场景
- 历史与古风题材
- 品牌与标志
- 商品与电商
- 图表与信息可视化
- 场景与叙事
- 建筑与空间
- 插画与艺术
- 摄影与写实
- 文档与出版物
- 桌游卡牌与版图
- 海报与排版

这些案例和参考图已完整放入本 skill 的 `db/` 目录，用于本地检索、启发和二次创作。

## 结构化模板来源

`references/structured-templates.md` 与 `references/awesome-boardgame-cases.md` 吸收了 `freestylefly/awesome-gpt-image-2` 的 Prompt-as-Code 思路和部分高价值案例结构，但不是全量镜像。

整合方式：

- 提炼结构、变量槽位和防坑规则。
- 保留对可迁移案例编号的说明。
- 不把外部仓库作为运行时依赖。

## 排版构图参考来源

`references/layout-composition-patterns.md` 与 `references/layout-composition-images/` 吸收了 `nevertoday/100-layout-compositions` 的 100 种排版构图参考。

整合方式：

- 完整保存 100 张高清原图与 100 张缩略图，供本地离线参考。
- 将图片型构图参考转写为 Agent 可检索、可复用的文字化构图模式。
- 保留上游署名与 CC BY 4.0 授权说明。

上游地址：https://github.com/nevertoday/100-layout-compositions

## 维护边界

- 新增案例：优先写入当前 skill 的 `db/<类型>/prompt.md` 和对应 `images/`。
- 新增规则：优先写入 `references/personal-preferences.md` 或 `references/output-checklists.md`。
- 新增专题流程：优先写入 `recipes/`。
- 重要演进：追加到 `references/evolution-log.md`。

## 许可与使用提醒

本 skill 的内置案例和参考资料来自公开学习与研究资源的整理。用于商业出图或对外分发时，应自行确认具体案例、参考图、品牌、角色、文字和图像素材的授权情况。

