# Learning Capture Rules

面向 `yh-image-inspirer` 的轻量会话学习规则。借用 `continuous-learning` 的思路，但不依赖全局 Hook。

## 什么时候要落档

出现以下任一情况，就应考虑把经验写进本 skill：

- 用户明确纠正了 prompt 策略
- 某类任务连续成功 2 次以上
- 某类翻车模式被修复
- 新增了稳定可复用的 brief 结构
- 新增了明确不该再做的反例

## 落档优先级

- 用户偏好类 -> `personal-preferences.md`
- 失败规避类 -> `output-checklists.md`
- 通用流程类 -> `SKILL.md` 或 `recipes/`
- 来源对照类 -> `upstream-gap-tracker.md`
- 已否决思路 -> `fossil-record.md`
- 只做叙事记录 -> `evolution-log.md`

## 快速判断表

| 新经验类型 | 应该写去哪里 | 说明 |
| --- | --- | --- |
| 用户说“以后都默认中文，不要英文按钮” | `personal-preferences.md` | 默认偏好 |
| 某类 UI 截图总会乱码，后来靠逐字文案解决 | `output-checklists.md` | 质量规则 |
| 系列卡牌必须先锁变量表才能稳定 | `recipes/series-generation.md` | 固定流程 |
| 新发现某上游模板已吸收过 | `upstream-gap-tracker.md` | 来源治理 |
| 某种升级方案试过但不合适 | `fossil-record.md` | 反例归档 |

## 最小记录原则

落档时，至少写明：

- 触发任务是什么
- 学到的规则是什么
- 未来什么场景复用
- 应写入哪个文件

不要只写“记住这个经验”，而不写落点。

## 与来源治理的关系

如果学到的是：

- 来自用户工作流的偏好 -> 不需要新增 `source_id`
- 来自外部仓库或新技能 -> 先补 `source-registry.md`
- 来自已有来源的新差异 -> 更新 `upstream-gap-tracker.md`
