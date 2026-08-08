---
name: yh-slides
description: >
  从内容到演示文稿的端到端制作。支持 PPTX、HTML 与本地 React Deck 输出、AI 插画生成、
  多种视觉风格、TTS 配音、网页/视频/音频导入、PPT 转换，以及通过独立 FigEdit
  将位图幻灯片、截图、论文图和架构图重建为可编辑 SVG/PPTX。
  当用户提到"做PPT""做幻灯片""演示文稿""slides""HTML presentation""deck""keynote""做个报告""位图重建""截图转可编辑PPT"时使用。
---
# AI Presentation Workflow
用于从主题、文档、网页或媒体素材生成演示文稿。默认先理解用户意图，再映射到用户侧产物选项和内部执行路径；路线码仍可作为快捷输入和内部记录。
除非另有说明，所有脚本命令都假设当前工作目录是 `yh-slides` 技能根目录；复制到其他 CLI 时保持 `scripts/`、`references/`、`assets/` 的相对结构即可。API fallback 配置仅从运行环境变量或显式指定的 `YH_SKILLS_ENV_FILE` 读取；不要把真实 `.env` 放进本技能目录，也不要依赖父目录扫描。
命名层级：`2A/2B/2C/2D` 是用户侧产物选项；`Path A/B/H/C/D/E` 是内部执行路径。详细映射见 `references/getting-started/product-path-taxonomy.md`。
| 用户侧产物选项 | 内部执行路径 | 工作方式 | 适用场景 |
|---|---|---|---|
| `2A 通用可编辑 PPTX（简易 HTML 转换）` | `Path A` | 用受限 HTML/CSS 做 PPTX 中间稿；PPT 原生文字、形状、图表和版式为主，可加入局部插画/照片；最终经 `html2pptx` 输出可编辑 PPTX | 正式汇报、企业演示、需要稳定后期修改 |
| `2A-S 高保真原生可编辑 PPTX（SVG → DrawingML）` | `Path S` | 逐页 SVG 作为严谨视觉源，经本地 DrawingML 导出为原生可编辑 PPTX；支持复杂图表、图标、形状、备注与动画 sidecar | 咨询级图表、复杂信息图、强原生可编辑、避免 HTML 转换偏移 |
| `2A-T 原生 PPTX 模板填充` | `Template Fill` | 复用用户提供的 PPTX 模板页库，分析可替换槽位，选择/重排/复用原生页面并替换文字、表格、图表 | 已有公司模板、想保留原设计、只换内容和数据 |
| `2B 整图视觉 PPTX` | `Path B` | 每页一张完整 AI 图，文字也可在图里；最终组装为图片型 PPTX | 最强视觉冲击、接近样张、不需要改字 |
| `2C 视觉底图 + 可编辑文字 PPTX` | `Path H` | AI 生成无正文文字的整页视觉底图，PPT 原生文本框叠加标题、正文、互动题和答案 | 想要好看，同时课堂/汇报文字可编辑 |
| `2D 多功能 HTML 演示` | `Path C / D / E` | HTML 是最终作品：单文件网页、动画/TTS 或本地 React Deck | 网页分享、配音动画、长期维护或复杂交互 |
| `2D-B Bento Deck` | `Bento Adapter` | 本地单文件、浏览器可编辑的 `.bento.html`，含 notes、评论、状态和 morph | 无安装编辑、离线审阅、对象状态/转场；不承诺 PPTX |
| `2D-P HTML 演讲者模式` | `Presenter Mode` | 本地 HTML 演示 + hidden notes + S 键演讲者窗口，含当前页、下一页、逐字稿、计时器和双窗口同步 | 演讲、技术分享、培训、路演、需要提词器或 speaker notes |
| `2B-R 可编辑重建` | `FigEdit Reconstruction` | 已有位图 → OCR/CV 测量 → Agent 语义拆解 → 可编辑 SVG → 原生 DrawingML PPTX | 位图幻灯片、截图、论文图、架构图需要恢复可编辑结构 |
---

## 全局生图后端策略（所有路径通用）

默认采用 `auto-runtime`：**当前对话模型 / Agent Runtime 原生生图能力优先，API 后端只做备用**。

- 用户明确指定 `gemini` / `imagen` / `API` 时，按用户指定执行。
- 用户未指定时，只要当前环境暴露原生生图工具，就优先使用原生工具，并把图片保存到项目目录。
- 不要因为技能目录里有 `scripts/generate_image.py` 就默认调用 API；该脚本是 fallback，不是默认入口。
- 只有当前环境没有原生生图工具、原生工具无法稳定落盘、或原生工具明确失败且任务仍需继续时，才使用环境变量或显式 `YH_SKILLS_ENV_FILE` 中的 API key 调用 `scripts/generate_image.py`。
- 详细规则见 `references/integrations/image-backend-policy.md`。

---

## Step 0: 意图启动面板（先于一切制作）

**不要直接跳入生成。** `yh-slides` 默认先理解用户意图，再给出推荐产物和内部路径；`1B + 2A + 3B` 这类路线码仍可直接解析，但不再强迫普通用户第一步理解组合码。

读取 `references/quickstart-panel.md` 获取用户侧启动面板、路线码映射、默认推荐、启发式选择规则和协作档位。执行时只保留这些不变量：已明确的信息不重复问；缺失项按任务推荐补齐并允许纠偏；“直接做”仍需记录路线与风险；关键选择给推荐、备选、自定义入口和代价；所有档位至少通过对应 P0/P1 门。

