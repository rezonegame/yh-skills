# yh-slides

演示文稿端到端制作技能。支持意图驱动入口、PPTX/HTML/React 多产物路径、多种视觉风格与 AI 图片生成。

当前版本增加了完整本地资产库模式：`ppt-master`、`guizang-ppt-skill`、`html-ppt-skill` 和可选 `bento` 适配器的本地模板、主题、布局、运行时、校验器和必要脚本已吸收到 `templates/`、`assets/`、`scripts/` 和 `references/provenance/`，并通过 `references/meta/asset-registry.json` 按需发现。模板库只增强 Step 4 的推荐，不替代 `yh-slides` 原有 Step 0 强引导入口。

底层协作精神吸收自 `huashu-slides` 的启发式共创方法。

同时吸收了这些项目的工作流与设计思想：
- `baoyu-slide-deck`
- `Kami`
- `huashu-design`
- `open-design`
- Open-Slide-style fixed-canvas authoring

这些项目只作为已吸收的方法来源记录；除明确声明的独立 FigEdit 技能联动外，`yh-slides` 的运行流程、模板方法和质量检查必须在本技能目录内离线可用，不依赖外部仓库、外部索引资产或远程 slide runtime。

学术演讲现提供 `academic-deck.json` v2：加入论证模式、研究问题、证据引用、单 exhibit 结果页、时间预算、结论与 Q&A 附录校验。版式选择同时支持“内容先冻结、按容量和结构家族比较候选”的方法层。两项增强分别参考 `academic-pptx-skill` 与 `dashi-ppt-skill`；后者仅方法级吸收，不含其 AGPL 主题、编辑器、runtime 或专有导出组件。

说明：前端运行资源与文档引用已本地化；图片生成、图片搜索等 API 后端仍然需要各自的网络 API 端点，这属于功能调用而不是静态引用资产。

命令约定：除非单独说明，先进入 `yh-slides` 技能根目录再运行命令，所有脚本都使用 `scripts/...` 相对路径。复制到其他 CLI 时保持 `scripts/`、`references/`、`assets/` 三个目录结构即可。

依赖约定：Path A 的 `html2pptx.js` 依赖 `pptxgenjs` 与 `cheerio`，已通过技能根目录的 `package.json` 本地化。首次使用或迁移到新机器时，在技能根目录运行 `npm install`；若 `node_modules/` 已随技能存在，则可离线直接运行。

配置约定：真实 API key 不放在本技能目录。通过运行环境变量提供，或显式设置 `YH_SKILLS_ENV_FILE` 指向私有 env 文件；本技能只保留 `.env.example` 作为占位说明，脚本不会搜索父目录。生图默认优先使用当前对话模型 / agent runtime 的原生工具；只有用户指定 API、原生工具不可用、无法稳定落盘或明确失败时，才退到显式配置的 API 后端。

---

## 产物选项与内部路径

`2A/2B/2C/2D` 是用户侧产物选项；`Path A/B/H/C/D/E` 是内部执行路径。完整说明见 [product-path-taxonomy.md](references/getting-started/product-path-taxonomy.md)。

