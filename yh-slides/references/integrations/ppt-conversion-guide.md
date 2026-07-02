# PPT 转 HTML 转换指南

## 概述

本指南描述如何将现有 PowerPoint (.pptx) 文件转换为 HTML 幻灯片，保留所有文本、图片、顺序和演讲者备注。使用 `python-pptx` 库进行内容提取，然后通过标准 HTML 幻灯片流程生成输出。

**流程概览**:
```
.pptx 文件 → 提取内容 → 用户确认 → 风格选择 → 生成 HTML
```

---

## 1. 提取流程

### 1.1 环境准备

安装依赖：

```bash
pip install python-pptx Pillow
```

### 1.2 完整提取函数

```python
#!/usr/bin/env python3
"""
PPTX 内容提取工具

功能：
- 提取每张幻灯片的文本内容
- 提取嵌入图片并保存到 assets/ 目录
- 提取演讲者备注
- 识别幻灯片布局类型
- 输出结构化 JSON 供后续使用
"""

import json
import os
import re
from pathlib import Path
from typing import Any

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from PIL import Image


def extract_pptx(pptx_path: str, output_dir: str = None) -> dict[str, Any]:
    """
    从 PPTX 文件中提取所有内容。

    Args:
        pptx_path: PPTX 文件路径
        output_dir: 输出目录（默认为 pptx 文件同名目录）

    Returns:
        包含所有提取内容的字典
    """
    pptx_path = Path(pptx_path)
    if not pptx_path.exists():
        raise FileNotFoundError(f"PPTX 文件不存在: {pptx_path}")

    # 设置输出目录
    if output_dir is None:
        output_dir = pptx_path.stem + "_extracted"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 创建图片输出目录
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    # 加载 PPTX
    prs = Presentation(str(pptx_path))

    result = {
        "filename": pptx_path.name,
        "slide_width": prs.slide_width,
        "slide_height": prs.slide_height,
        "total_slides": len(prs.slides),
        "slides": []
    }

    # 逐页提取
    for slide_index, slide in enumerate(prs.slides):
        slide_data = {
            "index": slide_index + 1,  # 1-based
            "layout": _detect_layout(slide),
            "texts": [],
            "images": [],
            "notes": _extract_notes(slide)
        }

        # 提取所有形状中的内容
        for shape in slide.shapes:
            shape_data = _extract_shape(shape, assets_dir, slide_index)
            if shape_data:
                if shape_data["type"] == "text":
                    slide_data["texts"].append(shape_data)
                elif shape_data["type"] == "image":
                    slide_data["images"].append(shape_data)

        # 识别幻灯片标题（第一个大字号文本）
        slide_data["title"] = _detect_title(slide_data["texts"])

        result["slides"].append(slide_data)

    # 保存提取结果
    output_json = output_dir / "extracted.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"提取完成: {len(prs.slides)} 张幻灯片")
    print(f"图片保存至: {assets_dir}")
    print(f"数据保存至: {output_json}")

    return result


def _detect_layout(slide) -> str:
    """
    根据幻灯片中的形状类型和数量，推断布局类型。

    Returns:
        布局类型字符串
    """
    shapes = list(slide.shapes)
    text_count = sum(1 for s in shapes if s.has_text_frame)
    image_count = sum(1 for s in shapes if s.shape_type == MSO_SHAPE_TYPE.PICTURE)
    table_count = sum(1 for s in shapes if s.has_table)

    # 封面检测：第一张幻灯片 + 标题型布局
    layout_name = slide.slide_layout.name if slide.slide_layout else ""
    if "title" in layout_name.lower() and text_count <= 2:
        return "cover"

    # 全图检测
    if image_count >= 1 and text_count <= 1:
        return "full-image"

    # 表格检测
    if table_count >= 1:
        return "table"

    # 图文混排
    if image_count >= 1 and text_count >= 1:
        return "image-text"

    # 列表检测（多个同级文本框）
    if text_count >= 3:
        return "list"

    # 数据统计（包含数字的大字）
    for shape in shapes:
        if shape.has_text_frame:
            text = shape.text_frame.text.strip()
            if re.match(r'^[\d,.]+%?$', text):
                return "data"

    # 默认
    return "title-content"


def _extract_shape(shape, assets_dir: Path, slide_index: int) -> dict | None:
    """
    从单个形状中提取内容（文本或图片）。
    """
    result = None

    # 图片形状
    if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
        image = shape.image
        ext = image.content_type.split("/")[-1]
        # 规范化扩展名
        ext_map = {"jpeg": "jpg", "x-emf": "emf", "x-wmf": "wmf"}
        ext = ext_map.get(ext, ext)

        filename = f"slide_{slide_index + 1}_img_{shape.shape_id}.{ext}"
        filepath = assets_dir / filename

        with open(filepath, "wb") as f:
            f.write(image.blob)

        # 获取尺寸信息
        width = shape.width
        height = shape.height

        result = {
            "type": "image",
            "filename": filename,
            "filepath": str(filepath),
            "width": width,
            "height": height,
            "left": shape.left,
            "top": shape.top
        }

    # 文本形状
    elif shape.has_text_frame:
        paragraphs = []
        for para in shape.text_frame.paragraphs:
            runs_text = []
            for run in para.runs:
                run_data = {
                    "text": run.text,
                    "bold": run.font.bold,
                    "italic": run.font.italic,
                    "size": run.font.size.pt if run.font.size else None,
                    "color": None
                }
                if run.font.color and run.font.color.rgb:
                    run_data["color"] = str(run.font.color.rgb)
                runs_text.append(run_data)

            paragraphs.append({
                "text": para.text,
                "level": para.level,
                "runs": runs_text
            })

        # 过滤空段落
        paragraphs = [p for p in paragraphs if p["text"].strip()]

        if paragraphs:
            result = {
                "type": "text",
                "paragraphs": paragraphs,
                "full_text": "\n".join(p["text"] for p in paragraphs),
                "left": shape.left,
                "top": shape.top,
                "width": shape.width,
                "height": shape.height
            }

    return result


def _extract_notes(slide) -> str:
    """
    提取演讲者备注。
    """
    if slide.has_notes_slide:
        notes_slide = slide.notes_slide
        if notes_slide.notes_text_frame:
            return notes_slide.notes_text_frame.text.strip()
    return ""


def _detect_title(texts: list[dict]) -> str:
    """
    从文本列表中检测标题（最大的字号或第一个文本）。
    """
    if not texts:
        return ""

    # 找到最大字号的文本
    max_size = 0
    title_text = ""

    for text_data in texts:
        for para in text_data.get("paragraphs", []):
            for run in para.get("runs", []):
                if run.get("size") and run["size"] > max_size:
                    max_size = run["size"]
                    title_text = run["text"]

    # 如果没有字号信息，取第一个文本
    if not title_text and texts:
        title_text = texts[0]["paragraphs"][0]["text"] if texts[0]["paragraphs"] else ""

    return title_text.strip()


def print_extracted_summary(result: dict):
    """
    打印提取结果的摘要表格。
    """
    print(f"\n{'='*60}")
    print(f"文件: {result['filename']}")
    print(f"总页数: {result['total_slides']}")
    print(f"{'='*60}")
    print(f"{'页码':<6} {'布局':<15} {'标题':<30} {'备注'}")
    print(f"{'-'*60}")

    for slide in result["slides"]:
        notes_indicator = "[有备注]" if slide["notes"] else ""
        title = slide["title"][:28] + ".." if len(slide["title"]) > 30 else slide["title"]
        print(f"#{slide['index']:<5} {slide['layout']:<15} {title:<30} {notes_indicator}")

    print(f"{'='*60}\n")


# ==================== 命令行入口 ====================
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python extract_pptx.py <pptx文件路径> [输出目录]")
        sys.exit(1)

    pptx_file = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None

    result = extract_pptx(pptx_file, output)
    print_extracted_summary(result)
```

