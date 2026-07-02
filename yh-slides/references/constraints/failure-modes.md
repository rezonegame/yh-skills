# 失败模式清单（Failure Modes）

> **适用路径**：全部 4 条路径
> **使用时机**：生成出问题时的排查手册

本文档收集 yh-slides 4 条路径里**最容易翻车的 20+ 种失败模式**，每种都给出：

- **症状**：视觉 / 代码 / 日志里的直接表现
- **根因**：为什么发生
- **修复**：具体步骤
- **预防**：下次怎么避免

---

## Path A 失败模式（HTML → PPTX）

### FM-A-1: PPTX 里元素位置全错

**症状**：
- HTML 浏览器预览正常，但 html2pptx 转出的 PPTX 里元素位置错乱
- 文字堆到左上角、图片飞出幻灯片外

**根因**：
- 元素没有 `position: absolute`
- html2pptx 的布局依赖绝对定位还原坐标；flow / flex / grid 定位会被忽略

**修复**：
```bash
grep -L 'position:absolute' slides/*.html
# 列出所有没有 absolute 的文件，逐个补
```
每个 `<div>` / `<h1>` / `<img>` 都加：
```html
<... style="position:absolute;top:60pt;left:60pt;width:Npt;height:Npt">
```

**预防**：
- 生成 Path A HTML 前必读 [anti-patterns.md AP-10](./anti-patterns.md)
- 用 `assets/seeds/path-a-seed.html` 作为起点，不要从零写

---

### FM-A-2: PPTX 显示空白 / 元素缺失

**症状**：
- PPTX 打开后多页是空白或缺少大部分内容
- html2pptx 命令本身没报错

**根因**：
- HTML 尺寸不是 `720pt × 405pt`
- html2pptx 会把超出 720×405 的内容裁掉
- 用 `1920×1080` 或 `100vw` 的会整个塌掉

**修复**：
每个 slide 根容器都改成：
```html
<div class="slide" style="width:720pt;height:405pt;position:relative;overflow:hidden">
```

**预防**：
- Path A 的 P0-1 检查：`grep 'width:720pt' slides/*.html` 数量应等于 slide 数量
- 不要复用非 Path A 的 HTML 模板

---

### FM-A-3: 图片里出现机器乱码文字

**症状**：
- AI 生成的插画里有奇怪的字母 / 假汉字
- 看着像"外星人语言"

**根因**：
- 图片 prompt 没有写 `no text in image`
- AI 模型默认会尝试在图片里画文字

**修复**：
- 对已生成的图片：修改 prompt 加 `no text in image, no letters, no words` 后重新生成
- 如果图片已经成为唯一源文件且必须恢复可编辑结构，改走 2B-R / FigEdit Reconstruction；不要擦除背景后叠字

**预防**：
- 所有 Path A/B 的图片 prompt 必须显式包含 `no text in image`
- 在 `tasks.json` 模板里把这段设为必填默认

---

### FM-A-4: 字体在 PPTX 里变成黑体 / 宋体

**症状**：
- HTML 里指定了 `Noto Serif SC` / `Playfair Display`
- PPTX 打开后全部变回 PowerPoint 默认字体

**根因**：
- html2pptx 不嵌入 Web Font
- 目标机器没装对应字体
- PowerPoint 只渲染本地已安装的字体

**修复**：
- 如果部署目标机可控：在那台机器上装 Noto Serif SC + Playfair Display
- 否则：改用 PowerPoint 自带字体（思源宋体 / Times New Roman 等）

**预防**：
- 交付前确认目标机字体环境
- 或者直接走 Path B（图片里的字不依赖字体）

---

## Path B失败模式

### FM-B-std-1: 图片批量生成中途失败

**症状**：
- `generate_image.py batch` 跑到一半某张失败
- 后续任务全部停下

**根因**：
- API 限流 / 网络抖动 / 配额耗尽
- 或某个 prompt 触发内容安全

**修复**：
```bash
# 继续从上次断点
uv run scripts/generate_image.py batch --tasks tasks.json --cooldown 10 --skip-existing
```
- `--skip-existing` 会跳过已生成的，只重跑失败的
- 把 cooldown 从 8 加到 10-15 秒

