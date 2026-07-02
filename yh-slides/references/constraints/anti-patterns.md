# 反模式清单（Anti-Patterns）

> **适用路径**：全部产物路径  
> **强制级别**：所有路径通用的"绝不做"清单

这个文档记录 yh-slides 所有路径共享的"绝对禁止"做法。违反它们的结果要么是审美崩塌，要么是功能出错。

---

## 🚫 审美类反模式

### AP-1: 使用 Emoji 作图标

**禁止**：`🎯 💡 ✅ 🔥 ⭐` 等 emoji 出现在标题、正文、按钮中

**原因**：
- 破坏"杂志级" / "专业级"的视觉格调
- 在不同系统（Windows / Mac / Linux）渲染差异大
- AI 生成感强烈，降低专业度

**正确做法**：
- Path A / C / D：用本地 `assets/vendor/js/lucide.js` / `lucide.min.js` 或 inline SVG；不要依赖 CDN
- Path B（AI 图片）：在 prompt 里明确 `no emoji, use line icons or typography`

```html
<!-- ❌ 禁止 -->
<h2>🎯 目标</h2>

<!-- ✅ 正确 -->
<h2><i data-lucide="target" class="ico-md"></i> 目标</h2>
```

---

### AP-2: 自定义 Hex 颜色（Magazine 路径）

**禁止**：在 magazine 路径下用户或 Claude 自由指定颜色

**原因**：
- guizang 的 5 套主题色是"精心调配的美学下限保护"
- 随机 hex 值（如 `#ff6600`）会立刻破坏电子杂志美感
- 混搭（如墨水 ink + 沙丘 paper）会彻底违和

**正确做法**：
- 只从 [themes.md](../aesthetics/magazine/themes.md) 的 5 套里选一套
- 整体替换 `:root` 块的 6 个变量，不要只改一两个
- 用户要求 "红色主题" → 推荐 墨水经典 + 荧光标记强调

```css
/* ❌ 禁止 */
:root {
  --ink: #2e4d7a;   /* 随机取色 */
  --paper: #fff9e5;  /* 不匹配 */
}

/* ✅ 正确：完整替换一套 */
:root {
  --ink: #0a1f3d;        /* 靛蓝瓷 */
  --ink-rgb: 10,31,61;
  --paper: #f1f3f5;
  --paper-rgb: 241,243,245;
  --paper-tint: #e4e8ec;
  --ink-tint: #152a4a;
}
```

**例外**：Path A / Path C 的 Custom 子路径（非 magazine）允许自定义颜色，但建议用 `references/aesthetics/web-styles-gallery.md` 的预设。

---

### AP-3: 标题字号 × 字数不匹配

**禁止**：中文大标题 `h1-zh / display-zh` 字号设太大，导致每行 1-2 个字强制换行

**例子**：
```html
<!-- ❌ 禁止：字号 10vw，标题却 10 个字 -->
<h1 class="h1-zh" style="font-size:10vw">设计先行一人成军</h1>
<!-- 结果：渲染成 "设/计/先/行/一/人/成/军" 8 行竖排 -->
```

**正确做法**：
- `.display-zh`（最大）：字数 ≤ 5，字号 7-8vw
- `.h1-zh`：字数 ≤ 10，字号 4-5vw
- 长标题用 `<br>` 手工断行
- 必要时加 `white-space: nowrap`

```html
<!-- ✅ 正确：长标题手工断行 -->
<h1 class="h1-zh">
  设计先行<br>
  <em style="opacity:.65">一人成军</em>
</h1>
```

---

### AP-4: 图片使用 `align-self: end` 贴底

**禁止**：图文混排时给图片加 `align-self: end` 试图让图片与左列文字底对齐

**原因**：
- `align-self` 在非 grid/flex 容器里完全失效
- 失效后图片会掉到文档流末尾，被 `.foot` 和 `#nav` 遮挡
- 即使在 grid 里生效，低分屏仍会被底栏压到

**正确做法**：
- 图文混排**必须用 `.frame.grid-2-7-5`**（或 `.grid-2-6-6` / `.grid-2-8-4`）
- 右列图片用标准比例 `16/10` 或 `4/3` + `max-height: 56vh`
- 让"左列 callout 贴底"用 `justify-content: space-between`，而不是动右列