---

## Step 1: 需求发现与方向锁定（先于技术启动）

**正向制作不要跳过这一步。** 没搞清楚受众、目标和视觉方向，后面生成的内容大概率不符合需求，来回返工 2-3 轮。`2B-R` 已有明确视觉源，只确认页序、重建范围、必须可编辑的对象、允许保留为图片的对象和交付格式，然后直接进入 FigEdit 预检。

按 Step 0 的启动面板或路线码补齐需求字段；用户已明确回答的字段不要重复问。已由产物选项确认的内容不要重复询问，例如 `2A` 已代表通用可编辑 PPTX（简易 HTML 转换），`2C` 已代表视觉底图 + 可编辑文字，`2D` 已代表多功能 HTML 演示，`3B` 已代表课程化重构。

| 协作码 | 问法 |
|---|---|
| `1A` 全自动 | 只问缺失且会明显影响结果的 1-3 个问题，其余写明默认判断 |
| `1B` 引导式 | 一次补齐关键字段，并为每项给推荐值 |
| `1C` 一步一步 | 分阶段问，每次只问当前阶段必要问题 |
| `1D` 自定义 | 按用户指定的确认范围来问 |

启动判断后只补齐 6 类关键信息：受众、时长/页数、素材准备程度、品牌与硬约束、图片策略、项目名。每项都给推荐值和备选项；已由用户或路线码明确的信息不要重复问。

### Step 1-A: 方向选择（Path C magazine 强制，其他路径推荐）

如果用户选择或你推荐 `Path C magazine`，先读取 `references/aesthetics/magazine/directions.md`，让用户在 5 个方向包里选一个：

1. Monocle Editorial · 国际杂志风（默认兜底）
2. WIRED Tech · 数据 + 工程
3. Kinfolk Slow · 慢生活 / 人文
4. Domus Architectural · 建筑 / 空间感
5. Lab / Reference · 学术 + 工艺手册

**规则**：
- 如果用户说“不知道，你推荐”，默认 Monocle；技术/benchmark/AI 产品偏 WIRED；读书/人物/私享偏 Kinfolk；设计/建筑/portfolio 偏 Domus；研究/方法论/教程偏 Lab。
- 方向一旦确认，要写入项目记录或大纲顶部；中途不要混搭多个方向。
- 方向包会同时决定主题色、主力 layout、chrome/kicker/foot 的语气和推荐页数范围。

### Step 1-B: 主题提取 / 复用（可选但重要）

如果用户提供品牌规范、参考网站、截图、公司模板、旧 PPT、参考图或本地模板方向，先走 `references/aesthetics/design-system-workflow.md`，并把 `DESIGN.md` 从“品牌记录”扩展为“项目主题包”：

- 创建或读取项目目录下的 `DESIGN.md`
- 提取真实颜色、字体、布局姿态、图片策略、页型偏好和禁忌
- 记录 `palette`、`type scale`、`layout rhythm`、`image strategy`、`page archetypes`、`avoid list`
- 用一句话复述将采用的设计系统，等用户有机会纠偏
- 再进入路径选择和内容结构化

如果没有可提取材料，不要为了主题包额外打断用户；按当前任务的受众、路径和内容策略生成默认主题判断，并在 Step 4 的风格推荐中说明。

### Step 1-C: 材料与事实缺口核查（可选但重要）

如果主题涉及品牌、产品、公司、当前事实或数据，不要把缺失信息直接脑补进 PPT：

- 品牌 / 产品 / 公司：优先确认 logo、品牌色、指定字体、产品图、官网截图、UI 截图、旧版 PPT 或设计规范。
- 品牌 / 产品 / 公司资产是硬门槛：只要设计里出现真实可识别的品牌或产品名，就必须取到对应 logo；实体产品还要产品图，数字产品还要 UI 截图。对比、榜单、评测、介绍型 deck 中出现多个品牌时，逐个列清单并补齐 logo，不能只抽品牌色后开做。完整流程见 `references/brand-asset-protocol.md`。
- 当前事实 / 数据 / 人物 / 公司状态：要求用户提供来源，或明确需要联网核查；高变化信息必须核实日期和来源。
- 缺失材料一次性整理为 gap list，集中问一次；不要每页制作时反复打断用户。
- 如果用户要求快速草稿但材料缺失，在大纲顶部标注“待替换素材 / 待核查数据”，后续不得把占位内容当成事实。
- 如果 logo 或关键资产暂时取不到，停下说明缺口并使用诚实 placeholder；不要用手画 SVG、CSS 剪影或通用图标假装官方资产。

当输入是长 PDF、报告或多来源证据包时，读取 `references/evidence-driven-methodology.md`，先建立 Source Inventory 和 slide-to-source register，再写 storyline。可用 `scripts/pdf_evidence_pipeline.py` 生成可复核的中间材料；它只辅助提取与登记，不替代事实核查。

**根据答案校准路线**：如果补充信息与 Step 0 路线冲突，要提醒用户并建议调整组合码，而不是静默覆盖。

