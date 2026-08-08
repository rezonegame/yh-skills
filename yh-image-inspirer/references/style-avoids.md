# 风格特化反向约束（Style-Specific Avoids）

> 来源：gc-minimal-zine-poster 的 Negative Constraints 架构。
> 核心理念：「不要做什么」比「要做什么」更能防止翻车。每个风格族需要自己的专属硬避免。

## 通用硬避免（适用于所有风格）

- 水印、二维码、平台 logo（除非用户明确要求）
- 价格标签、促销贴纸（除非用户明确要求）
- 样机 mockup（除非用户明确要求）
- AI 生成的典型痕迹（多余手指、融合文字、变形 logo）
- 过度锐化、HDR 过度、过度饱和（除非风格要求）

---

## 极简/Zine 风格 Hard Avoids

### 必须避免
- **满版场景**：full-bleed subject or scene — 画面应以纸张/留白为主体，不是图像
- **商业海报层级**：commercial poster headline hierarchy — 没有大标题+副标题+CTA 的广告结构
- **产品广告布局**：product ad layout, logo lockup, CTA, brand campaign feeling
- **干净数字背景**：clean digital UI background — 不要纯白/纯灰的数字化背景
- **光面样机**：glossy paper mockup or heavy paper shadow
- **3D 渲染**：3D rendering, cinematic lighting, hard shadows, depth of field
- **霓虹/赛博**：neon, cyberpunk, vaporwave
- **可爱卡通**：cute cartoon, kawaii illustration, anime poster
- **时尚编辑**：fashion editorial drama
- **密集剪贴簿**：dense scrapbook, too many objects/stickers/colors
- **高清写实**：high-resolution stock-photo realism
- **干净长文**：long, clean, perfectly readable text blocks

### Prompt 中的避免表述
```
Avoid: full-bleed scene, commercial headline, product ad, logo/CTA,
glossy mockup, clean UI white, cinematic lighting, 3D, neon, cute
cartoon, fashion editorial drama, dense scrapbook, too many colors,
long clean text.
```

---

## Mondo/丝网印刷海报 Hard Avoids

### 必须避免
- **数字光滑感**：smooth digital gradients, clean vector look
- **照片级写实**：photorealistic rendering, stock photography
- **浅色背景**：light/white backgrounds（除非是复古旅行海报风格）
- **过多颜色**：more than 5 ink colors（包括黑白）
- **商业广告结构**：corporate ad layout, price tags, promotional badges
- **现代 UI 元素**：flat design, material design, rounded corners, drop shadows
- **卡通化**：cartoon style, chibi, simplified illustration
- **过度装饰**：too many decorative elements competing for attention
- **干净排版**：clean Swiss typography, modern sans-serif hierarchy

### Prompt 中的避免表述
```
Avoid: digital smoothness, photorealistic rendering, white backgrounds,
more than 5 screen-print colors, corporate ad layout, flat UI design,
cartoon style, decorative clutter, clean modern typography.
```

---

## 电商/商品海报 Hard Avoids

### 必须避免
- **信息过载**：too much text, multiple CTAs, competing information hierarchies
- **背景抢戏**：background more interesting than the product
- **不协调配色**：clashing colors between product and background
- **廉价感**：low-quality product rendering, bad lighting, sloppy cutout
- **杂乱构图**：too many supporting elements around the product
- **风格漂移**：product looks different from the reference photo
- **不当氛围**：mood inappropriate for the product category
- **缺失层级**：no clear visual hierarchy between title, product, and info

### Prompt 中的避免表述
```
Avoid: text overload, background competing with product, clashing colors,
cheap rendering, cluttered composition, product identity drift,
inappropriate mood, missing visual hierarchy.
```

---

## 信息图/图解 Hard Avoids

### 必须避免
- **装饰优先**：decorative elements competing with data
- **数据模糊**：unclear data visualization, misleading scales
- **色彩混乱**：too many colors without semantic meaning
- **层级不清**：no clear reading order or information hierarchy
- **文字过密**：dense paragraphs instead of concise labels
- **风格过强**：stylistic choices that obscure data clarity
- **缺失图例**：no legend or key for color-coded data
- **比例失调**：distorted proportions that mislead interpretation