**预防**：
- batch 一开始就用 `--cooldown 8` 以上
- 失败日志保留，检查是否某类 prompt 被触发安全过滤

---

### FM-B-std-2: 图片风格不一致（混 Snoopy + Bauhaus）

**症状**：
- 同一套 PPTX 里有的页是 Snoopy 线稿，有的是 Bauhaus 几何
- 观众一眼看出是 AI 东拼西凑

**根因**：
- tasks.json 里不同页的 prompt 用了不同风格关键词
- 没有统一"风格 prefix"

**修复**：
- 重新写 tasks.json：抽取统一的 `style_prefix`（如 `"in Snoopy cartoon line art style, no text"`），所有 task 共享
- 重跑 batch

**预防**：
- Step 2（设计系统）后，把选中的风格描述固化为 prompt 的第一行
- 参考 `references/aesthetics/proven-styles-*.md` 的 style definition 格式

---

### FM-B-std-3: PPTX 文件体积过大（> 200MB）

**症状**：
- `.pptx` 文件 300MB+
- PowerPoint 打开慢、分享卡

**根因**：
- 图片用 4K 分辨率但幻灯片只显示 1920×1080
- 每张 PNG 5-10MB × 20 页

**修复**：
```bash
# 重新以 2K 生成
uv run scripts/generate_image.py batch --tasks tasks.json --image-size 2K
# 重新组装 PPTX
uv run scripts/create_slides.py ...
```

**预防**：
- 演示用 2K 足够（屏幕 Retina 也是 1440p 渲染）
- 4K 只在"大屏海报打印"时用

---

## 2B-R / FigEdit Reconstruction 失败模式

### FM-2BR-1: 预检失败

**症状**：缺少 FigEdit、PaddleOCR、PaddlePaddle、OpenCV 或转换依赖。

**修复**：运行 `python scripts/figedit_batch.py preflight`，按输出的安装命令显式安装。不要在制作过程中静默安装大型依赖。

### FM-2BR-2: 检测噪声进入最终图

**症状**：多余矩形、错误箭头或 OCR 错字出现在 SVG/PPTX。

**根因**：把 OCR/OpenCV 候选当成最终对象，而没有 Agent 语义审查。

**修复**：回到逐页 Manifest，删除、合并或改写错误候选；检测结果只作为测量证据。

### FM-2BR-3: 资产被错误矢量化

**症状**：Logo、特色图标、截图、地图或复杂图表被通用图形替代。

**修复**：将该对象改为 source-preserved crop，并保留周围标题、边框、标签和连接线为可编辑对象。

### FM-2BR-4: 质量门阻止整套导出

**症状**：`status` 返回失败，`assemble` 不生成最终 PPTX。

**修复**：读取 `summary_report.md` 和 `failed_pages.json`，逐页修复缺失输出、公式泄漏、editability review 或未批准的 `delivery_review`。这是预期保护行为，不得回退为图片型 PPTX。

---

## Path C 失败模式

### FM-C-1: 页面样式全塌 / 元素堆叠

**症状**：
- 浏览器打开后，所有 `<section>` 挤在一起
- 没有 scroll-snap 效果
- 字体全部变成默认 sans

**根因**：
- Claude 发明了种子里没有的 class（如 `.stat-card`、`.title-zh-big`）
- 浏览器 fallback 到默认样式
- 整个排版架构崩溃

**修复**：
```bash
# 找出未定义的 class
diff <(grep -oE 'class="[^"]+"' index.html | grep -oE '[a-z][a-z0-9-]+' | sort -u) \
     <(grep -oE '\.[a-z][a-z0-9-]+' assets/seeds/path-c-magazine-seed.html | sort -u)
```
- `<` 开头的行就是发明的 class
- 要么改成种子里已有的类，要么在种子 `<style>` 里补上定义

**预防**：
- 生成前必做 [class-preflight.md](./class-preflight.md) 的 Step 1-4
- 用种子文件作为起点，不要从空白 HTML 开始

---

### FM-C-2: scroll-snap 不工作 / 翻页错位

**症状**：
- 鼠标滚轮翻页后停在页面中间
- 或键盘翻页跳过一页

