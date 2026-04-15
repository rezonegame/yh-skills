# 视口适配规范 (Viewport Fitting Specification)

**状态**: 强制执行 (MANDATORY)
**适用范围**: 所有 yh-slides 生成的演示文稿

---

## 1. 黄金法则

```
每页 = 精确一个视口高度 (100vh / 100dvh)
永远不在页内滚动。
内容超限 → 分页或缩减，禁止滚动。
```

这是一条不可协商的设计原则。每一张幻灯片都必须在打开的瞬间完全展示在屏幕上，用户不需要也不能在单张幻灯片内滚动。

---

## 2. 内容密度限制

为确保每页都能精确适配视口，每张幻灯片的内容量必须严格遵守以下限制：

| 幻灯片类型 | 最大内容量 | 说明 |
|------------|-----------|------|
| **Title slide** | 1 heading + 1 subtitle + 可选 tagline | 封面页保持极简 |
| **Content slide** | 1 heading + 4-6 bullet points（每条最多 2 行） | 或 1 heading + 2 段短文 |
| **Feature grid** | 1 heading + 6 cards（2x3 或 3x2 网格） | 不超过 6 个卡片 |
| **Code slide** | 1 heading + 8-10 lines of code | 代码片段必须精简 |
| **Quote slide** | 1 quote（最多 3 行）+ attribution | 引用页保持呼吸感 |
| **Image slide** | 1 heading + 1 image（最大 60vh） | 图片不能超过视口的 60% |

**内容超出限制时 → 拆分为多张幻灯片，绝不滚动。**

---

## 3. Mandatory CSS

以下 CSS 块**必须**包含在每份演示文稿中。这是视口适配的基础架构。

```css
/* ===========================================
   VIEWPORT FITTING: MANDATORY BASE STYLES
   These styles MUST be included in every presentation.
   They ensure slides fit exactly in the viewport.
   =========================================== */

/* 1. Lock html/body to viewport */
html, body {
    height: 100%;
    overflow-x: hidden;
}

html {
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
}

/* 2. Each slide = exact viewport height */
.slide {
    width: 100vw;
    height: 100vh;
    height: 100dvh; /* Dynamic viewport height for mobile browsers */
    overflow: hidden; /* CRITICAL: Prevent ANY overflow */
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    position: relative;
}

/* 3. Content container with flex for centering */
.slide-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-height: 100%;
    overflow: hidden; /* Double-protection against overflow */
    padding: var(--slide-padding);
}

/* 4. ALL typography uses clamp() for responsive scaling */
:root {
    /* Titles scale from mobile to desktop */
    --title-size: clamp(1.5rem, 5vw, 4rem);
    --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
    --h3-size: clamp(1rem, 2.5vw, 1.75rem);

    /* Body text */
    --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
    --small-size: clamp(0.65rem, 1vw, 0.875rem);

    /* Spacing scales with viewport */
    --slide-padding: clamp(1rem, 4vw, 4rem);
    --content-gap: clamp(0.5rem, 2vw, 2rem);
    --element-gap: clamp(0.25rem, 1vw, 1rem);
}

/* 5. Cards/containers use viewport-relative max sizes */
.card, .container, .content-box {
    max-width: min(90vw, 1000px);
    max-height: min(80vh, 700px);
}

/* 6. Lists auto-scale with viewport */
.feature-list, .bullet-list {
    gap: clamp(0.4rem, 1vh, 1rem);
}

.feature-list li, .bullet-list li {
    font-size: var(--body-size);
    line-height: 1.4;
}

/* 7. Grids adapt to available space */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    gap: clamp(0.5rem, 1.5vw, 1rem);
}

/* 8. Images constrained to viewport */
img, .image-container {
    max-width: 100%;
    max-height: min(50vh, 400px);
    object-fit: contain;
}
```

### CSS 说明

| 编号 | 作用 | 关键点 |
|------|------|--------|
| 1 | 锁定 html/body | `height: 100%` + `overflow-x: hidden` 防止水平滚动 |
| 2 | 幻灯片容器 | `100vh` + `100dvh` 双重声明覆盖所有浏览器；`overflow: hidden` 防止溢出 |
| 3 | 内容容器 | flexbox 居中 + `overflow: hidden` 双重保护 |
| 4 | 响应式排印 | 所有尺寸用 `clamp(min, preferred, max)` 实现视口自适应 |
| 5 | 容器约束 | `max-width` + `max-height` 确保不超出视口 |
| 6 | 列表约束 | 列表项间距和字号随视口缩放 |
| 7 | 自适应网格 | `auto-fit` + `minmax()` 自动适应可用空间 |
| 8 | 图片约束 | `max-height: min(50vh, 400px)` 确保图片不撑破布局 |

