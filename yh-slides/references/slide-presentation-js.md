# SlidePresentation JavaScript 参考手册

## 概述

`SlidePresentation` 是 HTML 幻灯片的导航控制器，负责键盘导航、触摸滑动、进度追踪和动画触发。本文档包含完整的类定义、Intersection Observer 集成和可选增强效果。

---

## 1. SlidePresentation 类

### 1.1 构造函数与初始化

```javascript
class SlidePresentation {
  constructor(options = {}) {
    // 配置项
    this.slideSelector = options.slideSelector || '.slide';
    this.dotSelector = options.dotSelector || '#navDots';
    this.progressBarSelector = options.progressBarSelector || '#progressBar';

    // DOM 元素
    this.slides = document.querySelectorAll(this.slideSelector);
    this.navDotsContainer = document.querySelector(this.dotSelector);
    this.progressBar = document.querySelector(this.progressBarSelector);

    // 状态
    this.currentSlide = 0;
    this.totalSlides = this.slides.length;
    this.isTransitioning = false;
    this.transitionTimeout = null;

    // 触摸状态
    this.touchStartY = 0;
    this.touchStartX = 0;
    this.touchThreshold = 50;

    // 初始化
    this.init();
  }

  init() {
    this.generateNavDots();
    this.setupKeyboardNav();
    this.setupTouchNav();
    this.setupWheelNav();
    this.setupIntersectionObserver();
    this.updateProgress();
    this.updateNavDots();
  }
}
```

### 1.2 键盘导航

支持方向键、空格键、Home/End 键。

```javascript
setupKeyboardNav() {
  document.addEventListener('keydown', (e) => {
    // 防止在输入框中触发
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
      case 'ArrowRight':
      case ' ':
        e.preventDefault();
        this.goToSlide(this.currentSlide + 1);
        break;

      case 'ArrowUp':
      case 'ArrowLeft':
        e.preventDefault();
        this.goToSlide(this.currentSlide - 1);
        break;

      case 'Home':
        e.preventDefault();
        this.goToSlide(0);
        break;

      case 'End':
        e.preventDefault();
        this.goToSlide(this.totalSlides - 1);
        break;

      case 'f':
      case 'F':
        this.toggleFullscreen();
        break;
    }
  });
}
```

### 1.3 触摸/滑动支持

支持垂直和水平滑动切换幻灯片。

```javascript
setupTouchNav() {
  const container = document.documentElement;

  container.addEventListener('touchstart', (e) => {
    this.touchStartY = e.touches[0].clientY;
    this.touchStartX = e.touches[0].clientX;
  }, { passive: true });

  container.addEventListener('touchend', (e) => {
    const touchEndY = e.changedTouches[0].clientY;
    const touchEndX = e.changedTouches[0].clientX;

    const deltaY = this.touchStartY - touchEndY;
    const deltaX = this.touchStartX - touchEndX;

    // 判断主方向：垂直或水平
    if (Math.abs(deltaY) > Math.abs(deltaX)) {
      // 垂直滑动
      if (Math.abs(deltaY) > this.touchThreshold) {
        if (deltaY > 0) {
          this.goToSlide(this.currentSlide + 1);
        } else {
          this.goToSlide(this.currentSlide - 1);
        }
      }
    } else {
      // 水平滑动
      if (Math.abs(deltaX) > this.touchThreshold) {
        if (deltaX > 0) {
          this.goToSlide(this.currentSlide + 1);
        } else {
          this.goToSlide(this.currentSlide - 1);
        }
      }
    }
  }, { passive: true });
}
```

### 1.4 鼠标滚轮导航

带节流的滚轮导航，防止过快翻页。

```javascript
setupWheelNav() {
  let wheelTimeout = null;
  const wheelDelay = 800; // 节流间隔（毫秒）

  document.addEventListener('wheel', (e) => {
    if (wheelTimeout) return;

    wheelTimeout = setTimeout(() => {
      wheelTimeout = null;
    }, wheelDelay);

    if (e.deltaY > 0) {
      this.goToSlide(this.currentSlide + 1);
    } else if (e.deltaY < 0) {
      this.goToSlide(this.currentSlide - 1);
    }
  }, { passive: true });
}
```

### 1.5 幻灯片跳转

核心跳转方法，包含边界检查和防抖。