### Prompt 中的避免表述
```
Avoid: decorative elements competing with data, unclear visualization,
colors without semantic meaning, missing reading order, dense text,
style obscuring clarity, missing legends, distorted proportions.
```

---

## 古风/历史题材 Hard Avoids

### 必须避免
- **现代元素混入**：modern objects, contemporary clothing, digital UI
- **文化错配**：mixing different historical periods or cultures incorrectly
- **过度滤镜**：excessive Instagram-style filters, HDR
- **卡通化历史**：cartoon/chibi treatment of historical figures
- **塑料质感**：plastic-looking materials, CG rendering feel
- **信息标签化**：museum-style labels and tags in the scene

### Prompt 中的避免表述
```
Avoid: modern objects, cultural mixing errors, excessive filters,
cartoon treatment of historical figures, plastic CG feel, museum labels.
```

---

## Anti-Plastic / 真实质感 Hard Avoids（新增 2026-07-29）

> 这不是一个独立风格族，而是**所有涉及人物/场景的生成任务**的质量门禁。
> 无论走极简、Mondo、电商、信息图还是古风路线，只要画面中出现人物或真实场景，就必须启用本约束。

### 必须避免

#### 1. 皮肤质感
- **过度磨皮**：excessive skin smoothing, airbrushed skin, no pores — 零毛孔/零肌理是塑料感的第一来源
- **死白肤色**：deathly white skin, porcelain white, uniform white all over face — 人脸应有冷暖过渡和血色
- **陶瓷/塑料感**：ceramic skin, plastic doll skin, matte plastic finish — 皮肤不应像模型材质
- **无血色**：no blood flush, no capillary color on cheeks/lips — 脸颊和唇周应有自然红润
- **单色肤质**：uniform skin tone with no variation — 真实皮肤有肤色不均、毛细血管、细微色差

#### 2. 动作动态
- **漂浮/无重力**：floating, weightless, no gravity — 人物应有站在地面上的重量感
- **匀速机械**：uniform mechanical movement, robotic constant speed — 所有动作应有缓起缓落
- **衣物脱节**：fabric moving independently of body, no cloth lag — 衣料应随身体动作自然滞后

#### 3. 眼神表情
- **空洞呆滞**：blank stare, dead eyes, doll eyes, no life in eyes — 眼神应有情绪和焦点
- **无微动**：no blinking, no micro-movement, frozen face — 应保留自然眨眼和眉眼微动
- **无情绪匹配**：emotionless eyes regardless of scene context — 眼神情绪应匹配画面氛围

#### 4. 画面氛围
- **过度干净**：sterile clean, clinical white, no atmosphere — 绝对的干净是最假的
- **无光影层次**：flat lighting, no shadow depth, no contrast — 光影应有明暗立体感
- **无空气感**：no atmospheric particles, no dust, no haze — 画面应有空间空气感
- **生硬抠图**：cutout look, subject pasted on background — 人物和场景应自然融合

### Prompt 中的避免表述（通用版，适用于所有含人物/场景的生成）

```
Avoid: excessive skin smoothing, no pores, porcelain white skin,
plastic doll finish, floating weightless movement, mechanical uniform
motion, blank staring eyes, no blinking, sterile clean atmosphere,
flat lighting, cutout compositing look.
```

### 快速判断

| 询问 | 是塑料感 | 不是塑料感 |
|------|---------|-----------|
| 皮肤看起来像什么？ | 陶瓷、塑料、蜡像 | 真人皮肤，有毛孔和血色 |
| 人物动作感觉？ | 在飘、匀速、无重量 | 有发力感、有快慢节奏 |
| 眼神给你什么感觉？ | 空洞、无焦点、无情绪 | 有情绪、有焦点、有微动 |
| 画面整体感觉？ | 太干净、太亮、像渲染图 | 有空气感、有光影层次 |

---

## 使用方法

1. 根据类型路由表确定风格族
2. 读取对应风格族的 Hard Avoids
3. 在 prompt 的「避免」段落中嵌入对应的避免表述
4. 在出图前检查表中验证没有违反硬避免
