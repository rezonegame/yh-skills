# AI Art Style Gallery — 经过验证的 18+ 风格库

> 从数百次 AI 图片生成实验中筛选出的最佳风格。按效果梯队排序，每种风格包含完整的视觉 DNA。

---

## 第一梯队（强烈推荐，效果极好）

> 核心洞察：**插画/漫画类风格的 AI 生成效果远好于「专业极简」类风格。** 漫画风格有明确的视觉语言（线条、角色、色块），AI 可以充分发挥；极简风格（暗色底+发光文字+大量留白）缺乏视觉元素，生成出来「空」且「平」。

---

### 1. Warm Comic Strip — Snoopy 温暖漫画风

| 属性 | 定义 |
|------|------|
| **Philosophy** | Peanuts 漫画的温暖与哲理感——简单的角色说着深刻的话，日常场景中蕴含人生智慧 |
| **Colors** | 泛黄报纸底 `#F5F0E1` / 暖黑墨线 `#2D2418` / 柔和粉彩填充 |
| **Typography** | 手写感标题 + 清晰正文，标题:正文 = 2.5:1 |
| **Composition** | 漫画分格式（2-4 格/页），从左到右阅读流，温暖留白 |
| **Visual language** | 圆头小孩、小狗、小鸟组成温暖小世界。背景极简（草地、天空、狗屋、树） |
| **Reference** | "Like a Peanuts comic strip — warm, philosophical, charming" |
| **详细模板** | `references/proven-styles-snoopy.md` |
| **适用路径** | Path A / Path B 均可 |

**关键经验：** 不要在 prompt 中过度约束视觉细节（颜色比例、构图位置、角色姿势），否则会严重降低多样性。只描述情绪和内容，让 AI 自由发挥。

**推荐场景：** 品牌介绍、企业文化、教育科普、温暖叙事类主题

---

### 2. Manga Educational — 学習漫画风

| 属性 | 定义 |
|------|------|
| **Philosophy** | Japanese educational manga (学習漫画) — a character GUIDES you through the concept with reactions and drama |
| **Colors** | 明亮暖色调，白色底 + 选择性彩色面板，网点灰（screen-tone）用于强调区域 |
| **Typography** | Bold manga-style 标题（冲击力），正文在对话/思考气泡中，拟声词作为装饰元素。大小对比 3:1 |
| **Composition** | 动态漫画分格布局（3-5 格/页），角色反应驱动强调，速度线增加活力，戏剧性角度 |
| **Visual language** | 表情丰富的 anime 风格角色，反应表情（惊讶、困惑、顿悟！），漫画效果（汗滴、闪光、速度线），不同粗细的面板边框 |
| **Reference** | "Like a 'Manga Guide to Statistics' page — a character walks you through the concept, reacting with surprise and delight" |
| **Ratio** | 60% illustration / 30% text (in bubbles) / 10% effects |
| **适用路径** | Path A / Path B 均可 |

**推荐场景：** 教育培训、技术教程、知识科普、教材课件

---

### 3. Ligne Claire Comics — 清线漫画风

| 属性 | 定义 |
|------|------|
| **Philosophy** | Hergé's Tintin tradition — maximum information clarity through visual restraint |
| **Colors** | 白/奶油底 `#FFFDF7` / 黑色轮廓 `#000000` / 平涂饱和色（3-5 固有色，无渐变） |
| **Typography** | 手绘感标题 + 清晰 sans-serif 正文。关键引用用对话气泡。标题:正文 = 2.5:1 |
| **Composition** | 分格布局（2-4 格/页），从左到右顺序阅读流，格间距清晰 |
| **Visual language** | 统一线宽轮廓，平涂色无阴影无网线，无渐变，精确细节但零视觉噪音 |
| **Reference** | "Like a Tintin page explaining a concept — every panel advances understanding, nothing is decorative" |
| **Ratio** | 70% 干净底 / 20% illustration / 10% text |
| **适用路径** | Path A / Path B 均可 |

**推荐场景：** 技术分享、流程说明、历史叙事、知识体系展示

---