| 答案组合 | 推荐路径 |
|---------|---------|
| 需要可编辑文字 + 企业正式 | 建议 `2A` / Path A |
| 要最强视觉冲击 + 不需要改字 | 建议 `2B` / Path B |
| 要强视觉且文字可改 | 建议 `2C` / Path H |
| 网页分享 + 零依赖 + 杂志质感 | 建议 `2D`，内部走 Path C（magazine 精品网页） |
| 网页分享 + 零依赖 + 轻量定制 | 建议 `2D`，内部走 Path C（轻量单文件网页） |
| 含动画 + 含配音 / TTS | 建议 `2D`，内部走 Path D |
| 网页演示 + 长期维护 + 复杂交互 / 静态部署 | 建议 `2D`，内部走 Path E |

---

## Step 2: 技术启动（基于 Step 1 的最小化问句）

Step 1 确认完毕后，按路线码对应路径只问必要的技术细节。路线码已经在 Step 0 确认过，不要在这里重复询问，除非用户要求变更。

### 路径最小化确认项

| 路径 | 只补齐这些技术问题 |
|---|---|
| `2A / Path A` | 是否需要局部 AI 插画或照片；项目名；标准制作下建议先做 1-2 页样稿，精品交付强制 |
| `2A-S / Path S` | 是否需要复杂图表/原生形状/动画/备注；是否接受逐页 SVG 质量门；项目名；标准制作建议先做 1-2 页 SVG 样稿，精品交付强制 |
| `2A-T / Template Fill` | 已有 PPTX 模板路径；新内容来源；是否允许重排/复用/删除模板页；是否需要备注；建议先用 2-3 页验证填充质量 |
| `2B / Path B` | 图片尺寸 1K/2K/4K；是否允许图片内文字；项目名；标准制作/精品交付强制先做 1 页样稿 |
| `2C / Path H` | 是否需要整页视觉底图；哪些文字必须由 PPT 文本框承担；底图是否必须无标题/正文/题目/答案文字；标准制作/精品交付强制先做 1-2 页样稿 |
| `2B-R / FigEdit` | 位图来源与页序；哪些元素必须原生可编辑；哪些照片、Logo、截图、地图或复杂图表允许保留为可替换图片；建议先用 1 页验证重建质量 |
| `2D / Path C` | 单文件网页演示；magazine 精品网页或 minimal 轻量网页；项目名；标准制作/精品交付强制先做 1-2 页样稿或首屏预览 |
| `2D-P / Presenter Mode` | 演讲时长；每页 notes 粒度；是否需要逐字稿/提示信号/计时器；项目名；标准制作/精品交付强制先做 1-2 页 presenter 样稿 |
| `2D / Path D` | 是否启用 TTS；动画风格；项目名；标准制作/精品交付强制先做 1-2 页动效样稿 |
| `2D / Path E` | 是否需要复杂交互/复用组件；是否接受本地前端工程；标准制作/精品交付强制先做 2-3 页静态样稿并截图检查 |
| `2D-B / Bento Adapter` | 是否必须单文件/离线；是否需要浏览器编辑、notes、评论、状态/morph；是否明确接受协作链接的访问风险；标准制作/精品交付强制先做 2 页样稿 |

Path E 默认不依赖 `@open-slide/core`、Open-Slide CLI 或外部 runtime。它只吸收固定 1920×1080 画布、React/TSX 组件化、静态导出和截图 QA 的方法；如果未来用户明确要求兼容 Open-Slide，应作为单独适配决策，而不是默认路径。

`2D-B` 使用固定的本地 Bento shell，不是 Path E 的替代品。只有用户明确需要“可编辑单文件 / 评论回流 / 状态或 morph”时才读取 `references/integrations/bento-deck-adapter.md` 与 `references/contracts/bento-deck.md`；不要在线更新 shell、引入 CDN/分析脚本或默认启用协作。

Path S、Template Fill、Presenter Mode 的详细本地离线规范分别见：

- `references/integrations/path-s-svg-native-pptx.md`
- `references/integrations/template-fill-pptx.md`
- `references/integrations/presenter-mode.md`

本地模板/主题/布局/图标/运行时资产统一通过 `references/meta/asset-registry.json` 发现。默认只推荐 2-3 个最匹配资产；只有用户明确要求“查看全部模板 / 全部主题 / 全部资产库”时，才读取完整索引并展开列表。模板资产不得绕过 Step 0 意图启动、Step 3 大纲确认、Step 4 风格确认、样稿 checkpoint 和 Step 7 QA。

### 如果用户只说"帮我做个 PPT"

先走 Step 0 的意图启动面板，按默认推荐策略给出产物建议；如果用户要 magazine 质感，进入 Step 4 的风格选择；如果有品牌资料，先建 `DESIGN.md`。再基于答案推荐并确认路径。**禁止直接跳入生成。**

### 技术配置细则

**2-A. 输入来源**（若未在 Step 1 明确）：从零创建 / PPT 转换 / 网页导入 / 视频音频导入

**2-B. `2B-R / FigEdit Reconstruction` 说明**：这是正式的位图逆向重建入口，不是 2C，也不依赖 2B 先生成。它调用独立 FigEdit，把普通文字、稳定几何、连接线和公式恢复为可编辑对象，把照片、Logo、截图、地图、复杂图表等保留为可替换图片资产。详细流程见 `references/integrations/figedit-reconstruction.md`。

**2-C. 图片尺寸**（有 AI 图片时）：推荐顺序 2K > 1K > 4K（仅强打印需求）

