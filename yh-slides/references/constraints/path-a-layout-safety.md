# Path A Layout Safety

> 用途：Path A（HTML -> editable PPTX）生成前的固定画布排版安全规约。它补足 `path-a-seed.html` 的骨架能力，避免文字贴边、出框、被页脚遮挡或转成 PPTX 后挤压。

## 固定坐标系统

Path A 的坐标单位必须是 `pt`。

- Slide canvas: `720pt x 405pt`
- Hard safe area: `x = 32..688`, `y = 32..370`
- Dense content area: `x = 40..680`, `y = 48..360`
- Header/chrome lane: `y = 18..38`，只放页眉、小标题、页码等低信息密度元素
- Footer lane: `y = 372..390`，只放页脚、来源、进度，不放正文
- Any semantic body text must stay inside the hard safe area.

不要把标题、正文、卡片、图表直接贴到 `x < 32`、`x + width > 688`、`y < 32` 或 `y + height > 370` 的区域。装饰线、背景色块和 bleed image 可以出血，但不能承载正文。

## 文本框安全规则

1. 所有文本都必须有明确 `left/top/width/height/font-size/line-height`，不要依赖浏览器自动撑开。
2. 文本框不能与卡片边缘共用同一个 `left/top`；卡片内文本必须有 `10pt` 以上内边距，推荐 `12pt`。
3. 正文中文最小字号 `8.5pt`；高密度页推荐 `9.5pt - 11pt`；标题推荐 `20pt - 30pt`。
4. 中文正文 line-height 推荐 `1.25 - 1.45`；高密度页面不要低于 `1.22`。
5. 文本框高度估算：`fontSize * lineCount * lineHeight + 4pt`。如果估算高度超过容器高度，必须缩短文案、拆分卡片或拆页。
6. H1 最多 2 行；如果标题超过 14 个中文字符，手工断行或降低字号。
7. 列表每条建议不超过 18 个中文字符；超过时改成短标题 + 小字解释。
8. 不使用 `overflow:hidden` 掩盖正文溢出，除非该元素是装饰裁切。

## 高密度页型模板

Path A 可以高密度，但必须有可预测的页型。没有用户指定时，在下面三种里选一个，再写 HTML。

### A1 Manual Four Cards

适合：方法手册、原则集合、案例复盘。

- Header: `left 40 top 22 width 640 height 18`
- Title block: `left 40 top 52 width 300 height 72`
- Lead card: `left 380 top 52 width 300 height 72`
- Four cards: two columns x two rows, each `300 x 92`, gap `18`
- Footer: `left 40 top 374 width 640 height 12`

### A2 Core Loop + Matrix

适合：机制设计、产品策略、业务流程。

- Left explanation: `left 40 top 58 width 245 height 286`
- Center loop/diagram: `left 305 top 68 width 180 height 180`
- Right matrix/checklist: `left 505 top 58 width 175 height 286`
- Bottom insight strip: `left 305 top 270 width 375 height 74`

### A3 Process + Risk Board

适合：从 0 到 1 流程、项目路线图、教学步骤。

- Top title band: `left 40 top 42 width 640 height 54`
- Process rail: `left 44 top 118 width 632 height 76`
- Three detail cards: `left 44/258/472 top 218 width 190 height 118`
- Bottom warning/decision strip: `left 44 top 350 width 632 height 20`

## 构建前布局表

标准制作与精品交付时，写 HTML 前先给自己生成一张布局表，至少包含：

| Element | left | top | width | height | role |
|---------|------|-----|-------|--------|------|

检查每一行：

- `left >= 32`
- `top >= 32`，页眉元素除外
- `left + width <= 688`
- `top + height <= 370`，页脚元素除外
- 卡片内文字 `left = cardLeft + 10..14`
- 卡片内文字 `top = cardTop + 10..14`

## P0 自检

- 没有正文文本贴住画布边缘。
- 没有正文文本贴住卡片边缘。
- 没有文本框高度明显小于文字行数需求。
- 没有正文进入页脚保留区。
- 高密度页面采用 A1/A2/A3 或明确等价的布局表。
- 转成 PPTX 后抽查每页 shape 数与文本框存在性，确认不是整页截图。
