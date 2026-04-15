# Design Movements Reference — 设计运动与风格参考库

> 将用户的美学语言转化为可执行的 AI prompt。帮助建立共同的风格词汇："这个方向偏田中一光" vs "那个偏构成主义"。

---

## 1. 如何翻译用户的审美语言

当用户说 "我想要 XX 风格" 时，不要直接把名字丢给 AI。需要：

### 翻译流程

```
用户说 "我想要瑞士风格"
    ↓
识别设计运动核心 DNA（网格系统、无衬线、数学精确）
    ↓
提取视觉特征（白底、黑字、强对比、几何排版）
    ↓
映射到 AI 风格预设（Müller-Brockmann Grid）
    ↓
或构建自定义 Base Style Prompt
```

### 常见用户表述的翻译

| 用户说 | 实际想要 | 映射到 |
|--------|---------|--------|
| "简洁高级感" | 大量留白 + 微妙字重 + 单一强调色 | Build Luxury Minimal |
| "学术感" | 网格系统 + 精确排版 + 数据可视化 | Müller-Brockmann Grid |
| "有数据感" | 图表密集 + 注释系统 + 科学严谨 | Fathom Data Narrative |
| "有文化感/东方" | 自然色调 + 概念图 + 柔和科技感 | Takram Speculative |
| "杂志排版感" | 编辑式排版 + 数据卡片 + 黑白+单色 | Pentagram Editorial |
| "年轻潮" | 大色块 + 粗字 + 非对称 | Neo-Pop Magazine |
| "有手绘感" | 草稿质感 + 火柴人 + 随性标注 | Whiteboard Sketch (xkcd) |
| "温暖治愈" | 柔和色调 + 角色故事 + 哲理感 | Warm Comic Strip (Snoopy) |
| "复古" | 纸张质感 + 手绘排版 + 怀旧色 | Vintage Ad / Risograph |
| "国风" | 东方美学 + 矿物色 + 传统纹样 | 敦煌壁画 / 浮世绘 |

---

## 2. 经典设计运动映射

### 2.1 Neo-Brutalism — 新粗野主义

| 属性 | 描述 |
|------|------|
| **核心特征** | 粗黑边框、大胆撞色、原始感排版、拒绝精致 |
| **视觉 DNA** | 粗边框 (3-4px)、实心色块、阴影偏移 (offset shadow)、不等间距 |
| **色彩** | 黑 + 亮黄 + 亮粉 + 亮蓝，高饱和度直接碰撞 |
| **字体** | 粗重无衬线、全大写标题、系统默认体 |
| **代表** | Gumroad、Figma marketing site、 craigslist 美学 |
| **AI 映射** | Neo-Pop Magazine（近似）或自定义 Neo-Brutalism prompt |
| **Prompt 关键词** | "raw, bold borders, offset shadows, chunky, unpolished, direct" |

### 2.2 Swiss Style — 瑞士国际主义

| 属性 | 描述 |
|------|------|
| **核心特征** | 数学网格系统、客观排版、信息层次清晰 |
| **视觉 DNA** | 严格的网格对齐、大量留白、摄影替代插画、不对称但平衡 |
| **色彩** | 白底 + 黑字 + 1-2 个强调色，极度克制 |
| **字体** | Helvetica / Akzidenz-Grotesk，左对齐，字重对比 (300 vs 700) |
| **代表** | Josef Müller-Brockmann、Max Bill、瑞士铁路时刻表 |
| **AI 映射** | **Müller-Brockmann Grid**（直接对应） |
| **Prompt 关键词** | "Swiss design, grid system, mathematical precision, Helvetica, asymmetric balance" |

### 2.3 Bauhaus — 包豪斯

