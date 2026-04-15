# API 配置指南

## 内置 API 配置

yh-slides 内置 Gemini 和 Unsplash 的 API 配置，可直接使用。

---

## Gemini API（AI 图像生成）

**用途**: AI 生成专属插图和全页视觉

### 配置信息

```yaml
gemini:
  api_key: "AIzaSyB3Co4QmK6GlEQQ4MBVE-iFZtXXzvnak0U"
  models:
    - name: "gemini-3.1-flash-image-preview"
      purpose: "主模型 — 图片生成/编辑/背景提取"
    - name: "imagen-3.0-generate-001"
      purpose: "备用图片生成（Gemini 失败时自动切换）"
    - name: "gemini-2.5-flash"
      purpose: "风格提取/文字属性识别（纯文本输出）"
  base_url: "https://generativelanguage.googleapis.com"
```

### 生成命令（内置脚本）

```bash
python ~/.claude/skills/yh-slides/scripts/generate_image.py \
  "[description]" \
  --output "[timestamp]-slide-[N]-[name].png" \
  --image-size 2K
```

### Python 直接调用示例

```python
import requests

def generate_image(prompt, style="minimalist"):
    """使用 Gemini 生成图像"""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key=AIzaSyB3Co4QmK6GlEQQ4MBVE-iFZtXXzvnak0U"

    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [{
            "parts": [{
                "text": f"Generate an image: {prompt}. Style: {style}, professional presentation illustration, clean background, suitable for slides."
            }]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"]
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

### 提示词最佳实践

生成高质量插图的提示词应包含：

1. **主题描述** — 清晰说明要生成什么
2. **风格指定** — 指定艺术风格（参考 `proven-styles-gallery.md`）
3. **用途说明** — "professional presentation illustration"
4. **背景要求** — "clean background, no text in image"

**关键规则**:
- 始终包含 "no text in image" — 文字作为可编辑元素单独添加
- 使用描述性段落，而非关键词列表
- 明确指定 hex 颜色
- 使用 "flat vector" / "flat illustration" 保持一致性

### 适用路径

| 路径 | Gemini 用途 |
|------|-----------|
| Path A | 生成关键幻灯片的插图 |
| Path B | 生成每一页完整视觉 |
| Path C | 不使用（零依赖） |
| Path D | 生成插图嵌入 HTML |

---

## Unsplash API（摄影图搜索）

**用途**: 搜索高质量摄影图片

### 配置信息

```yaml
unsplash:
  access_key: "V1NQdaaHe9vI7isiA7MCzlnX39yC0jAXsnuC7C0BfvM"
  base_url: "https://api.unsplash.com"
```

### JavaScript 搜索示例

```javascript
async function searchPhotos(query) {
  const response = await fetch(
    `https://api.unsplash.com/search/photos?query=${query}&client_id=V1NQdaaHe9vI7isiA7MCzlnX39yC0jAXsnuC7C0BfvM`
  );
  const data = await response.json();

  if (data.results.length > 0) {
    const image = data.results[0];
    return {
      url: image.urls.regular,
      author: image.user.name,
      attribution: `Photo by ${image.user.name} on Unsplash`
    };
  }
  return null;
}
```

### 推荐关键词

| 主题 | 关键词 |
|------|-------|
| 技术 | technology, coding, developer, computer, digital |
| 商务 | business, meeting, office, professional, corporate |
| 创意 | creative, design, art, inspiration, innovation |
| 自然 | nature, landscape, outdoor, environment, green |
| 人物 | people, team, collaboration, diversity, community |
| 教育 | education, learning, student, knowledge, school |
| 科学 | science, research, laboratory, experiment, discovery |

### 图片尺寸选择

| 尺寸 | 用途 |
|------|------|
| `urls.regular` | 演示文稿首选（1080px 宽） |
| `urls.full` | 全屏背景（可能过大） |
| `urls.small` | 缩略图（太小） |

### 适用路径

| 路径 | Unsplash 用途 |
|------|-------------|
| Path A | 封面/关键页背景图 |
| Path B | 不使用（AI 全页生成） |
| Path C | 可选，嵌入 HTML |
| Path D | 可选，嵌入 HTML |

---

## 配图策略

根据风格选择合适的配图来源：

### Unsplash 适合的风格

需要真实摄影的风格：ted, apple, editorial, kinfolk, newspaper

### Gemini AI 适合的风格

需要定制插画的风格：gamma, consulting, swiss, bauhaus, muji, brutalist, neo-tokyo, dark-mode, red-black-white, cartoon-2.5d, education

### 混合使用

education 风格：示意图用 Gemini，实景照片用 Unsplash

---

## 错误处理

```python
def get_image_with_fallback(topic, style="minimalist"):
    """获取图像，失败时使用备用方案"""
    try:
        image = search_unsplash(topic)
        if image:
            return image
    except Exception as e:
        print(f"Unsplash 搜索失败: {e}")

    try:
        image = generate_image(topic, style)
        if image:
            return image
    except Exception as e:
        print(f"Gemini 生成失败: {e}")

    return {
        "url": "https://via.placeholder.com/1080x720?text=Image+Not+Available",
        "source": "placeholder"
    }
```

## 速率限制

- **Gemini**: 按请求计费，建议缓存生成图像
- **Unsplash**: 免费，50 请求/小时（应用级别）

---

## 图片编辑 API（Gemini 多模态）

**用途**: 基于现有图片 + 自然语言指令进行局部重绘

### CLI 命令

```bash
python ~/.claude/skills/yh-slides/scripts/generate_image.py edit \
  --image slide.png \
  --prompt "把饼图换成柱状图" \
  --output edited.png
```

### API 说明

使用 Gemini 的 `generateContent` 接口，同时传入图片（inlineData）和文字指令。API 会根据指令修改图片并返回新图片。

详细 prompt 模板见 `references/prompt-templates.md`。

---

## 风格提取 API

**用途**: 从参考图片提取视觉风格描述

### CLI 命令

```bash
python ~/.claude/skills/yh-slides/scripts/generate_image.py extract-style --image reference.png
```

### 输出

返回一段中文风格描述文本，包含色板、字体风格、设计元素、情绪和布局倾向。

详细用法见 `references/style-extraction.md`。

---

## 背景提取 API

**用途**: 去除幻灯片图片中的文字和图表，保留干净背景

### CLI 命令

```bash
python ~/.claude/skills/yh-slides/scripts/generate_image.py clean-bg \
  --image slide.png \
  -o bg.png
```

### 适用场景

用于可编辑 PPTX 导出流程。提取的干净背景作为 PPTX 页面背景，文字以可编辑文本框形式叠加。

详细流程见 `references/editable-pptx-export.md`。
