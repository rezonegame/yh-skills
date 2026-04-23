# YH Skills Collection

![Version](https://img.shields.io/badge/version-1.6.0-blue) ![Last Updated](https://img.shields.io/badge/last%20updated-Apr%2023,%202026-green)

## 📅 更新日志 (Changelog)
- **v1.6.0** (2026-04-23): 更新 `gamified-course-designer` 与 `last30days`。优化了课程设计框架及跨平台热点搜索脚本。
- **v1.5.0** (2026-04-15): 整合整理，新增 `geo-content-optimizer`, `gamified-course-designer` 等多项核心技能。
- **v1.4.0** (2026-03-12): 新增 `multi-agent-debate` 多视角角色讨论框架。
- **v1.3.0** (2026-03-03): 新增 `last30days` 跨平台趋势搜索与分析技能。
- **v1.2.0** (2026-02-25): 新增 `humanizer-zh` 文本去 AI 痕迹与深度润色技能。
- **v1.1.1** (2026-02-19): 移除 backend-patterns 技能。
- **v1.1.0** (2026-02-19): 新增 MeepleLM 虚拟玩家测试技能。
- **v1.0.0** (2025-12-15): 初始版本发布。集成桌游设计、学术写作、内容创作及开发辅助等多领域技能。

这是一个包含多种 AI Agent 技能（Skills）的集合，旨在增强 AI 在特定领域的专业能力。这些技能涵盖了从桌游设计到学术研究、内容创作以及后端开发等多个方面，名字相同的skill，都经过使用和微调，保留了原skill的优点，并根据实际使用情况进行了优化，以及版权信息。

## 📂 技能列表

### 🎲 桌游与游戏化 (Board Games & Gamification)
这一系列技能专注于桌游各环节设计、机制研究及游戏化教育。

| 技能名称 | 核心说明与功能 | 适用场景 |
| :--- | :--- | :--- |
| `boardgame-design` | **桌游设计专家**。使用 5-Component Filter（清晰度、策略、互动、满意度、适配）评估机制。 | 核心机制设计与平衡评估 |
| `boardgame-boards` | **地图与板图指南**。涵盖布局系统、折叠模式、信息密度和路径清晰度。 | 游戏地图、中央版图布局 |
| `boardgame-boxes` | **包装盒设计规范**。提供尺寸选择、结构设计、封面艺术布局和生产规格。 | 实物包装、封面视觉设计 |
| `boardgame-cards` | **卡牌设计专家**。涵盖尺寸规范、层级布局、图标系统、背面对齐和排版。 | 游戏卡牌、数值展示 |
| `boardgame-components` | **通用配件设计**。包括标记（Tokens）、指示物、玩家辅助、规则书和记分板。 | 通用 UI/UX 配件设计 |
| `boardgame-tiles` | **版块方形/六边形设计**。专注于边缘连接系统、旋转兼容性和模切考虑。 | 版图拼接、地图块设计 |
| `boardgame-ralph-loop` | **自主迭代系统**。基于 Ralph Loop 方法论，提供自动化的测试和设计改进循环。 | 机制自动化压测与迭代 |
| `boardgame-writer` | **智研家桌游文案**。支持 7 种作者人设，提供深度、专业且具有传播力的评测。 | 公众号、知乎等长文推荐 |
| `meeplelm` | **虚拟玩家评测**。基于 MDA 推理链，模拟不同人设玩家的主观体验，生成深度评论。 | 虚拟 Playtest、评价预测 |
| `gamified-course-designer` | **游戏化课程设计**。基于布卢姆分类法，自动将教学内容转化为有趣的方案。 | 教育产品、课程趣味化升级 |

### 📝 内容创作与研究 (Content Creation & Research)
用于辅助高水平学术研究、专业内容创作及深度信息优化的核心工具。

| 技能名称 | 核心说明与功能 | 适用场景 |
| :--- | :--- | :--- |
| `humanizer-zh` | **文本去 AI 化**。剔除 AI 虚夸词汇，注入具有深度的真实“人味”，提升可读性。 | 书评、长评、深度润色 |
| `geo-content-optimizer` | **GEO 内容架构师**。针对 RAG 系统优化，提升事实密度与语义结构。 | Perplexity/SearchGPT 优化 |
| `merge-drafts` | **多稿合并专家**。将多份立场不同或细节分散的草稿合并为一份高质量正文。 | 深度文章整合、总结重组 |
| `scientific-writing` | **科学写作核心**。遵循 IMRAD 结构，确保逻辑严密且符合学术发表标准。 | 论文撰写、学术报告、综述 |
| `scientific-critical-thinking` | **科学批判思维**。评估研究的严谨性、方法论缺陷、实验设计及偏差检测。 | 论文评审、研究可行性分析 |
| `literature-review` | **系统综述检索**。集成多数据库检索，支持文献筛选、综合分析与引用验证。 | 文献综述、前沿动态追踪 |
| `openalex-database` | **OpenAlex 检索**。高效查询学术论文原始数据，分析研究趋势与文献计量。 | 深度学术调研、专家追踪 |
| `content-research-writer` | **深度研究助手**。打捞事实、优化 Hook 开头并提供分段反馈与协作。 | 深度报道、调研型文章 |
| `content-strategist` | **SEO 策略专家**。基于搜索意图优化内容结构、关键词整合及元标签。 | 营销着陆页、SEO 软文 |
| `doc-coauthoring` | **文档共创流**。引导用户完成从背景收集、结构细化到读者测试的编写。 | 提案书、需求文档、白皮书 |
| `multi-agent-debate` | **多视角辩论**。模拟 15 种专家/普通人人设进行三轮深度讨论，自动生成简报。 | 复杂决策、多角观点碰撞 |

### 💻 开发与技术 (Development & Tech)
专注于开发流程优化、自动化工具链与高频信息检索。

| 技能名称 | 核心说明与功能 | 适用场景 |
| :--- | :--- | :--- |
| `ducksearch` | **命令行搜索工具**。基于 DuckDuckGo 抓取纯净网页内容，支持 MCP 服务器。 | 快速检索、程序自动化取数 |
| `last30days` | **跨平台热点搜索**。深度抓取 Reddit, X, YouTube 等 17+ 平台的月度热门话题。 | 行业趋势分析、舆情追踪 |
| `obsidian-plugin-release` | **插件发布自动化**。管理版本升级、GitHub Release 及 BRAT 插件地址同步。 | Obsidian 插件开发者工具 |

## 📦 安装 (Installation)

### 选项 1: 手动安装（推荐 - 获取全部技能）
如果你希望一次性获取仓库中的所有技能，或者你的环境不支持 `npx`，建议直接克隆仓库：

1. 克隆仓库到本地：
   ```bash
   git clone https://github.com/rezonegame/yh-skills.git
   ```
2. 将克隆下来的文件夹路径配置到你的 AI Agent (如 Claude Desktop, Cursor 等) 的技能目录中，或者直接将需要的技能文件夹复制过去。

### 选项 2: 使用 Skills CLI（安装特定技能）
如果你只想安装其中的某一个技能（例如 `boardgame-design`），可以使用 `npx skills` 命令：

```bash
# 安装单个技能 (请将 @ 后面的名称替换为具体技能目录名)
npx skills add rezonegame/yh-skills@boardgame-design
```

### 选项 3: 直接下载
你也可以直接下载 ZIP 压缩包：
1. 访问 [Github 仓库页面](https://github.com/rezonegame/yh-skills)
2. 点击绿色的 **Code** 按钮
3. 选择 **Download ZIP**
4. 解压到你的技能目录

## �🚀 使用说明

这些技能通常以文件夹形式存在，每个文件夹内包含一个 `SKILL.md` 核心描述文件以及可能的辅助脚本或资源。

要使用这些技能：
1. 确保你的 AI Agent 环境支持加载本地技能或 MCP (Model Context Protocol)。
2. 根据需要导入相应的技能文件夹。
3. 参考各技能目录下的 `SKILL.md` 文件了解详细的触发指令和使用方法。

## 📦 仓库维护

本仓库由自动化脚本同步和维护。
