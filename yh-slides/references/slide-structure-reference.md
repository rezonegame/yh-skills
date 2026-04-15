# HTML 幻灯片结构参考手册

## 概述

本文档定义了 HTML 幻灯片的完整结构规范，涵盖基础架构、幻灯片类型、导航系统、响应式布局、无障碍性和性能优化。适用于华数幻灯片技能的所有输出路径。

---

## 1. 基础 HTML 结构

### 1.1 单文件架构（Path C — 独立 HTML 文件）

所有 CSS 和 JavaScript 内联在单个 HTML 文件中，便于分享和离线使用。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>演示文稿标题</title>
  <style>
    /* ===== CSS Custom Properties ===== */
    :root {
      /* --- 颜色系统 --- */
      --color-primary: #2563eb;
      --color-secondary: #7c3aed;
      --color-accent: #f59e0b;
      --color-bg: #0f172a;
      --color-surface: #1e293b;
      --color-text: #f1f5f9;
      --color-text-muted: #94a3b8;
      --color-border: #334155;

      /* --- 字体系统 --- */
      --font-heading: 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
      --font-body: 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
      --font-mono: 'Fira Code', 'Consolas', monospace;

      /* --- 字号比例 --- */
      --text-xs: 0.75rem;
      --text-sm: 0.875rem;
      --text-base: 1rem;
      --text-lg: 1.25rem;
      --text-xl: 1.5rem;
      --text-2xl: 2rem;
      --text-3xl: 3rem;
      --text-4xl: 4.5rem;

      /* --- 间距系统 --- */
      --space-xs: 0.25rem;
      --space-sm: 0.5rem;
      --space-md: 1rem;
      --space-lg: 1.5rem;
      --space-xl: 2rem;
      --space-2xl: 3rem;
      --space-3xl: 4rem;

      /* --- 幻灯片尺寸 --- */
      --slide-width: 100vw;
      --slide-height: 100vh;
      --slide-padding: clamp(1.5rem, 5vw, 4rem);

      /* --- 动画 --- */
      --transition-fast: 150ms ease;
      --transition-base: 300ms ease;
      --transition-slow: 500ms ease;
      --transition-page: 600ms cubic-bezier(0.4, 0, 0.2, 1);

      /* --- 圆角与阴影 --- */
      --radius-sm: 4px;
      --radius-md: 8px;
      --radius-lg: 16px;
      --radius-xl: 24px;
      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
      --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
      --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);

      /* --- 层级 --- */
      --z-nav: 100;
      --z-overlay: 200;
      --z-modal: 300;
    }

    /* ===== Reset & Base ===== */
    *, *::before, *::after {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    html {
      scroll-behavior: smooth;
      scroll-snap-type: y mandatory;
      overflow-y: scroll;
      overflow-x: hidden;
    }

    body {
      font-family: var(--font-body);
      font-size: var(--text-base);
      line-height: 1.6;
      color: var(--color-text);
      background: var(--color-bg);
      -webkit-font-smoothing: antialiased;
    }

    /* ===== 幻灯片容器 ===== */
    .slide {
      width: 100vw;
      height: 100vh;
      scroll-snap-align: start;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: var(--slide-padding);
      position: relative;
      overflow: hidden;
    }

    .slide-inner {
      width: 100%;
      max-width: 1200px;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }

    /* ===== 通用组件样式 ===== */
    .slide-number {
      position: absolute;
      bottom: 1rem;
      right: 1.5rem;
      font-size: var(--text-sm);
      color: var(--color-text-muted);
      opacity: 0.6;
    }

    .slide-badge {
      display: inline-block;
      padding: var(--space-xs) var(--space-sm);
      border-radius: var(--radius-sm);
      font-size: var(--text-xs);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      background: var(--color-primary);
      color: white;
    }

    /* ===== 动画基础类 ===== */
    .fade-in {
      opacity: 0;
      transform: translateY(20px);
      transition: opacity 0.6s ease, transform 0.6s ease;
    }
    .fade-in.visible {
      opacity: 1;
      transform: translateY(0);
    }

    .slide-up {
      opacity: 0;
      transform: translateY(40px);
      transition: opacity 0.8s ease, transform 0.8s ease;
    }
    .slide-up.visible {
      opacity: 1;
      transform: translateY(0);
    }

    .scale-in {
      opacity: 0;
      transform: scale(0.9);
      transition: opacity 0.5s ease, transform 0.5s ease;
    }
    .scale-in.visible {
      opacity: 1;
      transform: scale(1);
    }

    .stagger-1 { transition-delay: 0.1s; }
    .stagger-2 { transition-delay: 0.2s; }
    .stagger-3 { transition-delay: 0.3s; }
    .stagger-4 { transition-delay: 0.4s; }
    .stagger-5 { transition-delay: 0.5s; }

    /* ===== 导航组件 ===== */
    .nav-dots {
      position: fixed;
      right: 1.5rem;
      top: 50%;
      transform: translateY(-50%);
      z-index: var(--z-nav);
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .nav-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--color-text-muted);
      border: none;
      cursor: pointer;
      transition: all var(--transition-base);
      opacity: 0.4;
      padding: 0;
    }

    .nav-dot.active {
      opacity: 1;
      background: var(--color-primary);
      transform: scale(1.5);
    }

    .nav-dot:hover {
      opacity: 0.8;
      transform: scale(1.3);
    }

    .progress-bar {
      position: fixed;
      top: 0;
      left: 0;
      height: 3px;
      background: var(--color-primary);
      z-index: var(--z-nav);
      transition: width var(--transition-page);
    }

    /* ===== 响应式断点 ===== */
    /* 平板 */
    @media (max-width: 1024px) {
      :root {
        --text-4xl: 3rem;
        --text-3xl: 2.25rem;
        --text-2xl: 1.5rem;
        --slide-padding: clamp(1.5rem, 4vw, 3rem);
      }
      .nav-dots {
        right: 0.75rem;
      }
    }

    /* 手机 */
    @media (max-width: 768px) {
      :root {
        --text-4xl: 2.25rem;
        --text-3xl: 1.75rem;
        --text-2xl: 1.25rem;
        --text-xl: 1.125rem;
        --slide-padding: 1.25rem;
      }
      .nav-dots {
        display: none;
      }
      .slide-inner {
        max-width: 100%;
      }
      .two-col-layout {
        flex-direction: column !important;
      }
      .two-col-layout > div {
        width: 100% !important;
      }
    }
  </style>
