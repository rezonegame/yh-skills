# 视觉风格预览机制 (Style Preview Mechanism)

---

## 1. 核心理念

**"Show, Don't Tell" -- 让用户看到而不是描述。**

大多数人无法用语言准确描述自己的设计偏好。与其问"你想要极简还是大胆？"，不如直接生成视觉预览让用户选择。这是本系统风格发现流程的核心原则。

### 设计心理学依据

- **具象优于抽象**: 用户提供的是情绪反应，不是设计术语
- **比较产生判断**: 同时看到 3 个选项比逐个想象更容易做出选择
- **迭代优于一次性**: 选择后可以微调，而非必须一次选对

---

## 2. 两种选择方式

### 方式 A: 引导式探索 (Guided Discovery)

**适用对象**: 不确定自己喜欢什么风格的用户（大多数用户）

**流程**:
1. 用户回答 4 个情绪选项
2. 系统根据情绪映射生成 3 个风格预览
3. 用户在浏览器中查看预览
4. 用户选择最喜欢的风格（或混合多个风格）
5. 进入正式演示文稿生成

```
用户回答情绪问题
        │
        ▼
系统查询情绪→风格映射表
        │
        ▼
生成 3 个 HTML 预览文件
        │
        ▼
用户在浏览器中打开查看
        │
        ▼
用户反馈: 选择 / 混合 / 调整
        │
        ▼
确认风格 → 进入生成阶段
```

### 方式 B: 直接选择 (Direct Selection)

**适用对象**: 已经知道自己想要什么风格的高级用户

**流程**:
1. 用户直接指定风格名称（如 "Use Bold Signal" 或 "我想要 Dark Botanical"）
2. 系统跳过预览阶段，直接进入生成

**触发示例**:
- "Use the Bold Signal style"
- "我想要 Dark Botanical 风格"
- "用 Neon Cyber 风格"
- "我选 Swiss Modern"

---

## 3. 情绪选择问题

### 问题: "你希望观众在观看幻灯片时有什么感受？"

**Header**: Vibe
**Question**: "What feeling should the audience have when viewing your slides?"

| 选项 | 英文 | 描述 |
|------|------|------|
| 震撼/自信 | Impressed/Confident | 专业、可信赖，这个团队很专业 |
| 兴奋/能量 | Excited/Energized | 创新、大胆，这是未来 |
| 平静/专注 | Calm/Focused | 清晰、有深度，易于跟随 |
| 灵感/感动 | Inspired/Moved | 情感、故事性，令人难忘 |

**multiSelect**: true（最多可选 2 个）

---

## 4. 情绪→风格映射表

### Impressed / Confident (震撼/自信)

| 优先级 | 风格 | 气质 |
|--------|------|------|
| 1 | **Bold Signal** | 彩色卡片深色背景，自信高冲击力 |
| 2 | **Electric Studio** | 干净专业，双面板分割 |
| 3 | **Dark Botanical** | 优雅深色，柔和抽象形状 |

### Excited / Energized (兴奋/能量)

| 优先级 | 风格 | 气质 |
|--------|------|------|
| 1 | **Creative Voltage** | 电光蓝+霓虹黄，复古现代 |
| 2 | **Neon Cyber / Neo-Tokyo** | 赛博朋克，霓虹光效 |
| 3 | **Split Pastel** | 活泼双色分割，年轻现代 |

### Calm / Focused (平静/专注)

| 优先级 | 风格 | 气质 |
|--------|------|------|
| 1 | **Notebook Tabs** | 编辑风格纸张，有序整洁 |
| 2 | **Paper & Ink** | 文学质感，温暖奶油色 |
| 3 | **Swiss Modern / Swiss** | 精确网格，极简几何 |

### Inspired / Moved (灵感/感动)

| 优先级 | 风格 | 气质 |
|--------|------|------|
| 1 | **Dark Botanical** | 优雅暗色，艺术氛围 |
| 2 | **Vintage Editorial** | 有个性的编辑风格 |
| 3 | **Pastel Geometry** | 友好现代，温暖调色 |

### 多选组合的处理

当用户选择两个情绪时，取两个情绪列表的交集，优先选择在两个列表中都出现的风格，其次取第一个情绪的首选 + 第二个情绪的次选。

| 组合 | 推荐预览组合 |
|------|-------------|
| Impressed + Excited | Bold Signal, Neon Cyber, Creative Voltage |
| Impressed + Calm | Electric Studio, Swiss Modern, Notebook Tabs |
| Impressed + Inspired | Dark Botanical, Paper & Ink, Bold Signal |
| Excited + Calm | Split Pastel, Swiss Modern, Notebook Tabs |
| Excited + Inspired | Creative Voltage, Vintage Editorial, Pastel Geometry |
| Calm + Inspired | Paper & Ink, Vintage Editorial, Notebook Tabs |

