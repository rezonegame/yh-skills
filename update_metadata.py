
import os

skills = {
    'boardgame-design': '桌游设计专家技能。使用 5-Component Filter（清晰度、策略、互动、满意度、适配）来评估和设计游戏机制。',
    'boardgame-boards': '游戏板和地图设计指南。涵盖布局系统、折叠模式、信息 density 和路径清晰度。',
    'boardgame-boxes': '桌游包装盒设计。提供尺寸选择、结构设计、封面艺术布局和生产规格指导。',
    'boardgame-cards': '卡牌设计指南。涵盖卡牌尺寸、正面布局层级、图标系统、背面对齐和整版排版。',
    'boardgame-components': '通用配件设计。包括标记 (Tokens)、指示物、玩家辅助卡、规则书和记分板的设计规范。',
    'boardgame-tiles': '方块 (Tiles) 设计技能。专注于六边形、方形等方块的边缘连接系统、旋转兼容性和模切考虑。',
    'boardgame-ralph-loop': '基于 Ralph Loop 方法论的自主迭代设计技能。提供自动化的测试和设计改进循环。',
    'boardgame-writer': '智研家桌游公众号长文写作。支持 7 种作者人设（咕咚来了、苏微等），提供深度桌游评测与推荐。',
    'meeplelm': 'MeepleLM 虚拟玩家测试技能。基于 MeepleLM 框架，使用 5 种玩家人设和 MDA 推理链模拟桌游玩家评测。',
    'gamified-course-designer': '游戏化课程设计师。基于布卢姆分类法自动生成教学与游戏化方案，提升课程趣味性。',
    'humanizer-zh': '文本去 AI 痕迹与深度润色。剔除虚夸词汇，注入真实深度“人味”，非常适用于书评与长评。',
    'geo-content-optimizer': 'GEO 内容架构师。针对 RAG 系统（Perplexity/SearchGPT）优化，提升事实密度与语义结构。',
    'merge-drafts': '多稿合并专家。将多份草稿合并为一份统一、完整、直接交付的高质量文章。',
    'scientific-writing': '科学写作核心技能。遵循 IMRAD 结构，确保符合学术出版标准。',
    'scientific-critical-thinking': '科学批判性思维。用于评估研究的严谨性、方法论及偏差检测。',
    'literature-review': '系统性文献综述技能。支持跨数据库检索、综合和引用验证。',
    'openalex-database': 'OpenAlex 数据库查询。用于搜索学术论文、追踪趋势和文献计量分析。',
    'content-research-writer': '内容研究与协作写作。辅助打捞事实、优化 Hook 并提供分段反馈。',
    'content-strategist': 'SEO 内容策略专家。创建经过搜索引擎优化的内容，涵盖关键词整合与结构优化。',
    'doc-coauthoring': '文档共创工作流。引导用户完成从背景收集到读者测试的完整编写流程。',
    'multi-agent-debate': '多视角角色讨论框架。模拟 15 种人设进行三轮深度讨论，支持自动调研。',
    'ducksearch': '命令行网页搜索工具。基于 DuckDuckGo，支持抓取网页内容及作为 MCP 服务器。',
    'last30days': '跨平台趋势搜索。深度分析 Reddit, X, YouTube 等平台过去 30 天的热门讨论。',
    'obsidian-plugin-release': 'Obsidian 插件自动化发布。支持版本管理、GitHub Release 及 BRAT 插件同步。'
}

repo_root = r"d:\Github\yh-skills"

for name, desc in skills.items():
    file_path = os.path.join(repo_root, name, "SKILL.md")
    if os.path.exists(file_path):
        print(f"Updating {name}/SKILL.md...")
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        in_description = False
        updated = False
        for line in lines:
            if line.startswith('description:'):
                new_lines.append(f"description: {desc}\n")
                updated = True
                in_description = True
            elif in_description and (line.startswith('---') or line.strip() == ''):
                in_description = False
                new_lines.append(line)
            elif not in_description:
                new_lines.append(line)
        
        if not updated:
            # If no description field, add it after name
            for i, line in enumerate(new_lines):
                if line.startswith('name:'):
                    new_lines.insert(i+1, f"description: {desc}\n")
                    break

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    else:
        print(f"Warning: File not found: {file_path}")
