---
name: yh-slides
description: >
  从内容到演示文稿的端到端制作。支持 PPTX 和 HTML 双输出、AI 插画生成、
  多种视觉风格、TTS 配音、网页/视频/音频导入与 PPT 转换。
  当用户提到“做PPT”“做幻灯片”“演示文稿”“slides”“HTML presentation”“deck”“keynote”“做个报告”“视觉设计”时使用。
---

# AI Presentation Workflow

用于从主题、文档、网页或媒体素材生成演示文稿。支持 4 条输出路径：

- `Path A`: 编辑式 HTML -> PPTX
- `Path B`: 全 AI 视觉 -> PPTX
- `Path C`: 零依赖 HTML
- `Path D`: 富交互 HTML

## Step 0: 启动时必须确认的设置

每次开始任务时，都必须先逐项确认，不设默认值。

### Step 0 Template: 启动问句模板

启动 `yh-slides` 时，优先按下面顺序向用户确认，尽量不要跳问，也不要把多个关键决策合并得过于含糊。

标准启动问句：

```text
我会先确认这次演示的工作流设置，再开始制作。

1. 输入来源：从零创建、PPT/PPTX 转换、网页导入，还是视频/音频导入？
2. 输出路径：Path A、Path B、Path C，还是 Path D？
3. 如果你选 Path B：要走标准版，还是高级版可编辑导出？
4. 协作模式：全自动、引导式，还是协作式？
5. 图片尺寸：512、1K、2K，还是 4K？
6. 项目名想用什么？
```

如果用户明确要求“Path B + 可编辑文字”，推荐问句：

```text
这类需求更适合 Path B 的高级版。它会保留整页 AI 视觉感，并额外导出为可编辑 PPTX。
你这次要走 Path B 标准版，还是 Path B 高级版？
```

如果用户只说“帮我做个 PPT”，最少也必须补问：

```text
这次你想走哪条路径：Path A、Path B、Path C 还是 Path D？
如果选 Path B，我还需要继续确认是标准版还是高级版可编辑导出。
```

禁止行为：

- 不要在用户选 `Path B` 后直接默认标准版
- 不要在用户说“要可编辑”后直接擅自改成 `Path A`
- 不要跳过项目名确认
- 不要在未确认尺寸时直接开始批量生图

### 0-A. 输入来源

必须让用户明确选择其一：

- 从零创建
- PPT/PPTX 转换
- 网页导入
- 视频/音频导入

### 0-B. 输出路径

| 路径 | 工作方式 | 适用场景 |
|---|---|---|
| `Path A` | HTML 幻灯片 + 选择性 AI 插画 -> `html2pptx` -> 可编辑 PPTX | 需要可编辑文字、精确布局、企业演示 |
| `Path B` | 每页完整 AI 图片 -> PPTX | 视觉冲击、艺术展示、快速成稿 |
| `Path C` | 单文件 HTML，CSS/JS 全内联 | 网页分享、零依赖 |
| `Path D` | 多文件 HTML + GSAP + TTS | 多媒体演示、网页展示 |

| 维度 | Path A | Path B | Path C | Path D |
|---|---|---|---|---|
| 文字可编辑 | 是 | 标准版否 / 高级版是 | 是 | 是 |
| 视觉质量 | 好 | 极佳 | 好 | 好 |
| 动画支持 | PPTX 内 | 无 | CSS 原生 | GSAP |
| 输出 | `.pptx` | `.pptx` | `.html` | `.html` |

### 0-B-1. Path B 高级模式选择

当用户选择 `Path B` 时，必须继续确认：

- `标准版`：整页 AI 图片直接组装为 PPTX
- `高级版`：整页 AI 图片 -> 清背景 -> 提取文字框与样式 -> 重建可编辑 PPTX

规则：

- 如果用户要求“`Path B` 且文字可编辑”，优先推荐 `Path B 高级版`
- 不要因为“文字可编辑”自动改走 `Path A`
- 必须明确说明：`Path B 高级版` 是实验性流程，通常视觉还原优先于文字框精度
- 一旦用户确认 `Path B`，后续回复里不要只写“Path B”，必须写成 `Path B 标准版` 或 `Path B 高级版`

### 0-C. 协作模式

必须让用户明确选择：

- `全自动`
- `引导式`
- `协作式`

### 0-D. 可选增强

逐项确认是否启用：