**2-C-2. 图片后端策略**（有 AI 图片时）：遵守全局生图后端策略。默认优先使用当前对话模型 / agent runtime 原生生图工具；只有用户显式指定 API、原生工具不可用、无法稳定落盘或明确失败时，才使用 `scripts/generate_image.py` API fallback。详细规则见 `references/integrations/image-backend-policy.md`。

**2-D. 项目目录**（确认后自动创建）：
```
C:\PPTX\{项目名}\
├── images\
├── slides\
├── output\
├── DESIGN.md          # 可选：品牌 / 项目设计系统
├── 项目记录.md        # 推荐：方向、受众、页数、主题节奏
└── tasks.json
```

Path E 可在项目目录下增加 `react-deck\` 或等价工程目录；不要改写全局包配置，除非用户明确要求创建独立前端项目。

---

## Step 3: 内容结构化

将原始素材整理为逐页大纲。先确认内容策略，再生成每页标题、要点和视觉意图。

`2B-R` 不执行本步骤：它忠实重建现有位图，不重写内容结构，除非用户明确要求同时改稿或重新设计。

### Step 3-A: 内容策略选择（先推荐，后确认）

内容策略原则上已在 Step 0 通过 `3A-3D` 确认；在正式拆页前，只需要复述将采用的策略和风险。只有当用户没有给出第 3 类选择、或补充信息显示原选择明显不匹配时，才重新给出本节选项。

| 策略 | 适合 | 风险 |
|---|---|---|
| `3A 忠实整理` | 已写好的报告、正式材料、不能大改原意 | 可能像文档摘要，演示张力弱 |
| `3B 课程化重构` | 教学、培训、工作坊、带练习 | 会主动调整顺序和措辞 |
| `3C 演讲叙事版` | 读书分享、主题演讲、观点传播 | 可能减少信息密度或强化主观表达 |
| `3D 任务互动版` | 课堂活动、工作坊、训练营、讨论课 | 知识讲解会被拆成任务和答案揭示 |

示例：

```text
你选择的是 3B「课程化重构」：这份材料有概念、机制和练习边界，适合做成可讲可练的课件。

如果你想调整，也可以改为：
3A 忠实整理：更贴近原文，风险是像摘要
3C 演讲叙事版：更有观看张力，风险是细节变少
3D 任务互动版：互动更多，风险是讲解会被拆散
```

### Step 3-B: 逐页大纲

如果任务是研究答辩、论文、研讨会、基金简报、实验室汇报或其他证据驱动演讲，先读取 `references/getting-started/academic-presentation-workflow.md`，在普通逐页大纲之外确定 `structured_argument` / `visual_narrative`、叙事 spine、单一主张、研究问题、时间预算与引用策略。该层只约束学术沟通，不新增产物路径。

每页都要有：

- `Title`: 完整论断句 / 结论型标题（不是主题词）
- `Key points`: 最多 3-4 条
- `Visual type`: 描述视觉意图
- Path A → 是否需要插画
- Path B → 完整视觉场景描述（用于 prompt）
- 2D / Path C-D → 布局类型（参考种子文件的组件）

如果输入包含数据、系统关系、流程、时间线、组织结构或多方案比较，先读取 `references/integrations/diagram-chart-routing.md` 判断是否应转为图表 / 示意图；不要把所有信息都做成普通文本页。

**原则**：
- 一页一个核心观点；正文默认中文；只保留必要英文术语；不写"通用商务废话"。
- 每页正文控制在 20-40 词或等量中文信息量；超过就拆页或改成图表 / 结构图。
- 标题串起来应该能讲完整故事；如果只读标题看不出逻辑线，重写大纲。
- 每 3-4 页安排一次明确的 "so what / 对听众意味着什么"，避免只有信息堆叠没有判断。

### Step 3-C: 页型覆盖检查（Checkpoint 1 前强制）

在把大纲交给用户确认前，先读取 `references/aesthetics/template-methods.md` 的页型 archetype 章节，检查这份 deck 是否过度 bullet 化。

- 不强制 20 页结构；按项目页数、受众和叙事需要选择页型。
- 常用页型包括 Cover、Agenda、Problem / Context、Framework、Metrics / Data、Timeline / Roadmap、Diagram / Architecture、Quote / Key Insight、Comparison、Process / Workflow、Risks / Tradeoffs、FAQ / Appendix、Closing / CTA。
- 如果连续多页都是“标题 + 3 条 bullet”，优先改为图表页、流程页、对比页、案例页、转场页或总结页。
- 页型检查结果应写在大纲顶部或每页 `Visual type` 中，方便后续 Step 4/5 映射到设计与构建。
- 重要页面存在多个模板候选时，读取 `references/aesthetics/content-layout-candidates.md`：先冻结本页事实、数字、引用和受众行动，再按容量与结构家族比较候选；不得让换版式改写事实，候选不足以容纳必需内容时直接淘汰。

✅ **Checkpoint 1**：大纲给用户确认后再进入 Step 4。

---

## Step 4: 风格选择与设计系统

风格在 Step 0 的路线确认之后选择。默认不要一上来展开完整风格库；先根据路线码、主题、受众、内容策略和产物路径给出 **3 个最适合的风格方向 + `D. 打开风格库`**。只有用户选择 `D`、说“查看更多风格 / 打开风格库 / 还有哪些风格”，才分级展开风格库。

`2B-R` 不重新选择风格：以源图为视觉事实，只记录字体回退、颜色、裁切资产和可编辑性取舍。用户明确要求重新设计时，应改走 `2A-S`、`2C` 或新的正向制作任务。

如果 Step 1 已经锁定 magazine 方向、品牌规范或 `DESIGN.md`，这里不要重新发明风格；只做 3 个**同一方向内的版式/密度/图片策略变体**。例如 Monocle 已确认时，可以给“更数据密 / 更故事化 / 更图片主导”三种，而不是再给 WIRED/Kinfolk/Domus 混搭。

### Step 4-0: 质量基线判断（内部先做，必要时再问）

在展示风格选择面板前，先读取 `references/aesthetics/template-methods.md`，内部判断本项目应对齐哪类高质量演示基线：

- 产品发布型
- 技术解释型
- 知识课程型
- 工作流演示型
- 强视觉叙事型
- 商业汇报型

这一步不要默认变成新的用户问卷。只有用户目标模糊、多个基线冲突且会明显影响成品时，才按 Step 0-D 的“推荐项 / 备选项 / 自定义入口 / 风险提示”询问。通常只需在 Step 4-A 的推荐理由中写明“本次按某某基线判断”。

**PPTX 产物（2A/2B/2C）** — 可参考：
- `references/aesthetics/proven-styles-gallery.md` — 18+ 种 AI 艺术风格
- `references/aesthetics/style-samples.md` — `assets/style-samples/` 风格样例图索引；用户要看例子时优先展示 3 张候选样例
- `references/aesthetics/layout-scene-assets.md` — `assets/layout-samples/` 与 `assets/scene-templates/` 的使用索引；需要布局样例、设备 frame、视觉 prompt 参考时读取
- `references/aesthetics/proven-styles-snoopy.md` — Snoopy 风格完整模板
- `references/aesthetics/design-movements.md` — 设计运动风格参考

**HTML 产物（2D / Path C-D-E）** — 可参考：
- `references/aesthetics/magazine/directions.md` — 5 个 magazine 方向包（Path C magazine 首选）
- `references/aesthetics/magazine/themes.md` — 5 套精品主题色（magazine 路径首选）
- `references/aesthetics/web-styles-gallery.md` — 27 种 CSS/Web 风格完整 CSS
- `references/aesthetics/magazine-design-system.md` — magazine 设计系统总览
- `references/aesthetics/design-system-workflow.md` — 品牌 `DESIGN.md` 生成 / 映射流程
- `references/aesthetics/template-methods.md` — 质量基线、页型 archetype、模板矿化规则

**Path E / Local React Deck** — 必须参考：
- `references/integrations/local-react-deck-path.md` — 固定画布、本地 React/TSX 工程、静态导出和截图 QA
- `references/aesthetics/template-methods.md` — 本地模板方法层和页型映射

如果用户上传参考图：
```bash
python scripts/generate_image.py extract-style --image ref.png
```

### Step 4-A: 风格选择面板（强制）

用户确认路线后，必须先给 3 个推荐风格和 `D. 打开风格库`。三个推荐要与产物路径匹配：`2A` 优先可编辑和可维护，`2B` 可更大胆整图化，`2C` 必须考虑背景留白和中文可读性，`2D` 必须考虑网页布局和动效。

```text
第二步：选择视觉风格

