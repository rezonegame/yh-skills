# yh-slides 参考文件索引（_INDEX.md）

> 这是所有 references/ 文件的导航入口。遇到问题时，先查这里找对应文档。

---

## 快速诊断入口

| 问题类型 | 直接跳到 |
|---------|---------|
| 页面样式全塌 / class 找不到 | [constraints/class-preflight.md](constraints/class-preflight.md) |
| 视觉疲劳 / 主题切换不对 | [constraints/theme-rhythm.md](constraints/theme-rhythm.md) |
| 生成翻车 / 不知道怎么排查 | [constraints/failure-modes.md](constraints/failure-modes.md) |
| 命名层级与路径映射 | [getting-started/product-path-taxonomy.md](getting-started/product-path-taxonomy.md) |
| 质量检查交付前必看 | [constraints/quality-checklist.md](constraints/quality-checklist.md) |
| 网页演示截图 QA / contact sheet | [constraints/visual-qa.md](constraints/visual-qa.md) |
| 哪些做法是绝对禁止的 | [constraints/anti-patterns.md](constraints/anti-patterns.md) |
| 不知道选哪条路径 | [getting-started/path-selection.md](getting-started/path-selection.md) |
| 第一次用，想快速上手 | [getting-started/quick-start.md](getting-started/quick-start.md) |
| 数据 / 流程 / 架构不知道该用什么图 | [integrations/diagram-chart-routing.md](integrations/diagram-chart-routing.md) |
| 质量基线 / 页型 archetype / 模板矿化 | [aesthetics/template-methods.md](aesthetics/template-methods.md) |
| Path E 本地 React Deck | [integrations/local-react-deck-path.md](integrations/local-react-deck-path.md) |
| Path S 原生可编辑 PPTX | [integrations/path-s-svg-native-pptx.md](integrations/path-s-svg-native-pptx.md) |
| PPTX 模板填充 | [integrations/template-fill-pptx.md](integrations/template-fill-pptx.md) |
| HTML 演讲者模式 / 逐字稿 | [integrations/presenter-mode.md](integrations/presenter-mode.md) |
| 离线运行 / CDN 扫描 | [constraints/offline-runtime.md](constraints/offline-runtime.md) |
| 本地资产库 | [meta/asset-registry.md](meta/asset-registry.md) |
| 上游来源 / license / commit | [meta/upstreams.md](meta/upstreams.md) |
| 来源与演进原则 | [meta/evolution.md](meta/evolution.md) |
| 资产清单 / 遗留目录状态 | [meta/asset-inventory.md](meta/asset-inventory.md) |

---

## 约束铁律（constraints/）

> 适用所有路径。强制执行，不能绕过。

| 文件 | 内容 |
|------|------|
| [class-preflight.md](constraints/class-preflight.md) | 2D / Path C-D 生成前必做的类名预检（防止"发明 class"翻车） |
| [theme-rhythm.md](constraints/theme-rhythm.md) | 主题节奏规则（light/dark/hero 分布，连续限制，节奏模板） |
| [anti-patterns.md](constraints/anti-patterns.md) | 17 种反模式清单（审美 7 / 技术 5 / 流程 3） |
| [path-a-layout-safety.md](constraints/path-a-layout-safety.md) | Path A 720×405 安全区、文本框内边距与高密度页型 |
| [quality-checklist.md](constraints/quality-checklist.md) | P0-P3 分级质检（5 路径完整版，含自动化脚本） |
| [visual-qa.md](constraints/visual-qa.md) | 2D / Path C-D-E 截图、hash、近空白检测和 contact sheet |
| [comment-iteration-loop.md](constraints/comment-iteration-loop.md) | 成稿后评论归类与轻量迭代闭环 |
| [failure-modes.md](constraints/failure-modes.md) | 20+ 种失败模式 + 症状/根因/修复/预防 |
| [offline-runtime.md](constraints/offline-runtime.md) | 离线核心、线上增强、fallback 和 CDN 扫描规则 |

---

## 美学资产（aesthetics/）

> 设计系统、风格、主题色、布局代码库。

### magazine 子系统（Path C 精品路径）

| 文件 | 内容 |
|------|------|
| [aesthetics/magazine-design-system.md](aesthetics/magazine-design-system.md) | magazine 设计系统总览（guizang 移植说明 + 快速入口） |
| [aesthetics/magazine/directions.md](aesthetics/magazine/directions.md) | 5 个 magazine 方向包（Monocle/WIRED/Kinfolk/Domus/Lab） |
| [aesthetics/magazine/themes.md](aesthetics/magazine/themes.md) | 5 套精品主题色（墨水经典/靛蓝瓷/森林墨/牛皮纸/沙丘） |
| [aesthetics/magazine/layouts.md](aesthetics/magazine/layouts.md) | 10 种预设布局完整 section 代码 |
| [aesthetics/magazine/components.md](aesthetics/magazine/components.md) | 排版组件库（stat/callout/pillar/figure/rowline） |
| [aesthetics/magazine/image-prompts.md](aesthetics/magazine/image-prompts.md) | GPT Image 2 / GPT-M 2.0 配图类型、比例、提示词 |
| [aesthetics/magazine/checklist.md](aesthetics/magazine/checklist.md) | guizang 原版 checklist（P0-P4，magazine 路径专用） |

