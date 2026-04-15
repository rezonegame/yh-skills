# yh-slides

统一的演示文稿技能，支持：

- `Path A`: 编辑式 HTML -> 可编辑 PPTX
- `Path B`: 全 AI 视觉 -> PPTX
- `Path C`: 单文件 HTML
- `Path D`: 富交互 HTML

## 新增

`Path B` 现在分为两种模式：

- `标准版`: 整页 AI 图片直接组装为 PPTX
- `高级版`: 整页 AI 图片 -> 清背景 -> 提取文字框与样式 -> 导出可编辑 PPTX

## 关键规则

- 用户选择 `Path B` 时，必须继续确认是 `标准版` 还是 `高级版`
- 如果用户要求“Path B 且文字可编辑”，优先推荐 `Path B 高级版`
- 不要因为“文字可编辑”自动改走 `Path A`

## 主要脚本

- `scripts/generate_image.py`: 生成、编辑、批量生成、风格提取、清背景
- `scripts/create_slides.py`: Path B 标准版组装
- `scripts/build_pptx.py`: Path B 高级版可编辑导出

## Path B 高级版示例

```bash
uv run ~/.claude/skills/yh-slides/scripts/build_pptx.py \
  --slides "C:\PPTX\demo\images\slide-01.png" "C:\PPTX\demo\images\slide-02.png" \
  --auto-clean-bg \
  --bg-dir "C:\PPTX\demo\backgrounds" \
  --dump-json "C:\PPTX\demo\output\text-data.json" \
  --output "C:\PPTX\demo\output\demo-editable.pptx"
```
