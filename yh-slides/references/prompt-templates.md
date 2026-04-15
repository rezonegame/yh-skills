# AI Image Prompt 模板与工程指南

> 如何写出让 AI 生成惊艳图片的 prompt。核心原则：**SHORT > LONG**。

---

## 1. Path A Base Style Prompt — 插画风格模板

Path A 生成的是选择性插画（非整页 slide），嵌入 HTML 后转为 PPTX。

### 基础模板

```
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

### 使用方式

每次生成插画时，将具体内容描述 + Base Style 组合：

```
Per-slide prompt = [具体内容描述] + [Base Style]
```

### 示例

```
A small beagle dog sitting on top of a red doghouse, looking at the stars thoughtfully,
with a warm yellow bird perched nearby.

flat vector illustration, #F5F0E1 background,
warm pastel highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

### 关键规则

| 规则 | 说明 |
|------|------|
| 必须包含 "no text in image" | 文字将作为可编辑元素在 HTML 中添加 |
| 使用描述性段落 | 不要用关键词列表 |
| 明确指定 hex 颜色 | `#FF1493` 而非 "pink" |
| 使用 "flat vector" | 保持风格一致性 |
| 一张插画一个概念 | 不要在一张图中塞太多内容 |

---

## 2. Path B Per-Slide Prompt — 完整 Slide 模板

Path B 生成的是包含布局、文字、视觉的完整 slide 图片。

### Base Style Prompt 模板（保持简短，不超过 5 行）

```
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colors, not exact ratios]
```

### Per-Slide Prompt 模板

```
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1-2 sentences describing mood or scene. Let AI decide composition.]
```

---

## 3. The Golden Rule — SHORT > LONG

**3 句话描述情绪和内容的 prompt，比 30 行指定每个视觉细节的 prompt 效果更好。**

这是 Path B 最重要的原则，违反此规则是导致生成效果差的 #1 原因。

| 不要做（扼杀多样性） | 应该做（释放创造力） |
|---|---|
| 指定颜色比例（60%/25%/15%） | 描述情绪（"warm like a Sunday comic page"） |
| 指定布局位置（"标题居中，图片在右"） | 引用特定美学（"Peanuts comic strip"） |
| 限制角色（"NOT Snoopy — an original character"） | 让 AI 自然诠释风格 |
| 列出每个要包含的视觉元素 | 描述观众应该感受到什么 |
| 每个 slide prompt 重复 base style | 定义一次 base style，每个 slide prompt 保持简短 |

### 反模式（bad — 过度约束）

```
Design a professional presentation slide.
Professional presentation slide, 16:9 aspect ratio, 2048x1152 pixels.
Dark navy background, light gray text, gold accent.
Slide type: content. Layout: Title at top-left, two columns below.
Title: "看涨期权收益结构"
Body: "行权价: 100元, 权利金: 10元"
Visual: a line chart showing call option payoff
```

结果：像任何模板都能做出的通用 PPT。

### 正确模式（good — 简洁有力）

```
Create a slide that feels like a Bloomberg terminal data visualization
brought to life as editorial art.

VISUAL REFERENCE: Bloomberg Businessweek data feature meets cinematic lighting.
CANVAS: 16:9, 2048x1152, sharp rendering.
COLOR SYSTEM: Deep black (#0A0A0A) background 75%, white text 15%,
gold (#BF9A4A) accent 10%. The gold represents profit — it should GLOW.

DESIGN INTENT: The viewer should instantly FEEL the asymmetry of options —
limited downside, unlimited upside. The visual must make this visceral.

TEXT TO RENDER:
- Hero metric: "110" (giant, gold, the break-even price)
- Title: "盈亏平衡点" (medium, white, above the number)
- Left data: "行权价 100" "权利金 10" (small, gray)
- Insight: "亏损有底 盈利无限" (accent color, bottom)
```

结果：一个讲述故事的编辑式数据可视化。

---

## 4. Good vs Bad Prompt 对比

### 案例 1：封面 slide