A. 风格名 — 适合 / 优点 / 风险 / 可自定义方向
B. 风格名（推荐）— 适合 / 优点 / 风险 / 推荐理由
C. 风格名 — 适合 / 优点 / 风险 / 可自定义方向
D. 打开风格库
```

推荐时直接给出选择建议；用户可说“B 但更克制 / A 加一点杂志感 / 打开风格库 / 上传参考图”继续校准。

每个推荐方向都必须包含：设计哲学或一句话定位、视觉语言、图片策略、适合原因、风险提示和自定义入口。不要把“黑白极简 / 科技蓝 / 温暖橙”这类色板当作设计系统；设计系统必须说明构图、字体层级、图片使用方式和情绪意图。

### Step 4-A-2: 模板矿化规则（使用本地模板时强制）

如果使用本技能内的模板、页型或风格参考，不要原样搬运整套 runtime。按 `references/aesthetics/template-methods.md` 的模板矿化流程，只抽取：

- palette
- typography / type scale
- spacing
- cards / panels
- diagrams
- layout rhythm
- page archetype

禁止搬入第三方品牌、远程资源、外部导航脚本、外部 runtime 或未说明来源的素材。提取结果写入 `DESIGN.md` 或大纲顶部，并明确映射到当前产物和内部路径，例如 `2A / Path A`、`2D / Path C`、`2D / Path D` 或 `2D / Path E`。

### Step 4-B: 风格库分级展开（用户选择 D 时）

用户选择 `D` 或请求查看更多时，只展示风格大类，不一次性列出几十种风格。先给 `D1 教学课件类`、`D2 杂志出版类`、`D3 商业汇报类`、`D4 插画视觉类`、`D5 学术手册类`、`D6 网页互动类` 六类；用户选中大类后，再读取对应 reference 展开具体风格。若用户说“看看例子 / 给我看图 / 不确定风格”，读取 `references/aesthetics/style-samples.md`，从 `assets/style-samples/` 中展示 3 张最匹配样例图；不要一次展示全部样例。若用户说“版式参考 / 设备展示 / 场景底图 / prompt 参考 / 分镜”，读取 `references/aesthetics/layout-scene-assets.md`，再按需读取 `assets/layout-samples/` 或 `assets/scene-templates/` 的对应子目录。

- 2A/2B/2C：读取 `references/aesthetics/proven-styles-gallery.md`、`references/aesthetics/style-samples.md`、`references/aesthetics/proven-styles-snoopy.md`、`references/aesthetics/design-movements.md`
- 用户点名 Ian 手绘，或技术解释/教学内容需要克制的中文手绘语义图时：读取 `references/aesthetics/ian-handdrawn-technical.md`；只把它作为 2B/2C 候选，不自动选中
- 用户点名王虹、Notability、数学学术报告或中文手写网页 PPT 时：读取 `references/aesthetics/wanghong-handwritten.md`，从 `assets/wanghong/deck-template.html` 起步；需要时间轴动画版时使用 `scripts/build_timeline.py`
- 用户希望从大量本地版式中挑选时：读取 `templates/tosea/metadata.json`，按类别检索本地预览目录；只展示最匹配的 3 套，不一次加载整个库。维护时用 `scripts/build_tosea_metadata.py` 从实际目录重建索引
- 2D / Path C-D：读取 `references/aesthetics/magazine/directions.md`、`references/aesthetics/web-styles-gallery.md`、`references/aesthetics/style-preview-mechanism.md`
- 2D / Path E：读取 `references/integrations/local-react-deck-path.md` 和 `references/aesthetics/template-methods.md`
- 2D-B / Bento Adapter：读取 `references/integrations/bento-deck-adapter.md` 和 `references/contracts/bento-deck.md`

展开时仍遵守 Step 0-D：每个方向都要有推荐理由、风险提示和自定义入口。

### Step 4-C: 风格样张 / 样稿策略

样稿不是所有场景一刀切强制，但高视觉和高风险路径必须先校准。样张应使用同一页内容，避免内容差异干扰审美判断。

- 快速草稿档：默认不强制样稿；但 2B/2C 建议至少先做 1 页。
- 标准制作档：2A 样稿建议；2B、2C、2D（Path C magazine / Path D / Path E）强制先做样稿或首屏/动效原型。
- `2D-B` 同样强制先做 2 页样稿；只在状态/morph 服务叙事时使用，保持单一作者的统一写作与视觉声音。
- 精品交付档：所有路径强制样稿。
- 用户提供参考图、品牌规范、旧 PPT 或项目视觉风险高时：强制样稿校准方向。

```text
我可以先用同一页内容做 3 张小样，或先展示 3 张本地风格样例图：
1. 清线漫画教学风 — `assets/style-samples/slide04-ligne-claire.png`
2. xkcd 白板手绘风 — `assets/style-samples/slide04-xkcd.png`
3. 温暖叙事插画风 — `assets/style-samples/slide04-13-温暖叙事-warm-narrative.png`