</head>
<body>
  <!-- 进度条 -->
  <div class="progress-bar" id="progressBar"></div>

  <!-- 导航圆点 -->
  <nav class="nav-dots" id="navDots" aria-label="幻灯片导航"></nav>

  <!-- 幻灯片内容 -->
  <section class="slide" id="slide-1">
    <div class="slide-inner">
      <!-- 幻灯片具体内容 -->
    </div>
    <span class="slide-number">1 / 10</span>
  </section>

  <script>
    // JavaScript 逻辑（见 slide-presentation-js.md）
  </script>
</body>
</html>
```

### 1.2 多文件架构（Path D — 项目目录）

适用于需要进一步编辑或部署的场景。

```
slides-project/
├── index.html              # 入口文件，引用外部资源
├── styles/
│   ├── variables.css       # CSS 自定义属性
│   ├── reset.css           # Reset 与基础样式
│   ├── slides.css          # 幻灯片布局样式
│   ├── components.css      # 通用组件样式
│   ├── animations.css      # 动画定义
│   └── responsive.css      # 响应式断点
├── scripts/
│   ├── presentation.js     # SlidePresentation 导航控制器
│   ├── observer.js         # Intersection Observer
│   └── effects.js          # 可选增强效果（粒子、视差等）
├── assets/
│   ├── images/             # 图片资源
│   ├── fonts/              # 自定义字体
│   └── audio/              # TTS 旁白音频（可选）
└── data/
    ├── content.json        # 幻灯片结构化数据（可选）
    └── notes.json          # 演讲者备注
```

**index.html 结构**（多文件版）:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>演示文稿标题</title>
  <link rel="stylesheet" href="styles/variables.css">
  <link rel="stylesheet" href="styles/reset.css">
  <link rel="stylesheet" href="styles/slides.css">
  <link rel="stylesheet" href="styles/components.css">
  <link rel="stylesheet" href="styles/animations.css">
  <link rel="stylesheet" href="styles/responsive.css">
</head>
<body>
  <div class="progress-bar" id="progressBar"></div>
  <nav class="nav-dots" id="navDots" aria-label="幻灯片导航"></nav>

  <!-- 幻灯片 -->

  <script src="scripts/observer.js"></script>
  <script src="scripts/effects.js"></script>
  <script src="scripts/presentation.js"></script>
</body>
</html>
```

### 1.3 CSS Custom Properties 规范