**BAD:**
```
Create a cover slide for a presentation about AI.
16:9 ratio. Dark blue gradient background.
Title "人工智能的未来" in white, centered, 60pt font.
Subtitle "2025年度技术趋势报告" below in gray, 24pt.
Add some abstract circuit board patterns in the background.
Make it look professional and modern.
```

**GOOD:**
```
Create a cover slide about the future of AI.

VISUAL REFERENCE: A Bloomberg Businessweek cover — cinematic, editorial, data-rich.

TEXT TO RENDER:
- Title: "人工智能的未来"
- Subtitle: "2025年度技术趋势报告"

DESIGN INTENT: Feel the weight of the future — vast, intelligent, inevitable.
```

### 案例 2：数据 slide

**BAD:**
```
Design a data slide. Background color #FFFFFF. Title at top "Q3销售数据"
in bold 36pt. Show a bar chart with 4 bars: Q1=120, Q2=150, Q3=180, Q4=200.
Colors: blue bars. Add percentage labels on top of each bar. Legend at bottom right.
Grid lines in light gray. Source note at bottom: "数据来源：内部CRM".
```

**GOOD:**
```
Create a data slide showing quarterly sales growth with a dramatic upward trend.

VISUAL REFERENCE: A Fathom Information Design data narrative — precise, annotated, beautiful.

TEXT TO RENDER:
- Title: "Q3 销售增长 23%"
- Data callout: "新用户是主要驱动力"

DESIGN INTENT: The viewer should feel the momentum — growth is accelerating, not just happening.
```

### 案例 3：引用 slide

**BAD:**
```
Create a quote slide.
Background: warm cream color #FDF6EC.
Quote text: "创新不是创造新事物，而是重新组合旧事物。" in italic 28pt serif font.
Attribution: "— Steve Jobs" in regular 18pt, gray color #999.
Add a large opening quotation mark " in light coral color.
Decorative line separator between quote and attribution.
Minimalist style.
```

**GOOD:**
```
Create a quote slide with a feeling of quiet wisdom.

VISUAL REFERENCE: A page from a beautifully typeset book of philosophy.

TEXT TO RENDER:
- Quote: "创新不是创造新事物，而是重新组合旧事物。"
- Attribution: "— Steve Jobs"

DESIGN INTENT: The viewer should pause and reflect — this is a moment of calm in a fast presentation.
```

---

## 5. Prompt Quality Checklist

每次生成前，验证以下 5 项：

- [ ] **Visual Reference（视觉引用）** — prompt 是否命名了具体的艺术风格或出版物？（不是 "professional" 或 "modern" 这种空泛词）
- [ ] **Mood, not Layout（描述情绪而非布局）** — prompt 是否描述了观众应该 *感受到* 什么，而非元素应该 *放在哪里*？
- [ ] **Text Content（文字内容）** — 所有需要渲染的文字是否都准确列出？（包括标题、正文、数据标注）
- [ ] **Short Enough（足够简短）** — prompt 是否简洁？长 prompt 带着详细规格反而 *降低* 多样性。删除 AI 自己能决定的内容。
- [ ] **NO Micro-Management（不微操）** — 是否避免了 hex 颜色比例、字体大小、构图百分比、角色姿势指令？（这些是 "最差实践"）

---

## 6. Technical Rules — 技术规则

### 分辨率

| 参数 | 值 | 说明 |
|------|-----|------|
| 分辨率 | `2048x1152` (2K) | 16:9，文字清晰锐利 |
| 输出参数 | `--image-size 2K` | 生成命令中指定 |

### 文字渲染

| 规则 | 说明 |
|------|------|
| 列出所有文字 | AI 必须渲染精确的词句 |
| 中文优先 | slide 上的文字一律用中文，仅保留必要英文术语（人名、品牌名、技术专有名词） |
| 标题要短 | 中文标题 ≤8 字符，渲染效果最佳 |
| 段落式描述 | 用描述性段落，不用关键词列表 |

### Chinese Text Tips（中文渲染建议）