---

## 5. 预览文件生成流程

### 文件目录结构

```
.claude-design/slide-previews/
├── style-a.html    # 第一个风格选项
├── style-b.html    # 第二个风格选项
├── style-c.html    # 第三个风格选项
└── assets/         # 共享资源（如有）
```

### 生成步骤

1. **确定 3 个风格**: 根据用户情绪选择，从映射表中取 3 个不同风格
2. **生成预览文件**: 为每个风格创建一个独立的 HTML 文件
3. **写入文件**: 保存到 `.claude-design/slide-previews/` 目录

### 交付给用户的引导语

```
我为你创建了 3 个风格预览供你对比：

**Style A: [风格名]** -- [一句话描述]
**Style B: [风格名]** -- [一句话描述]
**Style C: [风格名]** -- [一句话描述]

在浏览器中打开每个文件查看实际效果：
- .claude-design/slide-previews/style-a.html
- .claude-design/slide-previews/style-b.html
- .claude-design/slide-previews/style-c.html

查看后告诉我：
1. 你最喜欢哪个风格？
2. 喜欢它的什么特点？
3. 有什么想调整的吗？
```

---

## 6. 每个预览文件的要求

### 基本规范

| 要求 | 规范 |
|------|------|
| **自包含** | 所有 CSS/JS 内联在单个 HTML 文件中，无外部依赖（字体除外） |
| **内容** | 单个标题页 (title slide)，展示风格美学 |
| **动画** | 包含入场动画，演示风格动效 |
| **代码量** | 50-100 行，精炼不冗余 |
| **语言** | 使用实际演示主题作为标题内容 |

### 必须展示的元素

每个预览文件必须让用户看到：

1. **Typography (字体)**: Display + Body 字体的实际效果
2. **Color Palette (配色)**: 背景、强调色、文字颜色的实际搭配
3. **Animation Style (动效)**: 元素入场动画的风格和速度
4. **Layout Feel (布局感)**: 整体视觉节奏和空间感
5. **Signature Elements (标志性元素)**: 该风格独有的视觉特征