| 用户侧产物选项 | 内部路径 | 输出 | 适用场景 | 种子文件 |
|------|------|------|---------|---------|
| **2A 通用可编辑 PPTX（简易 HTML 转换）** | Path A | 可编辑 `.pptx` | 受限 HTML 是 PPTX 中间稿；PPT 原生文字、形状、图表和版式为主，可加入局部插画/照片 | `assets/seeds/path-a-seed.html` |
| **2A-S 高保真原生可编辑 PPTX** | Path S | native editable `.pptx` | SVG → DrawingML；复杂图表、原生形状、备注和动画；更重但更可控 | `templates/` + `scripts/svg_to_pptx.py` |
| **2A-T 原生 PPTX 模板填充** | Template Fill | native editable `.pptx` | 复用已有 PPTX 模板，分析页面槽位并填充新内容 | `scripts/template_fill_pptx.py` |
| **2B 整图视觉 PPTX** | Path B | 图片型 `.pptx` | 每页完整 AI 图片，文字也可在图里；最强视觉冲击、快速成稿 | — |
| **2C 视觉底图 + 可编辑文字 PPTX** | Path H | 可编辑 `.pptx` | 无正文文字视觉底图 + PPT 原生文本框；好看且能改字 | — |
| **2D 多功能 HTML 演示** | Path C / D / E | `.html` / 静态网页 | HTML 是最终作品；单文件网页、动画配音或 React 交互 | `assets/seeds/path-c-*.html` / `path-d-animated-seed.html` |
| **2D-B Bento Deck** | Bento Adapter | `.bento.html` | 本地单文件、浏览器可编辑、notes/评论/状态/morph；默认离线 | `assets/seeds/path-bento-seed.json` |
| **2D-P HTML 演讲者模式** | Presenter Mode | `.html` | 本地 HTML + hidden notes + S 键 presenter window，支持当前/下一页/讲稿/计时器 | `templates/html-decks/html-ppt/` |
| **2B-R 可编辑重建** | FigEdit Reconstruction | 可编辑 `.pptx` + SVG/Manifest/报告 | 已有位图经语义拆解重建为可编辑文字、结构、公式和可替换图片资产 | `scripts/figedit_batch.py` |

注意：`2A / Path A` 和 `2D / Path C` 都会写 HTML，但前者的 HTML 是 PPTX 中间稿，后者的 HTML 是最终网页作品。若 HTML 需要转 PPTX，必须按 Path A 规范写。

---

## 快速上手

**不知道从哪开始？** → [references/getting-started/quick-start.md](references/getting-started/quick-start.md)

**不知道选哪条路径？** → [references/getting-started/path-selection.md](references/getting-started/path-selection.md)

**做学术答辩 / 论文汇报？** → [references/getting-started/academic-presentation-workflow.md](references/getting-started/academic-presentation-workflow.md)

**出错了？** → [references/constraints/failure-modes.md](references/constraints/failure-modes.md)

---

## 核心资产

### 种子文件（4 个）

```
assets/seeds/
├── path-a-seed.html           720pt×405pt + 全 absolute 骨架
├── path-c-magazine-seed.html  guizang 精品模板（WebGL + 5 主题 + 10 布局）
├── path-c-minimal-seed.html   轻量极简模板（无 WebGL）
└── path-d-animated-seed.html  GSAP + TTS 骨架

assets/vendor/
├── google-fonts-local.css     本地字体 CSS
├── fonts/                     本地 woff2 字体分片
└── js/                        Lucide / GSAP / ScrollTrigger / Motion 本地运行资源

assets/placeholders/
└── image-not-available.svg    本地缺图占位图
```

### 约束铁律

```
references/constraints/
├── class-preflight.md    类名预检（2D / Path C-D 强制）
├── theme-rhythm.md       主题节奏规则（2D / Path C-D-E 强制）
├── anti-patterns.md      17 种反模式（审美/技术/流程）
├── path-a-layout-safety.md  Path A 安全区、文本框内边距与高密度页型
├── quality-checklist.md  P0-P3 分级质检（2A/2B/2C/2B-R/2D）
├── visual-qa.md          截图 / hash / contact sheet（2D / Path C-D-E 强制）
├── comment-iteration-loop.md  评论归类与迭代闭环
└── failure-modes.md      20+ 失败模式 + 排查手册
```

### 本地模板方法层

```
references/aesthetics/
└── template-methods.md   质量基线、页型 archetype、模板矿化规则

references/integrations/
└── local-react-deck-path.md  2D / Path E 本地 React Deck 规则
```

### 本地吸收资产库