1. **标题短**：≤8 个中文字符，AI 渲染准确率最高
2. **避免生僻字**：常见字 > 生僻字 > 繁体字 > 古文
3. **数字用阿拉伯数字**：`2025` > `二零二五`
4. **英文术语保留原文**：`API` 不要写成 `应用程序接口`
5. **标点符号用全角**：中文内容配全角标点 `，。！？`
6. **如果渲染出错**：简化文字或缩短，重新生成

### 生成命令

```bash
python ~/.claude/skills/yh-slides/scripts/generate_image.py generate \
  "[full slide prompt]" \
  --output "slide-[NN]-[name].png" \
  --image-size 2K
```

### 并行生成

一次并行运行 3-5 个 slide 生成命令，显著提速：

```bash
# 并行生成 3 张 slide
python ~/.claude/skills/yh-slides/scripts/generate_image.py generate \
  "[slide1 prompt]" --output "slide-01.png" --image-size 2K &
python ~/.claude/skills/yh-slides/scripts/generate_image.py generate \
  "[slide2 prompt]" --output "slide-02.png" --image-size 2K &
python ~/.claude/skills/yh-slides/scripts/generate_image.py generate \
  "[slide3 prompt]" --output "slide-03.png" --image-size 2K &
wait
```

### 一致性检查

生成后的质量检查清单：

1. **文字准确** — 中英文文字渲染正确无误
2. **布局合理** — 元素位置与描述一致
3. **风格一致** — 颜色和设计语言在 slide 之间保持统一
4. **文字出错处理** — 如果某张 slide 有文字错误，用简化 prompt 重新生成

---

> **核心记住：** SHORT > LONG。让 AI 做设计决策，你做内容决策。

---

## 结构化图片生成 Prompt（来自 yh-slides 最佳实践）

### 核心结构

使用 XML 标签包裹指令，让 AI 更精准地理解任务：

```
你是一位专家级UI UX演示设计师，专注于生成设计良好的PPT页面。

<page_description>
[页面描述：标题、要点、视觉要求]
</page_description>

<design_guidelines>
- 要求文字清晰锐利，画面为4K分辨率，{aspect_ratio}比例。
- 配色和设计语言与模板/参考图严格相似。
- 根据内容和要求自动设计最完美的构图，不重不漏地渲染"页面文字"段落中的文本。
- 如非必要，禁止出现 markdown 格式符号（如 # 和 * 等）。
</design_guidelines>

PPT文字请使用全中文。
```

### 封面页特殊处理

第 1 页（封面页）时，追加：
```
**注意：当前页面为PPT的封面页，请你采用专业的封面设计美学技巧，务必凸显出页面标题，分清主次，确保一下就能抓住观众的注意力。**
```

### 带参考素材时

当有参考图片/模板时：
```
提示：除了模板参考图片（用于风格参考）外，还提供了额外的素材图片。
这些素材图片是可供挑选和使用的元素，你可以从这些素材图片中选择合适的图片、图标、图表或其他视觉元素
直接整合到生成的PPT页面中。请根据页面内容的需要，智能地选择和组合这些素材图片中的元素。
```

### 语言控制

| 语言 | 指令 |
|------|------|
| 中文 | `PPT文字请使用全中文。` |
| 英文 | `Use English for PPT text.` |
| 日文 | `PPTのテキストは全て日本語で出力してください。` |
| 自动 | 不添加语言指令 |

## 图片编辑 Prompt

### 局部重绘

当用户要求修改已生成的图片（如"把这个饼图换成柱状图"）：

```
该PPT页面的原始页面描述为：
{original_description}

现在，根据以下指令修改这张PPT页面：{edit_instruction}

要求维持原有的文字内容和设计风格，只按照指令进行修改。
```

CLI:
```bash
python ~/.claude/skills/yh-slides/scripts/generate_image.py edit \
  --image slide-03.png \
  --prompt "把饼图换成柱状图" \
  --output slide-03-v2.png
```

## 背景提取 Prompt

用于可编辑 PPTX 导出流程中提取干净背景：

