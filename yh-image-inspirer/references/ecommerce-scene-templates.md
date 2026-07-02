# 电商场景模板库

来源：`gpt-image2-ecommerce`（25 个结构化场景模板）+ `awesome-gpt-image-2`（电商专题案例）。本文件提供电商全场景的结构化 prompt 模板，每个模板含触发词、变量槽位、风格变体、品类适配建议和示例 prompt。

与 `db/商品与电商/prompt.md`（案例库）和 `recipes/ecommerce-poster.md`（电商海报流程）互补。

## 目录

- [使用方式](#使用方式)
- 场景 01–05：主图、生活方式、平铺、微距、促销
- 场景 06–10：社媒、UGC、模特、对比、包装
- 场景 11–15：信息图、概念广告、规格、组合、直播
- 场景 16–20：试穿、拆解、隐形模特、多角度、编辑风
- 场景 21–25：季节、奢华、设备、门店、运动
- [品类通用适配建议](#品类通用适配建议)
- [Anti-AI 处理要点](#anti-ai-处理要点)

## 使用方式

1. 根据用户关键词匹配触发词，选择最合适的场景模板。
2. 填充变量槽位（`{variable}`），应用品类适配建议。
3. 根据需要选择风格变体（variant），覆盖默认值。
4. 组装为完整 prompt，调用图像生成。

---

## 01. 白底/纯色底产品主图（Hero Image）

**触发词：** 白底图、主图、hero image、白背景、product shot、packshot、产品照、商品主图

**Prompt 结构：**
```text
{product_description}, professional product photography on clean white background, soft diffused studio lighting, centered, 8K, commercial e-commerce photography, no shadows, no props
```

**变量：**
- `{product_description}`：商品描述（材质、颜色、形态）

**风格变体：**
| 变体 | 描述 | 覆盖项 |
|------|------|--------|
| luxury | 高端奢侈品 | Rembrandt lighting, subtle rim light, gradient dark-to-light background |
| fresh | 清新自然 | bright natural light, light pastel tones |
| tech | 科技感 | dramatic side lighting, dark minimalist background |
| color | 彩色背景 | `{color}` gradient background |

**品类适配：**
- 美妆：强调质感和光泽，展示配方细节
- 3C：突出金属质感、屏幕细节、接口精度
- 食品：鲜艳色彩、新鲜外观、展示纹理
- 服装：展示面料质感、垂坠感、缝线细节
- 家居：展示材质质量、工艺、生活感
- 珠宝：微距细节、闪耀和切工、奢华灯光

---

## 02. 生活方式场景图（Lifestyle Scene）

**触发词：** 场景图、生活图、lifestyle、使用场景、氛围图

**Prompt 结构：**
```text
{product_description} in a {scene_description}, natural lighting, lifestyle photography, {mood} atmosphere, 8K
```

**变量：**
- `{scene_description}`：场景描述（厨房、书房、户外等）
- `{mood}`：氛围（温馨、现代、自然等）

**品类适配：**
- 厨房用品：温暖厨房台面，自然光从窗户洒入
- 数码产品：现代办公桌，简洁背景
- 运动装备：户外自然环境，动态感

---

## 03. 平铺俯拍图（Flat Lay）

**触发词：** 平铺图、flat lay、俯拍、摆拍、flatlay

**Prompt 结构：**
```text
overhead flat lay of {products_arrangement}, clean {background_surface}, styled composition, soft even lighting, 8K
```

**变量：**
- `{products_arrangement}`：商品排列描述
- `{background_surface}`：背景表面（大理石、木质、纯色等）

---

## 04. 细节/微距图（Detail / Macro）

**触发词：** 细节图、微距、macro、特写、质感图

**Prompt 结构：**
```text
extreme close-up macro shot of {product_detail}, {material_texture}, {lighting_type}, ultra-detailed, 8K
```

---

## 05. 促销海报/Banner（Poster / Banner）

**触发词：** 海报、poster、banner、促销、广告图、活动图、promotion、sale

**Prompt 结构：**
```text
promotional poster design. {product_description} on {background}. Bold {headline} at top, {subtitle}, price {price}, {cta} button. {style}, professional layout, {dimensions}
```

**变量：**
- `{headline}`：主标题
- `{subtitle}`：副标题
- `{price}`：价格信息（可选）
- `{cta}`：行动号召（默认 "Shop Now"）
- `{dimensions}`：尺寸（2000x3000px / 2000x2000px / 1080x1350px）

**风格变体：**
| 变体 | 描述 | 风格 |
|------|------|------|
| luxury | 高端奢华 | full-bleed rich gradient, gold accents, luxury magazine editorial, gold foil |
| minimal | 极简现代 | clean white or light gradient, minimalist modern typography, generous white space |
| festive | 节日主题 | festive themed gradient with decorative elements, cultural elements, seasonal motifs |
| flash-sale | 限时折扣 | bold attention-grabbing, high contrast, urgency elements |

**品类适配：**
- 美妆：rose gold accents, elegant serif fonts, luxury gift aesthetic
- 3C：dark backgrounds, neon accents, futuristic typography
- 食品：warm colors, dynamic food elements, freshness cues
- 服装：editorial style, model inclusion, aspirational lifestyle

---

## 06. 社媒内容图（Social Media）

**触发词：** 小红书、Instagram、TikTok、社媒图、种草图

**Prompt 结构：**
```text
{platform} style content image, {product_description}, {scene_style}, {aspect_ratio}, engaging visual, {mood}
```

**变量：**
- `{platform}`：平台（小红书 / Instagram / TikTok）
- `{aspect_ratio}`：比例（3:4 / 1:1 / 9:16）

**Anti-AI 处理：** CCD 复古胶片质感、可见瑕疵、真实感

---

## 07. UGC 买家秀（UGC Style）

**触发词：** UGC、买家秀、GRWM、用户分享、真实评价

**Prompt 结构：**
```text
authentic UGC style photo of {product_in_use}, casual real-life setting, natural imperfect lighting, smartphone quality feel, {platform} aesthetic
```

**Anti-AI 处理：** 轻微过曝、自然构图、不完美但真实

---

## 08. 模特展示图（Model Showcase）

**触发词：** 模特、model、人物展示、上身图、穿搭图

**Prompt 结构：**
```text
{model_description} wearing/holding {product_description}, {pose}, {background}, fashion photography, {style}
```

---

## 09. 对比图（Before / After）

**触发词：** 对比、before after、使用前后、效果对比

**Prompt 结构：**
```text
side-by-side comparison, left: {before_state}, right: {after_state}, clean split layout, {product_context}
```

---

## 10. 包装设计图（Packaging）

**触发词：** 包装、packaging、礼盒、gift box、开箱

**Prompt 结构：**
```text
{product_packaging_description}, {material_finish}, {display_angle}, studio lighting, premium packaging photography, 8K
```

---

## 11. 信息图/A+ 详情页（Infographic / A+）

**触发词：** 信息图、A+、详情页、卖点图、功能图

**Prompt 结构：**
```text
e-commerce infographic for {product}, showing {key_features}, clean layout with icons and text, {color_scheme}, professional design
```

---

## 12. 创意概念广告图（Creative Concept）

**触发词：** 创意图、概念图、creative、概念广告、品牌广告、创意广告

**Prompt 结构：**
```text
creative advertising photography. {product_description} with {creative_concept}, {special_effects}, {bold_palette}, {art_style}, award-winning advertising photography, ultra-detailed, cinematic
```

**风格变体：**
| 变体 | 描述 | 效果 |
|------|------|------|
| splash-dynamic | 飞溅动态 | water splash / powder explosion frozen in motion, high-speed photography |
| surreal | 超现实 | product in unexpected surreal environment, gravity-defying, impossible geometry |
| minimal-art | 极简艺术 | product as art object in minimalist composition, monochromatic or two-tone |

**品类适配：**
- 美妆：floating product with splash, ethereal lighting, formula particles
- 3C：holographic interfaces, data visualization, futuristic
- 食品：ingredient explosion, dynamic pour/splash, steam and fire
- 服装：editorial art direction, dramatic poses, fabric in motion

---

## 13. 尺寸/规格图（Size / Spec）

**触发词：** 尺寸、规格、使用步骤、size chart、规格图

**Prompt 结构：**
```text
product specification diagram for {product}, showing {dimensions_details}, clean technical illustration style, labeled measurements
```

---

## 14. 多件组合图（Multi-Product Bundle）

**触发词：** 套装、组合、bundle、多件、礼盒装

**Prompt 结构：**
```text
styled product bundle of {products_list}, arranged on {surface}, complementary composition, {style}, 8K
```

---

## 15. 直播间场景图（Livestream）

**触发词：** 直播、livestream、直播间、带货

**Prompt 结构：**
```text
e-commerce livestream scene, {host_description} presenting {product}, {studio_setup}, {lighting}, professional broadcast quality
```

---

## 16. 虚拟试穿/融入（Virtual Try-On）

**触发词：** 试穿、融入、try on、上身效果

**Prompt 结构：**
```text
virtual try-on showing {product} on {model/subject}, natural fit, {environment}, realistic integration
```

---

## 17. 技术拆解图（Exploded View）

**触发词：** 拆解图、爆炸图、exploded view、内部结构

**Prompt 结构：**
```text
technical exploded view of {product}, showing {internal_components}, clean white background, labeled parts, engineering illustration style
```

---

## 18. 隐形模特图（Ghost Mannequin）

**触发词：** 隐形模特、ghost mannequin、3D 衣服展示

**Prompt 结构：**
```text
ghost mannequin photography of {garment}, showing shape and fit without visible model, {angle}, studio lighting, fashion e-commerce standard
```

---

## 19. 多角度网格图（Multi-Angle Grid）

**触发词：** 多角度、网格、grid、360度、多视角

**Prompt 结构：**
```text
multi-angle product grid showing {product} from {angles_list}, clean white background, consistent lighting, 2x2 or 3x3 grid layout
```

---

## 20. 杂志/编辑风格图（Magazine / Editorial）

**触发词：** 杂志、封面、editorial、时尚大片、编辑风格

**Prompt 结构：**
```text
magazine editorial style product photography, {product} with {styling_concept}, {publication_aesthetic}, high-end fashion photography, 8K
```

---

## 21. 季节营销图（Seasonal Campaign）

**触发词：** 季节、四季、campaign、节日营销、春节、圣诞

**Prompt 结构：**
```text
{season} marketing campaign for {product}, {seasonal_elements}, {color_palette}, {mood}, professional campaign photography
```

---

## 22. 奢华氛围渲染图（Luxury Atmospherics）

**触发词：** 奢华、氛围、烟雾、高级感、luxury、atmospheric、梦幻、高端、premium

**Prompt 结构：**
```text
luxury product photography with atmospheric effects. {product} on polished dark surface, surrounded by {atmosphere_elements}. Dramatic rim light. Deep black background. 8K, cinematic quality
```

**风格变体：**
| 变体 | 描述 | 氛围元素 |
|------|------|----------|
| floral-dream | 花卉梦幻 | fresh flower petals floating, scattered gold leaf particles |
| smoke-mystique | 烟雾神秘 | multi-layered violet and midnight blue smoke swirling |
| golden-luxe | 金色奢华 | golden bokeh particles, warm amber glow, scattered gold flakes |
| ice-crystal | 冰晶冷冽 | floating ice crystals, frost patterns, diamond-like light refractions |

**品类适配：**
- 香水：multi-layer smoke + matching botanical elements
- 护肤：ethereal glow, subtle condensation, dreamy quality
- 珠宝：diamond-like light bokeh, dark background, sparkle focus
- 酒类：rich amber or ruby liquid, smoke wisps, candlelight warmth
- 巧克力：warm golden particles, cocoa powder dust, rich dark tones
- 手表：sharp metallic reflections, precise time visible, ice-blue or golden accent

---

## 23. 设备 Mockup 图（Device Mockup）

**触发词：** mockup、SaaS、APP、设备展示、屏幕展示

**Prompt 结构：**
```text
device mockup showing {app/interface} on {device_type}, {environment}, clean modern setting, professional product photography
```

---

## 24. 店铺/门面图（Storefront）

**触发词：** 店铺、门面、storefront、门店、实体店

**Prompt 结构：**
```text
{store_description} storefront, {architectural_style}, {signage}, {lighting}, inviting commercial photography
```

---

## 25. 运动 Campaign 图（Sports Campaign）

**触发词：** 运动、健身、sports、fitness、运动品牌、体育

**Prompt 结构：**
```text
{sport_type} commercial campaign poster. {athlete/model} in {pose}. Core prop: {prop} as visual anchor. Headline: "{headline}". Supporting copy: "{copy}". High-end sportswear brand advertising, strong lighting, {color_palette}
```

**风格变体：**
| 变体 | 描述 | 风格 |
|------|------|------|
| hero-visual | 主视觉 | single strong hero image, dramatic lighting |
| athlete-dynamic | 运动员动态 | action freeze-frame, motion blur, energy |
| triptych | 三联画 | three-panel layout, progression narrative |
| fitness-power | 力量感 | dramatic shadows, muscle definition, power pose |

---

## 品类通用适配建议

| 品类 | 色彩 | 灯光 | 材质关键词 | 风格 |
|------|------|------|------------|------|
| 美妆 | 玫瑰金、裸色、粉调 | 柔光、伦勃朗光 | 丝绒、玻璃、金属 | 高端编辑感 |
| 3C/数码 | 深色、霓虹、冷调 | 侧光、轮廓光 | 磨砂金属、玻璃、碳纤维 | 科技未来感 |
| 食品 | 暖色、鲜艳 | 自然光、逆光 | 新鲜、多汁、酥脆 | 温暖生活感 |
| 服装 | 中性色、品牌色 | 编辑光、自然光 | 面料纹理、垂坠感 | 时尚编辑感 |
| 家居 | 大地色、莫兰迪 | 柔光、窗光 | 木纹、棉麻、陶瓷 | 北欧简约感 |
| 珠宝 | 黑金、银白 | 点光、钻石光 | 切面、闪耀、铂金 | 奢华精致感 |
| 运动 | 高对比、品牌色 | 强光、动态光 | 网布、橡胶、科技面料 | 力量动感感 |

---

## Anti-AI 处理要点

电商场景（尤其是 UGC、直播、社媒）需要反 AI 感处理：

1. **胶片质感：** CCD 复古胶片色调、轻微颗粒感
2. **不完美：** 可见瑕疵、轻微过曝、自然阴影
3. **真实构图：** 非对称、随手拍感、手机拍摄质感
4. **环境光：** 自然光而非完美棚拍光
5. **平台特征：** 保留目标平台的 UI 特征和视觉语言