| 属性 | 描述 |
|------|------|
| **核心特征** | 形式追随功能，几何纯粹主义，艺术与工艺统一 |
| **视觉 DNA** | 圆、方、三角的基本形组合，无装饰，功能主义 |
| **色彩** | 三原色（红黄蓝）+ 黑白，Johannes Itten 色彩理论 |
| **字体** | Futura / Universal，几何无衬线，全大写 |
| **代表** | Walter Gropius、Wassily Kandinsky、Herbert Bayer |
| **AI 映射** | **Bauhaus 包豪斯**（直接对应） |
| **Prompt 关键词** | "Bauhaus, geometric shapes, primary colors, circle square triangle, functional beauty" |

### 2.4 De Stijl — 风格派 (Mondrian)

| 属性 | 描述 |
|------|------|
| **核心特征** | 纯粹抽象，只有水平线和垂直线，三原色填充 |
| **视觉 DNA** | 黑色线条分割、原色矩形块、严格非对称平衡 |
| **色彩** | 红 `#BE1E2D` / 黄 `#F5C518` / 蓝 `#21409A` + 黑线 + 白底 |
| **字体** | 无衬线，全大写，极简 |
| **代表** | Piet Mondrian、Theo van Doesburg、Gerrit Rietveld |
| **AI 映射** | Bauhaus 包豪斯（视觉语言高度重合）或自定义 |
| **Prompt 关键词** | "De Stijl, Mondrian, horizontal vertical lines only, red yellow blue rectangles, black grid" |

### 2.5 Art Deco — 装饰艺术

| 属性 | 描述 |
|------|------|
| **核心特征** | 奢华、几何装饰、对称构图、金属质感 |
| **视觉 DNA** | 扇形、锯齿形、日出射线、对称金字塔构图 |
| **色彩** | 黑金 `#000` + `#DAA520` / 深绿 / 深红 / 奶油底 |
| **字体** | Bodoni / Didot 风格衬线体，优雅的装饰性标题 |
| **代表** | Chrysler Building、Great Gatsby 美学、Cassandre 海报 |
| **AI 映射** | Vintage Ad 复古广告（近似）或自定义 Art Deco prompt |
| **Prompt 关键词** | "Art Deco, geometric ornament, gold accents, symmetry, 1920s luxury, sunburst patterns" |

### 2.6 Pop Art — 波普艺术

| 属性 | 描述 |
|------|------|
| **核心特征** | 大众文化为素材、高饱和色彩、重复和放大、反精英主义 |
| **视觉 DNA** | 网点印刷效果、粗轮廓线、漫画风格、产品图标放大 |
| **色彩** | 亮黄 / 亮粉 / 亮蓝 / 亮红，高对比直接撞色 |
| **字体** | 粗体漫画字体、漫画气泡、impact 风格 |
| **代表** | Andy Warhol、Roy Lichtenstein、Keith Haring |
| **AI 映射** | **Neo-Pop Magazine**（当代波普）或自定义 Pop Art prompt |
| **Prompt 关键词** | "Pop Art, halftone dots, bold outlines, high saturation, comic book style, mass culture" |

### 2.7 Constructivism — 构成主义

| 属性 | 描述 |
|------|------|
| **核心特征** | 为社会服务的艺术、几何抽象、动态对角线、摄影集成 |
| **视觉 DNA** | 对角线构图、圆形与矩形的动态碰撞、照片拼贴 |
| **色彩** | 红 + 黑 + 白（三色限制），革命性力量感 |
| **字体** | 粗壮 condensed 无衬线，斜体/旋转排版 |
| **代表** | Alexander Rodchenko、El Lissitzky、Varvara Stepanova |
| **AI 映射** | **Soviet Constructivism 苏联构成主义**（直接对应） |
| **Prompt 关键词** | "Constructivism, diagonal composition, red black white, geometric dynamism, propaganda poster" |

### 2.8 Japanese Design — 日本设计 (Tanaka Ikko 田中一光)