```
你是一位专业的图片文字&图片擦除专家。你的任务是从原始图片中移除文字和配图，
输出一张无任何文字和图表内容、干净纯净的底板图。

<requirements>
- 彻底移除页面中的所有文字、插画、图表。必须确保所有文字都被完全去除。
- 保持原背景设计的完整性（包括渐变、纹理、图案、线条、色块等）。保留原图的文本框和色块。
- 对于被前景元素遮挡的背景区域，要智能填补，使背景保持无缝和完整。
- 输出图片的尺寸、风格、配色必须和原图完全一致。
- 请勿新增任何元素。
</requirements>

注意，**任意位置的, 所有的**文字和图表都应该被彻底移除，**输出不应该包含任何文字和图表。**
```

CLI:
```bash
python ~/.claude/skills/yh-slides/scripts/generate_image.py clean-bg \
  --image slide-03.png -o bg-03.png
```

## 文字属性提取 Prompt

从生成的图片中提取文字内容和样式（用于可编辑 PPTX 导出）：

```
你的任务是精确识别这张图片中的文字内容和样式，返回JSON格式的结果。

## 核心任务
请仔细观察图片，精确识别：
1. **文字内容** - 输出你实际看到的文字符号。
2. **颜色** - 每个字/词的实际颜色
3. **空格** - 精确识别文本中空格的位置和数量
4. **公式** - 如果是数学公式，输出 LaTeX 格式

## 输出格式
- colored_segments: 文字片段数组，每个片段包含：
  - text: 文字内容（公式时为 LaTeX 格式）
  - color: 颜色，十六进制格式 "#RRGGBB"
  - is_latex: 布尔值，true 表示 LaTeX 公式片段（可选，默认 false）

只返回JSON对象，不要包含任何其他文字。
```

## 风格提取 Prompt

从参考图片提取风格描述：

```
你是一位专业的 PPT 设计分析师。分析这张图片并提取详细的风格描述，
用于生成具有相似视觉风格的 PPT 幻灯片。

重点关注：
1. 色板：主色、辅色、强调色、背景色
2. 字体风格：印象（衬线/无衬线、粗细、字号层级）
3. 设计元素：装饰图案、形状、图标风格、边框、阴影
4. 整体情绪：专业、活泼、极简、商务、创意等
5. 布局倾向：内容排列方式、间距偏好

输出一段简洁的中文风格描述，可直接用作 PPT 生成的风格提示词。
```

CLI:
```bash
python ~/.claude/skills/yh-slides/scripts/generate_image.py extract-style \
  --image reference.png
```

详细用法见 `references/style-extraction.md`。

---

## 7. Google's 6-Element Formula

```
[Subject] + [Composition] + [Action] + [Location] + [Style] + [Editing]
```

- Subject: what/who is the main focus
- Composition: camera angle, distance (wide, close-up, 85mm)
- Action: what the subject is doing
- Location: where the scene takes place
- Style: artistic style, color palette
- Editing: post-processing (soft focus, high contrast, film grain)

---

## 8. Path B 完整 Base Style 模板

以下 6 种 Base Style 可直接复制使用，定义一次后所有 slide 共用。

### Warm Narrative — 温暖叙事

```
A complete design system for this deck.

VISUAL REFERENCE: TED talk visual style meets Airbnb pitch deck — approachable storytelling.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality sharp rendering.

COLOR SYSTEM:
- Background: warm cream (#FDF6EC) 60%
- Text: dark charcoal (#3D3D3D) 25%
- Accent: coral (#E17055) 15%
- Color creates warmth, trust, human connection

TYPOGRAPHY AS DESIGN:
- Headlines: 36-44pt bold, warm and inviting
- Body: 18-20pt regular, short sentences not bullets
- Size ratio: 3:1 between title and body

COMPOSITION:
- Illustration occupies 40-50% of slide
- Text wraps around or sits beside visuals
- Rounded shapes, soft edges, no sharp corners

VISUAL LANGUAGE: Flat vector illustrations with warm palette, people-centric imagery,
storytelling flow, rounded shapes, hand-drawn feel optional
```

### Neo-Pop Magazine — 新波普

