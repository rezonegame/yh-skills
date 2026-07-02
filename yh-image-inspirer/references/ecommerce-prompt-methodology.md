# 电商 Prompt 方法论

来源：`gpt-image2-ecommerce` 的 SKILL.md 工作流、Prompt 写法指南、Anti-AI 防坑规则，以及 25 个 JSON 模板中的 `category_tips`、`examples`、`variants`。

本文件与 `ecommerce-scene-templates.md`（场景模板）互补：场景模板负责"选哪个模板"，本文件负责"怎么写好 prompt"和"怎么避免翻车"。

## 目录

- Prompt 写法五原则
- Anti-AI 防坑规则
- 桌游与文创品类适配
- 通用 Prompt 组装公式

---

## Prompt 写法五原则

### 1. 简洁为王

只写核心信息，不过度约束。GPT-Image-2 对简洁集中的 prompt 表现最好，塞太多修饰词反而降低主体识别度。

**好：**
```text
frosted glass serum bottle with matte white cap, soft studio lighting, white background, 8K
```

**差：**
```text
A beautiful, stunning, hyper-realistic, incredibly detailed, professional, high-quality photograph of an elegant frosted glass serum bottle with a luxurious matte white cap, placed on a pristine white surface, illuminated by perfectly soft diffused studio lighting from multiple angles, shot with a Canon EOS R5 at f/2.8...
```

### 2. 自然语言优先

GPT-Image-2 理解描述性句子比关键词堆叠更好。用自然的短句描述画面，而不是堆标签。

**好：**
```text
A card game box standing upright on a dark wooden table, warm side lighting casting soft shadows, gold foil details catching the light
```

**差：**
```text
card game box, upright, dark wood table, warm light, side lighting, shadows, gold foil, details, 8K, commercial
```

### 3. 材质描述要具体

显式描述纹理和材质，不要省略。这是区分"高级感"和"塑料感"的关键。

**桌游/文创常用材质词：**
- 卡牌：`matte laminated cardstock`, `linen-textured card`, `glossy UV-coated surface`, `embossed gold foil detail`
- 盒面：`rigid cardboard with spot UV coating`, `soft-touch matte finish`, `metallic foil stamping`
- 版图：`foldable game board with linen finish`, `thick chipboard with rounded corners`
- 文创：`washi paper texture`, `ceramic with crackle glaze`, `embroidered fabric`, `handmade paper with visible fibers`

### 4. 光照很重要

始终包含光照方向和质量。一个场景换光照，风格完全不同。

**桌游/文创常用光照：**
| 效果 | 描述 |
|------|------|
| 产品主图 | `soft diffused studio lighting, even illumination` |
| 氛围感 | `warm side lighting from left, soft shadows on right` |
| 高端感 | `Rembrandt lighting, subtle rim light on edges` |
| 自然感 | `natural window light from top-left at 45 degrees` |
| 戏剧性 | `dramatic overhead spotlight, dark surroundings` |
| 开箱感 | `bright even lighting, slight warmth, inviting` |

### 5. 善用参考图

传递产品实拍图作为 `--image` 参数，能显著提升产品识别一致性。对于桌游盒面、卡牌美术、文创产品，参考图几乎是必须的。

---

## Anti-AI 防坑规则

适用于 UGC/买家秀/社媒/小红书/直播截图等需要"真实感"的场景。

### 核心规则

1. **指定手机型号**：`iPhone 14 Pro`、`iPhone 15 Pro`。不要写"smartphone"。
2. **加入可见瑕疵**：毛孔、噪点、暖色偏色、构图不完美、轻微失焦。
3. **使用随性语言**：`NOT professional photography`、`NOT AI-generated look`。
4. **展示真实环境**：略微凌乱的桌面、水渍、用过的毛巾、散落的配件。
5. **参考胶片色调**：`Kodak Portra 400 color feel`、`warm yellow cast`。
6. **显式声明**：`NOT retouched, NOT smoothed, NOT AI-generated look`。
7. **避免 AI 签名词**：不用 `perfect`、`flawless`、`stunning`、`hyper-realistic`。

### CCD 复古胶片感（适合文创怀旧风）

```text
Vintage 2005 CCD digicam photo, harsh direct on-camera flash. Heavy film grain, blown-out highlights, strong yellow-green color shift, chromatic aberration at edges. Person holding {product} with casual expression. Dim room with string lights. Off-center, slightly tilted. Red date stamp '06.12.25' in bottom-right corner. Low resolution, NOT sharp, NOT AI-generated look.
```