所有设计 Token 必须通过 CSS 自定义属性定义，确保风格系统一致性。

```css
:root {
  /* 颜色：必须包含 primary, secondary, accent, bg, surface, text, text-muted, border */
  /* 字体：必须包含 heading, body, mono */
  /* 字号：使用 rem 单位，基于 1rem = 16px */
  /* 间距：使用 rem 单位，8px 基准网格 */
  /* 动画：fast(150ms), base(300ms), slow(500ms), page(600ms) */
}
```

**风格覆盖示例**（通过修改 Custom Properties 实现换肤）:

```css
/* 暗色商务风格 */
[data-theme="dark-business"] {
  --color-primary: #3b82f6;
  --color-bg: #0f172a;
  --color-surface: #1e293b;
  --color-text: #f1f5f9;
}

/* 明亮简约风格 */
[data-theme="light-minimal"] {
  --color-primary: #1d4ed8;
  --color-bg: #ffffff;
  --color-surface: #f8fafc;
  --color-text: #0f172a;
  --color-text-muted: #64748b;
  --color-border: #e2e8f0;
}
```

### 1.4 幻灯片容器结构

```html
<section class="slide" id="slide-{n}" data-type="{type}" data-theme="{theme}">
  <!-- 背景层：渐变/图片/视频 -->
  <div class="slide-bg" aria-hidden="true">
    <!-- 可选：背景图片 -->
    <!-- 可选：装饰元素 -->
  </div>

  <!-- 内容层 -->
  <div class="slide-inner">
    <!-- 幻灯片类型特定结构 -->
  </div>

  <!-- 页码 -->
  <span class="slide-number">{current} / {total}</span>

  <!-- 演讲者备注（HTML 注释形式） -->
  <!-- Notes: 这里是演讲者备注内容 -->
</section>
```

---

## 2. 十种幻灯片类型

### 2.1 封面 (Cover)

用途：演示文稿首页，展示标题、副标题、作者和日期。

```html
<section class="slide slide-cover" id="slide-1">
  <div class="slide-bg" aria-hidden="true">
    <div class="cover-decoration"></div>
  </div>
  <div class="slide-inner cover-content">
    <span class="slide-badge fade-in">2025 年度报告</span>
    <h1 class="cover-title fade-in stagger-1">演示文稿主标题</h1>
    <p class="cover-subtitle fade-in stagger-2">副标题或简要描述</p>
    <div class="cover-meta fade-in stagger-3">
      <span class="cover-author">演讲者姓名</span>
      <span class="cover-separator">|</span>
      <span class="cover-date">2025 年 1 月</span>
    </div>
  </div>
  <span class="slide-number">1 / 10</span>
</section>
```

**CSS**:
```css
.slide-cover {
  text-align: center;
  background: linear-gradient(135deg, var(--color-bg) 0%, var(--color-surface) 100%);
}

.cover-title {
  font-family: var(--font-heading);
  font-size: var(--text-4xl);
  font-weight: 800;
  line-height: 1.1;
  margin: var(--space-lg) 0;
  letter-spacing: -0.02em;
}

.cover-subtitle {
  font-size: var(--text-xl);
  color: var(--color-text-muted);
  max-width: 600px;
  margin: 0 auto;
}

.cover-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-md);
  margin-top: var(--space-2xl);
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

.cover-separator {
  opacity: 0.3;
}
```

**最佳实践**:
- 标题控制在 2 行以内
- 副标题不超过 1 行
- 使用渐变或装饰元素增强视觉层次
- 封面不需要页码（可选隐藏）

---

### 2.2 标题 + 内容 (Title + Content)

用途：章节过渡页或核心论点展示。

```html
<section class="slide slide-title-content" id="slide-2">
  <div class="slide-inner">
    <span class="slide-badge fade-in">第一章</span>
    <h2 class="slide-title fade-in stagger-1">章节标题</h2>
    <div class="slide-body fade-in stagger-2">
      <p>正文段落。每段聚焦一个核心观点，控制在 3-4 行以内。</p>
      <p>第二段内容，支持强调文本和<strong>加粗关键信息</strong>。</p>
    </div>
    <div class="slide-highlight fade-in stagger-3">
      <blockquote>核心引用或要点总结</blockquote>
    </div>
  </div>
  <span class="slide-number">2 / 10</span>
</section>
```