```
templates/html-decks/
├── html-ppt/              # themes / layouts / animations / presenter mode
└── guizang/               # magazine / Swiss seeds

assets/screenshot-backgrounds/
└── guizang/               # screenshot framing backgrounds

scripts/
├── template_fill_pptx.py
└── template_fill_pptx/

references/meta/
├── upstreams.md
├── upgrade-policy.md
├── asset-registry.md
└── asset-registry.json
```

自检命令：

```bash
python scripts/check_upstream_locks.py
python scripts/build_asset_registry.py
python scripts/check_yh_slides_integrity.py
python scripts/check_offline_ready.py
```

### magazine 设计系统（guizang 精华移植）

```
references/aesthetics/magazine/
├── themes.md      5 套精品主题色
├── layouts.md     10 种预设布局完整代码
├── components.md  排版组件库
└── checklist.md   原版质检清单
```

---

## 工作流概览

```
Step 0:   意图启动面板（目标 / 产物 / 素材 / 协作档位；路线码可选）
  ↓
Step 1:   需求发现与方向锁定（受众/时长/约束/图片策略）
  ↓
Step 2:   技术启动（路径确认 + 最小化问句）
  ↓
Step 3:   内容结构化（逐页大纲）           ← Checkpoint 1
          数据/流程/架构先判断是否需要图表或示意图
          页型 archetype 覆盖检查，避免 bullet dump
  ↓
Step 4:   设计系统（风格地图 → 推荐 3 选 1 → 样稿策略；2B/2C/2D 标准制作强制样稿） ← Checkpoint 2
          内部判断质量基线，使用模板时只矿化设计语言
  ↓
Step 5.0:   类名预检（2D / Path C-D 强制）
Step 5.0.5: 主题节奏规划（2D / Path C-D-E 强制）
Step 5:   构建幻灯片
  ↓
Step 6:   按路径组装输出（html2pptx / SVG DrawingML / template fill / create_slides / Path H / FigEdit / HTML）
  ↓
Step 7:   P0-P3 质量检查
  ↓
Step 8:   评论迭代循环（按文案/视觉/结构/事实/页序归类）
```

---

## 主要脚本

| 脚本 | 用途 |
|------|------|
| `scripts/generate_image.py generate` | 单张 AI 图片生成 |
| `scripts/generate_image.py batch` | 批量生成（断点续传） |
| `scripts/generate_image.py extract-style` | 从参考图提取风格 |
| `scripts/create_slides.py` | 2B / Path B PPTX 组装 |
| `scripts/figedit_batch.py` | 2B-R 独立 FigEdit 预检、逐页批处理、质量门和整套 PPTX 汇集 |
| `scripts/html2pptx.js` | Path A HTML → PPTX；依赖 `package.json` 中本地化的 `pptxgenjs` / `cheerio` |
| `scripts/build_asset_registry.py` | 扫描本地正式资产，生成离线资产索引 |
| `scripts/check_yh_slides_integrity.py` | 检查入口、资产、许可证、索引和关键文档是否完整 |
| `scripts/check_offline_ready.py` | 扫描 HTML/CSS/JS 是否残留 CDN/远程运行依赖 |
| `scripts/check_upstream_locks.py` | 审计吸收来源的 upstream lock 是否仍固定在记录的 commit |
| `scripts/validate_academic_deck.py` | 校验学术 v2 的论证、结果、引用、结论、时间与可访问性契约 |
| `scripts/validate_bento_deck.py` / `create_bento_deck.py` / `extract_bento_comments.py` | 校验、生成与评论回流 `2D-B` 本地 Bento deck |
| `references/integrations/diagram-chart-routing.md` | 数据 / 流程 / 架构 / 时间线转图规则 |
| `references/integrations/local-react-deck-path.md` | 2D / Path E 本地 React Deck |
| `references/integrations/template-fill-pptx.md` | 2A-T 原生 PPTX 模板填充 |
| `references/integrations/presenter-mode.md` | 2D-P HTML 演讲者模式 |
| `references/integrations/bento-deck-adapter.md` | 2D-B 路由、离线边界和工作流 |
| `references/constraints/visual-qa.md` | 2D / Path C/D/E 视觉截图 QA |