你看图选最终方向后，我再做 1-2 页真实样稿。
```

### Step 4-A-3: 本地资产库推荐层（按需）

来自 `ppt-master`、`guizang-ppt-skill`、`html-ppt-skill` 的可用资产已吸收到 `templates/`、`assets/`、`scripts/` 和 `references/provenance/`，供离线调用。它们现在是 `yh-slides` 的本地原生资产库，不是新的默认入口。

使用规则：

- 先完成 Step 0-3，再根据产物路径、受众和内容形状推荐资产。
- 默认读取 `references/meta/asset-registry.json`，只展示 2-3 个强推荐资产。
- 不要让用户一开始浏览全量模板库，除非用户明确要求。
- 有品牌资料或旧 PPT 时，先尊重 `DESIGN.md` / 原模板，再选择本地资产。
- AGPL 来源资产必须保留 provenance；不要把 `guizang-ppt-skill` 代码粘进未标来源的新文件。

推荐映射：

| 场景 | 优先路径 | 推荐资产来源 |
|---|---|---|
| 复杂图表 / 原生可编辑 / 咨询级结构 | `2A-S` | `ppt-master` charts、icons、layout templates |
| 已有 PPTX 公司模板复用 | `2A-T` | `ppt-master` template-fill workflow/scripts |
| 人文观点 / 杂志质感分享 | `2D / Path C` | `guizang-ppt-skill` magazine seed/layouts/themes |
| 数据 / 产品 / 工程 / 瑞士网格 | `2D / Path C` 或 `2A-S` | `guizang-ppt-skill` Swiss assets；必要时 Path S charts |
| 技术分享 / 需要逐字稿 / presenter | `2D-P` | `html-ppt-skill` presenter template/runtime |
| 多主题 HTML deck / 小红书图文 / 动效展示 | `2D / Path C-D` | `html-ppt-skill` themes/layouts/animations |

✅ **Checkpoint 2**：设计方向确认后再进入 Step 5。

---

## Step 5: 构建幻灯片

### Step 5-Pre: 按最终产物直接构建

不要强制所有演示先做 HTML。根据 Step 0 已确认的产物选择独立构建路径：

- `2A`：受限 HTML 只作为 PPTX 中间稿。
- `2A-S`：逐页 SVG 直接转换为 DrawingML。
- `2A-T`：直接分析、克隆并填充用户 PPTX 模板。
- `2B`：直接生成整页视觉图片并组装图片型 PPTX。
- `2C`：生成无正文文字底图并叠加原生 PPT 文本框。
- `2B-R`：调用独立 FigEdit 做位图逆向重建。
- `2D`：HTML 是最终作品，可继续派生 PDF。

只有 `2D` 或用户明确要求 HTML 聚合预览时，才读取 `references/slide-decks.md` 并使用 HTML deck、缩略图和 HTML→PDF 工具。

### Step 5.0: 构建前预检（Path C / D / E 强制）

在写任何 HTML / React slide 代码前，先执行对应预检，不要凭记忆发明 class、动效标记或主题节奏：

- `Path C / D`：读取 `references/constraints/class-preflight.md`，对照种子 `<style>` 块列出并验证本次要用的所有 class。
- `Path C magazine`：同时检查 `data-anim` / `data-animate` 动效标记，关键语义块不能漏标。
- `Path C / D / E`：读取 `references/constraints/theme-rhythm.md`，先画主题节奏表；不允许连续 3 页同主题，8 页以上必须同时有 `hero-dark` 和 `hero-light`。

这些预检失败属于 P0 失败，必须先修再构建。

---

### Step 5-A/B/C/D: 按路径构建

完成 Step 5.0 和 Step 5.0.5 后，读取 `references/paths/path-workflows.md` 中对应路径执行：

| 路径 | 必读细节 |
|---|---|
| Path A | HTML -> editable PPTX、720pt x 405pt、absolute 定位、局部插画规则；构建前必须读取 `references/constraints/path-a-layout-safety.md`，先确认安全区、文本框内边距和高密度页型；需要复杂图表/结构页时可读取 `assets/layout-samples/kami-diagrams/` 作页型参考 |
| `2B / Path B` | `tasks.json` prompt manifest、整图视觉 PPTX、图片内文字准确性检查 |
| `2C / Path H` | 无正文文字视觉底图、PPT 原生文本框叠加、背景留白和文本可读性 |
| `2B-R / FigEdit Reconstruction` | 独立 FigEdit 预检、逐页测量、Agent Manifest、SVG/PPTX 组合、严格质量门；读取 `references/integrations/figedit-reconstruction.md` |
| `2D / Path C` | HTML deck / 单文件网页演示、magazine / minimal 种子、配图槽位、Motion One 离线资产；幻灯片场景默认多文件 HTML deck，不转 PPTX |
| `2D / Path D` | 多文件 HTML、GSAP、TTS、`data-anim` 动效声明；幻灯片/动画 deck 默认先聚合为 HTML |
| `2D / Path E` | Local React Deck、1920×1080 固定画布、组件化页型、静态导出、截图 QA；HTML/静态网页是最终作品 |
| `2D-B / Bento Adapter` | 固定本地 `Bento_Slides.bento.html`、`bento-deck.json`、生成/校验/评论导出；最终交付为可编辑 `.bento.html` |

---

## Step 6: 组装输出

按 `references/paths/path-workflows.md` 的对应命令组装输出。组装后进入 Step 7，不要跳过质量检查。

---

## Step 7: 分级质量检查（P0-P3）

**所有路径生成完成后，必须执行此步骤。** 完整检查清单在 `references/constraints/quality-checklist.md`。

### 检查流程

进入 Step 7 后读取 `references/constraints/quality-checklist.md`，按当前 Path 执行完整 P0/P1；2D / Path C-D-E 与 2D-B 都必须读取 `references/constraints/visual-qa.md` 做截图 QA。对有多页内容、数据或本地媒体的项目，先创建并校验 `deck-plan.json`（见 `references/contracts/deck-plan.md`）；它检查模板文案泄漏、文案预算、媒体路径、重复版式和图表洞察。`2D-B` 还必须创建并通过 `bento-deck.json`（见 `references/contracts/bento-deck.md`），可用 `--deck-plan` 对齐页序；生成后必须本地打开验证编辑、notes、状态/morph 和评论回流。对需要先审阅视觉/叙事方案的重要 deck，再创建 `design-brief.json`（见 `references/contracts/design-brief.md`），并用 `--deck-plan` 交叉验证页序和受众行动；经用户确认后才开始构建。两者都不替代路径专项 QA。**P0 不通过 = 不能交付**，修复后重新进入对应 QA。

研究答辩、论文、研讨会、基金简报或证据驱动技术演讲再额外使用 `academic-deck.json` v2（见 `references/contracts/academic-deck.md`）；仅在该模式检查学术论证 spine、早期研究问题、行动标题、单一结果 exhibit、非原创证据的页内引用、结论/参考文献/附录顺序、时间预算与可访问性。学术视觉值是可覆盖默认值，用户模板、品牌和已确认方向仍优先，但不得牺牲证据准确性和可读性。用户明确选择个人风格时，才通过绝对路径 `YH_SLIDES_STYLE_PROFILE` 读取 `references/contracts/style-profile.md` 定义的配置，且当前项目指令优先。

文档转 PPT 或证据密集型 deck 还必须按 `references/evidence-driven-methodology.md` 检查论点—证据映射、行动标题、图表洞察、来源登记和输出残留。模板文案、占位符、空壳页或来源无法定位都按 P0 处理。

通过标准：`100% P0` + `90%+ P1`。如果出错，查 `references/constraints/failure-modes.md` 快速定位根因。

### Step 7.5: 5 维设计自评（精品交付强制）

P0/P1 通过后，按 Philosophy、Hierarchy、Execution、Specificity、Restraint 五维自评；任何一项低于 3 分都必须回去修。最终交付前至少能确认：方向一致、层级清楚、执行可靠、内容具体、视觉克制。

对于重要汇报、课程、路演或多轮修改后的 deck，可在 Step 7.5 后调用 `autoreason-review` 作为叙事质量门：只评审大纲、页序、主张-证据关系、标题力度、信息层级和克制。不要用它替代截图 QA、PPTX/HTML 构建、渲染检查、文字溢出检查或路径专项质量门。

### Step 8: 评论迭代循环（成稿后）

交付预览后，如果用户给出修改意见，按 `references/constraints/comment-iteration-loop.md` 做轻量迭代；文案/视觉小改直接改相关页并回到 QA，结构大改回到 Step 3-C，事实修正回到 Step 1-C。

---

## 关键决策规则

- **优先 `2A / Path A`**：需要最稳妥的原生可编辑 PPTX、企业正式演示、后期频繁修改；可加入局部配图。Path A 高密度页面必须先套用 `path-a-layout-safety.md` 的安全区与页型模板，避免文字贴边或出框
- **优先 `2B / Path B`**：需要最强视觉冲击、接近样张、且不需要改字
- **优先 `2C / Path H`**：需要视觉好看且标题、正文、互动题、答案可编辑；默认要求底图不承载正文文字
- **优先 `2B-R / FigEdit Reconstruction`**：输入已经是位图，且需要恢复可编辑文字、结构、连接线、公式或可替换资产
- **优先 `2D / Path C magazine`**：个人分享 / 电子杂志 / 网页发布 / 追求精品质感；HTML 是最终作品
- **优先 `2D / Path D`**：含配音 / 含动画 / 教学课件；HTML 是最终作品
- **优先 `2D / Path E`**：网页演示需要长期维护、复杂交互、组件复用、静态部署或严格截图 QA
- **优先 `2D-B / Bento Adapter`**：需要一个可离线本地打开、浏览器可编辑、可评论的单文件 deck，或叙事确实需要状态/morph
- **优先王虹手写风**：用户明确要求中文手写、Notability 或数学学术讲解网页风格；资产与运行时全部走本地 `assets/wanghong/`
- **品牌优先**：如果有 `DESIGN.md`，优先遵守品牌系统；如果没有品牌系统，`2D / Path C magazine` 优先使用 `directions.md` 的 5 个方向包
- **独立技能原则**：外部项目只作为已吸收的方法来源；唯一例外是已注册的独立 FigEdit 技能，由 2B-R 薄适配层调用；其他路径不依赖外部仓库、外部索引资产、远程模板或远程 slide runtime
- **不允许**：跳过 Step 0 意图启动 / 把 `2C` 当成 `2B-R` / 2B-R 使用背景擦除或图片叠字降级 / 2B-R 未通过全部逐页质量门就生成整套交付 / 默认用 API 生图绕过原生工具 / 跳过方向锁定（2D / Path C magazine）/ 跳过 Step 3-C 页型覆盖检查 / 跳过当前路径要求的构建预检 / 跳过 Step 7 P0 检查 / 精品交付档跳过 5 维自评

---

## 内置能力与参考索引

学术模式校验器为 `scripts/validate_academic_deck.py`；学术工作流与双来源整合边界见 `references/getting-started/academic-presentation-workflow.md` 和 `references/meta/academic-and-dashi-integration.md`。

核心脚本位于 `scripts/`：`generate_image.py`、`create_slides.py`、`figedit_batch.py`、`html2pptx.js`、`export_deck_pdf.mjs`、`export_deck_stage_pdf.mjs`、`gen_deck_thumbs.mjs`、`create_contact_sheet.py`、`pdf_evidence_pipeline.py`、`build_timeline.py`、`prepare_render_html.py` 与 `build_tosea_metadata.py`。Path A 的 Node 依赖随技能目录的 `package.json` 本地化，优先在技能根目录运行 `npm install` 后使用。2B-R 通过 `figedit_batch.py` 调用独立 FigEdit；不复制其 OCR/CV/重建内核。HTML deck 默认外壳是 `assets/deck_index.html`，幻灯片架构和导出规范见 `references/slide-decks.md`，品牌/logo 资产协议见 `references/brand-asset-protocol.md`。本地 Tosea 预览库位于 `templates/tosea/`，王虹手写运行时位于 `assets/wanghong/`。完整 reference、seed、模板、layout、scene 资产索引见 `references/_INDEX.md`；维护来源和演进原则见 `references/meta/evolution.md`，资产状态见 `references/meta/asset-inventory.md`。

---

## 输出

- `.pptx` for `Path A`
- `.pptx` for `2B / Path B`
- `.pptx` for `2C / Path H`
- native editable `.pptx` + per-page SVG/Manifest/quality reports for `2B-R / FigEdit Reconstruction`
- HTML deck + derived `.pdf` for slide/deck tasks by default
- `.html` for `2D / Path C`
- `.bento.html` for `2D-B / Bento Adapter`
- multi-file HTML for `2D / Path D`
- static local React deck / HTML build for `2D / Path E`

---

## 来源与持续进化记录

来源、吸收原则和维护边界见 `references/meta/evolution.md`。除明确声明的独立 FigEdit 技能联动外，执行时不得依赖外部仓库、外部索引资产、远程模板或远程 slide runtime。
