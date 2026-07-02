# Path Workflows

> 用途：承接 `SKILL.md` 中下沉的 Path A/B/H/C/D/E 构建细节与组装命令。先在 `SKILL.md` 完成路径选择、内容结构化、设计确认和预检，再按本文件执行具体路径。
> 命令约定：除非特别说明，先 `cd` 到 `yh-slides` 技能根目录；所有脚本都用 `scripts/...` 相对路径，避免写死某个 CLI 的 home 目录。

## Path A / 2A: Simple HTML -> Editable PPTX

Path A 服务于 `2A 通用可编辑 PPTX（简易 HTML 转换）`。这里的 HTML 是 PPTX 中间稿，不是网页最终作品；生成关键页插画，制作受限 HTML 幻灯片，用 `html2pptx` 转成可编辑 PPTX。

- 起点：`assets/seeds/path-a-seed.html`，720pt x 405pt 骨架。
- 生图后端：默认 `auto-runtime`。当前 CLI / agent runtime 有原生生图工具时优先原生工具；没有原生工具、无法稳定落盘或用户显式指定 `gemini` / `imagen` 时，才用脚本 API 后端。
- 铁律：HTML 根容器必须是 `720pt x 405pt`；内部元素必须 `position:absolute` 并用 pt 定位；图片 prompt 必须含 `no text in image`；图片路径必须是本地相对路径。
- 排版安全：写 HTML 前必须读取 `references/constraints/path-a-layout-safety.md`；正文必须在 safe area 内，卡片内文字必须有 10pt 以上内边距，高密度页必须采用 A1/A2/A3 或等价布局表。
- 参考：`references/aesthetics/proven-styles-gallery.md`、`references/aesthetics/prompt-templates.md`、`references/constraints/path-a-layout-safety.md`。

```bash
node scripts/html2pptx.js \
  "C:\PPTX\{项目名}\slides\slide1.html" \
  "C:\PPTX\{项目名}\slides\slide2.html" \
  -o "C:\PPTX\{项目名}\output\{项目名}.pptx"
```

## Path S / 2A-S: SVG -> Native Editable PPTX

Path S 服务于复杂图表、咨询级信息图、原生形状可编辑、备注和动画的高保真 PPTX。它比 Path A 更重，不作为普通正式汇报的默认路径。

- 起点：先完成 `design_spec.md` 与 `spec_lock.md`，记录 canvas、颜色、字体、图片资源、page_rhythm、page_layouts、page_charts。
- 模板来源：优先使用本地 `templates/charts/`、`templates/icons/`、`templates/layouts/`；上游来源只通过 `provenance/upstream-locks/` 和 `references/provenance/` 追溯。
- 逐页生成：每页生成前重读 `spec_lock.md`，不要凭记忆取色、字体或图片文件名。
- SVG 约束：不用 `foreignObject`、远程图片、脚本、动画标签或不可转换 SVG 特性；顶层语义块用 `<g id="...">` 组织，方便动画和对象选择。
- 备注：生成 `notes/total.md`，再用 `scripts/total_md_split.py` 拆页。
- 动画：全局动画通过 `scripts/svg_to_pptx.py` flags；对象级动画只在用户要求时使用 `animations.json`。

```bash
python scripts/svg_quality_checker.py "C:\PPTX\{项目名}"
python scripts/total_md_split.py "C:\PPTX\{项目名}"
python scripts/finalize_svg.py "C:\PPTX\{项目名}"
python scripts/svg_to_pptx.py "C:\PPTX\{项目名}"
```

详细规范见 `references/integrations/path-s-svg-native-pptx.md`。

## Template Fill / 2A-T: Native PPTX Template Reuse

Template Fill 只在用户提供现有 `.pptx` 模板并明确要求“保留原设计、填充新内容”时使用。它不走 HTML，也不走 SVG。

- 项目目录必须包含 `sources/`、`analysis/`、`exports/`、`validation/`。
- 先分析模板为 `analysis/slide_library.json`，把 PPTX 当作页面结构库，而不是按原顺序机械替换。
- 生成 `analysis/fill_plan.json`：可选择、重排、删除、复用源页；每页记录 layout rationale。
- 应先跑 capacity check，正文过长时优先改写、拆页或换版式，不默认缩字体。
- 输出后用 PPTX readback 验证标题、表格、图表、notes 和页数。