### PPTX 产物 AI 图片风格

| 文件 | 内容 |
|------|------|
| [aesthetics/proven-styles-gallery.md](aesthetics/proven-styles-gallery.md) | 18+ 种 AI 艺术风格定义（prompt 关键词 + 参考） |
| [aesthetics/proven-styles-snoopy.md](aesthetics/proven-styles-snoopy.md) | Snoopy 线稿风格逐页模板（最稳定） |
| [aesthetics/style-samples.md](aesthetics/style-samples.md) | `assets/style-samples/` 风格样例图索引；用于 Step 4 给用户看例子 |
| [aesthetics/ian-handdrawn-technical.md](aesthetics/ian-handdrawn-technical.md) | Ian 中文手绘技术解释；2B/2C 路由、视觉 DNA、Prompt 与专项 QA |
| [aesthetics/layout-scene-assets.md](aesthetics/layout-scene-assets.md) | `assets/layout-samples/` 与 `assets/scene-templates/` 外部精选资产索引；用于布局、设备 frame、视觉 prompt 参考 |
| [aesthetics/prompt-templates.md](aesthetics/prompt-templates.md) | AI 图片生成 prompt 工程指南（结构/关键词/反例） |
| [aesthetics/style-extraction.md](aesthetics/style-extraction.md) | 从参考图提取风格描述的方法 |
| [aesthetics/screenshot-framing.md](aesthetics/screenshot-framing.md) | 截图保真、美化、比例适配和离线降级规则 |

### 2D / Path C-D-E Web 风格

| 文件 | 内容 |
|------|------|
| [aesthetics/web-styles-gallery.md](aesthetics/web-styles-gallery.md) | 27 种 CSS/Web 风格完整 CSS（直接用于非 magazine 路径） |
| [aesthetics/style-preview-mechanism.md](aesthetics/style-preview-mechanism.md) | 3 选 1 视觉风格预览机制（给用户看样品再定） |

### Swiss 扩展

| 文件 | 内容 |
|------|------|
| [aesthetics/swiss/swiss-map-component.md](aesthetics/swiss/swiss-map-component.md) | S08 地图/点位/路线组件契约；离线 fallback 必须可见 |

## 本地吸收资产库（meta/）

| 文件 | 内容 |
|------|------|
| [meta/upstreams.md](meta/upstreams.md) | 上游仓库、固定 commit、license、provenance 规则 |
| [meta/upgrade-policy.md](meta/upgrade-policy.md) | 离线本地化升级政策；保护强引导流程 |
| [meta/asset-registry.md](meta/asset-registry.md) | `asset-registry.json` 的结构和使用规则 |
| [meta/asset-registry.json](meta/asset-registry.json) | 由 `scripts/build_asset_registry.py` 生成的本地资产索引 |
| [meta/second-pass-upstream-audit.md](meta/second-pass-upstream-audit.md) | 对三个上游素材的二次覆盖审查与结论 |

### 通用设计原则

| 文件 | 内容 |
|------|------|
| [aesthetics/design-principles.md](aesthetics/design-principles.md) | 设计框架、反 AI 审美铁律、品牌定制方法 |
| [aesthetics/design-system-workflow.md](aesthetics/design-system-workflow.md) | 品牌 `DESIGN.md` 生成、提取与映射流程 |
| [aesthetics/design-movements.md](aesthetics/design-movements.md) | 设计运动与风格参考库（Bauhaus / Swiss 等） |
| [aesthetics/template-methods.md](aesthetics/template-methods.md) | 质量基线、页型 archetype、模板矿化规则 |

---

## 种子文件（assets/seeds/）

> 各路径的起点 HTML 文件。**从种子开始，不要从空白开始。**

| 文件 | 路径 | 内容 |
|------|------|------|
| [path-a-seed.html](../assets/seeds/path-a-seed.html) | Path A | 720pt×405pt 骨架 + 全 absolute + 5 页示例 |
| [path-c-magazine-seed.html](../assets/seeds/path-c-magazine-seed.html) | 2D / Path C | guizang 精品模板（WebGL + 5 主题 + 10 布局） |
| [path-c-minimal-seed.html](../assets/seeds/path-c-minimal-seed.html) | 2D / Path C | 极简模板（轻量，无 WebGL，7 页示例） |
| [path-d-animated-seed.html](../assets/seeds/path-d-animated-seed.html) | 2D / Path D | GSAP + TTS 骨架（data-anim 系统 + 进度条） |

---

## 入门文档（getting-started/）

| 文件 | 内容 |
|------|------|
| [getting-started/quick-start.md](getting-started/quick-start.md) | 5 分钟快速上手（3 个最常见场景的完整命令） |
| [getting-started/path-selection.md](getting-started/path-selection.md) | 路径选择决策树（协作模式 + 需求字段 → 推荐路径） |

