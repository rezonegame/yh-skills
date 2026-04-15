# 可编辑 PPTX 导出指南

## 概述

将 AI 生成的 PPT 图片转为可编辑的 .pptx 文件，核心工作流分为 4 步：

```
原始幻灯片图片
    |
    v
Step 1: 背景提取 -- 移除文字和配图，输出干净底板
    |
    v
Step 2: 文字属性提取 -- 用 LLM 识别文字内容、颜色、粗体、LaTeX 等
    |
    v
Step 3: PPTX 还原 -- 以底板为背景，逐页重建文字框、表格等元素
    |
    v
Step 4: 画质修复 -- 对底板的涂抹痕迹做局部修复（按需）
    |
    v
可编辑 .pptx 文件
```

---

## Step 1: 背景提取

从原始幻灯片图片中移除所有文字、图表、插画，输出一张干净纯净的底板图。底板将作为 PPTX 的页面背景图。

### Prompt 模板

```
你是一位专业的图片文字&图片擦除专家。你的任务是从原始图片中移除文字和配图，输出一张无任何文字和图表内容、干净纯净的底板图。
<requirements>
- 彻底移除页面中的所有文字、插画、图表。必须确保所有文字都被完全去除。
- 保持原背景设计的完整性（包括渐变、纹理、图案、线条、色块等）。保留原图的文本框和色块。
- 对于被前景元素遮挡的背景区域，要智能填补，使背景保持无缝和完整。
- 输出图片的尺寸、风格、配色必须和原图完全一致。
- 请勿新增任何元素。
</requirements>
```

### CLI 命令

```bash
python ~/.claude/skills/yh-slides/scripts/generate_image.py clean-bg \
  --image slide.png \
  -o bg.png
```

| 参数 | 说明 |
|------|------|
| `--image` | 原始幻灯片图片路径 |
| `-o` | 输出的底板图路径 |

---

## Step 2: 文字属性提取

使用 LLM（多模态）识别幻灯片中的所有文字，并提取其视觉属性：内容、颜色、是否粗体、是否斜体、是否为 LaTeX 公式等。

### Prompt 模板

将原始幻灯片图片发送给 LLM，要求输出结构化 JSON：

```json
{
    "colored_segments": [
        {"text": "普通文字内容", "color": "#333333"},
        {"text": "重点标题", "color": "#FF0000", "bold": true},
        {"text": "x^2 + y^2 = z^2", "color": "#0066CC", "is_latex": true},
        {"text": "斜体说明", "color": "#666666", "italic": true}
    ]
}
```

### 输出字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `text` | string | 文字内容，LaTeX 公式保持原始表达式 |
| `color` | string | 十六进制颜色值（含 # 前缀） |
| `bold` | boolean | 是否粗体（可选，默认 false） |
| `italic` | boolean | 是否斜体（可选，默认 false） |
| `is_latex` | boolean | 是否为 LaTeX 数学公式（可选，默认 false） |

### 配合 MinerU 使用

如果已有 MinerU 的 OCR 结果，可以直接从其 bbox 信息中提取文字位置和内容，再由 LLM 补充颜色、样式等视觉属性。

---

## Step 3: PPTX 还原

以底板图为页面背景，根据提取的文字属性在对应位置重建文本框、表格等可编辑元素。

### 核心技术要点

#### 字号计算 -- 二分搜索法

由于 LLM 无法直接判断字号，采用二分搜索策略：

1. 从一个较大的起始字号（如 72pt）开始
2. 将文字渲染到文本框中，检查是否超出目标 bbox
3. 如果超出，缩小字号；未超出，增大字号
4. 重复直到收敛到刚好 fits bbox 的最大字号

```
搜索范围: [min_size, max_size]
循环:
  mid = (min_size + max_size) / 2
  if 文字渲染后 fits bbox:
    min_size = mid          # 尝试更大的字号
  else:
    max_size = mid          # 字号太大，缩小
直到 max_size - min_size < 阈值
```

#### CJK 字符宽度估算

精确的字体度量需要字体文件加载，为简化计算使用经验公式：

| 字符类型 | 宽度估算 |
|----------|----------|
| CJK 字符（中文、日文、韩文） | 约 1.0 x fontSize |
| 非字符（英文、数字、标点） | 约 0.5 x fontSize |

判断 CJK 的方法：

```python
def is_cjk(char):
    cp = ord(char)
    return (
        0x4E00 <= cp <= 0x9FFF    # CJK Unified Ideographs
        or 0x3400 <= cp <= 0x4DBF  # CJK Extension A
        or 0x3000 <= cp <= 0x303F  # CJK Symbols
        or 0xFF00 <= cp <= 0xFFEF  # Fullwidth Forms
    )

def estimate_text_width(text, font_size):
    return sum(
        font_size if is_cjk(ch) else font_size * 0.5
        for ch in text
    )
```