### 4. Neo-Pop Magazine — 新波普杂志风

| 属性 | 定义 |
|------|------|
| **Philosophy** | Youth media / streetwear brand aesthetic, bold and playful |
| **Colors** | 奶油底 `#FFF8E7` / 黑字 `#000000` / 色块撞色：热粉 `#FF1493` + 青色 `#00CED1` + 金黄 `#FFD700` |
| **Typography** | 标题占 slide 面积 40-50%（字体即视觉），粗黑边框包围文字块，10:1 大小对比 |
| **Composition** | 模块化色块 + "controlled chaos"，层叠非对称布局，粗边框 |
| **Visual language** | 像素风 8-bit 图标、剪贴摄影、对话气泡、粗犷图形表面 |
| **Reference** | "Like a Supreme lookbook meets a HYPEBEAST article — treats typography as graphic art" |
| **Ratio** | 50% bg / 25% color blocks / 25% content |
| **适用路径** | Path A / Path B 均可 |

**推荐场景：** 年轻受众、潮流品牌、产品发布、创意提案

---

## 第二梯队（推荐，特定场景效果好）

---

### 5. Whiteboard Sketch — xkcd 白板手绘风

| 属性 | 定义 |
|------|------|
| **Philosophy** | xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself |
| **Colors** | 白底 `#FFFFFF` / 黑墨 `#000000` / 单一强调色（红 `#FF4444` 或蓝 `#4488FF`） |
| **Typography** | 手写/手绘感一切元素，粗糙不均匀基线，箭头和标注无处不在。关键数字可放大（60pt+） |
| **Composition** | 自由白板布局，手绘箭头连接概念，图表和火柴人，非正式但生动 |
| **Visual language** | 火柴人、手绘图表、摇晃线条、标注箭头、圈出关键词、方程式风格布局 |
| **Reference** | "Like an xkcd 'What If?' explanation — simple drawings that make complex ideas instantly click" |
| **Ratio** | 85% 白空间 / 10% sketch / 5% accent |
| **适用路径** | Path A / Path B 均可 |

**推荐场景：** 技术分享、内部分享、概念解释、极客文化主题

---

### 6. Soviet Constructivism — 苏联构成主义

| 属性 | 定义 |
|------|------|
| **Philosophy** | Revolutionary propaganda poster — power through geometry and limited color |
| **Colors** | 革命红 `#CC0000` 40% + 黑 `#1A1A1A` 25% + 奶油白 `#F5E6D3` 30% |
| **Typography** | 所有文字旋转 15-30 度，NO 水平线，bold condensed |
| **Composition** | 从左下到右上的对角楔形，几何形状从小到大（视觉渐强） |
| **Visual language** | NO 渐变，纯平涂 + 锐利边缘，三色限制，宣传海报能量 |
| **Reference** | "Like a 1920s Rodchenko poster — power, urgency, and geometric precision" |
| **适用路径** | Path B 效果最佳（AI 擅长生成大胆图形语言） |

**推荐场景：** 产品发布、keynote、宣言式表达、运动/革命叙事

---

### 7. Warm Narrative — 温暖叙事风

| 属性 | 定义 |
|------|------|
| **Philosophy** | Friendly storytelling, like a TED talk visual or Airbnb pitch deck |
| **Colors** | 暖奶油底 `#FDF6EC` / 深炭灰字 `#3D3D3D` / 珊瑚强调色 `#E17055` |
| **Typography** | 标题粗体且温暖，3:1 比例对正文。短句，不用 bullet points |
| **Composition** | 插画占 slide 的 40-50%，文字环绕视觉，圆角形状 |
| **Visual language** | 暖色调 flat vector 插画，以人为中心的图像，叙事流 |
| **Reference** | "Like a Mailchimp or Notion brand presentation — approachable and human" |
| **Ratio** | 60% 暖底 / 25% 内容 / 15% illustration |
| **适用路径** | Path A / Path B 均可 |

**推荐场景：** 品牌故事、用户案例、服务介绍、教育叙事

---

## 更多风格（第二/三梯队）

---

### 8. The Oatmeal — 信息图漫画

