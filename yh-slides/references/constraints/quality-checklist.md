# 分级质量检查清单（Quality Checklist）

> **适用路径**：2A/2B/2C/2B-R/Path C/Path D/Path E（各路径有独立的 P0-P3 规则）  
> **使用时机**：SKILL.md Step 7 生成后

本文档按 P0 / P1 / P2 / P3 四个等级组织质量检查项。**P0 是硬门槛，必须全过；P1 强烈建议；P2/P3 按需抛光**。

---

## 通用使用方法

1. 生成完 deck / PPTX 后，先找到你走的路径章节
2. 逐项 P0 检查 — **任何一条不过 → 必须修复后重新生成**
3. 检查 P1 — 强烈建议修复
4. Path C/D/E 必须执行 [visual-qa.md](./visual-qa.md)
5. 检查 P2/P3 — 按项目时间/预算决定是否抛光
6. 不接受"差不多就行"

---

## Path A（HTML → PPTX）

### 🔴 P0 — 必须通过（否则 html2pptx 翻车）

| # | 检查项 | 检查方法 |
|---|-------|---------|
| A-P0-1 | HTML 尺寸严格 720pt × 405pt | `grep 'width:720pt' slide*.html` 每个 slide 根容器都应匹配 |
| A-P0-2 | 所有元素使用 `position: absolute` | `grep -L 'position:absolute' slide*.html` 应为空 |
| A-P0-3 | 图片有明确宽高（pt 单位） | `grep '<img' slide*.html` 每条都要有 `width:Npt;height:Npt` |
| A-P0-4 | 图片路径是本地相对路径 | 不能是 `https://` 或 `file://` |
| A-P0-5 | AI 生成的图片 prompt 含 `no text in image` | 查生成时的 tasks.json |
| A-P0-6 | `html2pptx` 命令能跑通输出 `.pptx` | 运行组装命令不报错 |
| A-P0-7 | 正文文本不贴画布边缘 | 所有正文文本框位于 `x=32..688`、`y=32..370` 内；页眉/页脚除外 |
| A-P0-8 | 卡片内文字不贴卡片边缘 | 卡片内文本相对卡片左上至少内缩 10pt，推荐 12pt |
| A-P0-9 | 文本框高度足够 | 按 `fontSize * lineCount * lineHeight + 4pt` 估算，无明显出框 |
| A-P0-10 | 高密度页有明确页型 | 采用 `path-a-layout-safety.md` 的 A1/A2/A3 或等价布局表 |

### 🟡 P1 — 强烈建议

| # | 检查项 | 检查方法 |
|---|-------|---------|
| A-P1-1 | 字体统一（中文用 Noto Serif SC，英文用 Playfair） | 目视 |
| A-P1-2 | 没有文本溢出容器 | 抽查 3-4 页预览图；重点看标题、脚注、卡片末行和中文列表 |
| A-P1-3 | 图片是 no text 生成（无机器乱码字） | 目视 |
| A-P1-4 | 标题字号比正文大 1.5 倍以上 | 抽查 |

### 🟢 P2 — 视觉抛光

- A-P2-1: 审美节奏（Hero / 正文交替）
- A-P2-2: 图片留白充足（不贴边）
- A-P2-3: 颜色主题一致（一套主题色）
- A-P2-4: 图标使用 SVG / Lucide（不用 emoji）

### 🔵 P3 — 细节

