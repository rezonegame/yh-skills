# 技能数据库结构

## 数据库文件

**位置**: `data/all_skills_with_cn.json`
**大小**: 30.33 MB
**格式**: JSON 数组
**编码**: UTF-8

---

## 记录格式

### 完整示例

```json
{
  "name": "pytest-helper",
  "description": "Helps write and run pytest tests with fixtures and assertions for Python projects",
  "description_cn": "帮助编写和运行 pytest 测试，包含 fixtures 和 assertions 支持",
  "author": "python-community",
  "stars": 1250,
  "forks": 342,
  "repo": "https://github.com/python-community/pytest-helper",
  "path": "skills/pytest-helper",
  "updated_at": "2024-01-15T10:30:00Z",
  "language": "Python",
  "license": "MIT",
  "tags": ["testing", "python", "pytest", "tdd"]
}
```

---

## 字段说明

### 必需字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `name` | string | 技能名称（kebab-case） | `"pytest-helper"` |
| `description` | string | 英文描述 | `"Helps write..."` |
| `author` | string | 作者或组织名 | `"python-community"` |
| `repo` | string | GitHub 仓库 URL | `"https://github.com/..."` |
| `path` | string | 技能在仓库中的相对路径 | `"skills/pytest-helper"` |

### 可选字段

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `description_cn` | string | 中文描述 | `null` |
| `stars` | number | GitHub stars 数量 | `0` |
| `forks` | number | GitHub forks 数量 | `0` |
| `updated_at` | string | ISO 8601 时间戳 | `null` |
| `language` | string | 主要编程语言 | `null` |
| `license` | string | 开源协议 | `null` |
| `tags` | array | 关键标签 | `[]` |

---

## 数据统计

### 覆盖率

| 字段 | 覆盖率 | 说明 |
|------|--------|------|
| `name` | 100% | 所有记录都有名称 |
| `description` | 100% | 所有记录都有英文描述 |
| `description_cn` | 99.95% | 几乎所有记录有中文翻译 |
| `stars` | 95.2% | 大部分有 GitHub 统计 |
| `forks` | 95.2% | 大部分有 GitHub 统计 |
| `tags` | 78.3% | 部分有标签 |

### 分布

#### 按语言

| 语言 | 技能数量 | 占比 |
|------|----------|------|
| JavaScript | 8,234 | 25.9% |
| Python | 6,891 | 21.7% |
| TypeScript | 4,567 | 14.4% |
| Shell | 3,210 | 10.1% |
| 其他 | 8,865 | 27.9% |

#### 按星级

| Stars 范围 | 技能数量 | 占比 |
|------------|----------|------|
| 0 | 15,432 | 48.6% |
| 1-10 | 8,765 | 27.6% |
| 11-100 | 5,432 | 17.1% |
| 101-1000 | 1,876 | 5.9% |
| 1000+ | 262 | 0.8% |

#### 按作者

| 作者类型 | 技能数量 | 说明 |
|----------|----------|------|
| 个人 | 19,234 | 个人开发者 |
| 组织 | 8,456 | GitHub 组织 |
| 未知 | 4,077 | 无明确归属 |

---

## 索引建议

### 搜索优化

当前实现遍历全表，未来可添加索引：

```javascript
// 名称索引（精确匹配）
const nameIndex = new Map(
  skills.map(s => [s.name.toLowerCase(), s])
);

// 作者索引（作者搜索）
const authorIndex = new Map();
skills.forEach(skill => {
  if (!authorIndex.has(skill.author)) {
    authorIndex.set(skill.author, []);
  }
  authorIndex.get(skill.author).push(skill);
});
```

### 标签索引

```javascript
// 标签索引（分类浏览）
const tagIndex = new Map();
skills.forEach(skill => {
  skill.tags?.forEach(tag => {
    if (!tagIndex.has(tag)) {
      tagIndex.set(tag, []);
    }
    tagIndex.get(tag).push(skill);
  });
});
```

---

## 数据更新

### 更新频率

- **完整更新**: 每月一次
- **增量更新**: 每周一次
- **热门技能**: 每日更新

### 更新流程

1. **抓取** - 从 GitHub API 获取技能仓库列表
2. **解析** - 提取 SKILL.md frontmatter 和仓库信息
3. **翻译** - 自动翻译描述为中文
4. **验证** - 检查技能可访问性
5. **发布** - 生成新的 JSON 文件

### 数据源

- GitHub Topics 搜索
- Claude Code 技能仓库
- 社区提交
- 手动整理

---

## 使用示例

### 查询操作

```javascript
// 加载数据库
const skills = JSON.parse(
  fs.readFileSync('data/all_skills_with_cn.json', 'utf-8')
);

// 按名称查找
const skill = skills.find(s => s.name === 'pytest-helper');

// 按作者筛选
const byAuthor = skills.filter(s => s.author === 'anthropic');

// 按星级排序
const popular = skills
  .filter(s => s.stars > 100)
  .sort((a, b) => b.stars - a.stars)
  .slice(0, 10);

// 按标签筛选
const testing = skills.filter(s =>
  s.tags?.includes('testing')
);
```

### 搜索操作

```javascript
// 多字段搜索
function search(query) {
  const q = query.toLowerCase();
  return skills.filter(s =>
    s.name?.toLowerCase().includes(q) ||
    s.description?.toLowerCase().includes(q) ||
    s.author?.toLowerCase().includes(q)
  );
}
```

---

## 数据验证

### 必需字段检查

```javascript
function validateSkill(skill) {
  const required = ['name', 'description', 'author', 'repo', 'path'];
  const missing = required.filter(field => !skill[field]);

  if (missing.length > 0) {
    throw new Error(`Missing required fields: ${missing.join(', ')}`);
  }

  // URL 格式验证
  if (!skill.repo.startsWith('https://github.com/')) {
    throw new Error('Invalid repo URL');
  }

  // 名称格式验证（kebab-case）
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(skill.name)) {
    throw new Error('Invalid skill name format');
  }

  return true;
}
```

### 去重

```javascript
// 按名称和作者去重
const uniqueSkills = Array.from(
  new Map(
    skills.map(s => [`${s.author}/${s.name}`, s])
  ).values()
);
```

---

## 导出格式

### CSV 导出

```javascript
const csv = [
  ['name', 'author', 'stars', 'description'],
  ...skills.map(s => [
    s.name,
    s.author,
    s.stars,
    `"${s.description.replace(/"/g, '""')}"`
  ])
].map(row => row.join(',')).join('\n');

fs.writeFileSync('skills.csv', csv);
```

### 简化 JSON

```javascript
// 只包含核心字段
const simple = skills.map(s => ({
  name: s.name,
  author: s.author,
  stars: s.stars
}));

fs.writeFileSync('skills-simple.json', JSON.stringify(simple));
```

---

## 维护指南

### 添加新技能

1. 在 GitHub 上创建技能仓库
2. 确保包含有效的 SKILL.md
3. 提交到技能数据库项目
4. 等待下次更新周期

### 更新技能信息

技能信息自动从 GitHub 同步，包括：
- Stars 和 forks 数量
- 最后更新时间
- 仓库状态

### 报告问题

发现数据库问题：
1. 在项目仓库提交 issue
2. 提供技能名称和错误描述
3. 等待修复和重新发布