```
A complete design system for this deck.

VISUAL REFERENCE: Supreme lookbook meets HYPEBEAST article — typography as graphic art.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality sharp rendering.

COLOR SYSTEM:
- Background: cream (#FFF8E7) 50%
- Color blocks: hot pink (#FF1493) + cyan (#00CED1) + yellow (#FFD700) 25%
- Text: black (#000000) 25%
- Color creates energy, youth, playful rebellion

TYPOGRAPHY AS DESIGN:
- Headlines: 40-50% of slide area — TYPOGRAPHY IS THE VISUAL
- Body: minimal, 12-14pt
- Size ratio: 10:1 between display and body
- Thick black borders around text blocks

COMPOSITION:
- Modular color blocks with "controlled chaos"
- Stacked asymmetric layouts
- Thick borders as design element
- Content fills 75%, structured chaos not whitespace

VISUAL LANGUAGE: Pixel-art 8-bit icons, cutout photography, speech bubbles,
bold graphic surfaces, sticker/patch aesthetic
```

### Ligne Claire — 清线漫画

```
A complete design system for this deck.

VISUAL REFERENCE: Hergé's Tintin tradition — maximum information clarity through
visual restraint. Every line serves a purpose.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality sharp rendering.

COLOR SYSTEM:
- Background: white/cream (#FFFDF7) 70%
- Illustration: flat saturated fills (3-5 solid colors, no gradients) 20%
- Text: black (#000000) outlines and lettering 10%
- Color is informational, not decorative — each color codes a concept

TYPOGRAPHY AS DESIGN:
- Titles: hand-lettered comic feel, bold and warm
- Body: clean sans-serif, in speech bubbles or caption boxes
- Size ratio: 2.5:1 between title and body
- Key quotes in speech bubbles with pointer tails

COMPOSITION:
- Panel-based layouts (2-4 panels per slide), sequential left-to-right reading
- Clear gutters (white space) between panels
- Each panel advances one idea — no panel is decorative

VISUAL LANGUAGE: Uniform-weight black outlines, flat colors without shading
or hatching, no gradients ever, precise details but zero visual noise,
clean backgrounds, characters with simple but expressive faces
```

### Whiteboard Sketch — 白板手绘

```
A complete design system for this deck.

VISUAL REFERENCE: xkcd "What If?" meets a professor's whiteboard after an
exciting lecture — the beautiful mess of someone thinking out loud.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality sharp rendering.

COLOR SYSTEM:
- Background: pure white (#FFFFFF) 85%
- Ink: black (#000000) for all drawings and text
- Accent: ONE color only (red #FF4444 or blue #4488FF) for highlighting key insights
- The restraint IS the design — monochrome forces focus on the idea

TYPOGRAPHY AS DESIGN:
- Everything hand-drawn/handwritten feel, rough uneven baselines
- Key numbers rendered large (60-80pt) as visual anchors
- Annotations everywhere — arrows, circles, underlines
- Math-style notation where appropriate

COMPOSITION:
- Freeform whiteboard layout, no rigid grid
- Hand-drawn arrows connecting concepts
- Stick figures and simple diagrams
- Informal, alive, like someone just drew this

VISUAL LANGUAGE: Stick figures with expressive poses, hand-drawn wobbly charts
and graphs, annotation arrows, circled keywords, equation-style layouts,
crossed-out wrong answers, "aha!" moments marked with stars
```

### Manga Educational — 学習漫画

```
A complete design system for this deck.

VISUAL REFERENCE: Japanese educational manga (学習漫画) like "Manga Guide to
Statistics" — a character GUIDES you through concepts with reactions and drama.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality sharp rendering.

COLOR SYSTEM:
- Background: white with selective color panels
- Characters: bright warm palette, skin tones + hair colors
- Emphasis: screen-tone gray for flashback/explanation areas
- Accent: manga-style color bursts for key moments

TYPOGRAPHY AS DESIGN:
- Bold manga-style impact titles (thick, slightly angled)
- Body text in speech bubbles and thought clouds
- Onomatopoeia as decorative design elements
- Size contrast 3:1, dramatic for emphasis moments

COMPOSITION:
- Dynamic manga panel layouts (3-5 panels per slide)
- Character reactions drive emphasis — big eyes for surprise, sweat drops for confusion
- Speed lines radiating from key insights
- Reading flow: right-to-left for authenticity, or left-to-right for international

VISUAL LANGUAGE: Expressive anime-style characters, big emotional reaction faces,
manga effects (sparkles, speed lines, impact stars, sweat drops),
panel borders with varied thickness, dramatic angles on key reveals
```