```javascript
goToSlide(index) {
  // 边界检查
  if (index < 0 || index >= this.totalSlides) return;
  if (index === this.currentSlide) return;
  if (this.isTransitioning) return;

  // 设置过渡锁
  this.isTransitioning = true;
  clearTimeout(this.transitionTimeout);

  this.currentSlide = index;

  // 滚动到目标幻灯片
  const targetSlide = this.slides[index];
  targetSlide.scrollIntoView({ behavior: 'smooth' });

  // 更新 UI
  this.updateProgress();
  this.updateNavDots();
  this.updateAria();

  // 触发入场动画
  this.triggerSlideAnimations(targetSlide);

  // 释放过渡锁
  this.transitionTimeout = setTimeout(() => {
    this.isTransitioning = false;
  }, 600);
}
```

### 1.6 进度条更新

```javascript
updateProgress() {
  if (!this.progressBar) return;

  const progress = ((this.currentSlide + 1) / this.totalSlides) * 100;
  this.progressBar.style.width = `${progress}%`;
}
```

### 1.7 导航圆点生成与管理

```javascript
generateNavDots() {
  if (!this.navDotsContainer) return;

  this.navDotsContainer.innerHTML = '';

  this.slides.forEach((slide, index) => {
    const dot = document.createElement('button');
    dot.classList.add('nav-dot');
    dot.setAttribute('data-slide', index);
    dot.setAttribute('aria-label', `跳转到第 ${index + 1} 页`);

    if (index === this.currentSlide) {
      dot.classList.add('active');
      dot.setAttribute('aria-current', 'true');
    }

    dot.addEventListener('click', () => {
      this.goToSlide(index);
    });

    this.navDotsContainer.appendChild(dot);
  });
}

updateNavDots() {
  if (!this.navDotsContainer) return;

  const dots = this.navDotsContainer.querySelectorAll('.nav-dot');
  dots.forEach((dot, index) => {
    const isActive = index === this.currentSlide;
    dot.classList.toggle('active', isActive);
    dot.setAttribute('aria-current', isActive ? 'true' : 'false');
  });
}
```

### 1.8 ARIA 状态更新

```javascript
updateAria() {
  // 更新进度条 ARIA
  if (this.progressBar) {
    this.progressBar.setAttribute('aria-valuenow', this.currentSlide + 1);
    this.progressBar.setAttribute('aria-valuemin', '1');
    this.progressBar.setAttribute('aria-valuemax', this.totalSlides);
  }

  // 更新幻灯片 ARIA
  this.slides.forEach((slide, index) => {
    slide.setAttribute('aria-label', `第 ${index + 1} 页，共 ${this.totalSlides} 页`);
  });
}
```

### 1.9 全屏切换

```javascript
toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(() => {
      // 全屏请求失败，静默处理
    });
  } else {
    document.exitFullscreen();
  }
}
```

---

## 2. Intersection Observer

使用 Intersection Observer 检测幻灯片进入视口，触发 CSS 动画。

### 2.1 Observer 设置

```javascript
setupIntersectionObserver() {
  const observerOptions = {
    root: null,         // 视口作为 root
    rootMargin: '0px',
    threshold: 0.5      // 50% 可见时触发
  };

  this.observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // 更新当前幻灯片索引
        const slideIndex = Array.from(this.slides).indexOf(entry.target);
        if (slideIndex !== -1 && slideIndex !== this.currentSlide) {
          this.currentSlide = slideIndex;
          this.updateProgress();
          this.updateNavDots();
          this.updateAria();
        }

        // 触发入场动画
        this.triggerSlideAnimations(entry.target);
      }
    });
  }, observerOptions);

  // 观察所有幻灯片
  this.slides.forEach((slide) => {
    this.observer.observe(slide);
  });
}
```

### 2.2 动画触发

```javascript
triggerSlideAnimations(slide) {
  // 查找所有需要动画的元素
  const animatedElements = slide.querySelectorAll(
    '.fade-in, .slide-up, .scale-in, .stagger-1, .stagger-2, .stagger-3, .stagger-4, .stagger-5'
  );

  animatedElements.forEach((el) => {
    el.classList.add('visible');
  });

  // 触发计数动画（如果有）
  const counters = slide.querySelectorAll('[data-target]');
  this.animateCounters(counters);
}
```

---

## 3. 可选增强效果

### 3.1 自定义光标与拖尾效果

