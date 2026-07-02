# 翻页动画指南

## 6 种动画类型

### fade - 淡入淡出
最简洁的过渡效果，适合大多数场景。

```css
.slide.fade-enter { opacity: 0; }
.slide.fade-enter-active { opacity: 1; transition: opacity 0.5s ease; }
.slide.fade-exit { opacity: 1; }
.slide.fade-exit-active { opacity: 0; transition: opacity 0.5s ease; }
```

适用场景：简洁内容、文字为主、正式演示

### cinematic - 电影感（缩放+淡入）
带有轻微缩放的淡入效果，增加层次感。

```css
.slide.cinematic-enter { opacity: 0; transform: scale(1.05); }
.slide.cinematic-enter-active {
  opacity: 1; transform: scale(1);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
```

适用场景：复杂内容、视觉冲击力强、TED/Apple 风格

### zoom - 缩放
直接缩放效果，动感十足。

```css
.slide.zoom-enter { opacity: 0; transform: scale(0.8); }
.slide.zoom-enter-active {
  opacity: 1; transform: scale(1);
  transition: opacity 0.4s ease, transform 0.4s ease;
}
```

适用场景：数据展示、强调重点、活泼风格

### slide - 滑动切换
水平滑动，适合时间轴或流程展示。

```css
.slide.slide-enter { transform: translateX(100%); }
.slide.slide-enter-active { transform: translateX(0); transition: transform 0.5s ease; }
.slide.slide-exit { transform: translateX(0); }
.slide.slide-exit-active { transform: translateX(-100%); transition: transform 0.5s ease; }
```

适用场景：时间轴、流程步骤、故事叙述

### flip - 3D 翻转
3D 翻转效果，视觉冲击力强。

```css
.slide.flip-enter { transform: rotateY(-90deg); opacity: 0; }
.slide.flip-enter-active {
  transform: rotateY(0); opacity: 1;
  transition: transform 0.6s ease, opacity 0.6s ease;
}
```

适用场景：对比展示、前后对比、创意演示

### cut - 直接切换
无动画直接切换，最快速。

```css
/* 无过渡效果 */
.slide.cut-enter { opacity: 1; }
```

适用场景：快速演示、技术演示、简洁风格

---

## 动画选择建议

| 内容类型 | 推荐动画 | 原因 |
|---------|---------|------|
| 演讲/故事 | cinematic | 电影感，增强叙事 |
| 数据/图表 | zoom | 强调数据，吸引注意 |
| 时间轴/流程 | slide | 方向感，逻辑清晰 |
| 对比/前后 | flip | 翻转感，对比明显 |
| 简洁/正式 | fade | 低调，不分散注意力 |
| 快速演示 | cut | 最快，无干扰 |

---

## GSAP 动画实现

适用于 Path D（富交互 HTML）。引入 GSAP 库：

```html
<script src="assets/vendor/js/gsap.min.js"></script>
```

### 页面过渡动画

```javascript
// 淡入动画
gsap.fromTo(slide, { opacity: 0 }, { opacity: 1, duration: 0.5 });

// 电影感动画
gsap.fromTo(slide,
  { opacity: 0, scale: 1.05 },
  { opacity: 1, scale: 1, duration: 0.6, ease: "power2.out" }
);

// 滑动动画
gsap.fromTo(slide,
  { x: "100%" },
  { x: "0%", duration: 0.5, ease: "power2.out" }
);

// 缩放动画
gsap.fromTo(slide,
  { opacity: 0, scale: 0.8 },
  { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.7)" }
);
```

### 元素动画

```javascript
// 标题滑入
gsap.fromTo(".heading",
  { x: -50, opacity: 0 },
  { x: 0, opacity: 1, duration: 0.5, delay: 0.2 }
);

// 内容淡入（延迟）
gsap.fromTo(".body-text",
  { opacity: 0, y: 20 },
  { opacity: 1, y: 0, duration: 0.5, delay: 0.4 }
);

// 列表项逐个出现
gsap.fromTo(".list-item",
  { opacity: 0, x: -20 },
  { opacity: 1, x: 0, duration: 0.3, stagger: 0.1, delay: 0.3 }
);

// 数字计数动画
gsap.fromTo(".number",
  { textContent: 0 },
  {
    textContent: 85,
    duration: 1.5,
    ease: "power2.out",
    snap: { textContent: 1 },
    delay: 0.5
  }
);
```

---

## CSS 原生动画（Path C 零依赖使用）

```css
/* 滚动触发动画 */
.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1),
                transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide.visible .reveal {
    opacity: 1;
    transform: translateY(0);
}

/* 交错延迟 */
.reveal:nth-child(1) { transition-delay: 0.1s; }
.reveal:nth-child(2) { transition-delay: 0.2s; }
.reveal:nth-child(3) { transition-delay: 0.3s; }
.reveal:nth-child(4) { transition-delay: 0.4s; }

/* 缩放进入 */
.reveal-scale {
    opacity: 0;
    transform: scale(0.9);
    transition: opacity 0.6s, transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

/* 左侧滑入 */
.reveal-left {
    opacity: 0;
    transform: translateX(-50px);
    transition: opacity 0.6s, transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

/* 模糊进入 */
.reveal-blur {
    opacity: 0;
    filter: blur(10px);
    transition: opacity 0.8s, filter 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
```

---

## 背景动效

```css
/* 渐变网格 */
.gradient-bg {
    background:
        radial-gradient(ellipse at 20% 80%, rgba(120, 0, 255, 0.3) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(0, 255, 200, 0.2) 0%, transparent 50%),
        var(--bg-primary);
}

/* 网格图案 */
.grid-bg {
    background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 50px 50px;
}
```

---

## 无障碍支持

```css
@media (prefers-reduced-motion: reduce) {
  .reveal, .reveal-scale, .reveal-left, .reveal-blur {
    transition: opacity 0.3s ease;
    transform: none;
    filter: none;
  }
}
```

---

## 最佳实践

1. **动画服务叙事** — 动画应该强化内容，而不是分散注意力
2. **保持一致性** — 整个演示文稿使用同一种动画风格
3. **控制时长** — 过渡动画不超过 0.6 秒，元素动画不超过 0.5 秒
4. **避免过度** — 不要在每个元素上都添加动画
5. **考虑无障碍** — 提供减少动画的选项