### 小红书种草风

```text
Ultra-realistic Xiaohongshu RED product lifestyle photo, iPhone 15 Pro, NOT professional photographer. Slightly tilted angle, {product} on {surface}. Environmental details: slight water stain, natural shadows, lived-in feel. iPhone warm auto-white-balance, natural noise, NOT sharpened, Kodak Portra 400 feel, NOT AI-generated look, 8K.
```

---

## 桌游与文创品类适配

为 25 个电商场景模板补充桌游和文创业的专属提示。

### 01. 白底主图（Hero Image）

**品类提示：** Box front angle at 15-degree tilt to show depth, gold foil and spot UV details catching light, age rating and player count icons visible, shrink-wrap reflection on edges.

**示例：**
```text
Board game box, rigid cardboard with spot UV coating, standing at 15-degree tilt on clean white background. Gold foil title catching soft studio light, shrink-wrap edge visible. Age 14+, 2-4 players icons. Professional packshot, 8K.
```

### 02. 生活方式场景（Lifestyle）

**品类提示：** Show the game mid-play on a real table, cards fanned out, dice mid-roll, player hands reaching in, snack bowls and drinks at edges. Warm living room atmosphere.

**示例：**
```text
Family playing a board game at a dining table, top-down angle. Cards fanned out, dice mid-roll, wooden meeples placed on the board. Warm living room lighting, pizza box and juice glasses at edges. Genuine laughter, candid moment, NOT posed. iPhone 15 Pro, natural noise, 8K.
```

### 03. 平铺图（Flat Lay）

**品类提示：** All game components spread top-down: box, board, cards in stacks, dice, tokens, rulebook, player aids. Group by type with breathing room. Use a dark wood or felt surface.

**示例：**
```text
Board game complete component flat lay, top-down photography. Center: game board unfolded. Surrounding: card decks in neat stacks, dice pool, wooden tokens in cloth bag, rulebook, player aid cards. Dark walnut wood surface. Soft natural window light from top-left. Color palette: deep navy, gold, cream. 8K, no text, no watermark.
```

### 04. 细节微距（Detail Macro）

**品类提示：** Card texture close-up showing linen finish, embossed details, foil stamping. Board corner showing fold quality. Token surface showing paint detail.

**示例：**
```text
Macro close-up of a board game card surface, showing linen-textured cardstock with embossed gold foil icon. Shallow depth of field, sharp focus on foil detail, soft blur on card edge. Studio macro lighting, 8K, ultra-detailed texture.
```

### 05. 海报/Banner（Poster）

**品类提示：** Game box as hero element, component fan-out below, key selling points as callout badges (player count, duration, age), dramatic lighting, event/campaign info.

**示例：**
```text
Board game promotional poster. Hero: game box at dramatic angle with spotlight. Below: component spread (cards, board, tokens). Callout badges: "2-4 Players", "60 min", "Age 14+". Dark gradient background. Campaign title at top. Bold typography, gold accents. 4:5 ratio, 8K.
```

### 06. 社交媒体（Social Media）

**品类提示：** 小红书种草：game unboxing on desk, rulebook open, first play moment. Instagram: styled flat lay with aesthetic props. TikTok: dramatic unboxing moment.

**小红书示例：**
```text
Xiaohongshu RED unboxing photo, iPhone 15 Pro. Board game box half-open on a wooden desk, rulebook pulled out, a few cards and tokens scattered. Warm desk lamp lighting, coffee mug at edge, slight mess. Kodak Portra 400 feel, natural noise, NOT AI-generated look. Caption sticker area at top.
```

### 07. UGC/买家秀

**品类提示：** Real family game night, slightly messy table, game mid-play, kids laughing, phone snap quality. NOT styled, NOT professional.

**示例：**
```text
Authentic UGC photo, iPhone front camera. Family game night at dining table, board game mid-play, cards and tokens scattered, a kid reaching for dice. Warm overhead lighting, slightly messy, dishes in background. Visible noise, off-center framing, NOT professional, NOT AI-generated look, Kodak Portra 400 warm tone.
```

### 10. 包装设计（Packaging）

**品类提示：** Gift set with expansion, collector's edition box with insert tray, component compartments visible, premium unboxing sequence.

**示例：**
```text
Premium board game collector's edition packaging. Outer box opened: magnetic closure, foam insert tray with compartments for cards, tokens, and dice. Expansion box nested inside. Silk ribbon pull tab. Brand card with gold foil. Marble surface, dried flowers, soft directional lighting. 8K, luxury unboxing.
```

