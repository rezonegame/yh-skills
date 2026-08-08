# Prompt 编译器（Prompt Compiler）

> 来源：gc-minimal-zine-poster 的 First-Principles Prompt Fields + Standard Mode Prompt Compiler。
> 核心理念：Prompt 不是「风格词列表」，而是「回答 9 个渲染问题的紧凑画面描述」。

## 适用场景

所有需要生成图像 prompt 的任务。在「导演阶段分离」的阶段二（融合扩写）中使用本编译器，替代自由发挥式的 prompt 写法。

## 9 个第一性原理渲染问题

每个 prompt 必须按顺序回答以下 9 个问题。答案必须是**可渲染的具体视觉描述**，不是抽象概念。

### 1. Canvas（画布）
**问题**：输出的画框和基底表面是什么？
- 明确比例（3:4、16:9、1:1、3:5 等）
- 明确基底材质（纸张、屏幕、画布、金属、布料等）
- 明确边界处理（有边框/无边框/出血/安全区）

**示例答案**：
- 极简：`tall vertical 3:5 phone-poster; full-frame aged paper; no border, no mockup`
- Mondo：`vertical 2:3 movie poster; dark textured background; screen-print registration marks at corners`
- 电商：`vertical 4:5 product showcase; clean gradient background; no border, no mockup`

### 2. Attention Geometry（注意力几何）
**问题**：视线去哪里？多少是空的？
- 主体占画面的百分比（8%-25% 极简 / 30%-60% 电商 / 15%-40% Mondo）
- 留白/负空间的百分比
- 主体的精确位置（居中/左下/右上/偏移量）
- 禁止「贴边」：主体不应紧贴画框边缘

**示例答案**：
- 极简：`70%-90% plain paper; one visual cluster occupying 8%-25%; placed center, upper-middle, or lower-left`
- Mondo：`30%-50% negative space; main figure fills center-to-bottom; top reserved for title`
- 电商：`40%-60% background space; product centered or slightly above center; bottom reserved for info`

### 3. Image Anchor（图像锚点）
**问题**：画面中唯一可成像的主体是什么？
- 将用户的主题转化为**一个**对象、片段、裁切、标本、剪影、印刷插图、纹理窗口或小概念关系
- 不要试图描绘整个场景或完整叙事
- 如果用户给了复杂主题，提取**一个中心可成像概念**，而非总结全文

**示例答案**：
- 极简：`a single faded photograph of a staircase, cropped to show only three steps`
- Mondo：`a lone samurai silhouette standing against a rising moon, layered over geometric bamboo pattern`
- 电商：`the product bottle, front-facing, with subtle light reflections on glass surface`

### 4. Anchor Treatment（锚点处理）
**问题**：什么物质过程让锚点属于画面？
- 极简/复古：低对比度、复印柔化、撕边、半调、扫描线、孔版颗粒、墨迹晕染
- Mondo：分层剪影、套印错位、丝网墨迹边缘
- 电商：干净抠图、柔和阴影、光面反射
- 信息图：数据编码、色块填充、线条连接

**关键规则**：不要对锚色应用低饱和度或低对比度处理。低对比度只用于纸张、照片和辅助元素。

### 5. Typography System（文字系统）
**问题**：文字在视觉上如何表现？
- 字体类型选择（衬线/等宽/无衬线/手写/活字）
- 文字量（短语/标题+副标题/数据标注/几乎无文字）
- 文字行为（漂浮、紧贴边缘、模糊、错印、嵌入色块、结构化层级）
- 语言（中文/英文/双语）

**示例答案**：
- 极简：`small serif type; one short readable phrase; semi-legible microtext; text drifts and presses against image edge`
- Mondo：`bold condensed sans-serif title at top; film credits-style cast list at bottom; hand-lettered tagline`
- 电商：`large bold product name at top; 3 benefit bullet points below; brand logo bottom-left`

### 6. Color Logic（色彩逻辑）
**问题**：什么是克制的色彩策略？
- 读取 `references/color-engine.md` 获取风格族专属色彩标准
- 明确锚色的色相、材质形态、面积占比
- 确保锚色在缩略图下可见
- 只用一个主锚色，允许一个微小辅助色

**示例答案**：
- 极简：`paper tones plus gray/black support one fully saturated cobalt-blue risograph ink block, occupying ~1.5% of canvas`
- Mondo：`3-color screen-print: electric red fills the samurai silhouette, deep navy shadows, gold accent on moon crescent`
- 电商：`clean white-to-gray gradient background; product's amber liquid as primary color anchor; coral accent on CTA button`