| 属性 | 描述 |
|------|------|
| **核心特征** | 留白即表达、自然色系、和洋融合、传统纹样现代化 |
| **视觉 DNA** | 大量留白、圆形/有机形态、传统纹样（波浪、云、花）、质感细腻 |
| **色彩** | 自然色（灰绿 `#8B9D77` / 暖灰 `#F5F3EF` / 深墨 `#3D3D3D`）+ 偶尔的朱红 |
| **字体** | 圆润 sans-serif + 书法点缀，大标题轻字重 |
| **代表** | 田中一光、原研哉、无印良品、隈研吾 |
| **AI 映射** | **Takram Speculative 日式思辨风**（东方哲学派） |
| **Prompt 关键词** | "Japanese design, wabi-sabi, natural colors, generous whitespace, organic shapes, subtle texture" |

### 2.9 Memphis Design — 孟菲斯设计

| 属性 | 描述 |
|------|------|
| **核心特征** | 反极简、反好品味、大胆色彩和图案、玩乐精神 |
| **视觉 DNA** | 几何图案（波浪线、圆点、三角）、撞色、不同材质纹理混搭 |
| **色彩** | 粉色 `#FF6B9D` + 薄荷绿 `#98D4BB` + 黄 `#F7DC6F` + 黑 + 白 |
| **字体** | 圆润 sans-serif，装饰性标题 |
| **代表** | Ettore Sottsass、Memphis Group、1980s 设计 |
| **AI 映射** | 孔版印刷 Risograph（视觉语言相近）或自定义 Memphis prompt |
| **Prompt 关键词** | "Memphis design, playful geometric patterns, bold clashing colors, squiggles, dots, terrazzo texture" |

### 2.10 Scandinavian Minimalism — 北欧极简

| 属性 | 描述 |
|------|------|
| **核心特征** | 功能美学、自然材质、温暖极简、hygge 舒适感 |
| **视觉 DNA** | 大量留白 + 自然色 + 木质纹理 + 简洁线条 |
| **色彩** | 白 / 浅灰 / 浅木色 `#D4A574` / 雾蓝 `#B8C5D6` / 鼠尾草绿 |
| **字体** | 简洁 sans-serif，轻字重，宽松字间距 |
| **代表** | IKEA、Muuto、Arne Jacobsen、Alvar Aalto |
| **AI 映射** | Warm Narrative 温暖叙事风（氛围接近）或 Build Luxury Minimal（更高端） |
| **Prompt 关键词** | "Scandinavian minimalism, natural materials, warm whites, wood tones, cozy, functional elegance" |

---

## 3. Movement → AI Style Preset 映射表

| 用户提到的运动/风格 | 映射到预设风格 | 匹配度 |
|---|---|---|
| Swiss Style / 瑞士风格 | Müller-Brockmann Grid | 直接对应 |
| Bauhaus / 包豪斯 | Bauhaus 包豪斯 | 直接对应 |
| Constructivism / 构成主义 | Soviet Constructivism | 直接对应 |
| Pop Art / 波普 | Neo-Pop Magazine | 当代演化 |
| Japanese Design / 田中一光 | Takram Speculative | 东方哲学 |
| Peanuts / Schulz | Warm Comic Strip (Snoopy) | 直接对应 |
| Tintin / Herge | Ligne Claire Comics | 直接对应 |
| xkcd / 手绘白板 | Whiteboard Sketch | 直接对应 |
| 1950s 广告 / 复古 | Vintage Ad | 直接对应 |
| De Stijl / 蒙德里安 | Bauhaus | 高度相近 |
| Art Deco / 装饰艺术 | Vintage Ad | 近似（需自定义） |
| Neo-Brutalism / 新粗野 | Neo-Pop Magazine | 近似（需自定义） |
| Memphis / 孟菲斯 | 孔版印刷 Risograph | 视觉相近 |
| Nordic / 北欧 | Warm Narrative | 氛围接近 |
| 数据可视化 / 信息图 | Fathom Data Narrative | 直接对应 |
| 杂志排版 / Editorial | Pentagram Editorial | 直接对应 |
| Apple / 苹果极简 | Build Luxury Minimal | 氛围接近 |

