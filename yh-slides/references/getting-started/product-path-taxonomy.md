# Product Options and Internal Paths

> 用途：统一 `yh-slides` 的命名层级，避免把用户产物选项和内部执行路径混用。

## 两层命名

`2A/2B/2C/2D` 是用户侧的产物选项，回答“我要交付什么”。`2A-S`、`2A-T`、`2D-P`、`2D-B` 是在原产物体系下新增的高级/专项分支：只在复杂原生 PPTX、已有 PPTX 模板复用、演讲者模式、本地可编辑单文件等明确需求中推荐。

`Path A/B/H/C/D/E` 是内部执行路径，回答“我用什么制作工艺完成它”。

不要把不同层级并列描述，例如不要写“2B、2C、Path C、Path D 四种模式”。正确写法是：“产物选项 2A/2B/2C/2D；其中 2D 内部可走 Path C/D/E”。

## 正式映射

| 用户侧产物选项 | 内部执行路径 | 本质 | 最终交付 |
|---|---|---|---|
| `2A 通用可编辑 PPTX（简易 HTML 转换）` | `Path A` | 用受限 HTML/CSS 做 PPTX 中间稿，再转成 PowerPoint 原生文本、形状、图片 | `.pptx` |
| `2A-S 高保真原生可编辑 PPTX` | `Path S` | 逐页 SVG 作为视觉源，经 DrawingML 导出原生可编辑形状、文字、图表和动画 | `.pptx` |
| `2A-T 原生 PPTX 模板填充` | `Template Fill` | 复用已有 PPTX 模板页，分析槽位并替换文字、表格、图表 | `.pptx` |
| `2B 整图视觉 PPTX` | `Path B` | 每页是一张完整 AI 图，文字也可在图里 | 图片型 `.pptx` |
| `2C 视觉底图 + 可编辑文字 PPTX` | `Path H（混合型 PPTX）` | AI 生成无正文文字整页底图，PPT 原生文本框承担标题、正文、题目和答案 | `.pptx` |
| `2B-R 可编辑重建` | `FigEdit Reconstruction` | 已有位图经 OCR/CV 测量、Agent 语义拆解、SVG 与 DrawingML 重建 | `.pptx` + SVG + Manifest + 质量报告 |
| `2D 多功能 HTML 演示` | `Path C / D / E` | HTML 是最终作品，可做单文件网页、动画配音或 React 交互 | `.html` / 静态网页 |
| `2D-B Bento Deck` | `Bento Adapter` | 固定本地 shell + 结构化文档，浏览器内可编辑，含 notes、评论、状态/morph | `.bento.html` |
| `2D-P HTML 演讲者模式` | `Presenter Mode` | HTML 最终作品 + hidden notes + S 键 presenter window | `.html` / 静态网页 |

## 2A 和 2D 的边界

两者都可能使用 HTML，但 HTML 的角色完全不同：

| 维度 | `2A / Path A` | `2D / Path C/D/E` |
|---|---|---|
| HTML 角色 | PPTX 中间稿 | 最终交付物 |
| 写作规范 | 固定 `720pt x 405pt`、全 absolute、保守 CSS | 可响应式、可滚动、可动画、可交互 |
| 目标 | 转成可编辑 PPTX | 浏览器直接播放或分享 |
| 失败风险 | html2pptx 坐标偏移、文本框溢出 | 浏览器适配、动效、截图 QA |
| 适合 | 会议、课程、企业汇报、后期继续改 PPT | 网页分享、电子杂志、自动播放、互动展示 |

规则：如果 HTML 需要转 PPTX，就必须按 `Path A` 规范写；如果 HTML 作为最终网页交付，就属于 `2D`，再选择 `Path C/D/E`。不要把 `Path C` 的复杂网页模板直接拿去做 PPTX 转换源。

## 2D 内部分流

`2D` 是用户侧的大类，不直接等于某一个 Path。

- `Path C`: 单文件网页演示，适合链接分享、电子杂志、轻量多页 HTML。
- `Path D`: 动画 + 配音 HTML，适合自动播放、课堂导览、视频化演示。
- `Path E`: 本地 React/TSX 演示工程，适合长期维护、复杂交互、组件复用和静态部署。
- `Presenter Mode / 2D-P`: HTML 演讲者模式，适合现场演讲、技术分享、培训和需要逐字稿/提词器的场景；它可基于 Path C/D/E 的 HTML 资产，但必须额外满足 notes 和 presenter QA。
- `Bento Adapter / 2D-B`: 固定的本地单文件可编辑 deck；仅在需要浏览器编辑、评论回流或状态/morph 时使用，不替代 Path C/D/E，也不承诺 PPTX。

## 2A 高级分支

- `2A / Path A`: 默认可编辑 PPTX 路径，最稳、最快，适合大多数正式汇报。
- `2A-S / Path S`: 复杂图表、咨询级信息图、原生形状/矢量可编辑、避免 HTML 转换偏移时使用。流程更重，必须跑 SVG 质量门和 PPTX 可编辑性检查。
- `2A-T / Template Fill`: 用户已有 `.pptx` 模板并要求保留原设计时使用。不要把它用于从零生成普通 PPTX。

## 2B-R 的位置

`2B-R / FigEdit Reconstruction` 是正式的位图可编辑重建选项，不是
`2C`，也不要求源图来自 `2B`。输入可以是位图幻灯片、截图、论文图、
架构图或信息图。独立 FigEdit 负责测量与单页重建，`yh-slides` 负责批处理、
逐页质量门和整套 PPTX 汇集。

如果用户在正向制作开始前已经知道需要可编辑，应优先选择 `2A`、`2A-S`
或 `2C`；2B-R 主要解决已经失去源文件的位图资产。