```bash
python scripts/template_fill_pptx.py analyze \
  "C:\PPTX\{项目名}\sources\template.pptx" \
  -o "C:\PPTX\{项目名}\analysis\slide_library.json"

python scripts/template_fill_pptx.py scaffold \
  "C:\PPTX\{项目名}\analysis\slide_library.json" \
  -o "C:\PPTX\{项目名}\analysis\fill_plan.json"

python scripts/template_fill_pptx.py check-plan \
  "C:\PPTX\{项目名}\analysis\slide_library.json" \
  "C:\PPTX\{项目名}\analysis\fill_plan.json" \
  -o "C:\PPTX\{项目名}\analysis\check_report.json"

python scripts/template_fill_pptx.py apply \
  "C:\PPTX\{项目名}\sources" \
  "C:\PPTX\{项目名}\analysis\fill_plan.json" \
  -o "C:\PPTX\{项目名}\exports"
```

详细规范见 `references/integrations/template-fill-pptx.md`。

## Path B / 2B: Full AI Image PPTX

每页作为完整 AI 图片生成，布局、文字、视觉一体完成。文字可以在图片里，但基本不可编辑；生成后必须检查图片内文字准确性。

- Prompt manifest：先生成 `tasks.json`，记录每页 prompt、output、aspect ratio、尺寸。无论后端是 Codex Image2 还是 Gemini，都不要跳过。
- 当前 CLI / agent runtime 有原生图片工具时，默认逐张用原生工具生成整页图，并保存到 `images/`。
- 原生工具不可用或无法稳定落盘时，再使用 Gemini batch。
- 用户显式指定 `gemini` / `imagen` / `codex-image2` 时按用户指定执行；若指定后端不可用，先说明并建议 fallback。
- 规则：严格顺序生成，不并行；失败后用 `--skip-existing` 断点续传；prompt 必须控制机器乱码文字风险。
- 使用 Ian 中文手绘技术解释时，读取 `references/aesthetics/ian-handdrawn-technical.md`，每页在 prompt 末尾列出 `Required text only`，并明确禁止任何额外文字、URL、Logo 和填充字符。

```bash
python scripts/generate_image.py \
  batch --tasks "C:\PPTX\{项目名}\tasks.json" --model gemini --cooldown 8 --skip-existing --image-size 2K
```

```bash
uv run scripts/create_slides.py \
  "C:\PPTX\{项目名}\images\slide-01-cover.png" \
  "C:\PPTX\{项目名}\images\slide-02-intro.png" \
  --layout fullscreen \
  --bg-color 000000 \
  -o "C:\PPTX\{项目名}\output\{项目名}.pptx"
```

## Path H / 2C: Visual Background + Editable Text PPTX

混合型链路：AI 生成“无正文文字”的整页视觉底图 -> 用 PPT 原生文本框叠加标题、正文、互动题和答案 -> 输出可编辑 `.pptx`。这是“视觉好 + 可改字”的默认推荐路径。

- 底图 prompt 必须明确：`no text, no letters, no title, no body copy, no question text, no answer text`。
- 底图只承担背景、插画、氛围、结构空间和装饰，不承担课堂/汇报文字。
- 逐页大纲必须标注哪些文字进入 PPT 文本框，哪些视觉元素进入底图。
- 构图必须预留文字留白；中文文本框优先用 PPT 原生字体和层级。
- 组装逻辑可复用 `python-pptx` 或后续专门 Hybrid 脚本；不要走位图逆向重建，因为 2C 从一开始就不让底图承载正文文字。
- 使用 Ian 中文手绘技术解释时，底图必须同时禁止 words、letters、numbers、logos、URLs、pseudo-text 和 handwriting，并显式预留标题区与标签区；所有可见文字由 PPT 原生文本框承担。

## FigEdit Reconstruction / 2B-R: Raster -> Editable SVG and Native PPTX

2B-R 是正式的位图重建入口。它通过 `scripts/figedit_batch.py` 调用独立
FigEdit 技能，逐页生成测量证据、语义 Manifest、可编辑 SVG、原生 PPTX
和质量报告。普通文字、稳定几何、连接线和公式应恢复为可编辑对象；照片、
Logo、截图、地图和复杂图表允许保留为可替换图片资产。

```powershell
python scripts\figedit_batch.py preflight
python scripts\figedit_batch.py init --project-dir "C:\PPTX\{项目名}" --slides "01.png" "02.png"
python scripts\figedit_batch.py measure --project-dir "C:\PPTX\{项目名}" --ocr-profile v6_medium
# Agent 逐页编写并审查 reconstruction/page-NN/manifest.json
python scripts\figedit_batch.py compose --project-dir "C:\PPTX\{项目名}"
python scripts\figedit_batch.py status --project-dir "C:\PPTX\{项目名}"
python scripts\figedit_batch.py assemble --project-dir "C:\PPTX\{项目名}" --output "C:\PPTX\{项目名}\output\{项目名}-editable.pptx"
```