**CSS**:
```css
.slide-title-content {
  text-align: center;
}

.slide-title {
  font-family: var(--font-heading);
  font-size: var(--text-3xl);
  font-weight: 700;
  margin-bottom: var(--space-xl);
}

.slide-body {
  max-width: 800px;
  margin: 0 auto var(--space-xl);
  font-size: var(--text-lg);
  line-height: 1.8;
  color: var(--color-text-muted);
}

.slide-highlight blockquote {
  font-size: var(--text-xl);
  font-style: italic;
  color: var(--color-accent);
  border-left: 3px solid var(--color-accent);
  padding-left: var(--space-lg);
  max-width: 600px;
  margin: 0 auto;
}
```

**最佳实践**:
- 标题简洁有力，不超过 10 个字
- 正文控制在 100 字以内
- 使用 blockquote 突出核心观点
- 左对齐适合长文本，居中适合短句

---

### 2.3 图文混排 (Image + Text)

用途：产品展示、案例说明、概念解释。

**变体 A — 图左文右**:
```html
<section class="slide slide-image-text layout-image-left" id="slide-3">
  <div class="slide-inner two-col-layout">
    <div class="col-image fade-in">
      <img src="assets/product.jpg" alt="产品图片描述"
           loading="lazy" width="600" height="400">
      <p class="image-caption">图片说明文字</p>
    </div>
    <div class="col-text">
      <h2 class="slide-title fade-in stagger-1">标题</h2>
      <p class="fade-in stagger-2">描述文字，解释图片内容或关联信息。</p>
      <ul class="fade-in stagger-3">
        <li>要点一</li>
        <li>要点二</li>
        <li>要点三</li>
      </ul>
    </div>
  </div>
  <span class="slide-number">3 / 10</span>
</section>
```

**变体 B — 图右文左**（使用 `layout-image-right`）:

```html
<section class="slide slide-image-text layout-image-right">
  <div class="slide-inner two-col-layout">
    <div class="col-text">
      <!-- 文字内容 -->
    </div>
    <div class="col-image">
      <!-- 图片内容 -->
    </div>
  </div>
</section>
```

**变体 C — 图上文下**（使用 `layout-image-top`）:

```html
<section class="slide slide-image-text layout-image-top">
  <div class="slide-inner stack-layout">
    <div class="col-image">
      <img src="..." alt="..." loading="lazy">
    </div>
    <div class="col-text">
      <!-- 文字内容 -->
    </div>
  </div>
</section>
```

**变体 D — 图下文上**（使用 `layout-image-bottom`）:

```html
<section class="slide slide-image-text layout-image-bottom">
  <div class="slide-inner stack-layout">
    <div class="col-text">
      <!-- 文字内容 -->
    </div>
    <div class="col-image">
      <img src="..." alt="..." loading="lazy">
    </div>
  </div>
</section>
```

**CSS**:
```css
.slide-image-text {
  background: var(--color-surface);
}

/* 横向两栏（左图右文 / 右图左文） */
.two-col-layout {
  display: flex;
  align-items: center;
  gap: var(--space-3xl);
}

.two-col-layout .col-image,
.two-col-layout .col-text {
  flex: 1;
  min-width: 0;
}

/* 布局方向控制 */
.layout-image-left .two-col-layout {
  flex-direction: row;
}
.layout-image-right .two-col-layout {
  flex-direction: row-reverse;
}

/* 纵向堆叠（上图下文 / 下图上文） */
.stack-layout {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
  align-items: center;
}

.layout-image-top .stack-layout {
  flex-direction: column;
}
.layout-image-bottom .stack-layout {
  flex-direction: column-reverse;
}

.col-image img {
  width: 100%;
  height: auto;
  max-height: 60vh;
  object-fit: cover;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.image-caption {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  text-align: center;
  margin-top: var(--space-sm);
}
```

**最佳实践**:
- 图片比例保持 3:2 或 16:9
- 文字不超过 80 字
- 列表项不超过 5 个
- 图片 alt 属性必须提供描述

---

### 2.4 全图 (Full Image)

用途：视觉冲击、情感表达、背景展示。

```html
<section class="slide slide-full-image" id="slide-4">
  <div class="slide-bg">
    <img src="assets/hero.jpg" alt="背景图片描述"
         loading="lazy" class="full-image-bg">
  </div>
  <div class="slide-inner full-image-overlay">
    <div class="full-image-content fade-in">
      <h2 class="full-image-title">叠加在图片上的标题</h2>
      <p class="full-image-desc">图片上方的简短说明文字</p>
    </div>
  </div>
  <span class="slide-number">4 / 10</span>
</section>
```