| 属性 | 定义 |
|------|------|
| **Philosophy** | Matthew Inman 的 The Oatmeal 漫画——幽默的信息图，荒诞中传递知识 |
| **Colors** | 白底 + 粗黑轮廓 + 大面积单一填色（绿、蓝、橙交替） |
| **Typography** | 手写标题 + 对话气泡 + 大字强调，字体大小对比强烈 |
| **Composition** | 长条形叙事流，单格或双格宽幅，重点用大字和颜色突出 |
| **Visual language** | 夸张简笔角色、荒诞场景、幽默图表、bold 视觉隐喻 |
| **Reference** | "Like an The Oatmeal infographic — absurd, funny, and surprisingly informative" |
| **适用路径** | Path A / Path B 均可 |

**推荐场景：** 内部分享、轻松科普、创意提案、幽默叙事

---

### 9. 敦煌壁画

| 属性 | 定义 |
|------|------|
| **Philosophy** | 千年壁画的庄严与瑰丽——矿物颜料的沉稳质感，飞天与藻井的东方美学 |
| **Colors** | 土红 `#8B4513` / 石绿 `#2E8B57` / 石青 `#1E3A5F` / 金箔 `#DAA520` / 褪色白 `#F5F0E0` |
| **Typography** | 衬线体或书法感字体，金色装饰线，古朴典雅 |
| **Composition** | 对称或放射状构图，藻井纹样边框，人物与场景交织 |
| **Visual language** | 飞天造型、莲花纹样、祥云、矿物颜料质感、斑驳做旧效果 |
| **Reference** | "Like a Dunhuang cave mural — ancient pigments telling timeless stories" |
| **适用路径** | Path B（AI 擅长生成东方艺术质感） |

**推荐场景：** 国风品牌、文化遗产、东方美学、哲学思想

---

### 10. 浮世绘

| 属性 | 定义 |
|------|------|
| **Philosophy** | 江户时代的浮世之美——木版印刷的线条力度与平涂色彩 |
| **Colors** | 靛蓝 `#1B3F8B` / 朱红 `#C41E3A` / 米黄 `#F5E6C8` / 墨黑 `#1A1A1A` |
| **Typography** | 竖排文字，明朝体/宋体，书法落款风格 |
| **Composition** | 非对称波浪形构图（如神奈川冲浪里），前景-中景-远景层次分明 |
| **Visual language** | 木版印刷线条、平涂色块、波浪纹、墨渐变、浮世美人或武士 |
| **Reference** | "Like a Hokusai woodblock print — bold outlines, flat colors, dramatic wave patterns" |
| **适用路径** | Path B（AI 擅长生成浮世绘风格） |

**推荐场景：** 国风品牌、日本文化主题、艺术类演示、东方哲学

---

### 11. 孔版印刷 — Risograph

| 属性 | 定义 |
|------|------|
| **Philosophy** | 独立出版物的手工质感——层层叠印的半透明色块，Zine 美学的温暖 |
| **Colors** | 荧光粉 `#FF6B9D` / 荧光蓝 `#4ECDC4` / 荧光黄 `#F7DC6F` / 荧光橙 `#FF8A5C` + 牛皮纸底 `#D4B896` |
| **Typography** | 粗糙的 sans-serif，文字可略微叠印错位增加手工感 |
| **Composition** | 大面积色块叠印，半透明层叠效果，粗糙边缘 |
| **Visual language** | 丝网纹理、叠印错位、半透明色块、颗粒质感、Zine 版式 |
| **Reference** | "Like a risograph-printed indie zine — imperfect, layered, and beautiful" |
| **适用路径** | Path A / Path B 均可 |

**推荐场景：** 年轻受众、独立品牌、艺术创作、创意提案

---

### 12. 等轴测 — Isometric

