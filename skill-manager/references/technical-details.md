# 技术实现细节

## 搜索算法

### 加权评分系统

搜索使用多字段加权匹配算法：

```javascript
function searchSkills(query, limit = 10) {
  const lowerQuery = query.toLowerCase();
  const results = [];

  for (const skill of skillsDatabase) {
    let score = 0;

    // 名称匹配（最高权重：10分）
    if (skill.name?.toLowerCase().includes(lowerQuery)) {
      score += 10;
    }

    // 描述匹配（中等权重：5分）
    if (skill.description?.toLowerCase().includes(lowerQuery)) {
      score += 5;
    }

    // 作者匹配（较低权重：3分）
    if (skill.author?.toLowerCase().includes(lowerQuery)) {
      score += 3;
    }

    if (score > 0) {
      results.push({ skill, score });
    }
  }

  // 按评分和受欢迎程度排序
  return results
    .sort((a, b) => {
      // 先按搜索评分排序
      if (b.score !== a.score) return b.score - a.score;
      // 评分相同时按 stars 排序
      return (b.skill.stars || 0) - (a.skill.stars || 0);
    })
    .slice(0, limit)
    .map(r => r.skill);
}
```

### 排序逻辑

1. **搜索评分** - 匹配度越高越好
2. **Stars 数量** - 评分相同时，更受欢迎的优先
3. **最近更新** - 综合考虑活跃度

---

## 数据库结构

### 技能记录格式

```json
{
  "name": "skill-name",
  "description": "技能描述",
  "description_cn": "中文描述",
  "author": "author-name",
  "stars": 1234,
  "forks": 56,
  "repo": "https://github.com/author/repo",
  "path": "skills/skill-name",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 技能名称 |
| `description` | string | 英文描述 |
| `description_cn` | string | 中文描述 |
| `author` | string | 作者或组织 |
| `stars` | number | GitHub stars 数量 |
| `forks` | number | GitHub forks 数量 |
| `repo` | string | GitHub 仓库 URL |
| `path` | string | 技能在仓库中的路径 |
| `updated_at` | string | 最后更新时间（ISO 8601） |

### 数据库统计

- **总记录数**: 31,767
- **中文翻译覆盖率**: 99.95%
- **文件大小**: 30.33 MB（压缩 JSON）
- **平均记录大小**: ~1 KB

---

## 安装流程

### 1. 方法检测

```javascript
function detectBestMethod() {
  // 检测 SVN
  try {
    execSync('svn --version', { stdio: 'ignore' });
    return 'svn';
  } catch (e) {}

  // 检测 Git
  try {
    execSync('git --version', { stdio: 'ignore' });
    return 'git';
  } catch (e) {}

  // 回退到 HTTP
  return 'http';
}
```

### 2. 下载实现

#### SVN Export

```javascript
function downloadWithSVN(repo, skillPath, targetDir) {
  const svnUrl = `https://github.com/${repo}/trunk/${skillPath}`;
  execSync(`svn export "${svnUrl}" "${targetDir}"`, {
    stdio: 'inherit'
  });
}
```

#### Git Sparse Checkout

```javascript
function downloadWithGit(repo, skillPath, targetDir) {
  execSync(`git init "${targetDir}"`, { stdio: 'ignore' });
  execSync(`git -C "${targetDir}" config core.sparseCheckout true`, { stdio: 'ignore' });
  execSync(`echo "${skillPath}/*" > "${targetDir}/.git/info/sparse-checkout"`, { shell: true });
  execSync(`git -C "${targetDir}" remote add origin https://github.com/${repo}.git`, { stdio: 'ignore' });
  execSync(`git -C "${targetDir}" pull origin main`, { stdio: 'inherit' });
}
```

#### HTTP Download

```javascript
function downloadWithHTTP(repo, skillPath, targetDir) {
  const url = `https://raw.githubusercontent.com/${repo}/main/${skillPath}/SKILL.md`;
  const filePath = path.join(targetDir, 'SKILL.md');

  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(filePath);
    https.get(url, (response) => {
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve();
      });
    }).on('error', (err) => {
      fs.unlink(filePath, () => {});
      reject(err);
    });
  });
}
```

### 3. 验证安装

```javascript
function verifyInstallation(skillName, installDir) {
  const skillPath = path.join(installDir, skillName, 'SKILL.md');

  if (!fs.existsSync(skillPath)) {
    throw new Error(`SKILL.md not found at ${skillPath}`);
  }

  // 检查 frontmatter
  const content = fs.readFileSync(skillPath, 'utf-8');
  if (!content.match(/^---\s*\nname:/m)) {
    throw new Error(`Invalid SKILL.md format`);
  }

  return true;
}
```

---

## CLI 接口

### 命令结构

```bash
node src/index.js <command> [options]
```

### 可用命令

#### search - 搜索技能

```bash
node src/index.js search "<query>" [--limit N]
```

**参数**：
- `query` - 搜索关键词（必需）
- `--limit` - 返回结果数量（默认：10）

**输出**：
```json
[
  {
    "name": "skill-name",
    "author": "author",
    "stars": 1234,
    "forks": 56,
    "description": "...",
    "repo": "https://github.com/..."
  }
]
```

#### install - 安装技能

```bash
node src/index.js install "<skill-name>" --author "<author>" [--method <svn|git|http>]
```

**参数**：
- `skill-name` - 技能名称（必需）
- `--author` - 技能作者（必需）
- `--method` - 强制使用指定下载方法（可选）

**输出**：
```
✓ Method used: SVN
✓ Files installed: SKILL.md, scripts/, references/
✓ Installed to: /home/user/.claude/skills/skill-name/
```

---

## 错误处理

### 常见错误

#### 数据库加载失败

```javascript
try {
  const data = fs.readFileSync(SKILLS_DB_PATH, 'utf-8');
  skillsDatabase = JSON.parse(data);
} catch (error) {
  console.error(`✗ Failed to load skills database: ${error.message}`);
  console.error(`Please ensure ${SKILLS_DB_PATH} exists.`);
  process.exit(1);
}
```

#### 无搜索结果

```javascript
const results = searchSkills(query);