**根因**：
- Claude 在 `<section>` 加了 inline style 覆盖基础架构
- 或根容器 `<main id="deck">` 的 scroll-snap 被改
- 或视口不是 1920×1080（scroll-snap 在其他尺寸有差异）

**修复**：
- 检查 `<main>` 和 `<section>` 有没有多余的 inline style：
  ```bash
  grep -E '(main|section)[^>]*style=' index.html
  ```
- 删除所有对 `height` / `overflow` / `scroll-snap` 的 inline 覆盖
- F11 全屏浏览器到 1920×1080 再测

**预防**：
- 不要在基础架构 class（.slide / .frame / #deck）上加 inline
- 参考 [anti-patterns.md AP-9](./anti-patterns.md)

---

### FM-C-3: 图片显示不全 / 溢出容器

**症状**：
- 图片只显示一角或被裁到离谱
- 或图片把文字挤走

**根因**：
- 图片容器用了 `aspect-ratio: 原图比例`（如 2592/1798）
- 不同屏幕比例下产生奇怪空白
- 或没用 `object-fit: cover`

**修复**：
```html
<!-- 改成标准比例 + 固定高度 -->
<figure class="frame-img" style="height: 26vh">
  <img src="..." style="width:100%;height:100%;object-fit:cover;object-position:top center">
</figure>
```

**预防**：
- 图片永远用标准比例 `16/10` / `4/3` / `3/2` / `1/1`
- 或固定高度 `height: Nvh` + `object-fit: cover`
- 参考 [anti-patterns.md AP-5](./anti-patterns.md)

---

### FM-C-4: WebGL 背景不显示 / 报错

**症状**：
- Magazine 种子的 hero 页没有流动动画
- F12 控制台报 WebGL / canvas 相关错误

**根因**：
- 删改了 `<head>` 里的 `<canvas id="webgl-bg">`
- 或删了对应的 `<script>` 块
- 或本地 WebGL / canvas 相关脚本被删改

**修复**：
- 重新从 `assets/seeds/path-c-magazine-seed.html` 复制 `<head>` 部分
- 不要动 canvas 和 WebGL JS

**预防**：
- 种子的"禁改区"（`<!-- ===== 禁改区 ===== -->` 标记之间）**绝不动**
- 只改内容层 `<main id="deck">`

---

### FM-C-5: 主题切换不生效（light/dark 不切）

**症状**：
- 页面标记了 `<section class="slide dark">` 但背景依然浅色
- 或 hero 页 WebGL 颜色不变

**根因**：
- Magazine 种子依赖 `body.light-bg` / `body.dark-bg` class 的 JS 切换
- 或页面只写了 `hero` 没写 `hero light` / `hero dark`

**修复**：
- 确保每页都有**完整主题标记**：
  ```html
  <section class="slide hero dark">  <!-- ✅ -->
  <section class="slide hero">        <!-- ❌ 缺 light/dark -->
  ```
- 检查种子的主题切换 JS 是否完整

**预防**：
- 参考 [theme-rhythm.md](./theme-rhythm.md)：禁止裸写 `hero`
- 生成前先画节奏表

---

## Path D 失败模式

### FM-D-1: GSAP 动画不触发

**症状**：
- 翻页时没有淡入 / 滑动效果
- F12 控制台报 `gsap is not defined`

**根因**：
- 本地 `assets/vendor/js/gsap.min.js` 没有复制到输出目录
- 或动画 JS 在 `<head>` 执行，此时 DOM 还没渲染

**修复**：
- 检查 Network 面板确认本地 GSAP 文件加载成功
- 从 skill 的 `assets/vendor/` 重新复制到输出目录的 `assets/vendor/`
- 动画 JS 放到 `</body>` 前或包裹 `DOMContentLoaded`

**预防**：
- Path D 必须使用本地 GSAP vendor 资源
- 参考 [animation-guide.md](../integrations/animation-guide.md)

---

### FM-D-2: TTS 音频不播放

**症状**：
- 点击播放按钮无反应
- 或 Network 显示音频 404

**根因**：
- 音频文件路径相对路径错了（如 `audio/s1.mp3` 写成 `/audio/s1.mp3`）
- 或浏览器自动播放策略阻止（需用户交互后播）
- 或音频格式不兼容（某些浏览器不支持 OGG / M4A）