---

## 4. Responsive Breakpoints

以下断点**必须**包含在每份演示文稿中，针对不同视口尺寸进行内容缩放：

```css
/* ===========================================
   RESPONSIVE BREAKPOINTS
   Aggressive scaling for smaller viewports
   =========================================== */

/* Short viewports (< 700px height) - 小屏幕笔记本 / 平板横屏 */
@media (max-height: 700px) {
    :root {
        --slide-padding: clamp(0.75rem, 3vw, 2rem);
        --content-gap: clamp(0.4rem, 1.5vw, 1rem);
        --title-size: clamp(1.25rem, 4.5vw, 2.5rem);
        --h2-size: clamp(1rem, 3vw, 1.75rem);
    }
}

/* Very short viewports (< 600px height) - 矮窗口 / 浏览器分屏 */
@media (max-height: 600px) {
    :root {
        --slide-padding: clamp(0.5rem, 2.5vw, 1.5rem);
        --content-gap: clamp(0.3rem, 1vw, 0.75rem);
        --title-size: clamp(1.1rem, 4vw, 2rem);
        --body-size: clamp(0.7rem, 1.2vw, 0.95rem);
    }

    /* Hide non-essential elements to save space */
    .nav-dots, .keyboard-hint, .decorative {
        display: none;
    }
}

/* Extremely short (< 500px height) - 手机横屏 / 开发者工具 */
@media (max-height: 500px) {
    :root {
        --slide-padding: clamp(0.4rem, 2vw, 1rem);
        --title-size: clamp(1rem, 3.5vw, 1.5rem);
        --h2-size: clamp(0.9rem, 2.5vw, 1.25rem);
        --body-size: clamp(0.65rem, 1vw, 0.85rem);
    }
}

/* Narrow viewports (< 600px width) - 手机竖屏 */
@media (max-width: 600px) {
    :root {
        --title-size: clamp(1.25rem, 7vw, 2.5rem);
    }

    /* Stack grids vertically */
    .grid {
        grid-template-columns: 1fr;
    }
}
```

### 断点说明

| 断点 | 目标设备/场景 | 调整内容 |
|------|-------------|----------|
| `max-height: 700px` | 小屏笔记本 (1366x768), 平板横屏 | 缩小 padding, 缩小标题 |
| `max-height: 600px` | 浏览器分屏, 缩小窗口 | 进一步缩小, 隐藏装饰元素 |
| `max-height: 500px` | 手机横屏 (667x375), 开发者 DevTools | 极限压缩, 最小化字号 |
| `max-width: 600px` | 手机竖屏 (375x667) | 网格改为单列, 标题放大 |

---

## 5. Reduced Motion

必须尊重用户的减少动画偏好：

```css
/* ===========================================
   REDUCED MOTION
   Respect user accessibility preferences
   =========================================== */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.2s !important;
    }

    html {
        scroll-behavior: auto;
    }

    /* Remove transform-based reveals, keep only opacity */
    .reveal {
        opacity: 1 !important;
        transform: none !important;
        transition: opacity 0.3s ease !important;
    }
}
```

---

## 6. 溢出预防检查清单

在生成任何演示文稿之前，必须逐项验证以下检查清单：

- [ ] **1. 容器锁定**: 每个 `.slide` 都有 `height: 100vh; height: 100dvh; overflow: hidden;`
- [ ] **2. 字体 clamp**: 所有字号使用 `clamp(min, preferred, max)`，无固定 `px` 或 `rem`
- [ ] **3. 间距 clamp**: 所有间距使用 `clamp()` 或视口单位
- [ ] **4. 容器约束**: 内容容器有 `max-height` 限制
- [ ] **5. 图片约束**: 图片有 `max-height: min(50vh, 400px)` 或类似限制
- [ ] **6. 自适应网格**: 网格使用 `auto-fit` + `minmax()` 实现响应式列数
- [ ] **7. 断点完整**: 包含 700px, 600px, 500px 三个高度断点
- [ ] **8. 无固定高度**: 内容元素没有固定 `px` 高度值
- [ ] **9. 内容密度**: 每页内容不超过密度限制（最多 6 bullets, 最多 6 cards）
- [ ] **10. Reduced motion**: 包含 `prefers-reduced-motion` 媒体查询

---