---

## 技术集成（integrations/）

> 具体工具、脚本、格式的深度技术指南。

| 文件 | 内容 | 路径 |
|------|------|------|
| [integrations/figedit-reconstruction.md](integrations/figedit-reconstruction.md) | 位图 → FigEdit 可编辑 SVG/PPTX 批处理与质量门 | 2B-R |
| [integrations/image-backend-policy.md](integrations/image-backend-policy.md) | 原生生图优先 / API fallback 策略 | 2A, 2B, 2C, 2D |
| [integrations/open-design-metadata.md](integrations/open-design-metadata.md) | Open Design 兼容元数据（不放入 SKILL.md frontmatter） | 全部 |
| [integrations/diagram-chart-routing.md](integrations/diagram-chart-routing.md) | 数据图表 / 流程图 / 架构图 / 时间线选择规则 | 2A, 2D |
| [integrations/slide-structure-reference.md](integrations/slide-structure-reference.md) | 幻灯片类型模板（布局 + HTML 结构） | 2D / Path C-D |
| [integrations/viewport-fitting-spec.md](integrations/viewport-fitting-spec.md) | 视口适配规范（每页精确填充） | 2D / Path C-D |
| [integrations/slide-presentation-js.md](integrations/slide-presentation-js.md) | Scroll-snap + IntersectionObserver 导航控制器 | 2D / Path C |
| [integrations/animation-guide.md](integrations/animation-guide.md) | GSAP 翻页动画 + CSS 原生动画完整指南 | 2D / Path D |
| [integrations/tts-configuration.md](integrations/tts-configuration.md) | TTS 配音设置（生成/同步/音量） | 2D / Path D |
| [integrations/api-configuration.md](integrations/api-configuration.md) | Unsplash / AI API 配置 | 全部 |
| [integrations/import-guide.md](integrations/import-guide.md) | 网页/视频/音频导入指南 | 全部 |
| [integrations/ppt-conversion-guide.md](integrations/ppt-conversion-guide.md) | PPT/PPTX 转换指南 | 全部 |
| [integrations/local-react-deck-path.md](integrations/local-react-deck-path.md) | 本地 React/TSX 网页演示路径 | 2D / Path E |

---

## 路径指南（paths/）

> 每条路径的完整工作流深度指南（详细版 SKILL.md）。

| 文件 | 内容 |
|------|------|
| [paths/path-workflows.md](paths/path-workflows.md) | Path A/B/H/C/D/E 构建细节与组装命令 |

---

## 脚本参考（scripts/）

> Python/Node 脚本的完整 CLI 参考。

| 文件 | 内容 |
|------|------|
| `scripts/generate_image.py` | 脚本 API 生图 fallback（Gemini / Imagen） |
| `scripts/create_slides.py` | 2B / Path B 图片型 PPTX 组装 |
| `scripts/create_contact_sheet.py` | 按自然序生成带标签联系表，并报告近空白页与重复图片 |
| `scripts/figedit_batch.py` | 2B-R FigEdit 预检、批处理、质量门和整套 PPTX 汇集 |
| `scripts/html2pptx.js` | Path A HTML → 可编辑 PPTX 转换 |

---

## 共享配置（../.yh-skills/）

真实 API key 不放在 `yh-slides` 技能目录。复制到其他 CLI 时，可在 skills 根目录创建 `.yh-skills/.env`；当前技能目录只保留 `.env.example`。

---

## 目录结构全景

```
yh-slides/
├── SKILL.md                          ← 主入口（完整工作流）
├── README.md                         ← 项目说明
├── .env.example                      ← API fallback 配置占位；不含真实密钥
│
├── agents/
│   └── openai.yaml                   ← UI 元数据
│
├── assets/
│   ├── seeds/                        ← 4 个种子文件
│   ├── vendor/                       ← 本地字体、Lucide、GSAP、Motion 等运行资源
│   ├── placeholders/                 ← 本地占位图资源
│   ├── style-samples/                ← 风格样例与 Ian 手绘视觉锚点；索引见 references/aesthetics/style-samples.md
│   ├── layout-samples/               ← 图表布局、主题、设计系统样例；索引见 references/aesthetics/layout-scene-assets.md
│   ├── scene-templates/              ← 设备 frame、prompt gallery；索引见 references/aesthetics/layout-scene-assets.md
│   └── external-licenses/            ← 外部精选资产许可证快照
│
└── references/
    ├── _INDEX.md                     ← 本文件（导航入口）
    ├── constraints/                  ← 约束铁律（7+ 文件）
    ├── aesthetics/                   ← 美学资产（10+ 文件）
    │   └── magazine/                 ← guizang 精品子系统（7 文件）
    ├── getting-started/              ← 入门文档
    ├── integrations/                 ← 技术集成（12 文件）
    ├── paths/                        ← 路径深度指南
    ├── meta/                         ← 来源、演进记录和资产清单
    └── scripts/                      ← 脚本参考
```