详见 [magazine/checklist.md #4b](../aesthetics/magazine/checklist.md)。

---

### AP-5: 图片原图奇葩比例

**禁止**：直接用 `aspect-ratio: 2592/1798` 这种从原图复制的比例

**原因**：
- 不同屏幕下撑出奇怪空白或溢出
- 破坏网格对齐
- 图片容器尺寸不可预测

**正确做法**：
- 永远用标准比例：`16/10` / `4/3` / `3/2` / `1/1` / `16/9`
- 图片容器固定 `height: Nvh`，让 `object-fit: cover` 自动裁剪
- 图片只允许裁底部，**不能裁顶部和左右**

```html
<!-- ❌ 禁止 -->
<figure class="frame-img" style="aspect-ratio: 2592/1798">

<!-- ✅ 正确 -->
<figure class="frame-img" style="height: 26vh">
  <img src="screenshot.png" alt="...">
</figure>
```

---

### AP-6: 图片加厚边框 / 阴影

**禁止**：
- `box-shadow: 0 10px 30px rgba(0,0,0,.3)` 等强阴影
- `border: 2px solid #333` 等深色粗边框
- `border-radius: 12px` 以上的大圆角

**原因**：瞬间把"电子杂志" / "精品感"变成"消费 APP UI" 或 "2010 年的商务 PPT"

**正确做法**：
- 最多 `border-radius: 4px` 的微圆角
- 不加 `box-shadow`
- 如需边框，只加 `1px` 极淡的灰（如 `rgba(127,127,127,.12)`）

---

### AP-7: chrome 和 kicker 同义翻译

**禁止**：
```html
<!-- ❌ chrome 和 kicker 说同一件事的两种语言 -->
<div class="chrome">
  <div>设计先行 · Design First</div>
</div>
<div class="kicker">Phase 01 · 设计阶段</div>
```

**原因**：
- chrome 和 kicker 是两个不同维度
- 同义翻译让 AI 生成感爆棚
- 浪费宝贵的视觉"小字"空间

**正确做法**：
- `chrome` = 杂志页眉 / 栏目名（跨多页可相同）
- `kicker` = 这一页独一份的引导句（每页不同）

```html
<!-- ✅ 正确 -->
<div class="chrome">
  <div>Act II · Workflow</div>
  <div>05 / 27</div>
</div>
<div class="kicker">BUT</div>
<h1 class="h1-zh">慢一点...</h1>
```

---

### AP-8: 术语中英文反复切换

**禁止**：一会儿写 "Skills"，一会儿写 "技能"，一会儿写 "薄承载厚技能"

**原因**：
- 读者会觉得这是"AI 生成的东西、翻译都不统一"
- 破坏术语的"专业锚定"

**正确做法**：
- 术语优先用**圈内熟悉词**（Skills / Harness / Pipeline / Workflow 这些就用英文）
- 整个 deck 同一词只用 1 种写法
- 不要"硬翻译"成生硬的中文

---

## ⚙️ 技术类反模式

### AP-9: 发明不存在的 CSS class

**禁止**：Claude 生成时自作主张地使用种子 `<style>` 里没有定义的 class

**参考**：详细预检流程见 [class-preflight.md](./class-preflight.md)

---

### AP-10: Path A 遗漏 `position: absolute`

**禁止**（Path A 专属）：HTML 幻灯片的元素没有 `position: absolute`

**原因**：
- html2pptx 转换器依赖绝对定位还原坐标
- 用 flow / flex / grid 定位的元素，转 PPTX 后会错位或消失

**正确做法**：
- 所有 `.slide` 内部元素必须 `position: absolute`
- 用 `top` / `left` / `width` / `height` 精确指定位置
- 详见 `SKILL.md` 的 Path A 规范和 `path-a-seed.html`

```html
<!-- ❌ 禁止 -->
<div class="slide">
  <div class="flex">
    <h1>标题</h1>
    <img src="..." />
  </div>
</div>

<!-- ✅ 正确 -->
<div class="slide" style="position:relative;width:720pt;height:405pt">
  <h1 style="position:absolute;top:60pt;left:60pt;font-size:40pt">标题</h1>
  <img src="..." style="position:absolute;top:120pt;left:60pt;width:300pt;height:200pt">
</div>
```

---

### AP-11: Path A HTML 尺寸不是 720×405pt

**禁止**：Path A 的 HTML 用 `1920×1080` 或 `100vw×100vh`

**原因**：html2pptx 严格要求 720pt × 405pt（16:9 @ 标准演示尺寸）

**正确做法**：
```html
<div class="slide" style="width:720pt;height:405pt;position:relative;overflow:hidden">
```

---

### AP-11A: Path A 文本贴边或出框

**禁止**（Path A 专属）：为了塞下高密度内容，把正文文本框贴到画布边缘、卡片边缘或页脚保留区。

**原因**：
- html2pptx 转换后文字渲染可能比浏览器略有差异，贴边设计会放大溢出风险
- 中文列表、脚注、长标题最容易在 PPTX 中挤压或被裁切
- 可编辑 PPTX 的价值在于后期能改，文本框一旦没有余量，用户稍微改字就会出框

**正确做法**：
- 生成 Path A 前读取 `references/constraints/path-a-layout-safety.md`
- 正文文本放在 `x=32..688`、`y=32..370` 安全区内
- 卡片内文字至少内缩 `10pt`，推荐 `12pt`
- 高密度页面先选 A1/A2/A3 页型或写布局表，再写 HTML

---

### AP-12: 把 2C 底图做成带正文文字的整图

**禁止**（2C 专属）：`2C 视觉底图 + 可编辑文字 PPTX` 的底图 prompt 里让 AI 渲染标题、正文、互动题、答案或其他需要后期修改的文字。

**原因**：
- 2C 的核心价值是“视觉好 + PPT 文字可编辑”
- AI 底图一旦承担正文文字，就退化成 2B，后期无法稳定改字
- 中文、题目、答案、数据标注更应该由 PPT 原生文本框承担

**正确做法**：
- 2C 底图 prompt 必须写 `no text, no letters, no title, no body copy, no question text, no answer text`
- 底图只负责背景、插画、氛围、结构空间和装饰
- 标题、正文、互动题、答案、数据标注全部用 PPT 文本框叠加
- 如果用户真的想让整页图里包含文字，改选 `2B 整图视觉 PPTX`
- 如果唯一输入已经是位图且需要恢复可编辑结构，才考虑 `2B-R / FigEdit Reconstruction`；正向制作优先 2A、2A-S 或 2C

---

### AP-13: Path C / D 连外部 CSS / JS

**禁止**：Path C / D 引用外部 CSS / JS 作为必需运行资源

**原因**：
- Path C 的核心价值是离线可分享
- 引用外部 CSS / JS 破坏离线分享能力
- 外部运行资源不稳定时页面会裸奔

**正确做法**：
- 所有 CSS **内联到 `<style>` 块**
- 项目 JS 优先内联到 `<script>` 块
- 字体、Lucide、GSAP、Motion 等前端运行资源使用本地 `assets/vendor/`
- 图片使用本地相对路径；如确需 API 搜索图片，下载到本地后再引用

**Path D**：GSAP 已本地化到 `assets/vendor/js/gsap.min.js`，不要改回远程资源。

---

### AP-14: Console.log / debugger / 注释残留

**禁止**：生成的最终 HTML / JS 里留下：
- `console.log(...)` 调试语句
- `debugger;` 断点
- `// TODO: ...` / `// FIXME: ...` 等个人备忘注释

**正确做法**：
- 清理所有调试代码
- 保留"指向规范"的注释（如 "see references/..."）

---

## 📐 流程类反模式

### AP-15: 跳过 Step 0 协作模式 / Step 1 内容澄清

**禁止**：用户说"帮我做个 PPT"后直接开始生成

**原因**：
- 没搞清楚受众 / 时长 / 约束，生成的 PPT 大概率不符合需求
- 来回返工 2-3 轮，浪费用户时间

**正确做法**：
- 先走 SKILL.md 的 Step 0 协作模式，再按 Step 1 的 7 字段需求发现
- 明确受众、时长、素材、约束、图片需求
- 基于答案推荐路径

---

### AP-16: 跳过预检直接生成

**禁止**：选好路径后直接生成 slide 代码，不做类名预检 / 主题节奏规划

**原因**：
- 100% 概率翻车（class 塌 / 节奏乱）
- 用户看到糟糕结果，对整个 skill 失去信心

**正确做法**：
- Path C / D 生成前必做 Step 5.0（class preflight）和 Step 5.0.5（theme rhythm）
- Path A 生成前必读 720×405pt + absolute 规范
- Path B 生成前必填 prompt 模板 + tasks.json

---

### AP-17: 生成后不走分级质检

**禁止**：生成完就交付，不走 Step 7 的 P0-P3 检查

**正确做法**：
- 所有路径完成后对照 [quality-checklist.md](./quality-checklist.md)
- P0 不通过必须修复
- P1 强烈建议修复
- P2/P3 按需抛光

---

## 快速记忆

**审美 7 禁止**：Emoji / 自定义 hex / 字号过大 / align-self:end / 奇葩比例 / 重阴影 / chrome-kicker 同义  
**技术 5 禁止**：发明 class / 漏 position:absolute / 错尺寸 / 图片含文字 / 外部资源  
**流程 3 禁止**：跳澄清 / 跳预检 / 跳质检