| 属性 | 定义 |
|------|------|
| **Philosophy** | 等轴测视角的技术美学——精确的 30 度角，微缩世界的秩序感 |
| **Colors** | 浅灰底 `#F0F0F0` + 系统色板（蓝 `#4A90D9` / 绿 `#27AE60` / 橙 `#F39C12`） |
| **Typography** | 等轴测文字（可选），整洁 sans-serif，标注风格 |
| **Composition** | 2.5D 等轴测网格，元素沿三轴排列，鸟瞰视角 |
| **Visual language** | 等轴测方块/建筑/角色，网格底纹，阴影统一投射，微缩场景 |
| **Reference** | "Like an isometric city illustration — precise, ordered, and satisfyingly detailed" |
| **适用路径** | Path A（图标类）/ Path B（场景类）均可 |

**推荐场景：** 科技产品、数据流程、城市规划、系统架构

---

### 13. Bauhaus — 包豪斯

| 属性 | 定义 |
|------|------|
| **Philosophy** | Form follows function — 几何纯粹主义，色彩理论的教学实践 |
| **Colors** | 包豪斯三原色：红 `#BE1E2D` / 黄 `#F5C518` / 蓝 `#21409A` + 黑 `#000` / 白 `#FFF` |
| **Typography** | Universal / Futura 风格，全小写或全大写，几何 sans-serif |
| **Composition** | 圆、方、三角的严谨组合，不对称平衡，网格约束 |
| **Visual language** | 纯几何图形（圆、方、三角），无装饰线条，功能主义排版 |
| **Reference** | "Like a Bauhaus school poster — geometric purity, primary colors, and functional beauty" |
| **适用路径** | Path A / Path B 均可 |

**推荐场景：** 设计教育、建筑/艺术主题、极简品牌、德国文化

---

### 14. 工程蓝图 — Blueprint

| 属性 | 定义 |
|------|------|
| **Philosophy** | 工程图纸的严谨之美——深蓝底白线，每个细节都有其功能 |
| **Colors** | 蓝图底 `#0A2463` / 白线 `#FFFFFF` / 强调线 `#3E92CC` |
| **Typography** | 等宽字体（Courier 风格），技术标注风格，尺寸标注 |
| **Composition** | 正交网格，精确对齐，技术图例，边框和标题栏 |
| **Visual language** | 网格线、尺寸标注、剖面线、技术插图、等轴测视图 |
| **Reference** | "Like an architectural blueprint — precise, technical, and beautiful in its discipline" |
| **适用路径** | Path A / Path B 均可 |

**推荐场景：** 工程技术、建筑方案、系统设计、精密制造

---

### 15. 复古广告 — Vintage Ad

| 属性 | 定义 |
|------|------|
| **Philosophy** | 1950s 广告插画的怀旧魅力——手绘排版、柔和渐变、乐观主义 |
| **Colors** | 奶油底 `#FDF5E6` / 复古红 `#C1440E` / 复古蓝 `#2B4162` / 柔和金 `#D4A574` |
| **Typography** | 手绘 serif 标题 + 精致 script 副标题，复古排版 |
| **Composition** | 中心焦点构图，装饰边框，产品/人物居中 |
| **Visual language** | 手绘插画、复古纹理（网点、划痕）、装饰边框、复古字体 |
| **Reference** | "Like a 1950s magazine advertisement — optimistic, hand-lettered, and charmingly dated" |
| **适用路径** | Path B（AI 擅长复古风格渲染） |

**推荐场景：** 品牌历史、怀旧主题、餐饮/生活方式、营销提案

---

### 16. 达达拼贴 — Collage

| 属性 | 定义 |
|------|------|
| **Philosophy** | 达达主义的解构与重组——打破秩序，在混乱中发现意义 |
| **Colors** | 多源混合——报纸灰、拼贴色、撕纸白底 |
| **Typography** | 剪贴字体（不同字号/字体的文字块拼贴），刻意错位 |
| **Composition** | 自由拼贴布局，元素重叠、旋转、撕裂边缘，无网格 |
| **Visual language** | 拼贴碎片、撕纸效果、报纸/杂志剪切、图章/邮戳、手写标注 |
| **Reference** | "Like a Hannah Höch photomontage — fragments reassembled into provocative meaning" |
| **适用路径** | Path B（AI 擅长生成拼贴效果） |

**推荐场景：** 创意/艺术、头脑风暴、反常规主题、文化批评