#### 多色文字渲染

同一段落中可能包含多种颜色的文字片段。使用 python-pptx 的 `add_run()` 为每个颜色段创建独立的 run：

```python
from pptx.util import Pt
from pptx.dml.color import RGBColor

paragraph = textbox.text_frame.paragraphs[0]

for segment in colored_segments:
    run = paragraph.add_run()
    run.text = segment["text"]
    run.font.size = Pt(font_size)
    run.font.color.rgb = RGBColor.from_string(segment["color"][1:])  # 去掉 "#"

    if segment.get("bold"):
        run.font.bold = True
    if segment.get("italic"):
        run.font.italic = True
```

#### 表格还原

当幻灯片包含表格时，通过 HTML 作为中间格式还原：

```
LLM 识别表格结构 → 输出 HTML 表格 → HTMLTableParser 解析 → python-pptx Table 对象
```

```python
from pptx.util import Inches, Pt

# 创建表格
rows, cols = table_data["rows"], table_data["cols"]
table = slide.shapes.add_table(rows, cols, left, top, width, height).table

# 填充单元格
for r in range(rows):
    for c in range(cols):
        cell = table.cell(r, c)
        cell.text = table_data["cells"][r][c]
```

#### 中文字体

使用 Google Noto Sans SC 作为默认中文字体：

```python
from pptx.dml.color import RGBColor

run.font.name = "Noto Sans SC"
# 需要确保系统或 PPTX 中已嵌入 NotoSansSC-Regular.ttf
```

#### 边距设置

由于 MinerU 的 bbox 已经非常贴合文字区域，文本框边距设为 0：

```python
text_frame.margin_left = 0
text_frame.margin_right = 0
text_frame.margin_top = 0
text_frame.margin_bottom = 0
```

---

## Step 4: 画质修复

背景提取后，抹除区域可能留下涂抹痕迹、色块不均或纹理断裂。此步骤使用图像修复模型对底板做局部修复。

### Prompt 模板

```
你是一位专业的图像修复专家。这张ppt页面图片刚刚经过了文字/对象抹除操作，抹除工具在指定区域留下了一些修复痕迹。
<requirements>
- 重点修复标注的区域，消除涂抹痕迹，恢复自然的背景纹理和颜色过渡。
- 保持纹理、颜色、图案的连续性，确保修复区域与周围背景无缝衔接。
- 禁止添加任何文字、图表、插画等元素。
- 保持原图的整体色调和风格不变。
</requirements>
```

### 何时需要修复

- 底板出现明显的涂抹条痕或色块
- 渐变背景在文字区域出现断裂
- 纹理图案在擦除区域不连续
- 色块边界模糊或出现杂色

### 何时可以跳过

- 底板背景为纯色或简单渐变
- 抹除区域很小且痕迹不明显
- 后续会被 PPTX 的文本框完全覆盖的区域

---

## CLI 命令速查表

| 命令 | 用途 | 示例 |
|------|------|------|
| `clean-bg` | 从幻灯片图片中提取干净背景底板 | `python generate_image.py clean-bg --image slide.png -o bg.png` |
| `edit` | 对指定区域做局部修改后重新导出 | `python generate_image.py edit --image slide.png --prompt "..." -o edited.png` |
| `extract-style` | 分析页面的设计风格（配色、字体、布局等） | `python generate_image.py extract-style --image slide.png` |

所有命令均位于 `~/.claude/skills/yh-slides/scripts/generate_image.py`。

---

## 完整工作流示例

```bash
# 假设原始幻灯片为 slides/ 目录下的 PNG 图片

# 1. 批量提取背景
for img in slides/*.png; do
    base=$(basename "$img" .png)
    python ~/.claude/skills/yh-slides/scripts/generate_image.py clean-bg \
        --image "$img" -o "backgrounds/${base}_bg.png"
done

# 2. 用 LLM 提取文字属性（需要多模态调用）
# 将每张幻灯片图片发送给 LLM，收集 JSON 输出

# 3. 运行 PPTX 还原脚本，生成可编辑文件
python build_pptx.py \
    --bg-dir backgrounds/ \
    --text-data text_attributes.json \
    --output output.pptx

# 4. 检查底板质量，对需要修复的页面执行画质修复
python ~/.claude/skills/yh-slides/scripts/generate_image.py edit \
    --image backgrounds/problem_slide_bg.png \
    --prompt "修复涂抹痕迹，恢复背景纹理连续性" \
    -o backgrounds/problem_slide_bg_fixed.png
```