- TTS 配音
- GSAP 动画
- Unsplash 摄影
- 视觉风格预览

### 0-E. 图片尺寸

当路径涉及 AI 图片生成时，必须确认图片尺寸：

- `512`
- `1K`
- `2K`
- `4K`

建议默认推荐顺序：

- `2K`：高质量演示
- `1K`：更快
- `4K`：仅在强打印需求时使用

### 0-F. 项目目录

默认项目目录：

```text
C:\PPTX\{项目名}\
├── images\
├── slides\
├── output\
└── tasks.json
```

开始前必须确认项目名，并在 `Step 1` 前创建目录。

## Step 1: 内容结构化

将原始素材整理为逐页大纲。每页都要有：

- `Title`: 完整论断句，不是主题词
- `Key points`: 最多 3-4 条
- `Visual type`
- `Path A`: 是否需要插画
- `Path B`: 完整视觉场景描述
- `Path C/D`: 布局类型

原则：

- 一页一个核心观点
- 幻灯片正文默认用中文
- 只保留必要英文术语

✅ **Checkpoint 1**：将大纲展示给用户确认，再进入 Step 2。

## Step 2: 设计系统

给用户展示 3 个完整设计方向供选择，而不是只给色板。

可参考：

- `references/proven-styles-gallery.md`
- `references/web-styles-gallery.md`
- `references/design-movements.md`
- `references/style-extraction.md`

如果用户上传参考图，可先运行：

```bash
python ~/.claude/skills/yh-slides/scripts/generate_image.py extract-style --image ref.png
```

## Step 3: 构建幻灯片

### Step 3-A. Path A

生成关键页插画，然后制作 HTML 幻灯片，并用 `html2pptx` 转成可编辑 PPTX。

关键规则：

- HTML 输入尺寸必须是 `720pt x 405pt`
- 所有元素必须使用 `position: absolute`
- 图片里必须写 `no text in image`

### Step 3-B. Path B

每页作为完整 AI 图片生成，布局、文字、视觉一体完成。

Path B 分为两种交付模式：

- `标准版`：输出图片型 PPTX
- `高级版`：输出可编辑 PPTX

生成规则：

- 严格顺序生成，不并行撞 API
- 多页时优先使用 `batch`
- 失败后允许断点续传

推荐命令：

```bash
python ~/.claude/skills/yh-slides/scripts/generate_image.py \
  batch --tasks "C:\PPTX\{项目名}\tasks.json" --cooldown 8 --skip-existing --image-size 2K
```

### Step 3-C. Path C

生成单文件 HTML，所有 CSS/JS 内联，无外部依赖。

必读参考：

- `references/slide-structure-reference.md` — 幻灯片类型模板
- `references/viewport-fitting-spec.md` — 视口适配规范
- `references/slide-presentation-js.md` — Scroll-snap 导航控制器

### Step 3-D. Path D

生成多文件 HTML，支持 GSAP 和 TTS。

必读参考：

- `references/animation-guide.md` — GSAP 翻页动画 + CSS 原生动画
- `references/tts-configuration.md` — TTS 配音设置
- `references/slide-structure-reference.md` — 幻灯片类型模板

## Step 4: 组装输出

### 4-A. Path A -> 可编辑 PPTX

```bash
node ~/.claude/skills/pptx/scripts/html2pptx.js \
  "C:\PPTX\{项目名}\slides\slide1.html" \
  "C:\PPTX\{项目名}\slides\slide2.html" \
  -o "C:\PPTX\{项目名}\output\{项目名}.pptx"
```

### 4-B. Path B 标准版 -> 图片 PPTX

```bash
uv run ~/.claude/skills/yh-slides/scripts/create_slides.py \
  "C:\PPTX\{项目名}\images\slide-01-cover.png" \
  "C:\PPTX\{项目名}\images\slide-02-intro.png" \
  --layout fullscreen \
  --bg-color 000000 \
  -o "C:\PPTX\{项目名}\output\{项目名}.pptx"
```

### 4-B-Advanced. Path B 高级版 -> 可编辑 PPTX

先生成整页 PNG，再执行高级导出：

```bash
uv run ~/.claude/skills/yh-slides/scripts/build_pptx.py \
  --slides "C:\PPTX\{项目名}\images\slide-01-cover.png" "C:\PPTX\{项目名}\images\slide-02-intro.png" \
  --auto-clean-bg \
  --bg-dir "C:\PPTX\{项目名}\backgrounds" \
  --dump-json "C:\PPTX\{项目名}\output\text-data.json" \
  --output "C:\PPTX\{项目名}\output\{项目名}-editable.pptx"
```

