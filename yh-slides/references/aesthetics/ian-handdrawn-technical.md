# Ian 中文手绘技术解释

> 来源方法：`helloianneo/ian-handdrawn-ppt`，固定提交 `b2cc5f303337e5470fd6ac2870d261a43b218439`。本文件是 `yh-slides` 的本地风格契约，不是独立技能入口。

## 何时读取

- 用户明确要求 Ian 手绘、中文手绘技术图解或类似风格时。
- 技术解释、教学、知识卡片、方法论演示需要克制而清晰的手绘语义图时，可在 Step 4 作为候选推荐。
- 商务摄影、品牌模板复用、数据密集型报告或需要复杂原生图表时不要推荐。

## 路径路由

- `2B / Path B`：完整栅格页。适合短标题、少量短标签且用户接受文字进入图片。
- `2C / Path H`：无文字手绘底图加 PPT 原生文字。出现精确数字、专有名词、长文本、频繁改字或严格中文准确性时优先。
- 不新增模式或路径，也不把该风格设为知识类演示的默认值。

## 固定视觉 DNA

- 画布：正文 16:9，近白纸色 `#FBFAF5`；不要黄色或米黄色旧纸效果。
- 线条：近黑 `#111111` 的细钢笔或铅笔线，允许轻微排线，不使用粗重漫画描边。
- 标签色：淡蓝 `#D9E8F6`、淡绿 `#DCEAD6`、淡桃 `#F5DEB8`、淡紫 `#E4DCF4`；强调色可用 `#D66F4D`。
- 外壳：大留白、无满页边框、小页码位于左上、正文标题居中且克制，标题下使用淡蓝短下划线。
- 主图：用物件和空间关系解释概念，通常占页面宽度 50–60%、高度 35–45%。
- 人物：优先不用人物；确有叙事需要时最多一个角落里的微小读者代理。
- 套图：固定外壳、字号尺度和线条语言，只改变中央语义图形。

参考锚点：`assets/style-samples/ian-handdrawn-technical-anchor.png`。仅用于视觉校准，不得直接放进用户成品。

## 语义页型

按内容选择一个主关系，不要把多个页型拼成素材清单：

- `cover-metaphor`：一个核心物件隐喻主题。
- `single-concept`：一个对象及其关键关系。
- `left-right-contrast`：同一对象的两种状态或方案。
- `transformation`：从旧状态向新状态的可见变化。
- `horizontal-process`：少量连续动作构成的流程。
- `circular-loop`：确有反馈闭环时使用，不为装饰强造循环。
- `branching-map`：从共同起点分出少量路径。
- `taxonomy`：围绕一个中心进行分类。
- `matrix`：二维关系确实重要时使用。
- `main-metaphor`：用熟悉物件承担抽象关系。
- `warning`：一个清晰失败机制，不堆叠警示符号。
- `takeaway`：以单一结论和一个收束物件结束。

## Prompt 契约

每页 Prompt 都必须明确：页面角色、语义关系、核心物件、外壳不变量、允许文字和禁止项。

### `2B / Path B`

在 prompt 末尾列出：

```text
Required text only:
- <exact title>
- <exact short label 1>
- <exact short label 2>

Do not add any other words, letters, numbers, URLs, logos, captions, or filler text.
```

- 标题优先 5–12 个汉字；每页主标签 2–5 个，每个标签尽量 2–6 个汉字。
- 第一轮文字错误时先缩短文字并重生成；仍不准确则切换 `2C`，不要接受伪字。

### `2C / Path H`

```text
Generate a text-free 16:9 hand-drawn technical explanation background.
Leave the title zone and label zones visibly empty.
No words, letters, numbers, logos, URLs, pseudo-text, handwriting, or typographic marks anywhere.
```

- 在底图中规划标题区、标签区和正文安全区；文字全部用 PPT 原生文本框叠加。
- 不允许先生成带字底图再用遮挡块掩盖错误文字。

## 专项 QA

交付前同时检查单页和联系表：

- 外壳稳定，但中央物件与关系随内容变化。
- 三秒内能说出本页解释的关系，不是装饰物清单。
- 无黄纸、满页框、超大正文标题、阴影、渐变、霓虹、大色卡或 PPT 素材拼贴感。
- 主图大致符合 50–60% 宽、35–45% 高的占用范围，留白清晰。
- 不出现伪英文、伪 URL、额外标签或未经要求的品牌标识。
- `2B` 的图片文字与 Required text only 完全一致。
- `2C` 的底图不含任何文字，最终文字保持可编辑。
- 同一套图不连续重复相同物件、动作和页面原型。

未通过任一关键项时，重写 Prompt 或切换路径后重新生成，不进入交付。
