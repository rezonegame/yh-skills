# GPT-Image-2 高级 Prompt 模式

来源：`nexu-io/open-design` 的 43 个 image prompt-templates（Apache-2.0 / CC-BY-4.0）。本文件提取其中超出常规模板的高级模式，与 `structured-templates.md`、`ecommerce-scene-templates.md` 互补。

## 目录

1. [Global Style Tokens + Negative Prompt](#1-global-style-tokens--negative-promptgstnp-模式)
2. [HUD 叠加规范](#2-hud-叠加规范游戏-ui--桌游数字版)
3. [拆解图结构化规范](#3-拆解图结构化规范exploded-view)
4. [Pose Grid 动作分解表](#4-pose-grid-动作分解表44--33)
5. [Storyboard 序列](#5-storyboard-序列6-8-连拍)
6. [相机参数指定](#6-相机参数指定camera-settings)
7. [Anti-AI-Slop 清单](#7-anti-ai-slop-清单来自-open-design)
8. [2×2 编辑拼贴](#8-22-编辑拼贴fashion-editorial-collage)
9. [品牌发布会海报](#9-品牌发布会海报announcement-poster)
10. [12 格旅行拼贴](#10-12-格旅行拼贴travel-snapshot-collage)

---

## 1. Global Style Tokens + Negative Prompt（GST+NP 模式）

适用于需要多图一致性的场景：系列卡牌、8 连拍、分镜、动作分解。

**原理：** 将风格定义拆成两块——GST（全局风格令牌，正向）和 NP（负面提示，反向）。每张图的 prompt = GST + 单图内容 + NP。三段拼合，确保风格统一且避免常见翻车。

### GST 模板

```text
## GLOBAL STYLE TOKENS
ultra-high definition, 8K, crisp fine detail, textured skin, natural complexion,
native ambient light, subtle atmosphere, minimal backdrop, gentle motion blur,
kinetic tension, natural posture, refined features, relaxed mood, filmic grain,
low-saturation premium color grading, full-body framing, clean uncluttered frame,
authentic human texture, candid capture feel
```

### NP 模板

```text
## NEGATIVE PROMPT
deformed limbs, distorted hands or feet, warped face, motion smear, compression
artifacts, stray clutter, text watermark, heavy occlusion, broken proportions,
stiff posture, over-exposed skin, trashy texture, exaggerated deformity,
duplicated elements, pixelated grain
```

### 使用方式

为系列图锁定一套 GST 和 NP，每张图只改变中间的主体描述：

```text
{GST}
Medium half-body shot, a warrior mage holding a glowing staff, dynamic pose, warm rim light.
{NP}
```

```text
{GST}
Full-body wide shot, the same warrior mage casting a spell, arms raised, energy swirling.
{NP}
```

### 桌游卡牌应用

为一套 10 张角色卡牌锁定 GST（画风、光照、质感、边框感），每张只换角色名、职业、动作和主色调：

```text
## GST（锁定）
Fantasy card art, painterly oil-painting style, dramatic chiaroscuro lighting,
rich saturated colors, aged parchment border with gold filigree frame,
ornate corner flourishes, 2:3 vertical card format, 8K ultra-detailed,
no modern elements, no text overlay, no watermark

## NP（锁定）
blurry, low-res, modern clothing, plastic texture, flat lighting, cartoon style,
chibi proportions, extra limbs, deformed face, text, watermark, signature

## 单卡内容
A stoic dwarven blacksmith, muscular build, braided beard with iron rings,
leather apron over chainmail, holding a glowing warhammer, sparks flying,
warm forge light from below, dark stone workshop background.
```

---

## 2. HUD 叠加规范（游戏 UI / 桌游数字版）

适用于游戏截图、桌游 App UI、玩家面板数字版。

**原理：** 将 3D 场景和 UI 叠加层分开描述。先写场景（主体、环境、光照），再写 HUD（面板位置、内容、字体、颜色）。最后声明 UI 占比和字体规则。

### 结构

```text
# 3D Scene (underneath the UI)
- Center of frame: {character description}
- Environment: {scene description}
- Lighting: {lighting description}

# HUD overlay (drawn cleanly on top, readable, game-screenshot accurate)
- Top-left: {character status panel}
- Top-right: {minimap}
- Bottom-center: {skill hotbar / action bar}
- Bottom-left: {chat / log window}
- World-space UI: {floating labels, quest markers}

# Typography & language rules
- All text in clean Simplified Chinese (Song/serif for headings, sans for body)
- No garbled glyphs, no Latin filler
- HUD takes no more than ~25% of total frame area

# Negative prompt
no warped Chinese characters, no fake gibberish glyphs, no low-res UI,
no duplicated HUD widgets, no floating crooked text, no watermark
```

### 桌游玩家面板应用

```text
# Game board scene
A fantasy adventure game board viewed from above, hexagonal terrain tiles
with forests, mountains, and rivers, wooden player pieces, card decks fanned out.

# Player panel HUD overlay
- Top-left: Player portrait in ornate frame, name "艾拉·风行者", class "游侠"
- Below portrait: HP bar (red, 12/15), MP bar (blue, 8/10), Action points (3 gold circles)
- Top-right: Turn indicator "回合 3/10", round tracker with moon phases
- Bottom: 5 action card slots with icons (Move, Attack, Defend, Skill, Rest)
- Right edge: Quest tracker panel with 2 active quests

# Typography
All Chinese, Song for headings, sans for body. Clean, readable at a glance.
```

---

## 3. 拆解图结构化规范（Exploded View）

适用于桌游组件拆解、产品爆炸图、文创工艺展示。

**原理：** 用 JSON 结构定义拆解层级、标注线、图例位置。比自然语言描述更精确。

### 结构

```json
{
  "type": "exploded view product diagram poster",
  "subject": "{product}",
  "style": "clean high-tech 3D render, studio lighting, glowing accents",
  "background": "{gradient or solid}",
  "header": {
    "logo": "{brand + product name}",
    "subtitle": "{tagline}"
  },
  "layout": {
    "centerpiece": "vertically stacked exploded view showing {N} distinct layers",
    "callout_labels": {
      "count": 8,
      "left_side": ["label 1", "label 2", "label 3"],
      "right_side": ["label 4", "label 5", "label 6", "label 7", "label 8"]
    },
    "footer": {
      "left_text_block": { "headline": "{headline}", "body": "{description}" },
      "right_logo": "{brand}"
    }
  }
}
```

### 桌游组件拆解应用

```json
{
  "type": "board game component exploded view poster",
  "subject": "Fantasy Adventure Board Game - Complete Components",
  "style": "warm editorial photography, soft directional lighting, dark walnut surface",
  "background": "deep charcoal with subtle parchment texture",
  "header": {
    "logo": "龙之谷：暗影之战",
    "subtitle": "每一件组件，都是冒险的起点"
  },
  "layout": {
    "centerpiece": "vertically stacked exploded view: box lid → game board (unfolded) → 3 card decks in fanned stacks → token sheet with punch-out markers → 6 colored dice → wooden meeples → rulebook → player aid cards → insert tray",
    "callout_labels": {
      "count": 9,
      "left_side": [
        "游戏版图\n双面印刷，含 6 个区域",
        "角色卡牌组\n52 张，含 8 个职业",
        "事件卡牌组\n30 张随机事件"
      ],
      "right_side": [
        "资源标记\n40 个木质圆形标记",
        "命运骰\n6 颗 12mm 专属骰子",
        "规则书\n24 页全彩印刷",
        "玩家助卡\n4 张双面参考卡",
        "收纳内托\n定制 EVA 内衬"
      ]
    }
  }
}
```

---

## 4. Pose Grid 动作分解表（4×4 / 3×3）

适用于角色动作参考、卡牌姿态系列、教学图解。

**原理：** 将 N 个动作姿态排列在网格中，每格一个完整姿态，共享角色外观，背景纯色统一。适合 AI 视频生成的参考图，也适合桌游角色卡的姿态系列。

### 结构

```text
A SINGLE vertical image composed as a 4x4 grid of 16 connected square panels.

CHARACTER (must be IDENTICAL in all panels):
{character description - hair, outfit, proportions, face}

LAYOUT RULES:
- Exactly 4 columns × 4 rows = 16 equally-sized square cells
- Thin clean black grid lines separating cells
- Each cell shows the character FULL BODY (head to toe visible)
- Plain solid background behind character in every cell — NO complex backgrounds
- Character centered in each cell, taking up about 75% of cell height
- Camera angle: straight-on full-body shot, same eye-level in every cell
- Each cell has a small caption at the bottom showing the pose name
- Numbered 1 through 16 in circles at top-left corner

POSES:
Panel 1: {pose description}
Panel 2: {pose description}
...

Header text: "{title}"

Negative prompt: no watermark, no warped text, no inconsistent character,
no motion blur, no extra fingers, no cropped limbs
```

### 桌游角色卡应用（8 职业 × 2 姿态 = 16 格）

```text
A 4x4 grid poster showing 8 fantasy character classes in 2 poses each.

CHARACTER STYLE: Painterly fantasy card art style, dramatic lighting,
rich colors, aged parchment feel.

Panel 1-2: WARRIOR - (1) defensive shield stance, (2) overhead sword strike
Panel 3-4: MAGE - (1) hands channeling fire, (2) casting beam forward
Panel 5-6: ROGUE - (1) crouching with daggers, (2) mid-backstab leap
Panel 7-8: RANGER - (1) drawing bow, (2) dual-wielding short swords
Panel 9-10: CLERIC - (1) healing prayer pose, (2) smite with mace
Panel 11-12: PALADIN - (1) shield raised, (2) charging with lance
Panel 13-14: BARD - (1) playing lute, (2) inspiring allies with rapier
Panel 15-16: NECROMANCER - (1) summoning undead, (2) life drain pose

Header: "龙之谷 · 八大职业"
```

---

## 5. Storyboard 序列（6-8 连拍）

适用于角色展示序列、产品发布节奏、短视频分镜。

**原理：** 定义共享角色锁定（Character Lock）+ 每帧独立描述。确保角色在所有帧中完全一致，只改变姿态、机位和光照。

### 结构

```text
# [Title] — 8-Shot Storyboard

## SHARED CHARACTER LOCK (keep identical across all shots)
- Subject: {character}
- Hair: {hair description}
- Outfit: {outfit description}
- Expression baseline: {mood}
- Body language: {body type and posture}

## SHOT 1 — {shot name} ({framing}, {motion})
{style tokens}, {framing} shot, {character in specific pose},
{lighting}, {background}, {mood}. {negative prompt}.

## SHOT 2 — {shot name} ({framing}, {motion})
...
```

### 桌游角色展示应用

```text
# 角色卡牌展示 — 6-Shot Storyboard

## SHARED CHARACTER LOCK
- Subject: Female elven ranger, early 20s, athletic build
- Hair: Long silver-white hair with leaf braids
- Outfit: Forest green leather armor, emerald cloak, quiver on back
- Expression: Calm, focused, slightly mysterious
- Body language: Graceful, agile, predator-like poise

## SHOT 1 — Ready Stance (Half-Body, Static)
Card art style, half-body shot, ranger standing with bow at rest,
dappled forest light, ancient tree background, calm alert mood.

## SHOT 2 — Drawing Bow (Full-Body, Tension)
Card art style, full-body shot, ranger drawing bowstring to cheek,
aiming forward, dramatic rim light, forest clearing, intense focus.

## SHOT 3 — Arrow in Flight (Close-Up, Action)
Card art style, close-up on hands and bow, arrow just released,
motion blur on arrow, sharp focus on bowstring, dramatic lighting.

## SHOT 4 — Evasion (Full-Body, Motion)
Card art style, full-body shot, ranger mid-dodge to the left,
cloak flying, arrows whizzing past, dynamic low angle, forest chaos.

## SHOT 5 — Dual Blade (Close-Up, Combat)
Card art style, close-up, ranger with twin short swords drawn,
crossed in front of face, fierce expression, blood spatter, dark mood.

## SHOT 6 — Victory (Full-Body, Still)
Card art style, full-body shot, ranger standing victorious,
bow raised overhead, sunset backlight, fallen enemies in blur,
triumphant serene expression, golden hour warmth.
```

---

## 6. 相机参数指定（Camera Settings）

适用于需要精确控制画面质感的摄影类 prompt。

**原理：** 在 prompt 末尾指定相机参数，控制景深、透视、噪点等。

### 常用参数

```text
Camera: full-frame mirrorless, 85mm lens, f/2.0, ISO 100, 1/200s
→ 浅景深人像，锐利主体，柔和背景虚化

Camera: full-frame, 35mm lens, f/5.6, ISO 400, 1/60s
→ 中等景深环境人像，更多背景细节

Camera: full-frame, 50mm lens, f/1.4, ISO 200, 1/125s
→ 极浅景深，奶油般的虚化，适合产品特写

Camera: full-frame, 24mm lens, f/8, ISO 100, 1/250s
→ 广角深景深，适合场景全景

Camera: APS-C, 16mm lens, f/11, ISO 100, 1/125s
→ 超广角建筑/空间，透视夸张
```

### 桌游产品摄影应用

```text
Board game box and components arranged on dark wood table,
warm side lighting, shallow depth of field focusing on box front.
Camera: full-frame mirrorless, 50mm lens, f/1.8, ISO 200, 1/100s.
Bokeh on background components, sharp focus on gold foil title.
```

---

## 7. Anti-AI-Slop 清单（来自 Open Design）

Open Design 在 prompt 层面内置了 5 道防线，防止 AI 生成内容"看起来像 AI"：

### 7.1 Question Form First

Turn 1 只用 `<question-form>` 收集需求，不急着生成。先确认方向再动手。

### 7.2 Brand-Spec Extraction

用户给截图或 URL 时，先跑五步协议（locate → download → grep hex → codify brand-spec → vocalise），再写 prompt。**永远不从记忆猜品牌色。**

### 7.3 Five-Dim Critique

生成前自评 1-5 分，低于 3 分就重做：
- Philosophy（是否传达了正确的情感）
- Hierarchy（信息层级是否清晰）
- Execution（执行是否精确）
- Specificity（是否足够具体，不是泛泛而谈）
- Restraint（是否克制，没有过度装饰）

### 7.4 P0/P1/P2 Checklist

每个 skill 自带检查清单。P0 是必须通过的硬性门槛，P1 是强烈建议，P2 是锦上添花。

### 7.5 Slop Blacklist

以下元素被明确禁止：
- Aggressive purple gradients（暴力紫色渐变）
- Generic emoji icons（通用 emoji 图标）
- Rounded card with left-border accent（左边框圆角卡片）
- Hand-drawn SVG humans（手绘 SVG 小人）
- Inter as a display face（Inter 用于标题）
- Invented metrics（编造的数据指标）
- Honest placeholders > fake stats（诚实的占位符 > 假数据）

---

## 8. 2×2 编辑拼贴（Fashion Editorial Collage）

适用于产品多角度展示、角色多姿态卡片、品牌视觉拼贴。

**原理：** 定义 2×2 四格拼贴，每格一个独立姿态/角度，共享造型和光照。适合 4:5 竖版社媒发布。

### 结构

```text
2x2 photo collage of the same {subject}.
Consistent styling across all four panels.
Top left: {pose/angle 1}
Top right: {pose/angle 2}
Bottom left: {pose/angle 3}
Bottom right: {pose/angle 4}
Clean balanced collage grid, seamless composition.
Camera: full-frame mirrorless, 85mm lens, f/2.0, ISO 100, 1/200s.
Aspect ratio: 4:5.
```

### 桌游卡牌展示应用

```text
2x2 card art collage of the same fantasy character, a elven archer.
Consistent painterly style, dramatic lighting, rich colors.

Top left: portrait close-up, determined expression, hood up.
Top right: full-body action pose, drawing bow, mid-leap.
Bottom left: detail shot of enchanted bow with glowing runes.
Bottom right: environmental shot, standing on cliff overlooking forest.

Clean balanced grid, parchment border between panels, gold corner accents.
8K, fantasy card art quality. Aspect ratio: 4:5.
```

---

## 9. 品牌发布会海报（Announcement Poster）

适用于桌游新品发布、众筹上线、扩展包预告。

**原理：** 参考体育转会宣布海报的结构——大字标题、人物主视觉、品牌标识、标语、日期。层次分明，冲击力强。

### 结构

```text
Create a dramatic announcement poster in vertical social-media format.

Character: {hero character, chest-up framing, dramatic pose}
Color palette: {primary brand color} with {accent colors}

Background: layered graphic with {brand symbol} oversized in background,
{secondary element} silhouette, painterly brush-stroke textures, grunge.

Left side: stacked slogan text in bold uppercase: "{slogan}"
Center: huge distressed block headline "{NAME}"
Overlay: handwritten script across headline saying "{tagline}"
Bottom: brand name + year + small badges

Cinematic lighting, high contrast, premium poster design, sharp texture,
moody shadows, gritty editorial finish.
```

### 桌游发布海报应用

```text
Create a dramatic board game launch poster, vertical 4:5.

Hero: a fierce dragon emerging from darkness, glowing red eyes,
dramatic chest-up framing, scales catching rim light.

Color palette: deep midnight blue with gold and crimson accents.

Background: oversized dragon wing silhouette filling upper half,
ancient map texture, painterly smoke effects, subtle grunge.

Left side: stacked text "全新策略桌面游戏" in bold gold serif.
Center: huge distressed block headline "龙之谷" in aged gold.
Overlay: red brush stroke "2026 年度巨献" across the title.
Bottom: "策略 · 冒险 · 对抗 · 2-4 人 · 60 分钟" with dragon icon badges.

Cinematic lighting, high contrast, premium game box art quality.
```

---

## 10. 12 格旅行拼贴（Travel Snapshot Collage）

适用于旅行主题文创、城市主题桌游、生活方式产品展示。

**原理：** 12 张手机随拍风格的照片拼成不规则网格，每张都有随机感、不完美感。适合展示"真实体验"而非"精修大片"。

### 结构

```text
A 12-frame collage of candid snapshots of {subject} in {location}.
Each frame feels like a fleeting personal memory — imperfect, intimate, unposed.

Scenes include: {scene 1}, {scene 2}, {scene 3}...

Shot with smartphone aesthetic: slight motion blur, soft focus,
blown-out highlights, lens flare, high ISO noise at night,
uneven framing, accidental cropping.

Composition feels random — subject sometimes off-center, partially cut off.

Lighting varies: {lighting 1}, {lighting 2}, {lighting 3}.

Color grading: faded cinematic tones, slightly desaturated,
warm highlights, nostalgic film-like look, subtle grain.

Layout: 12 images in a loose, imperfect collage grid,
slightly tilted and misaligned like a scrapbook.

No text, no watermark.
```
