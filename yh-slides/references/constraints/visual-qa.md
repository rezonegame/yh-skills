# Visual QA

> 用途：Path C/D/E 的截图质量检查。Path A/B 可按高保真交付需要选择性使用；Ian 中文手绘技术解释的 2B/2C 交付强制执行。

## 使用时机

- Path C：生成单文件 HTML 后强制执行。
- Path D：生成多文件 HTML 后强制执行。
- Path E：构建本地 React Deck 后强制执行。
- Path A/B：如果用户要求高保真视觉验收，或需要交付前预览截图，建议执行。

## 最低检查项

P0 必须确认：

- 每页都能打开并截图。
- 没有白屏、空页或低方差近空白页。
- 没有明显截断、遮挡、重叠或文字溢出。
- 截图 hash 没有异常重复；重复必须是有意设计。
- 生成 contact sheet 并人工扫一遍整体节奏。

## 截图建议

使用 1920×1080 视口。命令可按当前环境调整：

```bash
chromium --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --window-size=1920,1080 \
  --screenshot="screenshots/page-01.png" \
  "http://127.0.0.1:5173/?p=1"
```

如果是本地 HTML 文件或不同路由，替换 URL 即可。关键是每一页都必须实际渲染到截图。

## Hash 与近空白检测

可用 Python/Pillow 或等价工具检查：

- 图片尺寸是否为 1920×1080 或预期视口尺寸。
- 每张图的像素方差；方差极低通常意味着白屏或纯色空页。
- perceptual hash 或普通文件 hash 是否大量重复。

不要把重复 hash 直接当作失败；先目视确认。封面和结束页不应完全相同，除非用户明确要求。

## Contact Sheet

contact sheet 是交付前最快的人工扫读方式。建议每行 4-5 页，缩略图下方标注页码。

统一使用本地脚本生成，并同时输出 QA 报告：

```bash
python scripts/create_contact_sheet.py screenshots \
  --pattern "*.png" \
  --output output/contact-sheet.png \
  --report output/contact-sheet-report.json \
  --columns 4 \
  --strict
```

文件按自然序排列；`--strict` 在检测到近空白页或像素重复页时返回非零。重复可能是有意设计，但必须先目视确认，再决定是否取消 strict 重新记录结果。

扫读时看：

- 节奏是否有变化：封面、正文、反差、图表、总结是否交替。
- 是否连续多页长得一样。
- 是否有明显空页、坏图、文字压边。
- 是否和 Step 4 选择的质量基线一致。

## 修复规则

- 白屏 / 空页 / 路由打不开：P0 失败，先修运行或资源路径。
- 截断 / 重叠 / 文本溢出：P0 失败，回到对应页修布局。
- 低方差近空白页：P0 失败，除非该页明确是留白转场且用户接受。
- 整体节奏单调：P1 问题，优先回到 Step 3-C 页型覆盖检查。
- 风格漂移：P1 问题，回到 `DESIGN.md` 和 Step 4 的质量基线。

## 交付记录

最终回复中简短说明：

- 截图页数。
- contact sheet 是否生成。
- 是否发现并修复 P0 问题。
- 未执行视觉 QA 的原因（仅 Path A/B 或用户明确不需要时可接受）。