**修复**：
- 检查路径：所有音频用 `audio/xxx.mp3` 相对路径
- 统一改用 MP3 格式
- 播放按钮用 `onclick` 触发（用户交互后浏览器允许）

**预防**：
- 生成前先放 1 个测试音频到 `audio/` 目录，浏览器试播
- 参考 [tts-configuration.md](../integrations/tts-configuration.md)

---

### FM-D-3: 动画与音频不同步

**症状**：
- 音频讲完了动画还在跑
- 或动画完了音频还没到

**根因**：
- 动画 duration 和音频 duration 没对齐
- 或 GSAP timeline 没监听 audio `ended` 事件

**修复**：
```javascript
audio.addEventListener('loadedmetadata', () => {
  gsap.timeline({ duration: audio.duration })
    .to(...)
})
```

**预防**：
- TTS 生成后记录每页音频时长
- 设计动画时对齐时长，不要"凭感觉定 2 秒"

---

## 通用失败模式（跨路径）

### FM-G-1: 项目目录混乱

**症状**：
- `images/` 里的图片命名没规律（`asdf.png` / `1.png` / `final-final.png`）
- 找不到哪张对应哪页

**根因**：
- tasks.json 的 `output_path` 没统一命名规范

**修复**：
- 重命名为 `slide-01-cover.png` / `slide-02-xxx.png`
- 重跑 PPTX 组装

**预防**：
- tasks.json 模板强制要求 `slide-{NN}-{slug}.png` 格式

---

### FM-G-2: 中文字体在终端显示错 / 文件名乱码

**症状**：
- Windows bash 打印 `\346\265\213\350\257\225`
- 或文件名变成 `æµ‹è¯•`

**根因**：
- Windows 系统默认 GBK 编码，bash UTF-8
- 或 cmd / PowerShell 的 chcp 不是 65001

**修复**：
- `chcp 65001` 切到 UTF-8
- 或所有项目名和文件名**只用英文 + 数字**

**预防**：
- Step 0 确认项目名时，建议纯英文（如 `product-launch-2026`）
- 中文内容放幻灯片里，不进路径

---

### FM-G-3: 生成出的内容过于"AI 味"

**症状**：
- 每页都是"1. XX 2. XX 3. XX"三段论
- 标题都是"XXX 的 N 个关键点"
- 空话连篇："通过创新的方法"、"打造卓越的体验"

**根因**：
- 跳过了 Step 0 协作模式或 Step 1 内容澄清
- 没搞清楚受众和论点，Claude 默认"通用商务英语翻译腔"

**修复**：
- 停下重来，先走 Step 0 协作模式，再走 Step 1 的 7 字段需求发现
- 让用户提供 1-2 页"真实想说的话"
- Claude 模仿那个语气重写

**预防**：
- 永远先问受众 / 时长 / 核心论点
- 参考 [anti-patterns.md AP-15](./anti-patterns.md)

---

## 快速诊断流程

遇到问题按以下顺序查：

```
问题发生
  │
  ├─ 是 Path 特定的吗?
  │    ├─ Path A → FM-A-*
  │    ├─ Path B → FM-B-*
  │    ├─ Path C → FM-C-*
  │    └─ Path D → FM-D-*
  │
  ├─ 是跨路径通用的吗?
  │    └─ FM-G-*
  │
  └─ 本清单没覆盖?
       ├─ 先查 quality-checklist.md 的 P0 项
       ├─ 再查 anti-patterns.md 的反模式
       └─ 最后考虑是种子文件 bug（抽样对比原始种子）
```

---

## 预防文化：左移质量

- **左移 1 级**：生成前做预检（class / 尺寸 / prompt 关键词）
- **左移 2 级**：Step 0 协作模式 + Step 1 内容澄清（避免方向错）
- **左移 3 级**：选对路径（从一开始要编辑就选 2A、2A-S 或 2C；唯一来源已经是位图时才选 2B-R，不要默认选 2B）

**失败模式大多数不是 bug，是流程跳步**。按 SKILL.md 的 Step 0-5 走，90% 的失败模式根本不会发生。