```javascript
class CustomCursor {
  constructor() {
    this.cursor = document.createElement('div');
    this.cursor.classList.add('custom-cursor');
    this.trail = [];
    this.trailLength = 8;

    this.init();
  }

  init() {
    // 创建光标元素
    Object.assign(this.cursor.style, {
      position: 'fixed',
      width: '8px',
      height: '8px',
      borderRadius: '50%',
      background: 'var(--color-primary)',
      pointerEvents: 'none',
      zIndex: '9999',
      transition: 'transform 0.1s ease',
      mixBlendMode: 'difference'
    });

    document.body.appendChild(this.cursor);

    // 创建拖尾
    for (let i = 0; i < this.trailLength; i++) {
      const dot = document.createElement('div');
      Object.assign(dot.style, {
        position: 'fixed',
        width: `${4 - i * 0.4}px`,
        height: `${4 - i * 0.4}px`,
        borderRadius: '50%',
        background: 'var(--color-primary)',
        pointerEvents: 'none',
        zIndex: '9998',
        opacity: `${1 - i / this.trailLength}`,
        transition: `transform ${0.1 + i * 0.03}s ease`
      });
      document.body.appendChild(dot);
      this.trail.push({ el: dot, x: 0, y: 0 });
    }

    // 监听鼠标移动
    document.addEventListener('mousemove', (e) => this.onMouseMove(e));

    // 触摸设备隐藏
    if ('ontouchstart' in window) {
      this.cursor.style.display = 'none';
      this.trail.forEach(t => t.el.style.display = 'none');
    }
  }

  onMouseMove(e) {
    this.cursor.style.transform = `translate(${e.clientX - 4}px, ${e.clientY - 4}px)`;

    this.trail.forEach((dot, i) => {
      setTimeout(() => {
        dot.el.style.transform = `translate(${e.clientX - 2}px, ${e.clientY - 2}px)`;
      }, i * 20);
    });
  }
}
```

**CSS 补充**:
```css
@media (hover: hover) {
  body { cursor: none; }
  a, button { cursor: none; }
}
@media (hover: none) {
  .custom-cursor { display: none !important; }
}
```

### 3.2 粒子系统背景 (Canvas)

```javascript
class ParticleSystem {
  constructor(canvasSelector = '#particleCanvas') {
    this.canvas = document.querySelector(canvasSelector);
    if (!this.canvas) return;

    this.ctx = this.canvas.getContext('2d');
    this.particles = [];
    this.particleCount = 60;
    this.connectionDistance = 150;
    this.animationId = null;

    this.init();
  }

  init() {
    this.resize();
    this.createParticles();
    this.animate();

    window.addEventListener('resize', () => this.resize());

    // 页面不可见时暂停
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.stop();
      } else {
        this.animate();
      }
    });
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  createParticles() {
    this.particles = [];
    for (let i = 0; i < this.particleCount; i++) {
      this.particles.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        radius: Math.random() * 2 + 1,
        opacity: Math.random() * 0.5 + 0.2
      });
    }
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // 更新和绘制粒子
    this.particles.forEach((p) => {
      p.x += p.vx;
      p.y += p.vy;

      // 边界反弹
      if (p.x < 0 || p.x > this.canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > this.canvas.height) p.vy *= -1;

      // 绘制粒子
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      this.ctx.fillStyle = `rgba(59, 130, 246, ${p.opacity})`;
      this.ctx.fill();
    });

    // 绘制连接线
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const dx = this.particles[i].x - this.particles[j].x;
        const dy = this.particles[i].y - this.particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < this.connectionDistance) {
          const opacity = 1 - distance / this.connectionDistance;
          this.ctx.beginPath();
          this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
          this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
          this.ctx.strokeStyle = `rgba(59, 130, 246, ${opacity * 0.2})`;
          this.ctx.lineWidth = 0.5;
          this.ctx.stroke();
        }
      }
    }

    this.animationId = requestAnimationFrame(() => this.animate());
  }

  stop() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }
}
```

**HTML 集成**:
```html
<canvas id="particleCanvas" style="position:fixed;inset:0;z-index:0;pointer-events:none;" aria-hidden="true"></canvas>
```

### 3.3 视差效果 (Parallax)

```javascript
class ParallaxEffect {
  constructor() {
    this.elements = [];
    this.init();
  }

  init() {
    // 查找所有视差元素
    document.querySelectorAll('[data-parallax]').forEach((el) => {
      this.elements.push({
        el,
        speed: parseFloat(el.dataset.parallax) || 0.5,
        startY: 0
      });
    });

    if (this.elements.length === 0) return;

    window.addEventListener('scroll', () => this.onScroll(), { passive: true });
  }

  onScroll() {
    const scrollY = window.scrollY;

    this.elements.forEach(({ el, speed }) => {
      const rect = el.getBoundingClientRect();
      const isVisible = rect.top < window.innerHeight && rect.bottom > 0;

      if (isVisible) {
        const offset = (rect.top * speed) * -1;
        el.style.transform = `translateY(${offset}px)`;
      }
    });
  }
}
```