---

## 4. 如何与用户讨论风格

### 推荐讨论流程

```
Step 1: 倾听用户的原始描述
  "我想要简洁高级的感觉"
  ↓
Step 2: 用设计运动建立共同语言
  "你说的 '简洁高级'，在设计中通常有两种方向：
   - 苹果式的 '奢侈极简'（大量留白、轻字重、一个强调色）
   - 瑞士式的 '网格极简'（数学精确、信息密集、学术感）
   你更偏向哪个？"
  ↓
Step 3: 展示具体预设
  "根据你的偏好，我推荐这三个设计系统："
  [展示 3 个预设，附 Philosophy + Reference + 示例]
  ↓
Step 4: 用户选择 → 进入 Checkpoint 2
```

### 风格讨论话术模板

**当用户不确定：**
> "我来展示 3 个不同方向的设计系统，你选一个最喜欢的。每个都有完整的视觉语言——不仅仅是颜色，而是整体哲学。"

**当用户提到具体运动：**
> "田中一光的风格非常棒——他的设计融合了日本传统美学和现代设计语言。我们有一个很接近的预设叫 '日式思辨风'，用暖灰底色、自然色调和柔和的科技感来传达深度思考。我来展示完整的设计系统给你看。"

**当用户想要混搭：**
> "有趣的想法！理论上可以融合风格元素，但我的建议是选择一个主导风格作为 Base，然后从中提取 1-2 个你喜欢的元素加入。比如以 '编辑杂志风' 为主，加入 '苏联构成主义' 的对角线构图能量。"

### 用户常见误区与纠正

| 用户说 | 误区 | 纠正 |
|--------|------|------|
| "要暗色底+发光文字" | Path B 中 AI 难以做好极简暗色风格 | 建议用 Path A，或改用有更多视觉元素的风格 |
| "要极简白底" | 太空泛，缺乏视觉语言 | "极简" 有多种实现——北欧式温暖？瑞士式精确？苹果式高端？ |
| "随便什么风格都行" | 没有 AI 风格参考，生成效果差 | 至少选一个美学方向作为 base |
| "要 3D 渲染风" | AI 生成 3D 效果不稳定 | 建议等轴测 (Isometric) 作为替代 |
| "要照片写实" | AI 生成照片中文字效果差 | 建议用插画风格（文字渲染更稳定） |

---

## 5. 从设计运动构建自定义风格

当现有预设都不匹配时，可以从设计运动中提取 DNA 构建自定义风格。

### 构建模板

```
[Custom Style Name]: "[运动名] + [主题特色]"

Philosophy: [一句话描述核心哲学]
Shape language: [round/angular/geometric/organic]
Line quality: [thin uniform / thick varied / sketchy / brushwork]
Color palette: [3-5 个颜色 + hex 值]
Character style: [如适用——比例、表情程度]
Background treatment: [detailed/minimal/abstract]
Emotional tone: [warm/energetic/philosophical/surreal]
Visual reference: "[一句话引用]"
```

### 示例：从 Art Deco 构建自定义风格

```
[Custom Style]: "Art Deco Luxury"

Philosophy: 1920s 的奢华几何美学——对称、金属质感、装饰性力量
Shape language: geometric (扇形、锯齿、金字塔)
Line quality: crisp, precise, metallic feel
Color palette: 深黑 #0A0A0A / 金色 #DAA520 / 深红 #8B0000 / 奶油 #FDF5E6
Character style: N/A (无角色)
Background treatment: minimal, metallic gradient
Emotional tone: luxurious, confident, timeless
Visual reference: "Like a 1920s Chrysler Building elevator panel — gilded geometry"
```

---

---

## 6. 花叔审美画像

**喜欢**：大字、色块、冲击力、温暖色调、有质感、功能主义（每个元素都有存在理由）
**不喜欢**：赛博霓虹、冷色系（深蓝/紫底）、扁平无聊的企业模板、过度装饰