## 7. 内容超限时的处理策略

### 策略 A: 分页（推荐，优先使用）

当单页内容超出密度限制时，将其拆分为多张幻灯片：

```
# 拆分前（内容过多）
Slide 1: 5 个要点 + 详细说明（每条 4 行）

# 拆分后（分页处理）
Slide 1: 要点 1-3 + 简短描述
Slide 2: 要点 4-5 + 简短描述
```

### 策略 B: 缩减（适用于不可拆分的内容）

当内容不适合拆分时，精简表达：

| 缩减方式 | 示例 |
|----------|------|
| 缩短 bullet | 从 2 行缩减为 1 行 |
| 减少数量 | 从 6 个 bullet 缩减为 4 个 |
| 精简代码 | 从 15 行代码缩减为 8 行关键行 |
| 拆分引用 | 从 5 行缩减为 3 行 |

### 策略 C: "continued" 延续页

对于强关联的内容，使用延续页：

```
Slide 1: "核心优势 (1/2)"
  - 优势 1: ...
  - 优势 2: ...
  - 优势 3: ...

Slide 2: "核心优势 (2/2)"
  - 优势 4: ...
  - 优势 5: ...
  - 优势 6: ...
```

### 绝对禁止的做法

| 禁止操作 | 原因 |
|----------|------|
| 减小字号至不可读 | 字号低于 12px 在投影仪上完全无法辨认 |
| 移除所有 padding/spacing | 内容贴边，视觉压迫感强 |
| 允许页面内滚动 | 违反黄金法则，演示体验断裂 |
| 强行压缩内容 | 文字过小导致观众无法阅读 |

---

## 8. 测试视口尺寸

生成演示文稿后，建议用户在以下视口尺寸中测试：

### Desktop (桌面端)

| 分辨率 | 设备/场景 | 测试重点 |
|--------|----------|---------|
| 1920x1080 | 标准桌面显示器 | 标准效果，留白是否合理 |
| 1440x900 | MacBook Pro 14" | 中等屏幕，字号是否舒适 |
| 1280x720 | 小屏笔记本 / 投影仪 | 最小桌面分辨率，内容是否清晰 |

### Tablet (平板)

| 分辨率 | 设备/场景 | 测试重点 |
|--------|----------|---------|
| 1024x768 | iPad 横屏 | 网格是否自适应 |
| 768x1024 | iPad 竖屏 | 布局是否仍然可用 |

### Mobile (移动端)

| 分辨率 | 设备/场景 | 测试重点 |
|--------|----------|---------|
| 375x667 | iPhone SE / iPhone 8 | 最小手机屏幕，极端情况 |
| 414x896 | iPhone 11 / XR | 标准手机屏幕 |
| 390x844 | iPhone 12/13/14 | 现代 iPhone |

### Landscape Phone (手机横屏)

| 分辨率 | 设备/场景 | 测试重点 |
|--------|----------|---------|
| 667x375 | iPhone SE 横屏 | 极矮视口，最严格的测试 |
| 896x414 | iPhone 11 横屏 | 矮视口测试 |

### 浏览器 DevTools 测试方法

```
1. 打开浏览器 DevTools (F12)
2. 切换到 Device Toolbar (Ctrl+Shift+M)
3. 选择 "Responsive" 模式
4. 手动输入上述尺寸
5. 逐一检查每张幻灯片是否完整显示
6. 特别关注 667x375 (手机横屏) 和 375x667 (手机竖屏)
```

---

## 9. 常见问题排查

### 问题 1: 内容溢出幻灯片

**症状**: 出现滚动条，内容被截断，元素超出视口

**排查步骤**:
1. 检查 `.slide` 是否有 `overflow: hidden`（不是 `auto` 或 `visible`）
2. 减少内容 -- 拆分为多张幻灯片
3. 确保所有字体使用 `clamp()` 而非固定 `px` 或 `rem`
4. 检查是否添加/修复了高度断点（700px, 600px, 500px）
5. 检查图片是否有 `max-height: min(50vh, 400px)`

### 问题 2: 移动端文字太小 / 桌面端文字太大

**症状**: 手机上无法阅读，大屏幕上比例失调

**解决方案**:
```css
/* 使用 clamp 配合视口相对的中间值 */
font-size: clamp(1rem, 3vw, 2.5rem);
/*              ↑       ↑      ↑
            最小值  随视口缩放  最大值 */
```