**CSS**:
```css
.slide-full-image {
  padding: 0;
}

.full-image-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}

.full-image-overlay {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-end;
  padding-bottom: 10vh;
}

.full-image-overlay::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.7) 0%,
    rgba(0, 0, 0, 0.2) 50%,
    transparent 100%
  );
}

.full-image-content {
  position: relative;
  color: white;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.full-image-title {
  font-size: var(--text-3xl);
  font-weight: 700;
  margin-bottom: var(--space-md);
}

.full-image-desc {
  font-size: var(--text-lg);
  opacity: 0.9;
}
```

**最佳实践**:
- 叠加文字必须有足够的对比度（渐变遮罩或暗色背景）
- 文字控制在 2 行以内
- 图片使用 `object-fit: cover` 避免变形
- 移动端考虑使用更暗的遮罩

---

### 2.5 引用 (Quote)

用途：名人名言、客户证言、核心理念。

```html
<section class="slide slide-quote" id="slide-5">
  <div class="slide-inner">
    <div class="quote-block fade-in">
      <div class="quote-mark" aria-hidden="true">&ldquo;</div>
      <blockquote class="quote-text">
        这是一段引用文字。可以是名人名言、客户证言或任何需要突出的文字内容。
      </blockquote>
      <div class="quote-author fade-in stagger-1">
        <img src="assets/avatar.jpg" alt="作者头像" class="quote-avatar" loading="lazy">
        <div>
          <cite class="quote-name">作者姓名</cite>
          <span class="quote-role">职位或身份</span>
        </div>
      </div>
    </div>
  </div>
  <span class="slide-number">5 / 10</span>
</section>
```

**CSS**:
```css
.slide-quote {
  text-align: center;
  background: linear-gradient(135deg, var(--color-bg), var(--color-surface));
}

.quote-block {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}

.quote-mark {
  font-size: 8rem;
  line-height: 1;
  color: var(--color-primary);
  opacity: 0.3;
  font-family: Georgia, serif;
  position: absolute;
  top: -3rem;
  left: -1rem;
}

.quote-text {
  font-size: var(--text-2xl);
  font-weight: 300;
  line-height: 1.6;
  font-style: italic;
  margin-bottom: var(--space-2xl);
}

.quote-author {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-md);
}

.quote-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.quote-name {
  display: block;
  font-style: normal;
  font-weight: 600;
  font-size: var(--text-base);
}

.quote-role {
  display: block;
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}
```

**最佳实践**:
- 引用文字控制在 2-3 行
- 引用符号使用装饰性大字号
- 作者信息放在引用下方
- 使用头像增加可信度（可选）

---

### 2.6 数据统计 (Data/Statistics)

用途：关键数据展示、KPI 呈现、对比分析。

```html
<section class="slide slide-data" id="slide-6">
  <div class="slide-inner">
    <h2 class="slide-title fade-in">关键数据</h2>
    <div class="data-grid fade-in stagger-1">
      <div class="data-card">
        <span class="data-value" data-target="98.5">0</span>
        <span class="data-unit">%</span>
        <span class="data-label">客户满意度</span>
      </div>
      <div class="data-card">
        <span class="data-value" data-target="1200">0</span>
        <span class="data-unit">万</span>
        <span class="data-label">年度营收</span>
      </div>
      <div class="data-card">
        <span class="data-value" data-target="350">0</span>
        <span class="data-unit">+</span>
        <span class="data-label">合作伙伴</span>
      </div>
      <div class="data-card">
        <span class="data-value" data-target="47">0</span>
        <span class="data-unit">个</span>
        <span class="data-label">全球市场</span>
      </div>
    </div>
  </div>
  <span class="slide-number">6 / 10</span>
</section>
```

**CSS**:
```css
.slide-data {
  text-align: center;
}

.data-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-xl);
  margin-top: var(--space-2xl);
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

.data-card {
  padding: var(--space-xl);
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  transition: transform var(--transition-base);
}

.data-card:hover {
  transform: translateY(-4px);
}

.data-value {
  font-size: var(--text-4xl);
  font-weight: 800;
  color: var(--color-primary);
  font-variant-numeric: tabular-nums;
}

.data-unit {
  font-size: var(--text-xl);
  color: var(--color-accent);
  margin-left: 2px;
}

.data-label {
  display: block;
  margin-top: var(--space-sm);
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}
```