### 1.3 输出数据结构

提取完成后，`extracted.json` 的结构如下：

```json
{
  "filename": "presentation.pptx",
  "slide_width": 9144000,
  "slide_height": 6858000,
  "total_slides": 5,
  "slides": [
    {
      "index": 1,
      "layout": "cover",
      "title": "年度战略报告",
      "texts": [
        {
          "type": "text",
          "paragraphs": [
            {
              "text": "2025 年度战略报告",
              "level": 0,
              "runs": [
                {
                  "text": "2025 年度战略报告",
                  "bold": true,
                  "italic": false,
                  "size": 44,
                  "color": "1F4E79"
                }
              ]
            }
          ],
          "full_text": "2025 年度战略报告",
          "left": 457200,
          "top": 2746380,
          "width": 8229600,
          "height": 1366520
        }
      ],
      "images": [],
      "notes": "欢迎大家参加年度战略报告会议..."
    }
  ]
}
```

---

## 2. 内容确认

### 2.1 向用户呈现提取结果

提取完成后，以表格形式向用户展示内容，供确认和调整。

**展示格式**:

```markdown
## PPT 内容提取结果

**文件**: presentation.pptx | **总页数**: 12

| # | 布局类型 | 标题/内容摘要 | 图片数 | 备注 |
|---|----------|---------------|--------|------|
| 1 | cover | 2025 年度战略报告 | 1 | 有备注 |
| 2 | title-content | 市场回顾 | 0 | - |
| 3 | image-text | 核心产品展示 | 1 | - |
| 4 | data | 关键业务指标 | 0 | 有备注 |
| 5 | list | 三大战略方向 | 0 | - |
| ... | ... | ... | ... | ... |

### 提取内容详情

**第 1 页 — 封面**
- 标题：2025 年度战略报告
- 副标题：面向未来的创新驱动
- 图片：background.jpg (1920x1080)
- 备注：欢迎大家参加...

**第 3 页 — 图文混排**
- 标题：核心产品展示
- 正文：我们的产品线覆盖...
- 图片：product-photo.jpg (800x600)

---
请确认以上内容是否准确，或指出需要调整的部分。
```