**调参建议**:
- 文字太小 → 增大 `clamp()` 的中间值系数（如 `3vw` → `4vw`）
- 文字太大 → 减小 `clamp()` 的中间值系数
- 移动端太小 → 增大最小值（如 `1rem` → `1.25rem`）

### 问题 3: 短屏幕上内容不填充

**症状**: 横屏手机或短浏览器窗口中出现大量空白

**解决方案**:
1. 添加 `@media (max-height: 600px)` 和 `(max-height: 500px)` 断点
2. 在短视口断点中减小 padding
3. 隐藏装饰元素（`display: none`）
4. 考虑在短视口中隐藏导航点和键盘提示

### 问题 4: 网格在窄屏幕上挤压

**症状**: 手机竖屏上网格列被压缩到不可用

**解决方案**:
```css
/* 窄屏幕断点中强制单列 */
@media (max-width: 600px) {
    .grid {
        grid-template-columns: 1fr;
    }
}
```

---

## 10. 完整的视口适配 CSS 模板

以下模板可直接复制到任何演示文稿中使用，整合了上述所有规则：

```css
/* ===========================================
   VIEWPORT FITTING: COMPLETE TEMPLATE
   Copy this entire block into every presentation.
   Customize :root variables per style.
   =========================================== */

/* --- Reset & Lock --- */
*, *::before, *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    height: 100%;
    overflow-x: hidden;
}

html {
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
}

/* --- Slide Container --- */
.slide {
    width: 100vw;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    position: relative;
}

/* --- Content Wrapper --- */
.slide-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-height: 100%;
    overflow: hidden;
    padding: var(--slide-padding);
}

/* --- Responsive Variables --- */
:root {
    /* Typography */
    --title-size: clamp(1.5rem, 5vw, 4rem);
    --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
    --h3-size: clamp(1rem, 2.5vw, 1.75rem);
    --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
    --small-size: clamp(0.65rem, 1vw, 0.875rem);

    /* Spacing */
    --slide-padding: clamp(1rem, 4vw, 4rem);
    --content-gap: clamp(0.5rem, 2vw, 2rem);
    --element-gap: clamp(0.25rem, 1vw, 1rem);
}

/* --- Content Constraints --- */
.card, .container, .content-box {
    max-width: min(90vw, 1000px);
    max-height: min(80vh, 700px);
}

.feature-list, .bullet-list {
    gap: clamp(0.4rem, 1vh, 1rem);
}

.feature-list li, .bullet-list li {
    font-size: var(--body-size);
    line-height: 1.4;
}

/* --- Adaptive Grid --- */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    gap: clamp(0.5rem, 1.5vw, 1rem);
}

/* --- Image Constraints --- */
img, .image-container {
    max-width: 100%;
    max-height: min(50vh, 400px);
    object-fit: contain;
}

/* ===========================================
   BREAKPOINTS
   =========================================== */

@media (max-height: 700px) {
    :root {
        --slide-padding: clamp(0.75rem, 3vw, 2rem);
        --content-gap: clamp(0.4rem, 1.5vw, 1rem);
        --title-size: clamp(1.25rem, 4.5vw, 2.5rem);
        --h2-size: clamp(1rem, 3vw, 1.75rem);
    }
}

@media (max-height: 600px) {
    :root {
        --slide-padding: clamp(0.5rem, 2.5vw, 1.5rem);
        --content-gap: clamp(0.3rem, 1vw, 0.75rem);
        --title-size: clamp(1.1rem, 4vw, 2rem);
        --body-size: clamp(0.7rem, 1.2vw, 0.95rem);
    }

    .nav-dots, .keyboard-hint, .decorative {
        display: none;
    }
}

@media (max-height: 500px) {
    :root {
        --slide-padding: clamp(0.4rem, 2vw, 1rem);
        --title-size: clamp(1rem, 3.5vw, 1.5rem);
        --h2-size: clamp(0.9rem, 2.5vw, 1.25rem);
        --body-size: clamp(0.65rem, 1vw, 0.85rem);
    }
}

@media (max-width: 600px) {
    :root {
        --title-size: clamp(1.25rem, 7vw, 2.5rem);
    }

    .grid {
        grid-template-columns: 1fr;
    }
}

/* ===========================================
   REDUCED MOTION
   =========================================== */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.2s !important;
    }

    html {
        scroll-behavior: auto;
    }

    .reveal {
        opacity: 1 !important;
        transform: none !important;
        transition: opacity 0.3s ease !important;
    }
}
```

> 使用时，将风格特定的 CSS 变量（颜色、字体等）添加到 `:root` 中，覆盖模板的默认值即可。
