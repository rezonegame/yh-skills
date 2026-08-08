# 变化引擎（Variation Engine）

> 来源：gc-minimal-zine-poster 的 Variation Engine 架构，扩展为通用视觉变化系统。
> 核心原则：Randomness must change **visual grammar**, not only position.

## 用途

连续出图（系列图、多方案对比、批量生成）时，从每个轴随机选一个选项，组合后确保视觉语法不重复。单图任务也需要选一组变化，避免默认落入「中间主体 + 下方文字」的舒适区。

## 通用五轴

### Axis 1：构图布局（Layout Family）

| 选项 | 描述 | 适用场景 |
|---|---|---|
| center-fragment | 居中小主体，大量留白环绕 | 产品展示、概念海报 |
| lower-left-float | 锚点在左下象限，上方大量留白 | 文艺海报、摄影精选 |
| upper-right-block | 右上色块/图片，文字松散漂移 | 编辑排版、杂志封面 |
| dual-panel | 两个小面板重叠或并排，窄缝隙 | 对比、叙事、日记风 |
| irregular-cutout | 撕裂/有机纸张形状承载图像或文字 | 手工质感、拼贴风 |
| type-led | 排版为主视觉锚点，图像次要或缺席 | 字体海报、标题设计 |
| dot-orbit | 点/字母/细线围绕小主体形成轨道 | 极简装饰、概念图 |
| single-specimen | 一个孤立对象或标记，几乎无辅助 | 产品特写、科学标本 |
| diagonal-cut | 对角线切割画面 | 动感海报、运动品牌 |
| grid-modular | 网格模块化布局 | 系列展示、信息密集 |
| top-bottom-split | 上下两段式 | 场景对比、前后对比 |
| spiral-flow | 螺旋引导视线 | 叙事海报、流程图 |

### Axis 2：主体处理（Image Anchor）

| 选项 | 描述 |
|---|---|
| tiny-faded-photo | 微小褪色照片 |
| torn-paper-clipping | 撕纸剪报 |
| flat-silhouette | 平面剪影 |
| solid-color-block | 纯色块 |
| old-printed-illustration | 旧印刷插图 |
| object-specimen | 物件标本 |
| translucent-geometric | 半透明几何叠加 |
| abstract-texture-window | 抽象纹理窗口 |
| full-bleed-hero | 满版主视觉 |
| layered-depth | 多层深度叠加 |
| break-the-frame | 突破画框边界 |
| cutout-shape | 异形裁切 |

### Axis 3：文字系统（Typography Mode）

| 选项 | 描述 |
|---|---|
| fragmented-letters | 碎片漂浮字母 |
| edge-pressed-phrase | 短语紧贴图像边缘 |
| archive-microtext | 档案式微缩文字+日期/天气 |
| diagonal-scattered | 对角线散落单词 |
| ghost-text | 低对比度幽灵文字 |
| headline-as-object | 标题即主体（粗活字印刷） |
| text-in-color-block | 文字嵌入色块内 |
| almost-textless | 几乎无文字，仅小注释 |
| structured-hierarchy | 结构化层级（大标题+副标题+正文） |
| data-overlay | 数据标注叠加（坐标、数值、标签） |
| vertical-stack | 竖排堆叠 |
| bilingual-mix | 中英双语混排 |

### Axis 4：材质纹理（Texture Mode）

| 选项 | 描述 |
|---|---|
| xerox-softness | 复印机柔化 |
| risograph-grain | 孔版印刷颗粒 |
| letterpress-ink-bleed | 活字印刷墨迹晕染 |
| halftone-degradation | 半调网点退化 |
| film-grain | 胶片颗粒 |
| scan-noise | 扫描噪点+纸张纤维 |
| aged-paper-mottling | 老化纸张斑驳 |
| motion-blur-text | 文字动感模糊 |
| clean-digital | 干净数字化（无纹理） |
| matte-absorbent | 哑光吸墨纸 |
| glossy-reflection | 光面反射 |
| screen-print | 丝网印刷质感 |

### Axis 5：情绪温度（Mood Mode）

| 选项 | 描述 |
|---|---|
| quiet | 安静、克制 |
| summer | 夏日、明亮 |
| solitude | 孤独、留白 |
| childhood | 童年、怀旧 |
| seaside | 海边、风 |
| afternoon | 午后、温暖 |
| night | 夜晚、深沉 |
| memory | 记忆、褪色 |
| surrealism | 轻微超现实 |
| bold-confident | 大胆、自信 |
| playful | 趣味、活泼 |
| dramatic | 戏剧性、张力 |
| editorial | 编辑感、专业 |
| premium-luxury | 高端、奢华 |

## 风格族专属轴配置

不同风格族可以从通用轴中选取子集，并添加专属选项：

### 极简/Zine 风格
- Layout: center-fragment, lower-left-float, upper-right-block, dual-panel, irregular-cutout, type-led, dot-orbit, single-specimen
- Anchor: tiny-faded-photo, torn-paper-clipping, flat-silhouette, solid-color-block, old-printed-illustration, object-specimen
- Typography: fragmented-letters, edge-pressed-phrase, archive-microtext, diagonal-scattered, ghost-text, headline-as-object, text-in-color-block, almost-textless
- Texture: xerox-softness, risograph-grain, letterpress-ink-bleed, halftone-degradation, film-grain, scan-noise, aged-paper-mottling, motion-blur-text
- Mood: quiet, summer, solitude, childhood, seaside, afternoon, night, memory, surrealism

### Mondo/丝网印刷海报
- Layout: center-fragment, diagonal-cut, full-bleed-hero, top-bottom-split, layered-depth
- Anchor: layered-depth, break-the-frame, solid-color-block, flat-silhouette, cutout-shape
- Typography: headline-as-object, structured-hierarchy, almost-textless, bilingual-mix
- Texture: screen-print, risograph-grain, halftone-degradation, letterpress-ink-bleed
- Mood: bold-confident, dramatic, night, surrealism

### 电商/商品海报
- Layout: center-fragment, single-specimen, grid-modular, dual-panel
- Anchor: full-bleed-hero, object-specimen, layered-depth, translucent-geometric
- Typography: structured-hierarchy, data-overlay, bilingual-mix
- Texture: clean-digital, glossy-reflection, matte-absorbent
- Mood: bold-confident, premium-luxury, playful, editorial

### 信息图/图解
- Layout: grid-modular, top-bottom-split, spiral-flow, diagonal-cut
- Anchor: data-overlay, grid-modular, object-specimen
- Typography: structured-hierarchy, data-overlay, vertical-stack
- Texture: clean-digital, matte-absorbent
- Mood: editorial, quiet, bold-confident

## 变化选择算法

1. 回顾最近 3 次同类任务的输出（如有）
2. 检查哪些轴选项已使用过
3. 优先选择**未使用过的视觉语法**（不只是位置不同）
4. 如果所有选项都用过一轮，组合两个之前未搭配过的选项
5. 如果配方过密，先简化文字系统或色彩处理

## Anti-Repetition 规则

- 连续 2 张图不能使用相同的 Layout + Anchor 组合
- 连续 3 张图不能使用相同的 Typography Mode
- 同批次至少 60% 的图使用不同的 Texture Mode
- 同批次所有图必须使用不同的 Mood Mode（除非用户要求统一情绪）
