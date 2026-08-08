# 产物-路径定义

> 从 SKILL.md 提取的产物路径映射表和全局生图后端策略。详细使用规则见 SKILL.md 各 Step。

## 产物-路径映射表

| 用户侧产物选项 | 内部执行路径 | 工作方式 | 适用场景 |
|---|---|---|---|
| `2A 通用可编辑 PPTX（简易 HTML 转换）` | `Path A` | 用受限 HTML/CSS 做 PPTX 中间稿；PPT 原生文字、形状、图表和版式为主，可加入局部插画/照片；最终经 `html2pptx` 输出可编辑 PPTX | 正式汇报、企业演示、需要稳定后期修改 |
| `2A-S 高保真原生可编辑 PPTX（SVG → DrawingML）` | `Path S` | 逐页 SVG 作为严谨视觉源，经本地 DrawingML 导出为原生可编辑 PPTX；支持复杂图表、图标、形状、备注与动画 sidecar | 咨询级图表、复杂信息图、强原生可编辑、避免 HTML 转换偏移 |
| `2A-T 原生 PPTX 模板填充` | `Template Fill` | 复用用户提供的 PPTX 模板页库，分析可替换槽位，选择/重排/复用原生页面并替换文字、表格、图表 | 已有公司模板、想保留原设计、只换内容和数据 |
| `2B 整图视觉 PPTX` | `Path B` | 每页一张完整 AI 图，文字也可在图里；最终组装为图片型 PPTX | 最强视觉冲击、接近样张、不需要改字 |
| `2C 视觉底图 + 可编辑文字 PPTX` | `Path H` | AI 生成无正文文字的整页视觉底图，PPT 原生文本框叠加标题、正文、互动题和答案 | 想要好看，同时课堂/汇报文字可编辑 |
| `2D 多功能 HTML 演示` | `Path C / D / E` | HTML 是最终作品：单文件网页、动画/TTS 或本地 React Deck | 网页分享、配音动画、长期维护或复杂交互 |
| `2D-B Bento Deck` | `Bento Adapter` | 本地可编辑 `.bento.html`，含 notes、评论、状态和 morph | 离线浏览器编辑、单文件审阅；不承诺 PPTX |
| `2D-P HTML 演讲者模式` | `Presenter Mode` | 本地 HTML 演示 + hidden notes + S 键演讲者窗口，含当前页、下一页、逐字稿、计时器和双窗口同步 | 演讲、技术分享、培训、路演、需要提词器或 speaker notes |
| `2B-R 可编辑重建` | `FigEdit Reconstruction` | 已有位图 → OCR/CV 测量 → Agent 语义拆解 → 可编辑 SVG → 原生 DrawingML PPTX | 位图幻灯片、截图、论文图、架构图需要恢复可编辑结构 |

## 全局生图后端策略（所有路径通用）

默认采用 `auto-runtime`：**当前对话模型 / Agent Runtime 原生生图能力优先，API 后端只做备用**。

- 用户明确指定 `gemini` / `imagen` / `API` 时，按用户指定执行。
- 用户未指定时，只要当前环境暴露原生生图工具，就优先使用原生工具，并把图片保存到项目目录。
- 不要因为技能目录里有 `scripts/generate_image.py` 就默认调用 API；该脚本是 fallback，不是默认入口。
- 只有当前环境没有原生生图工具、原生工具无法稳定落盘、或原生工具明确失败且任务仍需继续时，才使用运行环境变量或显式 `YH_SKILLS_ENV_FILE` 中的 API key 调用 `scripts/generate_image.py`。
- 详细规则见 `references/integrations/image-backend-policy.md`。