**最佳实践**:
- 数据指标控制在 2-4 个
- 数值使用 `font-variant-numeric: tabular-nums` 防止跳动
- 搭配计数动画增强效果
- 数据卡片添加 hover 交互

---

### 2.7 列表 (List)

用途：要点罗列、步骤说明、特性展示。

```html
<section class="slide slide-list" id="slide-7">
  <div class="slide-inner">
    <h2 class="slide-title fade-in">核心特性</h2>
    <ul class="feature-list fade-in stagger-1">
      <li class="feature-item">
        <span class="feature-icon" aria-hidden="true">01</span>
        <div class="feature-content">
          <h3 class="feature-name">特性名称</h3>
          <p class="feature-desc">简要描述这个特性的价值和用途。</p>
        </div>
      </li>
      <li class="feature-item">
        <span class="feature-icon" aria-hidden="true">02</span>
        <div class="feature-content">
          <h3 class="feature-name">特性名称</h3>
          <p class="feature-desc">简要描述。</p>
        </div>
      </li>
      <li class="feature-item">
        <span class="feature-icon" aria-hidden="true">03</span>
        <div class="feature-content">
          <h3 class="feature-name">特性名称</h3>
          <p class="feature-desc">简要描述。</p>
        </div>
      </li>
    </ul>
  </div>
  <span class="slide-number">7 / 10</span>
</section>
```

**CSS**:
```css
.slide-list {
  text-align: left;
}

.feature-list {
  list-style: none;
  max-width: 800px;
  margin: var(--space-2xl) auto 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-lg);
  padding: var(--space-lg);
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  transition: border-color var(--transition-base);
}

.feature-item:hover {
  border-color: var(--color-primary);
}

.feature-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary);
  color: white;
  border-radius: var(--radius-md);
  font-weight: 700;
  font-size: var(--text-sm);
}

.feature-name {
  font-size: var(--text-lg);
  font-weight: 600;
  margin-bottom: var(--space-xs);
}

.feature-desc {
  font-size: var(--text-base);
  color: var(--color-text-muted);
  line-height: 1.5;
}
```

**最佳实践**:
- 列表项控制在 3-5 个
- 每项描述控制在 1-2 行
- 使用编号或图标区分各项
- 支持有序列表和无序列表两种变体

---

### 2.8 两栏对比 (Two-Column)

用途：对比分析、优缺点、前后对比。

```html
<section class="slide slide-two-col" id="slide-8">
  <div class="slide-inner">
    <h2 class="slide-title fade-in">方案对比</h2>
    <div class="comparison fade-in stagger-1">
      <div class="comparison-col col-before">
        <h3 class="comparison-heading">传统方案</h3>
        <ul>
          <li>效率低下</li>
          <li>成本高昂</li>
          <li>维护困难</li>
        </ul>
      </div>
      <div class="comparison-divider" aria-hidden="true">
        <span>VS</span>
      </div>
      <div class="comparison-col col-after">
        <h3 class="comparison-heading">新方案</h3>
        <ul>
          <li>高效自动化</li>
          <li>成本降低 60%</li>
          <li>零维护负担</li>
        </ul>
      </div>
    </div>
  </div>
  <span class="slide-number">8 / 10</span>
</section>
```

**CSS**:
```css
.slide-two-col {
  text-align: center;
}

.comparison {
  display: flex;
  align-items: stretch;
  gap: var(--space-xl);
  margin-top: var(--space-2xl);
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.comparison-col {
  flex: 1;
  padding: var(--space-xl);
  border-radius: var(--radius-lg);
  text-align: left;
}

.col-before {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
}

.col-after {
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  color: white;
}

.comparison-divider {
  display: flex;
  align-items: center;
  font-size: var(--text-xl);
  font-weight: 800;
  color: var(--color-text-muted);
}

.comparison-heading {
  font-size: var(--text-xl);
  font-weight: 700;
  margin-bottom: var(--space-lg);
}

.comparison-col ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.comparison-col li {
  padding-left: var(--space-lg);
  position: relative;
}

.comparison-col li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.6em;
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.col-before li::before {
  background: var(--color-text-muted);
}

.col-after li::before {
  background: white;
}
```

**最佳实践**:
- 每栏要点控制在 3-5 个
- 左栏用中性色，右栏用强调色突出优势
- 分隔符使用 "VS" 或箭头

---

### 2.9 表格 (Table)

用途：数据对比、规格展示、日程安排。