- A-P3-1: PPTX 文件名规范（`{项目名}.pptx`）
- A-P3-2: 页码一致（封面不编号，正文从 01 起）
- A-P3-3: 输出目录结构符合 `C:\PPTX\{项目名}\output\`

---

## 2A-S / Path S（SVG → Native Editable PPTX）

### 🔴 P0 — 必须通过

| # | 检查项 | 检查方法 |
|---|-------|---------|
| S-P0-1 | `design_spec.md` 与 `spec_lock.md` 存在 | 检查项目根目录 |
| S-P0-2 | 每页 SVG 的 `viewBox` 匹配 `spec_lock.canvas` | `python scripts/svg_quality_checker.py "C:\PPTX\{项目名}"` |
| S-P0-3 | SVG 无 forbidden features | `svg_quality_checker.py` 必须 0 error |
| S-P0-4 | 每页生成前颜色/字体/图片来自 `spec_lock.md` | 抽查 SVG 与 lock 的颜色、字体、图片名 |
| S-P0-5 | 顶层语义块有稳定 `<g id="...">` | 抽查 SVG，动画和对象选择依赖这些 id |
| S-P0-6 | `total_md_split.py`、`finalize_svg.py`、`svg_to_pptx.py` 全链路成功 | 运行命令不报错 |
| S-P0-7 | 输出 native PPTX 能打开，关键文本/形状可编辑 | PowerPoint/WPS 双击文字和形状测试 |
| S-P0-8 | 本地资源无远程 runtime 依赖 | `python scripts/check_offline_ready.py` |

### 🟡 P1 — 强烈建议

- S-P1-1: 图表页坐标和数据标签人工核对。
- S-P1-2: `animations.json` 只在用户要求对象级动画时创建，并能通过 validate。
- S-P1-3: notes 能被导出/读取，不只是写在设计文档里。
- S-P1-4: `backup/{timestamp}/svg_output/` 存在，便于复导出。

### 🟢 P2 — 视觉抛光

- S-P2-1: `page_rhythm` 有 anchor/dense/breathing 变化。
- S-P2-2: charts/icons 来自本地模板库且风格统一。
- S-P2-3: native PPTX 与 SVG 预览差异可接受。

---

## 2A-T / Template Fill（原生 PPTX 模板填充）

### 🔴 P0 — 必须通过

| # | 检查项 | 检查方法 |
|---|-------|---------|
| T-P0-1 | 用户提供源 PPTX 模板和新内容材料 | `sources/` 中存在 `.pptx` 和内容源 |
| T-P0-2 | `slide_library.json` 成功生成 | `template_fill_pptx.py analyze` 输出有效 JSON |
| T-P0-3 | `fill_plan.json` 按目标故事选择/重排/复用页面 | 人工检查 plan，不接受机械全量顺序替换 |
| T-P0-4 | capacity check 已运行 | `check_report.json` 存在，严重 warning 已处理或记录接受理由 |
| T-P0-5 | apply 成功输出 `.pptx` | `exports/` 中存在带时间戳 PPTX |
| T-P0-6 | 输出 PPTX 保持原模板视觉和原生可编辑对象 | PowerPoint/WPS 抽查 |
| T-P0-7 | readback 验证关键标题、表格/图表、notes | `validation/` 中保存 readback 或验证说明 |

### 🟡 P1 — 强烈建议

- T-P1-1: 每个复用页面都有 layout rationale。
- T-P1-2: 章节页、封面、结束页的短文本不过载。
- T-P1-3: 模板中的页码、章节标记和 notes 已随新顺序更新。
- T-P1-4: 原模板动画保留或 page transition 策略明确。

### 🟢 P2 — 视觉抛光

- T-P2-1: 输出页数少而精，不为保留模板而硬塞内容。
- T-P2-2: 同一源页重复使用时目的明确，避免视觉疲劳。


---

## 2B / Path B（AI 整图 → 图片型 PPTX）

### 🔴 P0 — 必须通过

| # | 检查项 | 检查方法 |
|---|-------|---------|
| B-std-P0-1 | 图片尺寸匹配选定规格（512/1K/2K/4K） | `identify *.png` 或 PIL 检查 |
| B-std-P0-2 | 图片无明显截断 / 烂尾 | 目视 |
| B-std-P0-3 | 如果图片里包含文字，文字准确且无机器乱码 | 目视（正向制作需要可改字时改走 2C；已有位图需要恢复结构时走 2B-R） |
| B-std-P0-4 | `create_slides.py` 成功输出 `.pptx` | 运行命令不报错 |
| B-std-P0-5 | 所有 tasks.json 任务都成功（无 failed 状态） | 查生成日志 |
| B-std-P0-6 | Ian 手绘页只出现 `Required text only` 中列出的文字 | 对照 prompt 与逐页图片；额外字、伪字、URL 或 Logo 均失败 |

### 🟡 P1 — 强烈建议

- B-std-P1-1: 整套图片风格一致（不混用 Snoopy + Bauhaus）
- B-std-P1-2: 标题位置统一（如都在上 1/3 或都居中）
- B-std-P1-3: 中文在图片里清晰可读（若启用图片内文字）
- B-std-P1-4: 封面视觉最强，正文克制

### 🟢 P2 — 视觉抛光

- B-std-P2-1: 色彩平衡（整套色温一致）
- B-std-P2-2: 构图节奏交替（左图右文 / 居中 / 全屏）
- B-std-P2-3: 单张图片时长可承受（2K 图片 1 秒内能加载）

### 🔵 P3 — 细节

- B-std-P3-1: PPTX 播放时无卡顿
- B-std-P3-2: 文件大小合理（单 PPTX 建议 < 100MB）

---

## 2C Hybrid（视觉底图 + 可编辑文字 PPTX）

### 🔴 P0 — 必须通过

| # | 检查项 | 检查方法 |
|---|-------|---------|
| 2C-P0-1 | 底图 prompt 明确禁止正文文字、标题、题目、答案文字 | 查 tasks.json / prompt 记录，必须含 no text / no letters / no body copy |
| 2C-P0-2 | 生成底图中没有可读文字或机器乱码文字 | 目视每张底图 |
| 2C-P0-3 | PPTX 中标题、正文、互动题、答案为可编辑文本框 | PowerPoint 双击文字测试 |
| 2C-P0-4 | 背景为文字层预留足够留白 | 目视关键页，无文字压图、压脸、压主体 |
| 2C-P0-5 | 中文文本可读且不溢出 | 抽查全部页面或导出预览图 |
| 2C-P0-6 | 输出 PPTX 能正常打开 | PowerPoint / WPS 打开测试 |
| 2C-P0-7 | Ian 手绘底图完全无字，最终文字保持可编辑 | 逐张检查底图并在 PowerPoint 双击最终文字 |

### 🟡 P1 — 强烈建议

- 2C-P1-1: 文本框层级统一，大标题、正文、注释有稳定字号比例
- 2C-P1-2: 底图风格一致，不连续多页视觉噪音过高
- 2C-P1-3: 文本框与底图构图有呼应，不像后贴文字
- 2C-P1-4: 标准制作/精品交付必须先检查 1-2 页样稿后再批量生成

### 🟢 P2 — 视觉抛光

- 2C-P2-1: 背景主体避开标题和正文热区
- 2C-P2-2: 强调色与底图色彩协调
- 2C-P2-3: 互动题 / 答案揭示页层级清楚

### Ian 中文手绘专项（2B / 2C）

- 固定近白外壳、黑色细线和克制标题，正文页不得出现黄纸、满页框、阴影、渐变或超大标题。
- 中央语义图通常占宽 50–60%、高 35–45%，并保留明显空气。
- 优先无人；确有需要时最多一个角落微小人物。
- 套图外壳一致，中央物件、动作和页型随内容变化；不得连续重复同一隐喻。
- 交付前运行 `scripts/create_contact_sheet.py`，检查单页和联系表；风格漂移属于 P1，错误文字属于 P0。

---

## 2B-R / FigEdit Reconstruction（位图 → 可编辑 SVG 与原生 PPTX）

### 🔴 P0 — 必须通过

| # | 检查项 | 检查方法 |
|---|-------|---------|
| 2BR-P0-1 | FigEdit 独立技能和重依赖预检通过 | `figedit_batch.py preflight` |
| 2BR-P0-2 | 每页都有源图、测量证据、Manifest、SVG、PPTX 和质量报告 | 查 `reconstruction/page-NN/` |
| 2BR-P0-3 | 关键标题、标签、面板和流向完整 | 对比源图、preview 和 Manifest |
| 2BR-P0-4 | 普通文字、稳定几何和连接线为可编辑对象 | 检查 SVG/PPTX 对象 |
| 2BR-P0-5 | 重要公式导出为可编辑 Office Math | 查 `pptx_math_export` |
| 2BR-P0-6 | 特色图标、Logo、截图、地图和复杂图表未被通用图标替代 | 查资产清单与裁切联系表 |
| 2BR-P0-7 | 每页 `delivery_review` 四项语义审查全部批准 | 查最终 Manifest |
| 2BR-P0-8 | 所有页面通过后才生成整套原生 PPTX | `figedit_batch.py status/assemble` |

### 🟡 P1 — 强烈建议

| # | 检查项 | 检查方法 |
|---|-------|---------|
| 2BR-P1-1 | 布局拓扑、嵌套关系和阅读顺序接近源图 | 对比源图和 preview |
| 2BR-P1-2 | 字体回退、颜色、字号和对齐合理 | 抽查每种文字层级 |
| 2BR-P1-3 | 裁切资产无截断、拉伸或邻近污染 | 查看 contact sheet |
| 2BR-P1-4 | editability audit 为 `ok` | 查 `editability_report.md` |

### 🟢 P2 — 视觉抛光

- 2BR-P2-1: 字体、字重和行距进一步贴近源图
- 2BR-P2-2: 连接线端点、圆角、阴影和描边进一步校准
- 2BR-P2-3: 重复资产和视觉节奏保持一致

### 🔵 P3 — 细节

- 2BR-P3-1: Manifest 决策、置信度和复核状态记录完整
- 2BR-P3-2: `summary_report.md`、`failed_pages.json` 和转换 trace 可追溯

---

## 2D / Path C（单文件网页演示）

### 🔴 P0 — 必须通过

| # | 检查项 | 检查方法 |
|---|-------|---------|
| C-P0-1 | 所有 class 在 `<style>` 块中有定义（无 fallback） | 参考 [class-preflight.md](./class-preflight.md) 的 diff 命令 |
| C-P0-2 | Magazine 种子未改动 `<head>` 的 WebGL canvas 和导航 JS | `diff path-c-magazine-seed.html index.html` 头部应一致 |
| C-P0-3 | 1920×1080 视口下 scroll-snap 正常工作（翻页无错位） | 浏览器 F11 全屏测试 |
| C-P0-4 | 每个 `<section class="slide">` 都带主题标记（light/dark/hero） | `grep 'class="slide' index.html` 查所有标记 |
| C-P0-5 | 不连续 3 页同主题 | 参考 [theme-rhythm.md](./theme-rhythm.md) 的自检命令 |
| C-P0-6 | 图片路径是相对路径（`images/xxx.png`） | `grep -E 'src="(http|file|/)"' index.html` 应为空 |
| C-P0-7 | 视觉截图 QA 通过 | 按 [visual-qa.md](./visual-qa.md) 检查截图、近空白页、重复 hash 和 contact sheet |

### 🟡 P1 — 强烈建议

| # | 检查项 | 检查方法 |
|---|-------|---------|
| C-P1-1 | 8+ 页时有 ≥1 `hero dark` + ≥1 `hero light` | 节奏自检 |
| C-P1-2 | 至少 1 个 `dark` 正文页（非 hero） | 节奏自检 |
| C-P1-3 | 所有图片使用 `height: Nvh` 而非 `aspect-ratio`（图片网格） | `grep 'aspect-ratio' index.html` 应少 |
| C-P1-4 | 衬线 / 非衬线字体分工正确 | 目视 |
| C-P1-5 | chrome 和 kicker 不同义翻译 | 目视 |

### 🟢 P2 — 视觉抛光

- C-P2-1: WebGL 背景在 hero 页明显可见，非 hero 页隐约
- C-P2-2: 图片微圆角（4px），无阴影
- C-P2-3: 大标题字数 × 字号合理（不出现 1 字 1 行）
- C-P2-4: 图片只裁底部（`object-position: top center`）
- C-P2-5: 术语中英文统一

### 🔵 P3 — 细节

- C-P3-1: 页码动态生成（nav dots 数量与 slide 数量一致）
- C-P3-2: 键盘 ← → / 滚轮 / 触屏翻页都工作
- C-P3-3: `<title>` 已替换为实际项目名（无 `[必填]`）
- C-P3-4: `chrome` 里的静态页码 `NN / Total` 与实际一致

---

## Path D（多文件 HTML + GSAP + TTS）

### 🔴 P0 — 必须通过

| # | 检查项 | 检查方法 |
|---|-------|---------|
| D-P0-1 | GSAP 加载成功（本地 `assets/vendor/js/gsap.min.js` 存在并可加载） | 浏览器 Network 面板 |
| D-P0-2 | 如启用 TTS：所有音频文件路径正确，可播放 | 逐个点击 audio 播放 |
| D-P0-3 | 所有 class 在 `<style>` 有定义（C-P0-1 相同规则） | class preflight |
| D-P0-4 | 多文件结构完整（`index.html` + `styles/` + `scripts/` + `audio/`） | 目录树检查 |
| D-P0-5 | 主题标记规则同 Path C | 参考 theme-rhythm.md |
| D-P0-6 | 视觉截图 QA 通过 | 按 [visual-qa.md](./visual-qa.md) 检查 |

### 🟡 P1 — 强烈建议

| # | 检查项 | 检查方法 |
|---|-------|---------|
| D-P1-1 | 动画时长与音频同步（若启用 TTS） | 播放测试 |
| D-P1-2 | GSAP 翻页效果不抢文本可读性 | 目视 |
| D-P1-3 | 动画不卡顿（60 FPS） | 浏览器 Performance 面板 |
| D-P1-4 | 首次加载不阻塞（懒加载音频 / 大图） | Network 瀑布图 |

### 🟢 P2 — 视觉抛光

- D-P2-1: 动画节奏符合演讲节奏（不过快 / 过慢）
- D-P2-2: 过渡效果统一（不混用 slide / fade / rotate）
- D-P2-3: 字幕（若启用）时长合理
- D-P2-4: 音量均衡（无突兀音量变化）

### 🔵 P3 — 细节

- D-P3-1: 移动设备响应（平板 / 手机正常显示）
- D-P3-2: 打印友好（如需导出 PDF）
- D-P3-3: 辅助功能（`alt` 文本、键盘可访问）

---

## 2D-P / Presenter Mode（HTML 演讲者模式）

### 🔴 P0 — 必须通过

| # | 检查项 | 检查方法 |
|---|-------|---------|
| P-P0-1 | 每页有 hidden notes | 搜索 `<aside class="notes">` 或 `.notes`，数量应匹配 slide 数 |
| P-P0-2 | notes 不在观众视图可见 | 浏览器打开观众页目视，notes 默认隐藏 |
| P-P0-3 | 本地 runtime 加载，无 CDN 依赖 | `python scripts/check_offline_ready.py` |
| P-P0-4 | `S` 键能打开 presenter window | 浏览器手测 |
| P-P0-5 | CURRENT / NEXT / SCRIPT / TIMER 四区存在 | presenter window 手测 |
| P-P0-6 | `?preview=N` 单页预览可用且无 chrome | 浏览器打开 preview URL |
| P-P0-7 | 观众窗口和 presenter window 左右键同步 | 双窗口手测 |
| P-P0-8 | 逐字稿不是写在 slide 可见文本里 | 代码和目视检查 |

### 🟡 P1 — 强烈建议

- P-P1-1: notes 是口语提示信号，不是书面长文。
- P-P1-2: 每页 notes 长度符合场景；详细逐字稿才使用 150-300 字。
- P-P1-3: 过渡句自然引出下一页。
- P-P1-4: timer reset 和 fullscreen/overview 快捷键可用。

### 🟢 P2 — 视觉抛光

- P-P2-1: presenter 预览与观众页颜色/字体/布局一致。
- P-P2-2: notes 中关键词加粗或分段，便于扫读。
- P-P2-3: 动效克制，不干扰演讲节奏。

---

## 2D / Path E（Local React Deck）

### 🔴 P0 — 必须通过

| # | 检查项 | 检查方法 |
|---|-------|---------|
| E-P0-1 | 不依赖外部 slide runtime | 不应默认引入 Open-Slide、Open-Design runtime 或远程导航脚本 |
| E-P0-2 | 每页固定 1920×1080 画布 | 检查根组件 / canvas wrapper 尺寸 |
| E-P0-3 | 本地构建或预览命令通过 | 运行当前工程对应 build/dev preview，无报错 |
| E-P0-4 | 路由 / 页面不是空 DOM | 浏览器检查或截图检查 |
| E-P0-5 | 必需资源均为本地资源 | 无远程图片、字体、脚本作为必需依赖 |
| E-P0-6 | 视觉截图 QA 通过 | 按 [visual-qa.md](./visual-qa.md) 生成截图、hash 检查、contact sheet |
| E-P0-7 | `DESIGN.md` 或主题文件记录 tokens | palette、type scale、layout rhythm、image strategy、page archetypes、avoid list |

### 🟡 P1 — 强烈建议

| # | 检查项 | 检查方法 |
|---|-------|---------|
| E-P1-1 | 页面组件结构清晰，可维护 | 每页为独立组件或清晰数据驱动渲染单元 |
| E-P1-2 | 样式 tokens 集中管理 | 颜色、字号、间距不在每页散落硬编码 |
| E-P1-3 | 页型覆盖合理 | 检查 Step 3-C 的 archetype 标注 |
| E-P1-4 | 键盘 / 点击导航可用 | 本地预览测试 |
| E-P1-5 | 静态输出可独立打开或部署 | 检查 output/react-deck 或等价目录 |

### 🟢 P2 — 视觉抛光

- E-P2-1: contact sheet 整体节奏有变化，不连续多页同构
- E-P2-2: 图表 / 组件在 1920×1080 下无挤压
- E-P2-3: 动效或交互服务内容，不抢阅读焦点
- E-P2-4: 中英文、数字、代码的字体层级统一

### 🔵 P3 — 细节

- E-P3-1: presenter / speaker notes（如项目需要）
- E-P3-2: PDF / 静态 HTML 导出检查（如项目需要）
- E-P3-3: 辅助功能（`alt`、焦点状态、键盘可访问）

---

## 自动化自检脚本模板

### Path A 全 P0 检查

```bash
cd slides/
echo "=== A-P0-1: 尺寸 ==="
grep 'width:720pt' *.html | wc -l
echo "=== A-P0-2: absolute 定位 ==="
grep -L 'position:absolute' *.html
echo "=== A-P0-4: 图片路径 ==="
grep -oE 'src="[^"]+"' *.html | grep -E 'https?://|file://|^/'
```

### Path C 全 P0 检查

```bash
cd output/
echo "=== C-P0-1: 未定义 class ==="
diff <(grep -oE 'class="[^"]+"' index.html | grep -oE '[a-z][a-z0-9-]+' | sort -u) \
     <(grep -oE '\.[a-z][a-z0-9-]+' ../assets/seeds/path-c-magazine-seed.html | sort -u)

echo "=== C-P0-4: 主题标记 ==="
grep -oE 'class="slide [^"]+"' index.html | sort | uniq -c

echo "=== C-P0-6: 非本地图片 ==="
grep -oE 'src="[^"]+"' index.html | grep -vE '^src="(images/|[^:]+\.(png|jpg|svg))'
```

### Path C/D/E 视觉 QA

```bash
echo "=== 视觉 QA ==="
echo "1. 以 1920x1080 截图每一页"
echo "2. 检查白屏、空页、近空白页"
echo "3. 检查异常重复 hash"
echo "4. 生成 contact sheet 并人工扫读"
echo "详细步骤见 references/constraints/visual-qa.md"
```

---

## 修复优先级决策树

```
遇到问题
  │
  ├─ P0 问题? ───→ 必须立即修复，否则不能交付
  │
  ├─ P1 问题? ───→ 强烈建议修复（除非时间紧张且用户接受）
  │
  ├─ P2 问题? ───→ 按时间/预算决定
  │
  └─ P3 问题? ───→ 如有余力再抛光
```

**交付标准**：100% P0 通过 + 90%+ P1 通过 = 可交付