### 预览文件模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Style Preview - [风格名]</title>
    <!-- 字体引入 -->
    <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">
    <style>
        /* ==========================================
           [风格名] - 风格预览
           ========================================== */
        :root {
            /* 该风格的 CSS 自定义属性 */
            --bg-primary: ...;
            --text-primary: ...;
            --accent: ...;
            /* 响应式字体（必须用 clamp） */
            --title-size: clamp(1.5rem, 5vw, 4rem);
            --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
            /* 响应式间距 */
            --slide-padding: clamp(1rem, 4vw, 4rem);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: var(--font-body);
            background: var(--bg-primary);
            color: var(--text-primary);
            height: 100vh;
            height: 100dvh;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .preview-container {
            text-align: center;
            padding: var(--slide-padding);
            max-width: min(90vw, 800px);
        }

        /* 风格标志性元素 */
        .signature-element { ... }

        /* 入场动画 */
        .reveal {
            opacity: 0;
            transform: translateY(30px);
            animation: revealUp 0.8s ease forwards;
        }
        .reveal:nth-child(2) { animation-delay: 0.2s; }
        .reveal:nth-child(3) { animation-delay: 0.4s; }

        @keyframes revealUp {
            to { opacity: 1; transform: translateY(0); }
        }

        @media (prefers-reduced-motion: reduce) {
            .reveal { animation: none; opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="preview-container">
        <div class="signature-element reveal"><!-- 风格标志性元素 --></div>
        <h1 class="reveal" style="font-family: var(--font-display); font-size: var(--title-size);">
            演示文稿标题
        </h1>
        <p class="reveal" style="font-size: var(--body-size); margin-top: 1rem;">
            副标题或描述文字
        </p>
        <!-- 更多风格特征展示 -->
    </div>
</body>
</html>
```

---

## 7. 用户反馈收集

### 选择后的对话

用户查看预览后，使用 AskUserQuestion 收集反馈：

**Question**: Pick Your Style
**Header**: Style
**Question**: "你更喜欢哪个风格预览？"

| 选项 | 描述 |
|------|------|
| "Style A: [名称]" | [简短描述] |
| "Style B: [名称]" | [简短描述] |
| "Style C: [名称]" | [简短描述] |
| "混合元素" | 从不同风格中组合要素 |

### 如果选择"混合元素"

追问具体偏好：

**Question**: Style Mixing
**Header**: Customize
**Question**: "你想从哪些风格中组合元素？"

收集：
- 保留哪个风格的 **字体**
- 保留哪个风格的 **配色**
- 保留哪个风格的 **布局**
- 保留哪个风格的 **动效**
- 保留哪个风格的 **标志性元素**

### 反馈维度

收集用户的反馈时，关注以下维度：

| 维度 | 关键问题 |
|------|----------|
| 颜色 | "颜色是否合适？要不要换一个强调色？" |
| 字体 | "字体风格是否满意？" |
| 布局 | "内容的排列方式是否喜欢？" |
| 动效 | "动画速度和风格是否合适？" |
| 整体 | "整体感觉对不对？有没有什么想调整的？" |

---

## 8. 禁止使用的通用模式

生成预览时，**严禁**使用以下模式，它们会导致所有预览看起来千篇一律：

### 禁止字体

| 字体 | 原因 | 替代方案 |
|------|------|----------|
| `Inter` | 被过度使用的 AI 通用字体 | DM Sans, Work Sans, Plus Jakarta Sans |
| `Roboto` | Android 默认字体，缺乏个性 | Nunito, Source Sans 3, Outfit |
| `Arial` | 系统默认，毫无辨识度 | 任何 Google Fonts 上的 Display 字体 |

> 注意: 系统字体（`-apple-system`, `Segoe UI`）仅在 Apple Keynote 和 Typical 风格中允许使用，因为这是这些风格的设计语言一部分。

### 禁止配色

| 配色模式 | 原因 | 替代方案 |
|----------|------|----------|
| `#6366f1` 通用靛蓝 | 最常见的 AI 生成色 | 使用各风格定义的独特配色 |
| 紫色渐变 + 白底 | 被滥用的 AI slop 配色 | 根据风格选择暖色/冷色/中性色方案 |
| 默认蓝色 `#3B82F6` | Tailwind 默认蓝 | TED 红 `#E31C23`, 霓虹青 `#00ffcc` 等 |

### 禁止布局

| 布局模式 | 原因 | 替代方案 |
|----------|------|----------|
| 万物居中 | 缺乏节奏和层次 | 不对称布局、网格对齐、分层设计 |
| 千篇一律的卡片网格 | 每个预览看起来都一样 | 各风格的标志性布局元素 |
| 相同的 Hero Section | 无差异化的通用设计 | 各风格独特的首屏设计 |
| 三列等宽卡片 | AI 默认输出 | 变化的网格、分栏、列表等 |

### 禁止装饰

| 装饰元素 | 原因 | 替代方案 |
|----------|------|----------|
| 写实插图 (除特定风格) | 大多数风格不适用 | 抽象 CSS 形状、几何图案 |
| 无目的的毛玻璃效果 | 过度使用的装饰 | 有目的的半透明层（如 Neon Cyber 的光效） |
| 无目的的阴影 | 到处都是 box-shadow | 仅在有层次需求时使用 |

### 正确做法

每个预览都应该：
- 使用该风格**独特的** Font Pairing
- 使用该风格**定义的** Color Palette
- 展示该风格的**标志性元素**
- 营造独特的**视觉氛围**
- 让用户能**一眼区分**三个风格的不同

---

## 9. 完整流程示例

### 示例对话

```
用户: 我想做一个关于 AI 未来趋势的演示

系统: 好的！在开始设计之前，让我先了解一下你想要的视觉风格。

问题: 你希望观众在观看幻灯片时有什么感受？
用户选择: "兴奋/能量" + "震撼/自信"

系统: 我为你创建了 3 个风格预览：

Style A: Creative Voltage -- 电光蓝+霓虹黄，充满活力的复古现代风
Style B: Neon Cyber -- 赛博朋克霓虹光效，未来科技感
Style C: Bold Signal -- 彩色卡片深色背景，自信高冲击力

在浏览器中打开查看:
- .claude-design/slide-previews/style-a.html
- .claude-design/slide-previews/style-b.html
- .claude-design/slide-previews/style-c.html

用户: 我选 B，Neon Cyber。但背景能不能更暗一些？

系统: 好的！将使用 Neon Cyber 风格，背景调整为更深的深色。现在开始生成完整演示文稿。
```

---

## 10. 注意事项

1. **预览文件是临时的**: 演示文稿生成完成后，应清理 `.claude-design/slide-previews/` 目录
2. **预览不等同于成品**: 预览是 50-100 行的简短展示，成品是完整的演示文稿
3. **尊重用户选择**: 如果用户明确指定风格，不要强行推荐其他风格
4. **风格可以微调**: 用户在看到预览后提出的调整（颜色、字体等）都应该采纳
5. **保持 3 个选项的差异性**: 不要选择视觉上太相似的风格作为预览选项