### 2.2 用户交互要点

- **确认布局类型**：自动检测可能不准确，允许用户手动指定
- **确认内容顺序**：确保提取顺序与原 PPT 一致
- **处理合并幻灯片**：允许用户合并或拆分幻灯片
- **处理特殊元素**：图表、SmartArt、动画等需要额外说明

---

## 3. 风格选择

确认内容后，进入 Step 2（Design System）流程：

1. 展示可选风格列表（商务、极简、创意、科技等）
2. 用户选择风格或提供自定义要求
3. 应用 CSS Custom Properties 生成对应风格
4. 根据风格调整布局和配色

**布局类型到 HTML 模板的映射**:

| PPT 布局 | HTML 幻灯片类型 | 备注 |
|----------|----------------|------|
| cover | `slide-cover` | 封面 |
| title-content | `slide-title-content` | 标题+内容 |
| image-text | `slide-image-text` | 图文混排（需判断方向） |
| full-image | `slide-full-image` | 全图 |
| data | `slide-data` | 数据统计 |
| list | `slide-list` | 列表 |
| table | `slide-table` | 表格 |
| (其他) | `slide-title-content` | 默认 |

---

## 4. HTML 生成

### 4.1 转换原则

将提取的 PPTX 内容转换为 HTML 幻灯片时，必须遵循以下原则：

1. **内容完整性**：所有文本、图片、备注必须保留
2. **顺序一致**：幻灯片顺序与原 PPT 完全一致
3. **语义正确**：标题使用 h1/h2，正文使用 p，列表使用 ul/ol
4. **样式继承**：应用所选设计风格的 CSS Custom Properties
5. **图片路径**：引用 assets/ 目录中的图片文件

### 4.2 转换函数示例