```html
<section class="slide slide-table" id="slide-9">
  <div class="slide-inner">
    <h2 class="slide-title fade-in">功能对比</h2>
    <div class="table-wrapper fade-in stagger-1">
      <table class="data-table">
        <thead>
          <tr>
            <th>功能</th>
            <th>基础版</th>
            <th>专业版</th>
            <th>企业版</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>存储空间</td>
            <td>5 GB</td>
            <td>100 GB</td>
            <td>无限</td>
          </tr>
          <tr>
            <td>团队成员</td>
            <td>3 人</td>
            <td>20 人</td>
            <td>无限</td>
          </tr>
          <tr>
            <td>技术支持</td>
            <td>社区</td>
            <td>邮件</td>
            <td>专属客服</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <span class="slide-number">9 / 10</span>
</section>
```

**CSS**:
```css
.slide-table {
  text-align: center;
}

.table-wrapper {
  overflow-x: auto;
  margin-top: var(--space-2xl);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-base);
}

.data-table thead {
  background: var(--color-primary);
  color: white;
}

.data-table th {
  padding: var(--space-md) var(--space-lg);
  text-align: left;
  font-weight: 600;
  white-space: nowrap;
}

.data-table td {
  padding: var(--space-md) var(--space-lg);
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.data-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.03);
}

.data-table tbody tr:last-child td {
  border-bottom: none;
}

/* 高亮推荐列 */
.data-table td.highlight,
.data-table th.highlight {
  background: rgba(59, 130, 246, 0.1);
  font-weight: 600;
}
```

**最佳实践**:
- 列数控制在 3-5 列
- 行数控制在 3-8 行
- 表头使用强调色
- 推荐列使用 highlight 类高亮
- 移动端添加水平滚动

---

### 2.10 结束页 (End)

用途：致谢、Q&A、联系方式。

```html
<section class="slide slide-end" id="slide-10">
  <div class="slide-bg" aria-hidden="true">
    <div class="end-decoration"></div>
  </div>
  <div class="slide-inner end-content">
    <h2 class="end-title fade-in">谢谢聆听</h2>
    <p class="end-subtitle fade-in stagger-1">期待与您交流</p>
    <div class="end-contact fade-in stagger-2">
      <a href="mailto:email@example.com" class="contact-link">email@example.com</a>
      <a href="https://example.com" class="contact-link" target="_blank">example.com</a>
    </div>
    <div class="end-qr fade-in stagger-3">
      <img src="assets/qrcode.png" alt="扫码关注" loading="lazy"
           width="120" height="120">
    </div>
  </div>
</section>
```

**CSS**:
```css
.slide-end {
  text-align: center;
  background: linear-gradient(135deg, var(--color-bg), var(--color-surface));
}

.end-title {
  font-size: var(--text-4xl);
  font-weight: 800;
  margin-bottom: var(--space-md);
}

.end-subtitle {
  font-size: var(--text-xl);
  color: var(--color-text-muted);
  margin-bottom: var(--space-2xl);
}

.end-contact {
  display: flex;
  justify-content: center;
  gap: var(--space-xl);
  margin-bottom: var(--space-2xl);
}

.contact-link {
  color: var(--color-primary);
  text-decoration: none;
  font-size: var(--text-base);
  transition: opacity var(--transition-fast);
}

.contact-link:hover {
  opacity: 0.8;
  text-decoration: underline;
}

.end-qr img {
  border-radius: var(--radius-md);
  background: white;
  padding: var(--space-sm);
}
```

**最佳实践**:
- 提供清晰的联系方式
- 可选添加二维码
- 保持简洁，不要堆砌信息

---

## 3. 导航结构

### 3.1 键盘导航

| 按键 | 功能 |
|------|------|
| `ArrowDown` / `ArrowRight` / `Space` | 下一页 |
| `ArrowUp` / `ArrowLeft` | 上一页 |
| `Home` | 跳转到第一页 |
| `End` | 跳转到最后一页 |
| `F` | 切换全屏 |

### 3.2 Scroll Snap

```css
html {
  scroll-snap-type: y mandatory;
  overflow-y: scroll;
}

.slide {
  scroll-snap-align: start;
}
```

### 3.3 导航圆点 (Nav Dots)

```html
<nav class="nav-dots" id="navDots" aria-label="幻灯片导航">
  <button class="nav-dot active" data-slide="0" aria-label="第 1 页"></button>
  <button class="nav-dot" data-slide="1" aria-label="第 2 页"></button>
  <!-- 动态生成 -->
</nav>
```

### 3.4 进度条