**核心偏好**：用最简单的方式传达最多信息（费曼思维在视觉上的投射）

---

## 7. 设计运动 → Skill 风格对照表

这张表连接了「设计史上的运动」和 skill 中已有的 AI 生成风格，帮助在讨论时快速定位。

| 设计运动 | skill 中对应风格 | 关系说明 |
|---------|----------------|---------|
| Neo-Brutalism（新粗野主义） | Neo-Brutalism（#18）+ Neo-Pop | 粗边框、色块、大字 |
| 田中一光 / 日本图形设计 | Ligne Claire 清线 | 极简几何+东方美学，限色克制 |
| 瑞士国际主义 | Müller-Brockmann Grid | 网格系统+功能主义+无衬线大字 |
| 蒙德里安 / De Stijl | Neo-Pop 新波普 | 原色块分割、几何秩序 |
| 包豪斯 | Bauhaus 包豪斯 | 直接对应 |
| 孟菲斯设计 | Neo-Pop 新波普 | 高饱和混搭，但孟菲斯更「吵」 |
| 俄国构成主义 | 苏联构成主义 | 直接对应 |
| Apple Keynote | —（skill 中不做极简风） | 太冷太克制，AI 生成效果差 |
| Sagmeister & Walsh | 达达拼贴 Collage | 实验性、大胆用色 |
| Information is Beautiful | Ligne Claire 清线 | 数据→美学、复杂信息简化 |
| Giorgia Lupi（数据人文主义） | 温暖叙事 Warm Narrative | 有温度的数据可视化 |

---

## 8. 2026 年演示设计趋势

| 趋势 | 描述 | 是否推荐 |
|------|------|---------|
| Bento Grid 布局 | 模块化方格（像 Apple 推广视频） | 推荐——和色块风格兼容 |
| 超大字排版 | 标题字占幻灯片 50% 面积 | 已在用 |
| 竖版幻灯片 | 9:16 给手机阅读优化 | 线下培训不需要 |
| 非线性演示 | 可点击跳转的交互式菜单 | 线下培训不需要 |
| Glassmorphism | 毛玻璃+透明效果 | 不推荐——偏冷偏科技感 |

---

## 9. 搜索风格的最佳渠道

| 渠道 | 适合找什么 |
|------|-----------|
| Behance | 设计师完整项目展示 |
| Dribbble | 单张设计灵感 |
| Pinterest | 按风格聚合的情绪板 |
| Poster House (posterhouse.org) | 经典海报展览 |
| It's Nice That (itsnicethat.com) | 设计趋势和设计师访谈 |
| Fonts In Use (fontsinuse.com) | 看字体在真实设计中的应用 |
| SlidesGo / SlidesCarnival | 免费 PPT 模板看趋势 |

---

## 10. 使用场景指南

### 场景 1：用户说「我想要 XX 风格」

1. 在本文件中找到对应的设计运动
2. 查看「Skill 风格对照表」，找到 skill 中已有的最近风格
3. 用该已有风格的 prompt 模板作为起点
4. 根据设计运动的特征做调整

### 场景 2：用户不确定想要什么风格

1. 用花叔审美画像作为默认偏好
2. 按主题在 `proven-styles-gallery.md` 的推荐表中选 3 个
3. 用本文件中的设计运动名称作为讨论锚点（如「这个方向偏田中一光，那个偏构成主义」）

### 场景 3：需要从零设计一个新风格

1. 在本文件中选择 1-2 个设计运动作为视觉 DNA
2. 提取其核心视觉特征（配色、构图、字体、元素）
3. 写成 Base Style prompt
4. 在 `proven-styles-gallery.md` 中增加为新风格

---

> **更深入的风格参考：** `design-philosophy` skill 的 `references/design-styles.md` 包含 20 种设计哲学的完整提示词 DNA
