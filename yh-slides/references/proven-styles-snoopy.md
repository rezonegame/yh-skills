# Snoopy / Peanuts Style Guide — 温暖漫画风详细模板

> "Like a Peanuts comic strip — warm, philosophical, charming"
> 基于 Charles Schulz 的 Peanuts 漫画美学，经过多次 AI 生成实验验证的最佳实践。

---

## 1. Base Style Prompt

保持简短，不超过 5 行。定义一次，所有 slide 共用。

```
VISUAL REFERENCE: Charles Schulz Peanuts comic strip — warm, philosophical, charming.
Characters include round-headed kids, a lovable beagle dog, and a small yellow bird.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: Warm cream/newspaper tone background, soft muted pastels, warm ink lines.
```

### 关键原则

- **不指定颜色比例**（如 40%/30%/15%）——让 AI 自由发挥
- **不指定角色姿势**（如 "beagle lying on red doghouse"）——让 AI 创造多样性
- **不指定字体大小**（如 "title 48pt"）——不适用于 AI 图片生成
- **不指定构图位置**（如 "title centered, image on right"）——让 AI 做设计决策
- **只描述情绪和内容**——温暖、哲理、迷人

---

## 2. Cover Slide Template — 封面 slide

```
Create a warm, inviting cover slide for a presentation about [topic].

VISUAL REFERENCE: Charles Schulz Peanuts comic strip — warm, philosophical, charming.
Characters include round-headed kids, a lovable beagle dog, and a small yellow bird.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: Warm cream/newspaper tone background, soft muted pastels, warm ink lines.

TEXT TO RENDER:
- Title: "[标题文字]"
- Subtitle: "[副标题文字]"

DESIGN INTENT: The viewer should feel like opening the Sunday comics — anticipation, warmth, and a gentle smile.
```

### 变体提示

- 可在 mood 描述中加入主题相关的场景提示（如 "autumn afternoon" / "sunny morning"）
- 不要指定角色在做什么——让 AI 根据主题自由创作
- 封面 slide 的文字尽量短（标题 ≤8 字）

---

## 3. Content Slide Templates — 内容 slide

### 变体 A：概念解释型

```
Create a slide explaining [concept] in a warm, approachable way.

[Base Style]

TEXT TO RENDER:
- Title: "[概念名称]"
- Key point 1: "[要点1]"
- Key point 2: "[要点2]"
- Key point 3: "[要点3]"

DESIGN INTENT: Make the viewer feel like a wise friend is explaining something simple that turns out to be profound.
```

### 变体 B：问题/挑战型

```
Create a slide about the challenge of [problem], presented with gentle humor and insight.

[Base Style]

TEXT TO RENDER:
- Title: "[问题描述]"
- Body: "[正文内容]"

DESIGN INTENT: Like a Peanuts strip where Charlie Brown faces a familiar frustration — relatable, warm, and ultimately hopeful.
```

### 变体 C：对比/比较型

```
Create a slide comparing [A] and [B], showing the contrast in a thoughtful way.

[Base Style]

TEXT TO RENDER:
- Title: "[对比主题]"
- Left: "[A 的描述]"
- Right: "[B 的描述]"

DESIGN INTENT: Two panels, two perspectives — like the dialogue between different Peanuts characters, each with their own truth.
```

### 变体 D：流程/步骤型

```
Create a slide showing [N] steps to [achieve something], told as a gentle journey.

[Base Style]

TEXT TO RENDER:
- Title: "[流程标题]"
- Step 1: "[步骤1]"
- Step 2: "[步骤2]"
- Step 3: "[步骤3]"

DESIGN INTENT: A story unfolding panel by panel — each step is a small adventure, like walking through a familiar neighborhood.
```

### 变体 E：列表/要点型

```
Create a slide presenting [N] key insights about [topic].

[Base Style]

TEXT TO RENDER:
- Title: "[标题]"
- Point 1: "[要点1]"
- Point 2: "[要点2]"
- Point 3: "[要点3]"

DESIGN INTENT: Like reading a letter from a thoughtful friend who has distilled wisdom into a few honest sentences.
```

---

## 4. Data/Statistics Slide Template — 数据 slide

```
Create a data slide showing [metric/data], making numbers feel warm and human.

VISUAL REFERENCE: Charles Schulz Peanuts comic strip — warm, philosophical, charming.
Characters include round-headed kids, a lovable beagle dog, and a small yellow bird.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: Warm cream/newspaper tone background, soft muted pastels, warm ink lines.

TEXT TO RENDER:
- Title: "[数据标题]"
- Hero number: "[关键数字]"
- Context: "[数据背景/说明]"

DESIGN INTENT: Numbers should feel like characters telling a story — the "23%" is a round-headed kid with something important to say, not a cold statistic.

VISUAL NARRATIVE: Present the data in a hand-drawn, approachable way — like a child explaining something surprising they discovered. Charts should look like they could appear in a Peanuts Sunday strip.
```

### 使用建议

- 关键数字可以让 AI 放大突出（如把 "23%" 画成大字）
- 避免复杂的图表类型——简单柱状图或饼图效果最好
- 数据的文字说明保持口语化，不要用术语堆砌

---

## 5. Quote Slide Template — 引用 slide