---

### 17. 像素画 — Pixel Art

| 属性 | 定义 |
|------|------|
| **Philosophy** | 8-bit 时代的视觉怀旧——有限的色彩分辨率中创造无限想象 |
| **Colors** | 像素画色板：亮色为主，每色块使用 2-4 个色阶表现阴影 |
| **Typography** | 像素字体（Press Start 2P 风格），8-bit 感 |
| **Composition** | 网格对齐，像素精确，复古游戏 UI 布局 |
| **Visual language** | 像素角色、像素场景、复古游戏元素（生命条、得分板）、有限色阶 |
| **Reference** | "Like a classic 16-bit game scene — every pixel placed with purpose" |
| **适用路径** | Path B（AI 擅长像素风格） |

**推荐场景：** 年轻受众、游戏/科技主题、极客文化、怀旧创意

---

### 18. Neo-Brutalism — 新粗野主义（CSS 实现 + AI 生成双模式）

**视觉参考：** Gumroad 官网、Figma 社区模板、小红书官方 PPT
**验证项目：** 2026-02-09 蕴煜 AI 培训项目（Day1 67 页 + Day2 64 页全部 HTML 渲染成功）

| 属性 | 定义 |
|------|------|
| **Philosophy** | 粗暴直接——信息即设计，拒绝精致，拥抱原始力量 |
| **Colors** | 奶油(#F5E6D3) 40% + 革命红(#FF3B4F) 25% + 金黄(#FFD700) 20% + 深黑(#1A1A1A) 15%。高对比原色搭配，无渐变 |
| **Typography** | 超大无衬线粗体（Helvetica Neue Bold / Arial Black），字号占幻灯片 15-30% 面积 |
| **Composition** | 色块分区，粗黑边框包裹，偏移阴影，无渐变无模糊 |
| **Visual language** | 几何形状图标（圆、方、三角），粗边框，扁平化，无立体感 |
| **Reference** | "Like a Gumroad landing page — bold, chunky, unapologetic" |
| **适用路径** | Path A（HTML/CSS 原生实现）+ Path B（AI 生成） |

#### 核心 CSS 特征（已验证，131 页实战）

```css
/* 配色 */
--cream: #F5E6D3;
--red: #FF3B4F;
--yellow: #FFD700;
--black: #1A1A1A;

/* 核心要素 */
border: 4-6px solid #1A1A1A;  /* 粗黑边框 */
font-size: 3-6vw;             /* 超大字 */
box-shadow: 8px 8px 0 #1A1A1A; /* 偏移阴影（实色，无模糊） */
overflow: hidden;              /* 无溢出 */
```

#### 5 个核心 Prompt 要素

1. **粗黑边框** — 所有重要元素都有 4-6px 粗黑边框，边框必须完整不能断裂
2. **高饱和色块分区** — 色块之间边界清晰无模糊过渡，每个模块一个主色
3. **超大字排版** — 标题字号占幻灯片 15-30% 面积，无衬线粗体，左对齐或居中
4. **偏移阴影** — 阴影完全实色无模糊，向右下偏移 6-10px，颜色必须是黑色
5. **扁平化图标** — 几何形状图标，有粗边框，无立体感无渐变

#### 实测关键发现（131 页验证）

- **远距离可读性极强** — 粗边框+大字让投影效果远超其他风格，10 米外仍清晰
- **信息层次天然清晰** — 色块分区自带视觉分组，无需额外设计
- **HTML 渲染稳定性高** — CSS 简单（无复杂 SVG、无曲线），渲染成功率接近 100%
- **无需 AI 生成** — 纯 CSS 即可完美实现，不依赖 AI 图片生成（关键优势）
- **适合信息密集场景** — 每页可容纳 3-5 个模块，互不干扰

#### 最佳适用场景

- 企业内训（信息量大、需远距离可读）
- 线下技术分享（投影仪环境）
- 数据密集报告（多模块并存）
- Workshop 工作坊（需要清晰的步骤指引）

#### 注意事项

- 避免使用蓝色或紫色底（容易变成赛博风）
- 文字必须黑色或深色，不要白色（核心是「强对比」而非「反白」）
- 如果出现溢出，减少内容而非缩小字号——大字是灵魂

#### 与其他风格的区别

- vs Bauhaus：Neo-Brutalism 更「粗暴」，边框更粗，色彩更饱和
- vs Neo-Pop：Neo-Pop 有杂志感和装饰元素，Neo-Brutalism 完全功能主义
- vs 苏联构成主义：构成主义有对角线和动态感，Neo-Brutalism 是正交网格

#### 搜索关键词

- `neubrutalism web design`
- `brutalist poster design`
- `Gumroad brand design`
- `flat design with thick borders`

---

## Professional / Editorial 设计系统（Path A 专用）

> 以下风格 **强烈建议使用 Path A（HTML -> PPTX）**。它们依赖精确排版、数据可视化和网格系统，AI 图片生成无法达到所需精度。

---

### 19. Pentagram Editorial — 编辑杂志风（信息建筑派）

| 属性 | 定义 |
|------|------|
| **Philosophy** | Pentagram/Michael Bierut — 字体即语言，网格即思想。用极度克制的设计让数据和内容自己说话 |
| **Colors** | 奶油白 `#FFFDF7` bg / 近黑 `#1A1A1A` text / ONE accent color（如橙红 `#D4480B` 或品牌色） |
| **Typography** | 粗黑标题 (28pt+) + 轻正文 (10-13pt)，英文 section label 作为设计元素 (INSIGHT / PART 03) |
| **Composition** | 瑞士网格系统，2px 黑色边框卡片，精确的水平分隔线，数据可视化内嵌 |
| **Visual language** | 极简图标，条形图/饼图/趋势线，callout 框，tag 标签 |
| **Reference** | "Like a McKinsey insight report meets Monocle magazine — data-rich but editorially elegant" |
| **Ratio** | 60% whitespace / 30% content / 10% accent |
| **执行路径** | Path A only（HTML -> PPTX） |
| **实战验证** | 口腔行业分析 15 页 deck |

**推荐场景：** 数据报告、行业分析、正式商务、咨询提案

---

### 20. Fathom Data Narrative — 数据叙事风（科学期刊派）

| 属性 | 定义 |
|------|------|
| **Philosophy** | Fathom Information Design — 每一个像素都必须承载信息。科学严谨 + 设计优雅 |
| **Colors** | 白 `#FFFFFF` bg / 深灰 `#333` text / 海军蓝 `#1A365D` primary + 一个 highlight color |
| **Typography** | GT America/Graphik 风格 sans-serif，大数字 (60pt+) 作为视觉锚点，精确的脚注/来源标注 |
| **Composition** | 高信息密度但不拥挤，注释系统嵌入布局，small multiples 图表阵列，精确的时间线 |
| **Visual language** | 散点图、热力图、timeline、带注释的图表、数据标签精确到小数 |
| **Reference** | "Like a Nature paper's data supplement meets a Bloomberg data feature" |
| **Ratio** | 50% charts/data / 30% text / 20% whitespace |
| **执行路径** | Path A only（HTML -> PPTX） |

**推荐场景：** 行业分析、投资研究、科学数据展示、复杂报告

---

### 21. Müller-Brockmann Grid — 瑞士网格风（纯粹主义派）

| 属性 | 定义 |
|------|------|
| **Philosophy** | Josef Müller-Brockmann — 客观性即美。数学精确的网格系统让任何混乱的信息变得有序 |
| **Colors** | 白 `#FFFFFF` bg / 黑 `#000` text / 最多一个强调色 |
| **Typography** | Akzidenz-Grotesk/Helvetica，严格的 8pt 基线网格，绝对左对齐，字重对比 (300 vs 700) |
| **Composition** | 8 列数学网格，所有元素对齐到网格线，绝对不允许装饰元素，功能主义至上 |
| **Visual language** | 纯几何图形，黑色线条表格，精确对齐的列表，无图标无插画 |
| **Reference** | "Like the original Swiss Style poster — timeless, rational, zero decoration" |
| **Ratio** | 70% structured grid / 20% text / 10% accent |
| **执行路径** | Path A only（HTML -> PPTX） |

**推荐场景：** 正式商务、学术报告、信息密集型内容、极简主义品牌

---

### 22. Build Luxury Minimal — 奢侈极简风（当代品牌派）

| 属性 | 定义 |
|------|------|
| **Philosophy** | Build Studio — 精致的简单比复杂更难。用大量留白和微妙字重变化传达高端感 |
| **Colors** | 纯白 `#FFFFFF` bg / 深灰 `#2D2D2D` text / 单一 accent（品牌色）极少量使用 |
| **Typography** | 字重变化极微妙 (200-600)，标题巨大 (48pt+) 但轻，正文小而精 (12pt)，字间距宽松 |
| **Composition** | 黄金比例构图，元素极少，每页只说一件事，呼吸感优先 |
| **Visual language** | 高端产品图（如果有），极简图标线条，大面积纯色块，圆角卡片 |
| **Reference** | "Like an Apple keynote meets a Celine lookbook — confident restraint" |
| **Ratio** | 75% whitespace / 15% text / 10% accent |
| **执行路径** | Path A（HTML -> PPTX） |

**推荐场景：** 投资/融资路演、奢侈品牌、高端产品发布、极简品牌

---

### 23. Takram Speculative — 日式思辨风（东方哲学派）

| 属性 | 定义 |
|------|------|
| **Philosophy** | Takram — 技术是思考的媒介。用柔和的科技感和概念原型图传达深度思考 |
| **Colors** | 暖灰 `#F5F3EF` bg / 深灰 `#3D3D3D` text / 鼠尾草绿 `#8B9D77` accent |
| **Typography** | 圆润的 sans-serif，标题不用粗体而用大尺寸 (36pt+)，正文温暖 (14pt)，行高宽松 (1.8) |
| **Composition** | 柔和阴影 (blur 20px+)，圆角 (16px+)，概念图/流程图作为核心视觉，卡片式布局 |
| **Visual language** | 概念原型图、柔和渐变、流程图即艺术、手绘感图标、自然色调 |
| **Reference** | "Like a Takram project page — where technology feels thoughtful, not aggressive" |
| **Ratio** | 55% warm bg / 25% diagrams / 20% text |
| **执行路径** | Path A（HTML -> PPTX，配图可 AI 辅助生成） |

**推荐场景：** 培训课件/教材、国风/东方主题、技术哲学、研究提案

---

## 按主题自动推荐速查表

| 主题类型 | 第一推荐 | 第二推荐 | 第三推荐 |
|---------|---------|---------|---------|
| 品牌/产品介绍 | Snoopy 温暖漫画 | Neo-Pop 新波普 | 浮世绘/敦煌（东方品牌） |
| 教育/培训 | Neo-Brutalism | 学習漫画 | Snoopy 温暖漫画 |
| 技术分享 | xkcd 白板 | Neo-Brutalism | Ligne Claire |
| 数据报告 | Pentagram 编辑 | Fathom 数据 | Ligne Claire |
| 年轻受众 | Neo-Pop | 像素画 | 孔版印刷 |
| 创意/艺术 | 达达拼贴 | 孔版印刷 | The Oatmeal |
| 国风/东方 | 敦煌壁画 | 浮世绘 | Takram 思辨 |
| 正式商务 | Pentagram 编辑 | Müller-Brockmann 网格 | Build 极简 |
| 产品发布/keynote | 苏联构成主义 | Neo-Pop | Pentagram 编辑 |
| 内部分享 | Neo-Brutalism | The Oatmeal | xkcd 白板 |
| 行业分析/咨询 | Fathom 数据 | Pentagram 编辑 | Müller-Brockmann 网格 |
| 培训课件/教材 | Takram 思辨 | 温暖叙事 | 学習漫画 |
| 投资/融资路演 | Build 极简 | Pentagram 编辑 | 苏联构成主义 |

---

> **详细参考：** `design-philosophy` skill 的 `references/design-styles.md` 包含 20 种设计哲学的完整提示词 DNA