**HTML 用法**:
```html
<div class="slide-bg" data-parallax="0.3" aria-hidden="true">
  <img src="background.jpg" alt="" aria-hidden="true">
</div>
```

### 3.4 3D 倾斜悬停效果

```javascript
class Tilt3D {
  constructor(selector = '[data-tilt]') {
    this.elements = document.querySelectorAll(selector);
    this.init();
  }

  init() {
    // 触摸设备不启用
    if ('ontouchstart' in window) return;

    this.elements.forEach((el) => {
      el.style.transition = 'transform 0.1s ease';
      el.style.transformStyle = 'preserve-3d';

      el.addEventListener('mousemove', (e) => this.onMouseMove(e, el));
      el.addEventListener('mouseleave', (e) => this.onMouseLeave(e, el));
    });
  }

  onMouseMove(e, el) {
    const rect = el.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = ((y - centerY) / centerY) * -10;
    const rotateY = ((x - centerX) / centerX) * 10;

    el.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
  }

  onMouseLeave(e, el) {
    el.style.transition = 'transform 0.5s ease';
    el.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';

    setTimeout(() => {
      el.style.transition = 'transform 0.1s ease';
    }, 500);
  }
}
```

**HTML 用法**:
```html
<div class="data-card" data-tilt>...</div>
```

### 3.5 计数动画

```javascript
// 集成在 SlidePresentation 类中
animateCounters(elements) {
  elements.forEach((el) => {
    const target = parseFloat(el.dataset.target);
    const duration = 2000; // 2 秒
    const startTime = performance.now();
    const isFloat = target % 1 !== 0;

    const animate = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // 缓动函数 (ease-out)
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = target * eased;

      el.textContent = isFloat ? current.toFixed(1) : Math.floor(current);

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        el.textContent = isFloat ? target.toFixed(1) : target;
      }
    };

    requestAnimationFrame(animate);
  });
}
```

### 3.6 交错显示动画 (Staggered Reveal)

```javascript
class StaggerReveal {
  constructor(selector = '[data-stagger]', observer) {
    this.selector = selector;
    this.observer = observer;
    this.init();
  }

  init() {
    document.querySelectorAll(this.selector).forEach((container) => {
      const children = container.children;
      const delay = parseInt(container.dataset.stagger) || 100;

      Array.from(children).forEach((child, index) => {
        child.style.opacity = '0';
        child.style.transform = 'translateY(20px)';
        child.style.transition = `opacity 0.5s ease ${index * delay}ms, transform 0.5s ease ${index * delay}ms`;
      });
    });
  }

  reveal(container) {
    Array.from(container.children).forEach((child) => {
      child.style.opacity = '1';
      child.style.transform = 'translateY(0)';
    });
  }
}
```

**HTML 用法**:
```html
<ul data-stagger="150">
  <li>第一项（延迟 0ms）</li>
  <li>第二项（延迟 150ms）</li>
  <li>第三项（延迟 300ms）</li>
  <li>第四项（延迟 450ms）</li>
</ul>
```

---

## 4. 完整代码示例

以下是包含所有功能的完整 `SlidePresentation` 类，可直接用于单文件 HTML。

