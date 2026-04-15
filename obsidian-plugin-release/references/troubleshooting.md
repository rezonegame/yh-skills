# 常见问题排查

## 构建相关

### npm install 失败

**症状**：`ERESOLVE unable to resolve dependency tree`

**原因**：项目使用 pnpm/bun/yarn 等非标准包管理器，依赖树与 npm 不兼容。

**解决方案**：
```bash
npm install --legacy-peer-deps
```

若仍然失败，尝试忽略脚本：
```bash
npm install --legacy-peer-deps --ignore-scripts
```

---

### 项目依赖 pnpm/bun/uv 但本地未安装

**症状**：`'pnpm' is not recognized` 或 `Error [ERR_MODULE_NOT_FOUND]`

**解决方案**：使用 esbuild fallback 构建（见 SKILL.md 步骤 3 "Fallback 构建"）。

核心步骤：
1. `npm install esbuild`
2. 创建 `esbuild-build.mjs`
3. `node esbuild-build.mjs`

---

### esbuild 报错 "No loader is configured for .md files"

**症状**：项目中 TypeScript 代码 import 了 `.md`、`.py`、`.html` 等非标准文件。

**解决方案**：在 esbuild 配置中添加对应的 loader：

```javascript
loader: {
  '.ts': 'ts',
  '.md': 'text',
  '.py': 'text',
  '.html': 'text',
  '.svg': 'text',
  '.css': 'css'
}
```

---

### node_modules 安装后目录不完整

**症状**：`npm install` 成功但 `node_modules` 中缺少包。

**原因**：Windows 长路径限制 或 workspace 配置冲突。

**解决方案**：
```bash
# 清理后重装
Remove-Item -Recurse -Force node_modules  # PowerShell
npm install
```

## 发布相关

### BRAT 报 "no manifest.json"

**排查清单**：
1. 确认 `manifest.json` 在仓库**根目录**（非子目录）
2. 确认 Release Assets 中包含 `manifest.json`
3. 确认 `manifest.json` 包含必要字段（`id`、`version`、`name`）
4. 检查 `.gitignore` 是否屏蔽了 `manifest.json`

---

### Release Assets 缺少文件

**原因**：手动创建 Release 时忘记上传，或 GitHub Actions 构建失败。

**解决方案**：
1. 进入 Release 编辑页面
2. 在 "Attach binaries" 区域上传缺失文件
3. 点击 "Update release"

---

### git push 被拒绝

**症状**：`rejected - non-fast-forward`

**解决方案**：
```bash
git pull --rebase origin main
git push origin main
git push origin <TAG>
```

---

### tag 已存在

**症状**：`fatal: tag '<VERSION>' already exists`

**解决方案**：删除旧 tag 后重新创建：
```bash
git tag -d <VERSION>
git push origin :refs/tags/<VERSION>
git tag <VERSION>
git push origin <VERSION>
```

## 环境相关

### Windows PowerShell 语法差异

PowerShell 不支持 `&&` 连接符，使用 `;` 代替：
```powershell
# 错误
npm install && npm run build

# 正确
npm install; npm run build
```

删除目录使用：
```powershell
Remove-Item -Recurse -Force node_modules
```