任一页面未通过自动质量门或显式语义审查时，不得生成整套 PPTX。详细规范见
`references/integrations/figedit-reconstruction.md`。

## Path C / 2D: Single-File HTML as Final Deck

必须先完成 `SKILL.md` 的 Step 5.0 类名预检和 Step 5.0.5 主题节奏规划。

- Magazine 精品模板：`assets/seeds/path-c-magazine-seed.html`，含 WebGL、5 主题、10 布局。
- 极简模板：`assets/seeds/path-c-minimal-seed.html`，轻量，无 WebGL。
- 本地运行时资产：把 skill 的 `assets/vendor/` 复制到输出目录的 `assets/vendor/`，保证字体、Lucide、Motion 等离线可用。
- 布局参考：`references/aesthetics/magazine/layouts.md`。
- 组件参考：`references/aesthetics/magazine/components.md`。
- 动效资产：magazine 模板默认从 `assets/vendor/js/motion.min.js` 本地加载；不要改回 CDN。
- 配图：读取 `references/aesthetics/magazine/image-prompts.md`，先确定图片槽位和比例，再按 `auto-runtime` 选择后端生成。配图不能自带页眉、页脚、标题、页码、角标或装饰边框。
- 输出：`C:\PPTX\{项目名}\output\presentation.html`。

## Path D / 2D: Multi-File HTML + GSAP + TTS

必须先完成 Step 5.0 和 Step 5.0.5。

- 起点：`assets/seeds/path-d-animated-seed.html`。
- 本地运行时资产：把 skill 的 `assets/vendor/` 复制到输出目录的 `assets/vendor/`，保证字体、Lucide、GSAP、ScrollTrigger 等离线可用。
- 动画规则：动效服务内容，不抢文字可读性；统一用 `data-anim` 属性声明入场类型。
- 输出目录：`C:\PPTX\{项目名}\output\index.html`，并包含 `styles\`、`scripts\`、`audio\` 等资产目录。
- 参考：`references/integrations/animation-guide.md`、`references/integrations/tts-configuration.md`。

## Presenter Mode / 2D-P: HTML Deck with Speaker View

Presenter Mode 是 HTML 最终交付物的专项分支，适合演讲、分享、培训、路演、逐字稿和提词器需求。

- 本地资产：优先使用 `templates/html-decks/html-ppt/full-decks/presenter-mode-reveal/` 或把 `templates/html-decks/html-ppt/runtime.js` 接入现有 HTML deck。
- 每页必须把讲稿放进 `<aside class="notes">` 或 `.notes` 容器，不能写在观众可见区域。
- `S` 键打开 presenter window；观众窗口和 presenter window 必须能同步翻页。
- `?preview=N` 必须能渲染无 chrome 的单页 iframe 预览。
- 离线时不得依赖 CDN runtime、远程字体或远程图片。

最小页面结构：

```html
<section class="slide">
  <h1>Audience title</h1>
  <p>Audience-facing content only.</p>
  <aside class="notes">
    <p>Presenter prompt with <strong>keywords</strong> and a natural transition.</p>
  </aside>
</section>
```

详细规范见 `references/integrations/presenter-mode.md`。

## Path E / 2D: Local React Deck

本地 React/TSX 或等价前端工程路径。它吸收固定 1920×1080 画布、组件化 authoring、静态导出和截图 QA 方法，但不默认依赖 Open-Slide、Open-Design 或任何外部 slide runtime。

- 适用：长期维护、复杂交互、组件复用、静态部署、严格截图 QA。
- 起点：读取 `references/integrations/local-react-deck-path.md`。
- 主题：读取或生成 `DESIGN.md`，把 palette、type scale、layout rhythm、image strategy、page archetypes、avoid list 写入本地主题。
- 页型：先完成 Step 3-C 页型覆盖检查，再把每页映射为 React 组件或数据驱动页面。
- 画布：每页固定 1920×1080，由预览容器等比缩放；不要在 slide 内写响应式断点。
- 资源：图片、字体、脚本必须是本地项目资产；不能把远程资源作为必需依赖。
- 输出：`C:\PPTX\{项目名}\output\react-deck\` 或现有工程的静态构建目录。

推荐局部目录：

```text
C:\PPTX\{项目名}\react-deck\
├── src\
│   ├── App.tsx
│   ├── slides.tsx
│   └── theme.ts
├── public\
└── package.json
```

构建命令按现有工程决定，不硬编码唯一包管理器。若新建 Vite/React 工程，应保持工程局部化，不改写用户其他项目文件。

组装后必须执行 `references/constraints/visual-qa.md`：

- 每页截图
- hash / 近空白检测
- contact sheet
- 白屏、截断、重叠、文本溢出检查
