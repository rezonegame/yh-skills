---
name: skill-manager
description: 技能包管理器。当用户要求"查找技能"、"搜索技能"、"安装技能"、"浏览社区技能"、"寻找技能"时使用此技能。从包含31,767+个社区技能的数据库中搜索、浏览和安装技能，支持SVN导出、Git稀疏检出和HTTP回退方法，自动下载完整技能文件夹。
---

# Skill Manager

技能包管理器，用于从31,767+个社区技能中搜索、浏览和安装技能。

## 🤖 执行流程

### 第1步：解析搜索需求

从用户输入中提取搜索关键词。常见模式：
- "I need a skill for [topic]"
- "Find me a skill to help with [topic]"
- "Search for skills related to [topic]"
- "Show me skills by [author]"
- "查找[主题]相关的技能"

### 第2步：执行搜索

使用搜索脚本查询技能数据库：

```bash
cd C:\Users\wudao\.claude\skills\skill-manager
node src/index.js search "<query>" --limit 10
```

**搜索参数**：
- `<query>` - 搜索关键词
- `--limit N` - 返回结果数量（默认10）

### 第3步：展示搜索结果

格式化显示匹配的技能列表：

```markdown
## 搜索结果

1. **skill-name** (by author)
   ⭐ 1,250 stars | 🔀 342 forks
   📝 Description text...
   🔗 https://github.com/author/repo

2. **another-skill** (by author)
   ⭐ 856 stars | 🔀 123 forks
   ...
```

使用 AskUserQuestion 让用户选择要安装的技能。

### 第4步：安装选定技能

根据用户选择，执行安装命令：

```bash
node src/index.js install "<skill-name>" --author "<author>"
```

安装脚本会自动：
1. 检测可用的下载方法（SVN > Git > HTTP）
2. 下载完整技能文件夹到 `~/.claude/skills/`
3. 显示安装结果和使用的下载方法

### 第5步：验证安装

确认技能已正确安装：
- 检查 `~/.claude/skills/<skill-name>/SKILL.md` 存在
- 提示用户重启 Claude Code 以加载新技能

---

## 📁 技能数据库

技能数据库位于 `data/all_skills_with_cn.json`（30.33 MB），包含：
- 31,767 个技能
- 99.95% 带中文翻译
- GitHub 统计数据（stars, forks）

---

## 🔧 下载方法

技能自动选择最佳可用方法：

| 方法 | 速度 | 下载内容 | 要求 |
|------|------|----------|------|
| **SVN Export** | ⚡⚡⚡ | 完整技能文件夹 | SVN 客户端 |
| **Git Sparse Checkout** | ⚡⚡ | 完整技能文件夹 | Git 客户端 |
| **HTTP Only** | ⚡ | 仅 SKILL.md | 无 |

推荐安装 SVN 以获得最佳体验：
- Windows: `choco install svn` 或 TortoiseSVN
- Mac: `brew install svn`
- Linux: `apt-get install subversion`

---

## 📚 参考资源

### 详细文档

- **`references/installation-methods.md`** - 下载方法详细说明和故障排除
- **`references/technical-details.md`** - 搜索算法和实现细节
- **`references/database-schema.md`** - 技能数据库结构

### 示例用法

**搜索 Python 测试技能**：
```
User: I need a skill for Python testing
Assistant: [执行搜索，显示 pytest-helper 等结果]
User: Install the first one
Assistant: [使用 SVN 下载完整技能]
```

**按作者搜索**：
```
User: Show me skills by anthropic
Assistant: [搜索并显示 Anthropic 相关技能]
```

---

## ⚙️ 技术要求

- Node.js >= 14.0.0
- Internet 连接
- 推荐：SVN 客户端（或 Git 作为备选）

---

## 📝 使用命令

搜索：
```bash
node src/index.js search "<query>" [--limit N]
```

安装：
```bash
node src/index.js install "<skill-name>" --author "<author>"
```

---

**版本**: 2.0.0
**更新**: 支持 SVN 导出、Git 稀疏检出、自动方法检测