### 11. 信息图/详情页（Infographic）

**品类提示：** Game mechanics overview, component list with icons, player count/duration/age badges, comparison with base game vs expansion, rule summary flow.

**示例：**
```text
Board game product infographic. Top: hero image of box. Middle: 4 feature blocks with icons - (1) 2-4 Players, (2) 60 min playtime, (3) 14+ age, (4) Solo mode included. Bottom: component list with icons (cards, board, dice, tokens, rulebook). Dark navy and gold palette. Mobile-friendly, 2000x2500px.
```

### 12. 创意概念（Creative Concept）

**品类提示：** Game world come to life, characters stepping out of cards, board terrain as miniature landscape, dice as giant sculptures, cards floating in space.

**示例：**
```text`
Surreal creative concept: a board game world coming to life. Miniature terrain from the game board growing into a real landscape, card characters standing as life-sized figures, oversized dice rolling through the scene. Dramatic lighting, fantasy atmosphere, 8K.
```

### 13. 尺寸规格（Size Spec）

**品类提示：** Component dimension callouts, box size comparison with common objects, card size vs standard poker/tarot, board unfolded dimensions.

**示例：**
```text
Board game component size guide. Center: game box with dimension callouts (30x30x8cm). Surrounding: card size comparison (standard poker card vs game card), board unfolded size, token diameter, dice size. Clean white background, thin leader lines, minimal labels, 8K.
```

### 14. 多产品套装（Multi-Product）

**品类提示：** Base game + expansion bundle, starter set with accessories, themed collection, holiday gift set.

**示例：**
```text
Board game gift set on premium surface. Base game box centered (larger), expansion box to the right, card sleeves pack, playmat rolled to the left. Gold ribbon, dried pine branches, warm fairy lights. "Holiday Bundle" badge. Soft directional lighting, 8K.
```

### 15. 直播场景（Livestream）

**品类提示：** Game unboxing live, host holding up components, camera showing board close-up, chat overlay area, product card with price.

**示例：**
```text
Board game livestream unboxing scene. Host's hands holding game box at camera angle, components spread on table below. Ring light reflection visible. Chat overlay area on right side. Product card: game name, price, "Limited Edition" badge. Energetic lighting, slight motion blur on hands, authentic livestream feel, 9:16.
```

### 17. 拆解图（Exploded View）

**品类提示：** Component exploded view showing all parts: box lid, board, card decks, token sheets, dice, rulebook, insert tray. Apple-style floating arrangement.

**示例：**
```text
Board game complete component exploded view. Box lid floating at top, game board below, then card decks fanned out, token sheets, loose dice, rulebook, insert tray at bottom. Each part with thin leader line label. Clean light gray background, soft shadows. Apple-style precise spacing, 8K.
```

### 19. 多角度网格（Multi-Angle Grid）

**品类提示：** Box front/back/side views, card front/back detail, board quadrant close-ups, token variety showcase.

**示例：**
```text
Board game multi-angle grid. 2x2 layout: (1) box front, (2) box back with component list, (3) game board close-up showing terrain detail, (4) card back design detail. Consistent lighting, clean white background, thin divider lines, 1:1 ratio, 8K.
```

### 21. 季节营销（Seasonal Campaign）

**品类提示：** Holiday gift guide, summer game night, cozy winter indoor, spring family gathering, back-to-school dorm game.

**示例：**
```text
Holiday board game gift guide poster. Game box wrapped in red ribbon, surrounded by pine branches, ornaments, fairy lights, and hot cocoa. Warm fireplace glow in background. "Perfect Gift" gold foil text. Cozy festive atmosphere, 4:5 ratio, 8K.
```

---

## 通用 Prompt 组装公式

当没有匹配到具体模板时，用这个通用公式：

```text
{输出形态}, {主体描述}, {材质/质感}, {光照}, {背景}, {构图}, {质量声明}
```

**桌游示例：**
```text
Product photography, a fantasy adventure board game box with dragon illustration, rigid cardboard with spot UV and gold foil, warm side lighting from left, dark wooden table, 15-degree tilt showing depth, 8K commercial photography
```

**文创示例：**
```text
Flat lay photography, handcrafted Chinese calligraphy gift set with brush, ink stone, and rice paper, washi paper wrapping with red wax seal, natural window light from top-left, bamboo mat surface, top-down composition, 8K editorial photography
```