```python
def generate_html_from_extracted(extracted_data: dict, style: dict) -> str:
    """
    将提取的 PPTX 数据转换为完整 HTML。

    Args:
        extracted_data: extract_pptx() 返回的数据
        style: 包含 CSS variables 和风格选项的字典

    Returns:
        完整的 HTML 字符串
    """
    slides_html = []

    for slide in extracted_data["slides"]:
        layout = slide["layout"]
        slide_num = slide["index"]
        total = extracted_data["total_slides"]

        # 根据布局类型选择模板
        if layout == "cover":
            html = _render_cover(slide, style)
        elif layout == "image-text":
            html = _render_image_text(slide, style)
        elif layout == "data":
            html = _render_data(slide, style)
        elif layout == "list":
            html = _render_list(slide, style)
        elif layout == "table":
            html = _render_table(slide, style)
        elif layout == "full-image":
            html = _render_full_image(slide, style)
        else:
            html = _render_title_content(slide, style)

        # 添加备注（HTML 注释）
        if slide["notes"]:
            html += f"\n    <!-- Notes: {slide['notes']} -->"

        slides_html.append(html)

    # 组装完整 HTML
    full_html = _assemble_html(slides_html, style, extracted_data)
    return full_html


def _render_cover(slide: dict, style: dict) -> str:
    """渲染封面幻灯片"""
    title = slide["title"]
    subtitle = ""
    author = ""
    date = ""

    # 从文本中提取副标题和其他信息
    for text in slide["texts"]:
        for para in text["paragraphs"]:
            if para["level"] == 0 and para["text"] != title:
                subtitle = para["text"]
            elif para["level"] == 1:
                author = para["text"]

    # 处理背景图
    bg_html = ""
    if slide["images"]:
        img = slide["images"][0]
        bg_html = f"""
    <div class="slide-bg" aria-hidden="true">
      <img src="assets/{img['filename']}" alt="" class="cover-bg-image" loading="eager">
    </div>"""

    return f"""
  <section class="slide slide-cover" id="slide-{slide['index']}">
    {bg_html}
    <div class="slide-inner cover-content">
      <h1 class="cover-title fade-in">{_escape_html(title)}</h1>
      <p class="cover-subtitle fade-in stagger-1">{_escape_html(subtitle)}</p>
      <div class="cover-meta fade-in stagger-2">
        <span class="cover-author">{_escape_html(author)}</span>
      </div>
    </div>
    <span class="slide-number">{slide['index']} / {slide['texts'].__len__()}</span>
  </section>"""


def _render_title_content(slide: dict, style: dict) -> str:
    """渲染标题+内容幻灯片"""
    title = slide["title"]
    body_paragraphs = []

    for text in slide["texts"]:
        for para in text["paragraphs"]:
            if para["text"] != title and para["level"] == 0:
                body_paragraphs.append(para["text"])

    body_html = "\n".join(
        f"      <p>{_escape_html(p)}</p>" for p in body_paragraphs
    )

    return f"""
  <section class="slide slide-title-content" id="slide-{slide['index']}">
    <div class="slide-inner">
      <h2 class="slide-title fade-in">{_escape_html(title)}</h2>
      <div class="slide-body fade-in stagger-1">
        {body_html}
      </div>
    </div>
    <span class="slide-number">{slide['index']} / {slide['total']}</span>
  </section>"""


def _render_image_text(slide: dict, style: dict) -> str:
    """渲染图文混排幻灯片"""
    title = slide["title"]
    body = []
    image = slide["images"][0] if slide["images"] else None

    for text in slide["texts"]:
        for para in text["paragraphs"]:
            if para["text"] != title:
                body.append(para["text"])

    # 判断图文方向（基于位置）
    layout_dir = "layout-image-right"
    if image:
        img_center_x = image["left"] + image["width"] / 2
        slide_center_x = slide.get("slide_width", 9144000) / 2
        if img_center_x < slide_center_x:
            layout_dir = "layout-image-left"

    img_html = ""
    if image:
        img_html = f"""
        <div class="col-image fade-in">
          <img src="assets/{image['filename']}" alt="{title}" loading="lazy"
               width="{image['width'] // 9144}" height="{image['height'] // 9144}">
        </div>"""

    body_html = "\n".join(f"<p>{_escape_html(p)}</p>" for p in body)

    return f"""
  <section class="slide slide-image-text {layout_dir}" id="slide-{slide['index']}">
    <div class="slide-inner two-col-layout">
      {img_html}
      <div class="col-text">
        <h2 class="slide-title fade-in stagger-1">{_escape_html(title)}</h2>
        <div class="fade-in stagger-2">{body_html}</div>
      </div>
    </div>
    <span class="slide-number">{slide['index']} / {slide['total']}</span>
  </section>"""


def _escape_html(text: str) -> str:
    """转义 HTML 特殊字符"""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def _assemble_html(slides_html: list[str], style: dict, data: dict) -> str:
    """组装完整 HTML 文档"""
    slides_content = "\n".join(slides_html)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{_escape_html(data['slides'][0]['title'] if data['slides'] else '演示文稿')}</title>
  <style>
    {style['css']}
  </style>
</head>
<body>
  <div class="progress-bar" id="progressBar"></div>
  <nav class="nav-dots" id="navDots" aria-label="幻灯片导航"></nav>
{slides_content}
  <script>
    {style['js']}
  </script>
</body>
</html>"""
```

