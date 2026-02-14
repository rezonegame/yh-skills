# YH Skills Collection

这是一个包含多种 AI Agent 技能（Skills）的集合，旨在增强 AI 在特定领域的专业能力。这些技能涵盖了从桌游设计到学术研究、内容创作以及后端开发等多个方面。

## 📂 技能列表

### 🎲 桌游设计 (Board Game Design)
这一系列技能专注于桌游的各个设计环节，从机制到配件制作。

- **boardgame-design**: 桌游设计专家技能。使用 5-Component Filter（清晰度、策略、互动、满意度、适配）来评估和设计游戏机制。
- **boardgame-boards**: 游戏板和地图设计指南。涵盖布局系统、折叠模式、信息密度和路径清晰度。
- **boardgame-boxes**: 桌游包装盒设计。提供尺寸选择、结构设计、封面艺术布局和生产规格指导。
- **boardgame-cards**: 卡牌设计指南。涵盖卡牌尺寸、正面布局层级、图标系统、背面对齐和整版排版。
- **boardgame-components**: 通用配件设计。包括标记 (Tokens)、指示物、玩家辅助卡、规则书和记分板的设计规范。
- **boardgame-tiles**: 方块 (Tiles) 设计技能。专注于六边形、方形等方块的边缘连接系统、旋转兼容性和模切考虑。
- **boardgame-ralph-loop**: 基于 Ralph Loop 方法论的自主迭代设计技能。提供自动化的测试和设计改进循环。

### 📝 研究与写作 (Research & Writing)
一套用于辅助高水平学术研究和专业写作的工具。

- **scientific-writing**: 科学写作核心技能。指导遵循 IMRAD 结构，使用两阶段写作法（大纲 -> 完整段落），确保符合学术出版标准。
- **scientific-critical-thinking**: 科学批判性思维。用于评估研究的严谨性、方法论、实验设计、统计有效性及偏差检测。
- **literature-review**: 系统性文献综述技能。支持跨多个数据库（PubMed, arXiv 等）进行检索、筛选、综合和引用验证。
- **openalex-database**: OpenAlex 数据库查询技能。用于搜索学术论文、分析研究趋势、追踪引用和进行文献计量分析。
- **content-research-writer**: 内容研究与协作写作。辅助进行深入研究、添加引用、优化开头（Hook）并提供分段反馈。
- **content-strategist**: SEO 内容策略专家。创建经过搜索引擎优化的内容，涵盖关键词整合、元标签编写和结构优化。
- **doc-coauthoring**: 文档共创工作流。引导用户完成"背景收集 -> 结构细化 -> 读者测试"的文档编写流程。

### 💻 开发与技术 (Development & Tech)
用于辅助软件开发和技术任务的技能。

- **backend-patterns**: 后端开发模式。提供 Node.js, Express, Next.js 的架构模式、API 设计和数据库优化最佳实践。
- **ducksearch**: 命令行网页搜索工具。基于 DuckDuckGo，支持搜索网络信息、抓取网页内容及作为 MCP 服务器使用。

## � 安装 (Installation)

### 前置要求
- 已安装 Node.js 环境
- 能够运行 `npx` 或 `bun` 命令

### 快速安装（推荐）
```bash
npx skills add rezonegame/yh-skills
```

## �🚀 使用说明

这些技能通常以文件夹形式存在，每个文件夹内包含一个 `SKILL.md` 核心描述文件以及可能的辅助脚本或资源。

要使用这些技能：
1. 确保你的 AI Agent 环境支持加载本地技能或 MCP (Model Context Protocol)。
2. 根据需要导入相应的技能文件夹。
3. 参考各技能目录下的 `SKILL.md` 文件了解详细的触发指令和使用方法。

## 📦 仓库维护

本仓库由自动化脚本同步和维护。
