---
name: obsidian-plugin-release
description: Obsidian 插件自动化发布。支持版本管理、GitHub Release 及 BRAT 插件同步。
---

# Obsidian 插件发布流程

协助将本地开发的 Obsidian 插件同步到 GitHub 仓库，创建符合 BRAT 规范的发行版，确保插件可通过 BRAT 正常拉取和更新。

## 核心工作流（6 步）

### 步骤 1：验证插件结构

运行校验脚本确认插件目录合法：

```bash
node <skill_path>/scripts/validate_plugin.js
```

手动检查清单：
- `manifest.json` 存在且包含 `id`、`version`、`name`、`minAppVersion`
- `package.json` 存在且 `version` 与 `manifest.json` 一致
- `.git` 目录存在且远程指向 GitHub

### 步骤 2：升级版本号

运行版本自增脚本：

```bash
node <skill_path>/scripts/bump_version.js <NEW_VERSION>
```

该脚本自动更新以下文件中的版本号：
- `package.json` → `version` 字段
- `manifest.json` → `version` 字段
- `manifest-beta.json` → `version` 字段（若存在）
- `versions.json` → 追加新版本映射
- `README.md` → 替换旧版本号字符串

### 步骤 3：构建编译

**标准构建**（优先尝试）：

```bash
npm run build
```

**Fallback 构建**（当标准构建失败时）：

当项目依赖 pnpm、bun、uv 等本地未安装的工具时，创建 `esbuild-build.mjs` 作为替代：

```javascript
import esbuild from 'esbuild';
await esbuild.build({
  entryPoints: ['src/main.ts'],
  bundle: true,
  outfile: 'main.js',
  platform: 'node',
  external: ['obsidian', 'electron', '@codemirror/*', '@lezer/*'],
  format: 'cjs',
  loader: { '.ts': 'ts', '.md': 'text', '.py': 'text', '.html': 'text', '.svg': 'text' }
});
```

执行前确保安装 esbuild：`npm install esbuild`，然后运行 `node esbuild-build.mjs`。

构建完成后验证产物存在：
- `main.js`（必须，核心逻辑）
- `styles.css`（若项目有样式文件）

### 步骤 4：更新 README

在 `README.md` 中追加或更新变更记录。推荐格式：

```markdown
## Changelog

### v<NEW_VERSION> (YYYY-MM-DD)
- 新增：<功能描述>
- 修复：<问题描述>
- 优化：<改进描述>
```

### 步骤 5：同步 GitHub

提交代码并推送至远程仓库：

```bash
git add -f main.js manifest.json styles.css
git add .
git commit -m "release: <NEW_VERSION>"
git tag <NEW_VERSION>
git push origin main
git push origin <NEW_VERSION>
```

> **关键**：使用 `git add -f` 强制添加编译产物。多数项目的 `.gitignore` 会排除 `main.js`，但 BRAT 需要从仓库根目录或 Release Assets 获取该文件。

### 步骤 6：创建 GitHub Release 并上传资产

通过浏览器或 `gh` CLI 创建发行版：

**方式 A（推荐）—— GitHub Actions 自动发布**：

将 `references/release-workflow.yml` 复制到项目的 `.github/workflows/release.yml`。推送 tag 后自动触发 Release 创建与资产上传。

**方式 B —— 手动创建**：

1. 访问 `https://github.com/<owner>/<repo>/releases/new`
2. 选择刚推送的 tag
3. 填写标题（版本号）和发布说明
4. **上传 Assets**（至关重要）：
   - `main.js`
   - `manifest.json`
   - `styles.css`（若存在）
5. 发布 Release

**方式 C —— gh CLI**：

```bash
gh release create <NEW_VERSION> main.js manifest.json styles.css --title "<NEW_VERSION>" --notes "Release <NEW_VERSION>"
```

### 发布后验证

确认以下条件全部满足：
1. Release 页面显示 `main.js`、`manifest.json`（、`styles.css`）在 Assets 中
2. 仓库根目录包含 `manifest.json`
3. 在 Obsidian BRAT 中添加仓库地址，确认可正常安装

## BRAT 兼容性要点

BRAT 按以下优先级查找插件文件：
1. **Release Assets**（最新 Release 中的 `main.js` + `manifest.json`）
2. **仓库根目录**（main 分支中的文件）

> 缺少任一文件都会导致 BRAT 报错 "This does not seem to be an obsidian plugin, as there is no manifest.json file"。详见 `references/brat-compatibility.md`。

## GitHub Actions 自动发布

将 `references/release-workflow.yml` 的内容复制到项目的 `.github/workflows/release.yml`，推送 tag 后即可自动构建并发布 Release。详细配置见该文件注释。

## 附加资源

### 脚本

- **`scripts/bump_version.js`** — 版本号自增，同时更新 `package.json`、`manifest.json`、`versions.json` 和 `README.md`
- **`scripts/validate_plugin.js`** — 校验插件目录结构和 BRAT 兼容性

### 参考文档

- **`references/release-workflow.yml`** — GitHub Actions 自动发布模板
- **`references/brat-compatibility.md`** — BRAT 安装机制与兼容性要求
- **`references/troubleshooting.md`** — 构建失败、资产缺失等常见问题排查