if (results.length === 0) {
  console.log(`No skills found matching "${query}"`);
  console.log('Try:');
  console.log('  - Using different keywords');
  console.log('  - Searching in English or Chinese');
  console.log('  - Browsing by author');
  process.exit(0);
}
```

#### 安装失败

```javascript
try {
  downloadSkill(skill, targetDir, method);
} catch (error) {
  console.error(`✗ Installation failed: ${error.message}`);
  console.error('Troubleshooting:');
  console.error('  - Check internet connection');
  console.error('  - Verify the skill name and author');
  console.error('  - Try a different download method with --method');
  console.error('  - See references/installation-methods.md for details');
  process.exit(1);
}
```

---

## 性能优化

### 数据库索引

搜索遍历全部 31,767 条记录，但通过以下方式优化：

1. **提前退出** - 找到足够结果后停止
2. **惰性加载** - 只在需要时解析完整记录
3. **内存缓存** - 数据库保持常驻内存

### 并发下载

未来版本可能支持并发下载多个技能：

```javascript
// 计划中的功能
async function installMultiple(skills) {
  await Promise.all(
    skills.map(skill => downloadSkill(skill))
  );
}
```

---

## 扩展性

### 添加新的下载方法

```javascript
const downloadMethods = {
  svn: downloadWithSVN,
  git: downloadWithGit,
  http: downloadWithHTTP,
  // 添加新方法
  mercurial: downloadWithHg
};

function downloadSkill(repo, path, targetDir, method) {
  const downloader = downloadMethods[method];
  if (!downloader) {
    throw new Error(`Unknown download method: ${method}`);
  }
  return downloader(repo, path, targetDir);
}
```

### 自定义搜索权重

```javascript
const searchWeights = {
  name: 10,
  description: 5,
  author: 3,
  tags: 2  // 新增字段
};
```