```html
<div class="progress-bar" id="progressBar" style="width: 10%"></div>
```

进度条宽度计算公式:
```
width = ((currentSlide + 1) / totalSlides) * 100 + '%'
```

---

## 4. 响应式布局

### 4.1 断点定义

| 断点 | 宽度 | 适用设备 | 关键调整 |
|------|------|----------|----------|
| Desktop | > 1024px | 桌面显示器 | 完整布局，导航圆点显示 |
| Tablet | 768px - 1024px | 平板 | 缩小字号，调整间距 |
| Mobile | < 768px | 手机 | 单栏布局，隐藏导航圆点 |

### 4.2 关键响应式规则

```css
/* 平板：缩小字号 */
@media (max-width: 1024px) {
  :root {
    --text-4xl: 3rem;
    --text-3xl: 2.25rem;
  }
}

/* 手机：单栏 + 隐藏导航 */
@media (max-width: 768px) {
  :root {
    --text-4xl: 2.25rem;
    --text-3xl: 1.75rem;
    --slide-padding: 1.25rem;
  }
  .nav-dots { display: none; }
  .two-col-layout {
    flex-direction: column !important;
  }
  .comparison {
    flex-direction: column;
  }
  .data-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

---

## 5. 无障碍性

### 5.1 Semantic HTML

```html
<!-- 使用 section 代替 div 作为幻灯片容器 -->
<section class="slide" role="region" aria-roledescription="幻灯片">
  <!-- 标题层级正确 -->
  <h1>封面标题</h1>   <!-- 第一张 -->
  <h2>章节标题</h2>   <!-- 后续幻灯片 -->
</section>
```

### 5.2 ARIA 属性

```html
<!-- 幻灯片容器 -->
<section class="slide"
         role="region"
         aria-roledescription="幻灯片"
         aria-label="第 1 页，共 10 页">

<!-- 导航 -->
<nav class="nav-dots" aria-label="幻灯片导航">
  <button class="nav-dot" aria-label="跳转到第 1 页" aria-current="true"></button>
</nav>

<!-- 进度条 -->
<div class="progress-bar" role="progressbar"
     aria-valuenow="1" aria-valuemin="1" aria-valuemax="10"
     aria-label="演示进度"></div>
```

### 5.3 图片 Alt 文本

```html
<!-- 描述性 alt -->
<img src="chart.png" alt="2024 年季度营收增长趋势图，Q4 达到 350 万">

<!-- 装饰性图片 -->
<img src="decoration.png" alt="" aria-hidden="true">

<!-- 数据图片补充说明 -->
<figure>
  <img src="diagram.png" alt="系统架构图：前端连接 API 网关，后端包含三个微服务">
  <figcaption>图 1：系统架构概览</figcaption>
</figure>
```

---

## 6. 性能优化

### 6.1 图片优化

- 格式选择：优先 WebP，提供 PNG/JPG 回退
- 尺寸：不超过 1200px 宽度，使用 `loading="lazy"`
- 压缩：使用 `quality=80` 的压缩参数
- 响应式图片：使用 `srcset` 提供多尺寸

```html
<img src="photo.webp"
     srcset="photo-480w.webp 480w, photo-800w.webp 800w"
     sizes="(max-width: 768px) 480px, 800px"
     alt="描述"
     loading="lazy"
     width="800" height="600">
```

### 6.2 Lazy Loading

非首屏幻灯片的图片使用懒加载：

```html
<!-- 首屏图片：立即加载 -->
<img src="cover.jpg" alt="封面" fetchpriority="high">

<!-- 后续图片：懒加载 -->
<img src="slide3.jpg" alt="内容" loading="lazy">
```

### 6.3 CSS Variables 优化

- 所有颜色、字号、间距使用 CSS 自定义属性
- 避免重复定义，通过 `:root` 集中管理
- 使用 `clamp()` 实现流式排版，减少媒体查询

```css
/* 流式字号 */
.slide-title {
  font-size: clamp(1.75rem, 4vw, 3rem);
}
```

### 6.4 动画性能

- 仅对 `transform` 和 `opacity` 使用过渡动画
- 避免触发 layout 回流的属性（width, height, top, left）
- 使用 `will-change` 提示浏览器优化（谨慎使用）

```css
/* 好的动画属性 */
.fade-in {
  transition: opacity 0.6s ease, transform 0.6s ease;
}

/* 避免的动画属性 */
.bad-animation {
  transition: width 0.6s ease; /* 触发 layout */
}
```
