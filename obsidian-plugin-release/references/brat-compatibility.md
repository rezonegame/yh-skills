# BRAT 兼容性要求

## BRAT 安装机制

BRAT（Beta Reviewers Auto-update Tester）是 Obsidian 社区用于测试 beta 版插件的工具。其安装流程如下：

1. 用户在 BRAT 中输入 GitHub 仓库地址（如 `owner/repo`）
2. BRAT 查找最新 GitHub Release
3. 从 Release **Assets** 中下载：`main.js`、`manifest.json`、`styles.css`
4. 若 Release Assets 中缺少文件，BRAT 回退到仓库**根目录**（默认分支）查找
5. 缺少 `manifest.json` 则直接报错："This does not seem to be an obsidian plugin"

## 必须的文件

| 文件 | 必须 | 说明 |
|---|---|---|
| `manifest.json` | ✅ 是 | 包含 `id`、`version`、`name`、`minAppVersion` |
| `main.js` | ✅ 是 | 编译后的插件入口 |
| `styles.css` | ❌ 可选 | 插件自定义样式 |

## manifest.json 格式要求

```json
{
  "id": "plugin-id",
  "name": "Plugin Name",
  "version": "1.0.0",
  "minAppVersion": "0.15.0",
  "description": "Plugin description",
  "author": "Author Name",
  "authorUrl": "https://github.com/author",
  "isDesktopOnly": false
}
```

关键字段：
- `id`：插件唯一标识，必须与 Obsidian 社区插件列表中的 ID 一致
- `version`：语义化版本号，BRAT 用此判断是否有更新
- `minAppVersion`：最低 Obsidian 版本要求

## Release Assets 优先级

BRAT 的文件查找优先级：

```
1. Latest Release → Assets 中的 main.js / manifest.json
2. 仓库根目录 → 默认分支中的 main.js / manifest.json
```

> **最佳实践**：始终将编译产物上传到 Release Assets。仅依赖仓库根目录可能在 BRAT 的某些版本中出现兼容性问题。

## .gitignore 冲突

许多 Obsidian 插件模板的 `.gitignore` 包含 `main.js`，这会阻止编译产物被提交到仓库。

解决方案：
- 使用 `git add -f main.js` 强制添加
- 或从 `.gitignore` 中移除 `main.js`
- 推荐方案：依赖 GitHub Actions 自动构建并上传 Release Assets，无需手动提交 `main.js`

## BRAT 更新检测

BRAT 通过比较本地 `manifest.json` 中的 `version` 与 GitHub Release tag 来检测更新。确保：
- Release tag 名称与 `manifest.json` 中的 `version` 一致
- 每次发布递增版本号