高级版工作链路：

1. 使用 `generate_image.py clean-bg` 提取干净背景
2. 使用 Gemini 提取文字框、颜色、对齐和粗细
3. 用 `python-pptx` 重建可编辑文本框
4. 输出可编辑 `.pptx`

适用说明：

- 保留 Path B 的整页视觉感
- 允许后续编辑文字
- 个别页可能需要抽查位置和字号

### 4-C. Path C -> 单文件 HTML

输出到：

```text
C:\PPTX\{项目名}\output\presentation.html
```

### 4-D. Path D -> 多文件 HTML

输出目录：

```text
C:\PPTX\{项目名}\output\
├── index.html
├── styles\
├── scripts\
└── audio\
```

## Step 5: 预览与打磨

- `Path A`：抽查 3-4 张 HTML 预览图
- `Path B 标准版`：直接抽查 PNG
- `Path B 高级版`：还要抽查 2-3 页 PPTX 的文字框位置
- `Path C/D`：浏览器打开预览

确认项：

- 是否有页面需要调整
- 是否准备好在 PowerPoint / Keynote / 浏览器中打开

## 关键决策规则

- 需要最稳妥的“可编辑文字”时，优先 `Path A`
- 需要最强视觉冲击时，优先 `Path B`
- 需要 `Path B` 风格且还想改字时，优先 `Path B 高级版`
- 不要把 `Path B 高级版` 描述成默认稳定主路径，要明确它是实验性增强流程

## 内置能力

| 能力 | 命令 / 脚本 | 用途 |
|---|---|---|
| AI 图片生成 | `scripts/generate_image.py generate` | 单张生成 |
| 批量图片生成 | `scripts/generate_image.py batch` | 顺序批量生成 |
| 图片编辑 | `scripts/generate_image.py edit` | 修改已有图片 |
| 风格提取 | `scripts/generate_image.py extract-style` | 从参考图提取风格 |
| 清背景 | `scripts/generate_image.py clean-bg` | 为高级可编辑导出提取底板 |
| 图片型 PPTX 组装 | `scripts/create_slides.py` | Path B 标准版 |
| 可编辑 PPTX 导出 | `scripts/build_pptx.py` | Path B 高级版 |
| HTML -> PPTX | `~/.claude/skills/pptx/scripts/html2pptx.js` | Path A |

## 参考文件

| 文件 | 用途 | 适用路径 |
|------|------|----------|
| `references/prompt-templates.md` | AI 图片生成 prompt 工程指南 | A, B |
| `references/proven-styles-gallery.md` | 18+ 种 AI 艺术风格定义 | A, B |
| `references/proven-styles-snoopy.md` | Snoopy 风格逐页模板 | A, B |
| `references/web-styles-gallery.md` | 27 种 CSS/Web 风格完整 CSS | C, D |
| `references/design-principles.md` | 设计框架、反 AI 审美铁律、品牌定制 | 全部 |
| `references/design-movements.md` | 设计运动与风格参考库 | 全部 |
| `references/style-extraction.md` | 从参考图提取风格描述 | A, B |
| `references/style-preview-mechanism.md` | 3 选 1 视觉风格预览机制 | C, D |
| `references/editable-pptx-export.md` | AI 图片 → 可编辑 PPTX 导出技术指南 | B 高级 |
| `references/slide-structure-reference.md` | 幻灯片类型模板 | C, D |
| `references/viewport-fitting-spec.md` | 视口适配规范（每页精确填充） | C, D |
| `references/slide-presentation-js.md` | Scroll-snap + Intersection Observer 导航 | C |
| `references/animation-guide.md` | GSAP 翻页动画 + CSS 原生动画 | C, D |
| `references/tts-configuration.md` | TTS 配音设置 | C, D |
| `references/api-configuration.md` | Unsplash API 配置 | 全部 |
| `references/import-guide.md` | 网页/视频/音频导入指南 | 全部 |
| `references/ppt-conversion-guide.md` | PPT/PPTX 转换指南 | 全部 |

## 输出

- `.pptx` for `Path A`
- `.pptx` for `Path B 标准版`
- `.pptx` for `Path B 高级版`
- `.html` for `Path C`
- multi-file HTML for `Path D`
