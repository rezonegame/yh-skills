# API 配置指南

## 后端关系

`yh-slides` 的默认图片策略是 `auto-runtime`，不是固定只用 Gemini。先读 `references/integrations/image-backend-policy.md` 判断后端：

- 当前 CLI / agent runtime 有原生图片工具：优先使用原生工具
- 没有原生工具、原生工具无法稳定落盘，或用户明确要求 API 后端：使用 Gemini / Imagen API
- 用户显式指定 `codex-image2` / `gemini` / `imagen`：按用户指定执行

本文件只说明 **script/API backend** 的配置方式。Codex Image2 是 agent-native backend，不需要也不能通过这里配置 API key。

---

## Gemini API（AI 图像生成）

**用途**: 作为脚本化图片生成后端，支持批量、重试、断点续传和容器环境。

### 配置信息

```yaml
gemini:
  api_key: "${GEMINI_API_KEY}"
  models:
    - name: "gemini-3.1-flash-image-preview"
      purpose: "主模型 — 图片生成/编辑/背景提取"
    - name: "imagen-4.0-generate-001"
      purpose: "备用图片生成（Gemini 失败时自动切换）"
    - name: "gemini-2.5-flash"
      purpose: "风格提取/文字属性识别（纯文本输出）"
  base_url: "${GEMINI_API_BASE_URL}"
```

### 生成命令（内置脚本）

```bash
python scripts/generate_image.py generate \
  "[description]" \
  --model gemini \
  --output "[timestamp]-slide-[N]-[name].png" \
  --image-size 2K
```

批量生成：

```bash
python scripts/generate_image.py batch \
  --tasks tasks.json \
  --model gemini \
  --image-size 2K \
  --skip-existing
```

### Python 直接调用示例

```python
import requests
import os

def generate_image(prompt, style="minimalist"):
    """使用 Gemini 生成图像"""
    api_key = os.environ["GEMINI_API_KEY"]
    base_url = os.environ.get("GEMINI_API_BASE_URL", "GEMINI_API_BASE_URL")
    url = f"{base_url}/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key={api_key}"

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
| Path A | Codex Image2 不可用或用户指定 Gemini 时，生成关键幻灯片插图 |
| Path B | 批量生成每一页完整视觉，尤其适合非 Codex / 容器 / 断点续传 |
| 2D / Path C | 作为 magazine 配图素材后端之一；是否使用由 `auto-runtime` 决定 |
| Path D | 生成插图嵌入 HTML，或在无原生图片工具时作为默认后端 |

---

## Unsplash API（摄影图搜索）

**用途**: 搜索高质量摄影图片

### 配置信息

```yaml
unsplash:
  access_key: "${UNSPLASH_ACCESS_KEY}"
  base_url: "${UNSPLASH_API_BASE_URL}"
```

### JavaScript 搜索示例

```javascript
async function searchPhotos(query) {
  const accessKey = process.env.UNSPLASH_ACCESS_KEY;
  const baseUrl = process.env.UNSPLASH_API_BASE_URL;
  const response = await fetch(
    `${baseUrl}/search/photos?query=${query}&client_id=${accessKey}`
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
| 2D / Path C | 可选，嵌入最终 HTML |
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
        "url": "assets/placeholders/image-not-available.svg",
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
python scripts/generate_image.py edit \
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
python scripts/generate_image.py extract-style --image reference.png
```

### 输出

返回一段中文风格描述文本，包含色板、字体风格、设计元素、情绪和布局倾向。

详细用法见 `references/style-extraction.md`。

---

## 2B-R 与 API 的边界

2B-R 不使用 Gemini API 做背景擦除或文字框提取。位图可编辑重建由独立
FigEdit 的本地 OCR/CV、Agent Manifest 和 SVG→DrawingML 链路完成，详见
`references/integrations/figedit-reconstruction.md`。