```javascript
/**
 * SlidePresentation — HTML 幻灯片导航控制器
 *
 * 功能：
 * - 键盘方向键导航
 * - 触摸滑动支持
 * - 鼠标滚轮导航（带节流）
 * - 进度条实时更新
 * - 导航圆点生成与管理
 * - Intersection Observer 触发入场动画
 * - ARIA 无障碍状态更新
 * - 全屏切换
 * - 计数器动画
 *
 * 用法：
 * const presentation = new SlidePresentation();
 */
class SlidePresentation {
  constructor(options = {}) {
    // --- 配置 ---
    this.slideSelector = options.slideSelector || '.slide';
    this.dotSelector = options.dotSelector || '#navDots';
    this.progressBarSelector = options.progressBarSelector || '#progressBar';
    this.wheelDelay = options.wheelDelay || 800;
    this.touchThreshold = options.touchThreshold || 50;

    // --- DOM ---
    this.slides = document.querySelectorAll(this.slideSelector);
    this.navDotsContainer = document.querySelector(this.dotSelector);
    this.progressBar = document.querySelector(this.progressBarSelector);

    // --- 状态 ---
    this.currentSlide = 0;
    this.totalSlides = this.slides.length;
    this.isTransitioning = false;
    this.transitionTimeout = null;

    // --- 触摸 ---
    this.touchStartY = 0;
    this.touchStartX = 0;

    // --- 初始化 ---
    this.init();
  }

  init() {
    if (this.totalSlides === 0) {
      console.warn('SlidePresentation: 未找到幻灯片元素');
      return;
    }

    this.generateNavDots();
    this.setupKeyboardNav();
    this.setupTouchNav();
    this.setupWheelNav();
    this.setupIntersectionObserver();
    this.updateProgress();
    this.updateNavDots();
    this.updateAria();

    // 首屏动画
    this.triggerSlideAnimations(this.slides[0]);
  }

  // ==================== 导航 ====================

  goToSlide(index) {
    if (index < 0 || index >= this.totalSlides) return;
    if (index === this.currentSlide) return;
    if (this.isTransitioning) return;

    this.isTransitioning = true;
    clearTimeout(this.transitionTimeout);

    this.currentSlide = index;
    const targetSlide = this.slides[index];
    targetSlide.scrollIntoView({ behavior: 'smooth' });

    this.updateProgress();
    this.updateNavDots();
    this.updateAria();
    this.triggerSlideAnimations(targetSlide);

    this.transitionTimeout = setTimeout(() => {
      this.isTransitioning = false;
    }, 600);
  }

  // ==================== 键盘 ====================

  setupKeyboardNav() {
    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      switch (e.key) {
        case 'ArrowDown':
        case 'ArrowRight':
        case ' ':
          e.preventDefault();
          this.goToSlide(this.currentSlide + 1);
          break;
        case 'ArrowUp':
        case 'ArrowLeft':
          e.preventDefault();
          this.goToSlide(this.currentSlide - 1);
          break;
        case 'Home':
          e.preventDefault();
          this.goToSlide(0);
          break;
        case 'End':
          e.preventDefault();
          this.goToSlide(this.totalSlides - 1);
          break;
        case 'f':
        case 'F':
          this.toggleFullscreen();
          break;
      }
    });
  }

  // ==================== 触摸 ====================

  setupTouchNav() {
    document.addEventListener('touchstart', (e) => {
      this.touchStartY = e.touches[0].clientY;
      this.touchStartX = e.touches[0].clientX;
    }, { passive: true });

    document.addEventListener('touchend', (e) => {
      const deltaY = this.touchStartY - e.changedTouches[0].clientY;
      const deltaX = this.touchStartX - e.changedTouches[0].clientX;

      if (Math.abs(deltaY) > Math.abs(deltaX)) {
        if (Math.abs(deltaY) > this.touchThreshold) {
          this.goToSlide(this.currentSlide + (deltaY > 0 ? 1 : -1));
        }
      } else {
        if (Math.abs(deltaX) > this.touchThreshold) {
          this.goToSlide(this.currentSlide + (deltaX > 0 ? 1 : -1));
        }
      }
    }, { passive: true });
  }

  // ==================== 滚轮 ====================

  setupWheelNav() {
    let wheelTimeout = null;

    document.addEventListener('wheel', (e) => {
      if (wheelTimeout) return;

      wheelTimeout = setTimeout(() => {
        wheelTimeout = null;
      }, this.wheelDelay);

      if (e.deltaY > 0) {
        this.goToSlide(this.currentSlide + 1);
      } else if (e.deltaY < 0) {
        this.goToSlide(this.currentSlide - 1);
      }
    }, { passive: true });
  }

  // ==================== 进度条 ====================

  updateProgress() {
    if (!this.progressBar) return;
    const progress = ((this.currentSlide + 1) / this.totalSlides) * 100;
    this.progressBar.style.width = `${progress}%`;
  }

  // ==================== 导航圆点 ====================

  generateNavDots() {
    if (!this.navDotsContainer) return;
    this.navDotsContainer.innerHTML = '';

    this.slides.forEach((_, index) => {
      const dot = document.createElement('button');
      dot.classList.add('nav-dot');
      if (index === this.currentSlide) dot.classList.add('active');
      dot.setAttribute('data-slide', index);
      dot.setAttribute('aria-label', `跳转到第 ${index + 1} 页`);
      if (index === this.currentSlide) dot.setAttribute('aria-current', 'true');

      dot.addEventListener('click', () => this.goToSlide(index));
      this.navDotsContainer.appendChild(dot);
    });
  }

  updateNavDots() {
    if (!this.navDotsContainer) return;
    const dots = this.navDotsContainer.querySelectorAll('.nav-dot');
    dots.forEach((dot, index) => {
      const isActive = index === this.currentSlide;
      dot.classList.toggle('active', isActive);
      dot.setAttribute('aria-current', isActive ? 'true' : 'false');
    });
  }

  // ==================== ARIA ====================

  updateAria() {
    if (this.progressBar) {
      this.progressBar.setAttribute('aria-valuenow', this.currentSlide + 1);
      this.progressBar.setAttribute('aria-valuemin', '1');
      this.progressBar.setAttribute('aria-valuemax', String(this.totalSlides));
    }
    this.slides.forEach((slide, index) => {
      slide.setAttribute('aria-label', `第 ${index + 1} 页，共 ${this.totalSlides} 页`);
    });
  }

  // ==================== Intersection Observer ====================

  setupIntersectionObserver() {
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const index = Array.from(this.slides).indexOf(entry.target);
          if (index !== -1 && index !== this.currentSlide) {
            this.currentSlide = index;
            this.updateProgress();
            this.updateNavDots();
            this.updateAria();
          }
          this.triggerSlideAnimations(entry.target);
        }
      });
    }, {
      root: null,
      rootMargin: '0px',
      threshold: 0.5
    });

    this.slides.forEach((slide) => this.observer.observe(slide));
  }

  // ==================== 动画 ====================

  triggerSlideAnimations(slide) {
    const selectors = [
      '.fade-in', '.slide-up', '.scale-in',
      '.stagger-1', '.stagger-2', '.stagger-3', '.stagger-4', '.stagger-5'
    ];

    slide.querySelectorAll(selectors.join(', ')).forEach((el) => {
      el.classList.add('visible');
    });

    // 计数动画
    const counters = slide.querySelectorAll('[data-target]');
    this.animateCounters(counters);
  }

  animateCounters(elements) {
    elements.forEach((el) => {
      if (el.dataset.animated === 'true') return;
      el.dataset.animated = 'true';

      const target = parseFloat(el.dataset.target);
      const duration = 2000;
      const startTime = performance.now();
      const isFloat = target % 1 !== 0;

      const animate = (currentTime) => {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = target * eased;

        el.textContent = isFloat ? current.toFixed(1) : Math.floor(current);

        if (progress < 1) {
          requestAnimationFrame(animate);
        } else {
          el.textContent = isFloat ? target.toFixed(1) : String(target);
        }
      };

      requestAnimationFrame(animate);
    });
  }

  // ==================== 全屏 ====================

  toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen();
    }
  }
}

// ==================== 初始化 ====================
document.addEventListener('DOMContentLoaded', () => {
  // 初始化导航控制器
  const presentation = new SlidePresentation();

  // 可选：初始化粒子系统
  // const particles = new ParticleSystem('#particleCanvas');

  // 可选：初始化视差效果
  // const parallax = new ParallaxEffect();

  // 可选：初始化 3D 倾斜
  // const tilt = new Tilt3D('[data-tilt]');

  // 可选：初始化自定义光标
  // const cursor = new CustomCursor();
});
```

---

## 5. API 参考

### SlidePresentation 构造函数选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `slideSelector` | string | `'.slide'` | 幻灯片元素选择器 |
| `dotSelector` | string | `'#navDots'` | 导航圆点容器选择器 |
| `progressBarSelector` | string | `'#progressBar'` | 进度条选择器 |
| `wheelDelay` | number | `800` | 滚轮节流间隔（ms） |
| `touchThreshold` | number | `50` | 触摸滑动阈值（px） |

### 公开方法

| 方法 | 参数 | 说明 |
|------|------|------|
| `goToSlide(index)` | `index: number` | 跳转到指定幻灯片 |
| `toggleFullscreen()` | 无 | 切换全屏模式 |
| `updateProgress()` | 无 | 手动更新进度条 |
| `updateNavDots()` | 无 | 手动更新导航圆点状态 |

### 公开属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `currentSlide` | number | 当前幻灯片索引（0-based） |
| `totalSlides` | number | 幻灯片总数 |
| `slides` | NodeList | 所有幻灯片 DOM 元素 |