---

## 2B-R Reconstruction 示例命令

```powershell
python scripts\figedit_batch.py preflight
python scripts\figedit_batch.py init --project-dir "C:\PPTX\demo" --slides "01.png" "02.png"
python scripts\figedit_batch.py measure --project-dir "C:\PPTX\demo" --ocr-profile v6_medium
# 按 FigEdit 规范逐页编写并审查 manifest.json
python scripts\figedit_batch.py compose --project-dir "C:\PPTX\demo"
python scripts\figedit_batch.py assemble --project-dir "C:\PPTX\demo" --output "C:\PPTX\demo\output\demo-editable.pptx"
```

---

## 参考文件索引

完整索引见 [references/_INDEX.md](references/_INDEX.md)。风格样例图索引见 [references/aesthetics/style-samples.md](references/aesthetics/style-samples.md)。

| 类别 | 目录 | 内容 |
|------|------|------|
| 约束铁律 | `references/constraints/` | 预检 / 节奏 / 反模式 / 质检 / 失败模式 |
| 美学资产 | `references/aesthetics/` | magazine 系统 / AI 风格 / Web 风格 / 模板方法 |
| 技术集成 | `references/integrations/` | 图表路由 / 动画 / TTS / PPTX 导出 / API / Local React Deck |
| 入门文档 | `references/getting-started/` | 快速上手 / 路径选择 |

---

## FAQ

**Q: 用户说"帮我做个 PPT"，怎么办？**
A: 先走 Step 0 意图启动面板，按目标/产物/素材/协作档位给默认推荐。路线码可作为快捷输入，但不要强迫普通用户第一步理解组合码。


**Q: 2A、2B、2C、2D、2B-R 怎么区分？**
A: 2A 是“简易 HTML 转换成可编辑 PPTX”，最稳最好改；2B 是“整页 AI 图 PPTX”，最好看但基本不可编辑；2C 是“整页无正文文字视觉底图 + PPT 原生文本框”，好看且文字能改；2D 是“多功能 HTML 演示”，HTML 是最终作品；2D-B 是“本地可编辑的单文件 Bento deck”；2B-R 是“已有位图经 FigEdit 重建为可编辑 SVG 与原生 PPTX”。

**Q: Path C 生成后样式全塌，怎么回事？**
A: 99% 是发明了种子里没有的 class。运行 [class-preflight.md](references/constraints/class-preflight.md) 的 diff 命令检查。

**Q: 2A / Path A 和 2D / Path C 都用 HTML，区别是什么？**
A: Path A 的 HTML 是 PPTX 中间稿，必须固定 720×405pt、全 absolute，并转成可编辑 PPTX；Path C 的 HTML 是最终网页作品，可以使用浏览器能力，不转 PPTX。

**Q: magazine 种子和 minimal 种子怎么选？**
A: 要 WebGL 动态背景 + 精致排版 → magazine；要轻量快速定制 → minimal。

**Q: Path E 是否等于 Open-Slide？**
A: 不是。Path E 是本地 React/TSX 网页演示路径，吸收固定画布、组件化和截图 QA 方法，但不默认依赖 Open-Slide 或任何外部 slide runtime。

**Q: 模板资产是不是全量内置？**
A: 不是。本阶段内置的是模板方法层：质量基线、页型 archetype 和模板矿化规则。后续如要内置具体模板，必须先做精选、授权、中文适配和 QA。

**Q: guizang 的设计在哪里？**
A: `assets/seeds/path-c-magazine-seed.html` 是 guizang template.html 的 1:1 移植；
`references/aesthetics/magazine/` 是 guizang 的 components + layouts + themes 文档。