### 4.3 演讲者备注处理

演讲者备注以两种方式保留：

**方式一：HTML 注释**（嵌入在 HTML 文件中）

```html
<section class="slide" id="slide-3">
  <!-- Notes: 这里的备注内容可以在演讲者视图中查看 -->
  <div class="slide-inner">...</div>
</section>
```

**方式二：独立 JSON 文件**（Path D 项目结构）

```json
// data/notes.json
{
  "1": "欢迎大家参加年度战略报告会议",
  "3": "这页的数据来自 Q4 财报",
  "7": "Q&A 环节，准备回答技术问题"
}
```

### 4.4 图片处理注意事项

| 场景 | 处理方式 |
|------|----------|
| 嵌入图片 (PNG/JPG) | 直接保存到 assets/ 目录 |
| EMF/WMF 矢量图 | 转换为 PNG，需 Pillow 或 Inkscape |
| 背景图片 | 使用 `cover-bg-image` 类 |
| 超大图片 | 缩放至最大 1920px 宽度 |
| 透明背景 PNG | 保留透明度 |

---

## 5. 完整工作流

```
用户上传 .pptx 文件
        │
        ▼
┌─────────────────────────┐
│  Step A: 提取内容        │
│  - 运行 extract_pptx()  │
│  - 保存图片到 assets/    │
│  - 生成 extracted.json  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Step B: 内容确认        │
│  - 展示提取结果表格      │
│  - 用户确认/调整         │
│  - 确认布局映射          │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Step C: 风格选择        │
│  - 进入 Step 2 流程      │
│  - 选择设计风格          │
│  - 生成 CSS Variables    │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Step D: HTML 生成       │
│  - 转换为 HTML 幻灯片    │
│  - 应用风格              │
│  - 保留备注              │
│  - 输出 Path C 或 D      │
└───────────┬─────────────┘
            │
            ▼
       完成 HTML 幻灯片
```

---

## 6. 常见问题

### Q: PPT 中的动画如何处理？

PPT 动画无法直接转换为 CSS 动画。策略：
- 入场动画 → 对应 CSS fade-in / slide-up
- 强调动画 → 对应 CSS scale-in
- 复杂动画（路径动画等）→ 忽略，改用简单的入场效果

### Q: SmartArt 和图表如何处理？

- **SmartArt**：提取文本内容，按层级转换为 HTML 列表
- **图表**：提取数据标签文本，转换为数据统计幻灯片
- **嵌入 Excel 图表**：提取数据和标签

### Q: 字体如何处理？

- 提取字体名称但不嵌入
- 映射到 Google Fonts 或系统字体
- 中文优先使用 Noto Sans SC

### Q: Master Slide 和版式如何处理？

- 提取版式名称用于布局推断
- 背景图片/渐变从版式中提取
- 母版中的固定元素（页眉页脚）可选保留