### Warm Comic Strip — 温暖漫画 (Snoopy)

```
VISUAL REFERENCE: Charles Schulz Peanuts comic strip — warm, philosophical, charming.
Characters include round-headed kids, a lovable beagle dog, and a small yellow bird.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: Warm cream/newspaper tone background, soft muted pastels,
warm ink lines (not harsh black). Everything feels like a Sunday morning comic page.
```

**NOTE:** 保持此 Base Style 简短。不要添加详细的颜色比例、构图规则或排版规格——过度约束会扼杀多样性和角色变化。详见 `proven-styles-snoopy.md`。

---

## 9. NotebookLM Slide Prompts

### 风格模板

| 分类 | 模板 |
|------|------|
| Business Editorial | Modern Newspaper, Yellow×Black Editorial, Black×Orange Agency |
| Street/Trendy | Manga Style, Magazine Style, Pink Street-style, Digital Neo Pop |
| Typography-driven | Mincho × Handwritten Mix |
| Art/Avant-garde | Royal Blue×Red Watercolor, Sculpture×Vaporwave, Tech Art Neon |
| Product/Premium | Studio Mockup Premium |
| Athletic/Energy | Sports Athletic Energy |

每个模板定义：Global Design Settings (palette, font hierarchy, grid, icon style) + Layout Variations。

### NotebookLM 最佳实践

1. **Notes as source** — 在 NotebookLM notes 中写大纲，作为 slide 生成来源
2. **Brand book as source** — 上传品牌指南，prompt: "Use the brandbook for branding and styling references"
3. **Refresh old decks** — 上传现有 Google Slides，让 AI 用新品牌重新设计
4. **Multi-source synthesis** — 上传 PDFs + 视频 + 网页链接，AI 跨所有来源合成
5. **Specify audience** — "for busy managers" / "for beginners" / "for investors"
6. **Two-step method** — 先生成演讲稿，再用稿子生成 slides
7. **Avoid topic titles** — 用叙事性主题句代替 "Title: Subtitle" 格式
8. **Upload gold standard** — 上传你最好的过往演示作为风格参考

**Sources:**
- [Google Blog: 8 ways to use Slide Decks in NotebookLM](https://blog.google/technology/google-labs/8-ways-to-make-the-most-out-of-slide-decks-in-notebooklm/)
- [GitHub: awesome-notebookLM-prompts](https://github.com/serenakeyitan/awesome-notebookLM-prompts)
- [XDA Developers: 3 NotebookLM prompts for slides](https://www.xda-developers.com/notebooklm-prompts-to-make-presentation-slides/)

---

## 10. Public Prompt Resources

| Resource | Link | Highlights |
|----------|------|-----------|
| Superside: 15+ AI Prompts for Presentations | [Link](https://www.superside.com/blog/ai-prompts-presentations) | Full-type templates: business, case study, webinar |
| Slidesgo Smart Guide | [Link](https://slidesgo.com/slidesgo-school/ai-presentations/best-ai-prompts-presentations-smart-guide) | 8 core templates + prompt methodology |
| SlidesAI: 75+ Presentation Prompts | [Link](https://www.slidesai.io/blog/prompts-to-make-presentations-with-ai) | 75+ ready-to-use prompts by scenario |
| awesome-notebookLM-prompts | [Link](https://github.com/serenakeyitan/awesome-notebookLM-prompts) | 20+ visual style YAML templates |
| Sabrina Ramonov: Viral PowerPoints | [Link](https://www.sabrina.dev/p/viral-powerpoints-slides-free-notebooklm) | 3-tier framework with 14 viral layouts |
| Google: Gemini Image Prompting | [Link](https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/) | 6-element formula for image prompts |
| DataCamp: NotebookLM Guide | [Link](https://www.datacamp.com/tutorial/notebooklm) | Full NotebookLM tutorial with slides |