### 7. Reproduction Texture（复现纹理）
**问题**：什么印刷/扫描/渲染过程定义了整体画面？
- 极简：平面正交扫描纸张外观、哑光吸墨纸、漫射光、低中对比度
- Mondo：丝网印刷墨迹、纸张纹理、轻微套印错位
- 电商：干净数字化、柔和阴影、无纹理
- 信息图：干净矢量感、轻微纸张纹理或无

### 9. Emotional Temperature（情感温度）
**问题**：观众在辨认出对象之前应该感受到什么？
- 选择一个主要情绪词（安静/大胆/趣味/戏剧性/编辑感/高端/怀旧/孤独等）
- 情绪词应影响光线、对比度、色调的选择
- 不要让情绪词变成风格词堆砌（「充满活力的、动态的、现代的」不算有效情绪）

### 10. Skin & Atmosphere Realism（皮肤质感与氛围真实感）
**问题**：画面中的人物皮肤和空间氛围是否可信？
- 人物场景：皮肤是否保留自然毛孔肌理和血色过渡？是否避免过度磨皮/死白/塑料感？
- 所有场景：光影是否有明暗层次？空间是否有空气感（轻微颗粒/浮尘/景深）？
- 根据风格族选择真实感程度（极简/复古/纪实可保留颗粒，电商/UI 可适当干净但不过度）
- 参考 `references/style-avoids.md` 中的「Anti-Plastic / 真实质感」Hard Avoids

**示例答案**：
- 人物特写：`natural skin texture with visible pores, subtle blood flush on cheeks, no plastic smoothing, no porcelain finish`
- 所有场景：`natural lighting with soft shadow contrast, subtle film grain, atmospheric dust particles, no sterile clean look`
- 电商产品：`pristine product surface with natural reflections, clean but not sterile, subtle depth of field`

### 11. Hard Avoids（硬性避免）
**问题**：什么绝对不能出现？
- 读取 `references/style-avoids.md` 获取风格族专属避免列表
- 在 prompt 中明确列出避免项
- 避免项应与风格族相关，不是通用的「不要低质量」

## Prompt 输出结构

每个 prompt 写成 **4 个紧凑段落**（不写编号，不写字段名）：

### 段落 1：Canvas + 空间 + 主体位置
画布描述、基底材质、负空间比例、主体集群的大小和位置。

### 段落 2：主体隐喻 + 锚点类型 + 锚点处理
将用户主题转化为一个可成像主体，描述其物质形态和视觉处理方式。

### 段落 3：文字 + 色彩 + 印刷纹理
字体类型、文字行为、明确的高纯度色相、材质形态、面积占比、印刷/扫描纹理。

### 段落 4：情绪 + 避免列表
整体情感基调、平面扫描/渲染感受、硬性避免项。

## 坐标系统一规则（Coordinate Discipline · 吸收自南鸢 nuyoah 人像反推方法论）

**问题：** 当 prompt 混用"人物左侧"和"画面左侧"时，模型会随机解读，导致视线方向、手势位置、构图偏移全部出错。

**规则：**

1. **全程使用观者坐标**——画面左/右始终以观看者的视角为准
2. 禁止混用"人物自身左侧"和"画面左侧"——选一套，贯穿全 prompt
3. 描述视线方向时必须明确参照系：
   - ✅ 正确："双眼瞳孔偏向画面左侧，视线落在画面左侧的草莓上"
   - ❌ 错误："眼睛看向左边的草莓"（模型不知道是哪个左边）
4. 描述手势位置时同样锁定坐标：
   - ✅ 正确："画面左侧食指斜向左上，画面右侧食指接近竖直"
   - ❌ 错误："左手手指指向左上方"（左右手可能反转）
5. 非对称构图必须用坐标描述偏移方向："头部向画面左侧倾斜"、"身体沿对角线从画面左下向右上延伸"

**编译检查：** 输出 prompt 前扫描所有方向性描述，确认是否全部统一为观者坐标。发现混用 → 修正后再输出。

**关键纪律**：
- 段落 3 必须包含精确的高纯度色相、材质形式和视觉占比
- 结构比措辞更重要。一个紧凑的 4 段 prompt 比一个长篇风格散文更有效
- 禁止把字段名直接拼进 prompt（如「主体：XX，风格：XX」）
- prompt 应该是一个「可以直接渲染的画面」，不是「参数列表」

## 编译检查表

输出 prompt 前，验证：

|- [ ] 10 个渲染问题是否全部回答？
- [ ] 每个答案是否是可渲染的具体描述（而非抽象概念）？
- [ ] 是否使用了 4 段式结构？
- [ ] 段落 3 是否包含精确的色相名、材质形态和面积占比？
- [ ] 是否有字段名标签混入 prompt？（不应该有）
- [ ] prompt 读起来是否像一个「画面」而不是「参数列表」？
- [ ] 风格族专属 Hard Avoids 是否已嵌入段落 4？
- [ ] 锚色是否未被弱化词污染？