```
Create a quote slide that feels like a moment of quiet wisdom from a Sunday comic.

[Base Style]

TEXT TO RENDER:
- Quote: "[引用内容]"
- Attribution: "— [作者/来源]"

DESIGN INTENT: The viewer should pause and reflect — this is the Peanuts panel where the character says something simple that changes how you see the world.
```

### 变体

- 如果引用较长，可以拆成多行，让 AI 排版
- 作者名字保持简短（中文名 ≤6 字，英文名用缩写）

---

## 6. Closing Slide Template — 结尾 slide

### 变体 A：温暖收束

```
Create a closing slide with a sense of gentle completion and hope.

[Base Style]

TEXT TO RENDER:
- Main message: "[结束语]"
- Call to action: "[行动号召，如有]"

DESIGN INTENT: Like the final panel of a Peanuts story arc — the characters are still there, the world continues, and somehow everything feels a little bit warmer.
```

### 变体 B：感谢页

```
Create a thank you slide that feels sincere and warm, not corporate.

[Base Style]

TEXT TO RENDER:
- "谢谢" or "Thank you"
- Optional: "[联系信息]" / "[一句话感想]"

DESIGN INTENT: Like a handwritten thank-you note — genuine, brief, and making you smile.
```

---

## 7. Key Experiences and Tips — 关键经验总结

### 经验 1：不要过度约束（最重要）

> 这是经过数十次生成实验得出的最重要结论。

**错误做法：**
```
A beagle dog with black ears and white body lying on top of a red doghouse
with a sign saying "SNOOPY" on the left side of the slide.
On the right side, a round-headed boy with a yellow shirt stands looking up.
The background is a light cream color making up 60% of the slide.
Title text at top center in bold font.
```
→ 每张 slide 都长一样，AI 被锁死在固定构图里。

**正确做法：**
```
Create a warm comic strip style slide about [topic].

VISUAL REFERENCE: Charles Schulz Peanuts comic strip — warm, philosophical, charming.
CANVAS: 16:9, 2048x1152.
COLOR SYSTEM: Warm cream background, soft muted pastels, warm ink lines.

TEXT TO RENDER:
- Title: "[text]"
- Body: "[text]"

DESIGN INTENT: [描述情绪]
```
→ 每张 slide 都有独特构图，但风格统一。

### 经验 2：让 Base Style 只出现一次

Base Style 在 prompt 末尾追加，但 **不要在每个 slide prompt 中重复完整 Base Style**。最佳实践：

1. 定义一次 Base Style（见第 1 节）
2. 每个 slide prompt 只写 `[Base Style]` 占位符 + 内容 + 情绪
3. 实际生成时替换为完整 Base Style

### 经验 3：情绪 > 细节

AI 擅长理解 "feeling"，不擅长执行 "specification"。

| 效果差 | 效果好 |
|--------|--------|
| "a bar chart on the left side" | "numbers that tell a story" |
| "title in bold 48pt font" | "a message that feels handwritten and sincere" |
| "3 panels arranged horizontally" | "a story unfolding naturally" |
| "warm cream background 60%" | "the warmth of a Sunday morning" |

### 经验 4：中文文字要短

| 情况 | 建议 |
|------|------|
| 标题 ≤8 字 | 最佳，渲染准确 |
| 标题 9-15 字 | 可接受，偶尔出错 |
| 正文 ≤30 字 | 最佳 |
| 正文 >30 字 | 考虑拆分到多个 slide |

### 经验 5：封面和结尾最重要

1. **Cover slide** — 一定生成 AI 插画/图片，设定整个 deck 的视觉基调
2. **Closing slide** — 可选但强烈推荐，留下深刻印象
3. **中间 slide** — 选择性地为 2-3 个 "aha moment" slide 生成插画

### 经验 6：接受 AI 的诠释

AI 不会画出 Snoopy（版权原因），但会画出"圆头小孩+可爱小狗+小黄鸟"的温暖世界。这种诠释正是我们想要的——灵感来自 Peanuts，但不是 Peanuts 的复制。

如果你发现 AI 画出了过于相似的角色，**不要在 prompt 中添加 "NOT Snoopy"**。相反，改变情绪描述或内容主题，AI 自然会调整角色造型。

---

## 8. Quick Reference — 快速参考

### Base Style (复制粘贴)

```
VISUAL REFERENCE: Charles Schulz Peanuts comic strip — warm, philosophical, charming.
Characters include round-headed kids, a lovable beagle dog, and a small yellow bird.
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: Warm cream/newspaper tone background, soft muted pastels, warm ink lines.
```

### Slide Checklist

| Slide 类型 | 是否需要插画 | 注意事项 |
|---|---|---|
| Cover | 是 | 设定视觉基调 |
| 内容 slide | 选 2-3 张 | 选择 "aha moment" |
| 数据 slide | 可选 | 简单图表最好 |
| 引用 slide | 推荐 | 情绪要温柔 |
| 结尾 slide | 推荐 | 留下温暖印象 |

### 生成命令

```bash
python ~/.claude/skills/yh-slides/scripts/generate_image.py generate \
  "[complete prompt with Base Style]" \
  --output "slide-[NN]-[name].png" \
  --image-size 2K
```
