# Web 视觉风格画廊 (Web Styles Gallery)

统一收录自 frontend-slides (12 styles) 和 html-ppt-designer (17 styles)，去重合并为 27 种独立风格。

---

## 深色主题 (Dark Themes)

---

### 1. Bold Signal

**气质**: Confident, high-impact, bold, modern

**布局**: 彩色卡片浮于深色渐变背景。序号左上角，导航右上角，标题左下角。

**Font Pairing:**
- Display: `Archivo Black` (900)
- Body: `Space Grotesk` (400/500)

**Color Palette:**
```css
:root {
    --bg-primary: #1a1a1a;
    --bg-gradient: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
    --card-bg: #FF5722;
    --text-primary: #ffffff;
    --text-on-card: #1a1a1a;
    --text-secondary: #999999;
}
```

**Signature Elements:**
- 大面积彩色卡片作为视觉焦点（橙色/珊瑚色/活力强调色）
- 大号章节序号（01, 02...）
- 导航面包屑，带 active/inactive 透明度切换
- 网格布局实现精准对齐

**Best Use Cases:** Pitch decks, keynotes, 高影响力品牌展示

---

### 2. Electric Studio

**气质**: Bold, clean, professional, high contrast

**布局**: 分屏设计 -- 白色上半区 + 蓝色下半区。品牌标识分布在角落。

**Font Pairing:**
- Display: `Manrope` (800)
- Body: `Manrope` (400/500)

**Color Palette:**
```css
:root {
    --bg-dark: #0a0a0a;
    --bg-white: #ffffff;
    --accent-blue: #4361ee;
    --text-dark: #0a0a0a;
    --text-light: #ffffff;
}
```

**Signature Elements:**
- 双面板垂直分割
- 面板边缘的强调色条
- 引用排版作为视觉英雄元素
- 极简自信的留白节奏

**Best Use Cases:** Agency 演示、品牌提案、专业报告

---

### 3. Creative Voltage

**气质**: Bold, creative, energetic, retro-modern

**布局**: 分屏面板 -- 电光蓝左区 + 深色右区。Script 字体做点缀。

**Font Pairing:**
- Display: `Syne` (700/800)
- Mono: `Space Mono` (400/700)

**Color Palette:**
```css
:root {
    --bg-primary: #0066ff;
    --bg-dark: #1a1a2e;
    --accent-neon: #d4ff00;
    --text-light: #ffffff;
    --text-secondary: #cccccc;
}
```

**Signature Elements:**
- 电光蓝 + 霓虹黄高对比组合
- 半调纹理 (Halftone) 图案
- 霓虹徽章/标注
- Script 字体增添创意气质

**Best Use Cases:** Creative pitches, 创意提案, 艺术方向展示

---

### 4. Dark Botanical

**气质**: Elegant, sophisticated, artistic, premium

**布局**: 居中内容在深色背景上。角落有抽象柔和形状做装饰。

**Font Pairing:**
- Display: `Cormorant` (400/600) -- 优雅衬线体
- Body: `IBM Plex Sans` (300/400)

**Color Palette:**
```css
:root {
    --bg-primary: #0f0f0f;
    --text-primary: #e8e4df;
    --text-secondary: #9a9590;
    --accent-warm: #d4a574;
    --accent-pink: #e8b4b8;
    --accent-gold: #c9b896;
}
```

**Signature Elements:**
- 抽象柔和渐变圆（模糊叠加效果）
- 暖色系点缀（粉、金、赤陶色）
- 细垂直强调线
- 斜体签名式排版
- 仅使用抽象 CSS 形状，不使用插图

**Best Use Cases:** 高端品牌, 奢侈品, 艺术画廊, 生活方式品牌

---

### 5. Neon Cyber / Neo-Tokyo (合并风格)

**气质**: Futuristic, cyberpunk, neon, techy, confident

> 合并自 frontend-slides 的 "Neon Cyber" 和 html-ppt-designer 的 "Neo-Tokyo"，结合两者的赛博朋克美学。

**布局**: 深色全屏背景，粒子/网格图案层，霓虹光效元素。

**Font Pairing:**
- Display: `Clash Display` (Fontshare) 或 `Syne` (800) (Google Fonts fallback)
- Body: `Satoshi` (Fontshare) 或 `Space Grotesk` (Google Fonts fallback)

**Color Palette:**
```css
:root {
    --bg-primary: #0a0f1c;
    --bg-secondary: #111827;
    --neon-cyan: #00ffcc;
    --neon-magenta: #ff00aa;
    --neon-pink: #ff4488;
    --neon-purple: #aa44ff;
    --text-primary: #ffffff;
    --text-secondary: #9ca3af;
    --glow-cyan: rgba(0, 255, 204, 0.3);
    --glow-magenta: rgba(255, 0, 170, 0.3);
}
```

**Signature Elements:**
- 粒子背景系统 (canvas 或 CSS)
- 霓虹发光效果 (box-shadow + text-shadow)
- 网格线图案叠加
- 赛博朋克色彩组合（青色 + 品红 + 紫色）
- 高对比度深色界面
- 扫描线或故障效果 (可选)

**Best Use Cases:** 科技创业公司, 游戏展示, 未来主题, 技术大会

---

### 6. Terminal Green

**气质**: Developer-focused, hacker aesthetic, technical

**布局**: 终端/命令行界面风格。扫描线纹理，等宽字体为主。

**Font Pairing:**
- Display + Body: `JetBrains Mono` (400/700) -- 全程等宽字体

**Color Palette:**
```css
:root {
    --bg-primary: #0d1117;       /* GitHub Dark */
    --bg-secondary: #161b22;
    --terminal-green: #39d353;
    --text-primary: #c9d1d9;
    --text-secondary: #8b949e;
    --accent-bright: #58a6ff;
    --border-color: #30363d;
    --cursor-blink: #39d353;
}
```

**Signature Elements:**
- 扫描线纹理背景 (CSS repeating-linear-gradient)
- 闪烁光标动画
- 代码语法高亮风格排版
- 终端提示符 ($, >) 装饰元素
- 等宽字体全场景使用
- 命令行风格进度指示

**Best Use Cases:** 开发者工具, API 文档, 技术教程, DevRel 演示

---

### 7. Dark Mode

**气质**: 深色模式, modern, professional, 护眼

**布局**: 暗色全屏，干净排版，高对比度文字。

**Font Pairing:**
- Display: `Inter` (700/800) 或 `Plus Jakarta Sans` (800)
- Body: `Inter` (400/500) 或 `Plus Jakarta Sans` (400)

**Color Palette:**
```css
:root {
    --bg-primary: #1a1a2e;
    --bg-secondary: #16213e;
    --bg-surface: #0f3460;
    --text-primary: #e0e0e0;
    --text-secondary: #a0a0a0;
    --accent: #e94560;
    --border: #2a2a4a;
}
```

**Signature Elements:**
- 多层次深色背景（深蓝到深紫渐变）
- 表面层 (surface) 创造视觉层次
- 强调色用于焦点元素
- 护眼友好高对比度
- 无装饰的干净界面

**Best Use Cases:** 科技产品, 开发者演示, 现代品牌, 日常专业演示

---

## 浅色主题 (Light Themes)

---

### 8. Notebook Tabs

**气质**: Editorial, organized, elegant, tactile

**布局**: 奶油色纸张卡片浮于深色背景。右侧边缘彩色标签页。

**Font Pairing:**
- Display: `Bodoni Moda` (400/700) -- 经典编辑风格
- Body: `DM Sans` (400/500)

**Color Palette:**
```css
:root {
    --bg-outer: #2d2d2d;
    --bg-page: #f8f6f1;
    --text-primary: #1a1a1a;
    --text-secondary: #555555;
    --tab-mint: #98d4bb;
    --tab-lavender: #c7b8ea;
    --tab-pink: #f4b8c5;
    --tab-sky: #a8d8ea;
    --tab-cream: #ffe6a7;
}
```

**Signature Elements:**
- 纸张容器带微妙阴影
- 右侧彩色章节标签页（竖排文字）
- 左侧活页孔装饰
- 标签文字随视口缩放: `font-size: clamp(0.5rem, 1vh, 0.7rem)`

**Best Use Cases:** 报告, 综述, 教育内容, 有条理的信息展示

---

### 9. Pastel Geometry

**气质**: Friendly, approachable, modern, organized

**布局**: 白色卡片浮于柔和彩色背景。右侧边缘竖排装饰药丸。

**Font Pairing:**
- Display + Body: `Plus Jakarta Sans` (400/800)

**Color Palette:**
```css
:root {
    --bg-primary: #c8d9e6;
    --card-bg: #faf9f7;
    --pill-pink: #f0b4d4;
    --pill-mint: #a8d4c4;
    --pill-sage: #5a7c6a;
    --pill-lavender: #9b8dc4;
    --pill-violet: #7c6aad;
    --text-primary: #1a1a1a;
    --text-secondary: #555555;
}
```

**Signature Elements:**
- 圆角卡片配柔和阴影
- 右侧边缘竖排药丸（不同高度，类似标签页）
- 统一药丸宽度，高度递变：短 -> 中 -> 长 -> 中 -> 短
- 角落的下载/操作图标

**Best Use Cases:** 产品概述, 教程, 友好型品牌展示

---

### 10. Split Pastel

**气质**: Playful, modern, friendly, creative

**布局**: 双色垂直分割（蜜桃色左区 + 薰衣草色右区）。

**Font Pairing:**
- Display + Body: `Outfit` (400/800)

**Color Palette:**
```css
:root {
    --bg-peach: #f5e6dc;
    --bg-lavender: #e4dff0;
    --text-dark: #1a1a1a;
    --badge-mint: #c8f0d8;
    --badge-yellow: #f0f0c8;
    --badge-pink: #f0d4e0;
}
```

**Signature Elements:**
- 分割背景色块
- 活泼的徽章药丸配图标
- 右侧面板的网格图案叠加
- 圆角 CTA 按钮

**Best Use Cases:** 创意 agency, 年轻品牌, 活动推广, 社交媒体展示

---

### 11. Vintage Editorial

**气质**: Witty, confident, editorial, personality-driven

**布局**: 居中内容在奶油色背景上。抽象几何形状做点缀。

**Font Pairing:**
- Display: `Fraunces` (700/900) -- 独特衬线体
- Body: `Work Sans` (400/500)

**Color Palette:**
```css
:root {
    --bg-cream: #f5f3ee;
    --text-primary: #1a1a1a;
    --text-secondary: #555555;
    --accent-warm: #e8d4c0;
    --accent-terracotta: #c47a5a;
    --accent-olive: #6b7c5e;
}
```

**Signature Elements:**
- 抽象几何形状（圆圈轮廓 + 直线 + 圆点）
- 粗边框 CTA 框
- 诙谐、对话式文案风格
- 仅使用几何 CSS 形状，不使用插图

**Best Use Cases:** 个人品牌, 博客展示, 编辑风格内容, 故事叙述

---

### 12. Swiss Modern / Swiss (合并风格)

**气质**: Clean, precise, geometric, Bauhaus-inspired, minimal

> 合并自 frontend-slides 的 "Swiss Modern" 和 html-ppt-designer 的 "Swiss"，融合严格网格与极简美学。

**布局:** 严格网格系统，不对称构图，精确对齐。

**Font Pairing:**
- Display: `Archivo` (800) 或 `Helvetica Neue` (900)
- Body: `Nunito` (400) 或 `Helvetica Neue` (400)

**Color Palette:**
```css
:root {
    --bg-primary: #ffffff;
    --bg-dark: #000000;
    --text-primary: #000000;
    --text-secondary: #444444;
    --accent-red: #ff3300;
    --accent-blue: #0055ff;
    --grid-line: rgba(0, 0, 0, 0.06);
    --border-thick: #000000;
}
```

**Signature Elements:**
- 可见网格线（装饰性参考线）
- 不对称布局（左对齐标题，右对齐内容）
- 几何色块作为视觉焦点
- 无衬线字体，精确字距
- 红/蓝/黑/白配色体系
- 粗线条分隔符
- 严格网格间距

**Best Use Cases:** 企业展示, 数据可视化, 建筑设计, 专业报告

---

### 13. Paper & Ink

**气质**: Editorial, literary, thoughtful, elegant

**布局**: 温暖奶油色背景，大量留白，经典排版。

**Font Pairing:**
- Display: `Cormorant Garamond` (400/600) -- 优雅经典衬线
- Body: `Source Serif 4` (400) 或 `IBM Plex Serif` (400)

**Color Palette:**
```css
:root {
    --bg-primary: #faf9f7;
    --bg-warm: #f5f0eb;
    --text-primary: #1a1a1a;
    --text-secondary: #555555;
    --accent-crimson: #c41e3a;
    --accent-gold: #b8860b;
    --rule-color: #cccccc;
}
```

**Signature Elements:**
- Drop caps（首字母放大下沉）
- Pull quotes（引用突出排版）
- 优雅的水平分割线
- 传统印刷排版节奏
- 克制的颜色使用（主要黑白 + 一处强调色）

**Best Use Cases:** 故事叙述, 文学展示, 品牌故事, 高端编辑内容

---

## 经典专业 (Classic Professional)

---

### 14. TED

**气质**: TED 演讲风格, impactful, visual storytelling

**布局:** 黑色背景，超大图片占据大部分空间，简洁有力的标题。

**Font Pairing:**
- Display: `Montserrat` (700/900) 或 `Helvetica Neue` (700)
- Body: `Open Sans` (400) 或 `Helvetica Neue` (400)

**Color Palette:**
```css
:root {
    --bg-primary: #000000;
    --bg-secondary: #111111;
    --text-primary: #ffffff;
    --text-secondary: #cccccc;
    --accent-red: #E31C23;
    --accent-red-hover: #ff1a1a;
}
```

**Signature Elements:**
- 极少文字，大图为主
- TED 红强调色 (#E31C23)
- 超大标题居中或底部
- 黑色背景，极致对比
- 全屏图片（50-70vh）
- 一句话说明，不超过两行

**Best Use Cases:** 演讲和演示, 故事叙述, 视觉冲击力强的内容, 灵感演讲

---

### 15. Apple Keynote

**气质**: 极简留白, super large titles, premium

**布局:** 极致留白，超大标题居中，产品/内容大图，一句话说明。

**Font Pairing:**
- Display: `-apple-system, BlinkMacSystemFont, 'SF Pro Display'` (700/800)
- Body: `-apple-system, BlinkMacSystemFont, 'SF Pro Text'` (400)

**Color Palette:**
```css
:root {
    --bg-primary: #ffffff;
    --bg-light: #f5f5f7;
    --text-primary: #1d1d1f;
    --text-secondary: #6e6e73;
    --accent-blue: #0071e3;
    --accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

**Signature Elements:**
- 超大标题（4-5rem, clamp 响应式）
- 极致留白（padding: clamp(3rem, 10vw, 8rem)）
- 产品大图居中展示
- 浅色纯净背景
- 无衬线系统字体
- 一句话说明，居中对齐
- 渐变色用于视觉点缀（非背景）

**Best Use Cases:** 产品发布, 创意展示, 高端品牌, 科技发布会

---

### 16. Typical

**气质**: 典型PPT风格, standard, familiar, business-ready

**布局:** 标题在上，内容列表在下，标准 PPT 布局。

**Font Pairing:**
- Display: `Calibri` (700) 或 `Segoe UI` (700)
- Body: `Calibri` (400) 或 `Segoe UI` (400)

**Color Palette:**
```css
:root {
    --bg-primary: #ffffff;
    --bg-accent: #f0f4f8;
    --text-primary: #333333;
    --text-secondary: #666666;
    --primary-blue: #2b5797;
    --accent-blue: #0078d4;
    --border: #dee2e6;
}
```

**Signature Elements:**
- 标准标题栏 + 内容区域
- 项目符号清晰有序
- 蓝色主题色系
- 标准页眉页脚
- 中等文字密度
- 表格和图表友好

**Best Use Cases:** 商务汇报, 教学演示, 标准化报告, 企业内部沟通

---

### 17. Gamma Modern

**气质**: 现代卡片, gradient, dynamic, youthful

**布局:** 现代卡片设计，渐变背景，动态布局，圆角元素。

**Font Pairing:**
- Display: `Plus Jakarta Sans` (800) 或 `Outfit` (800)
- Body: `Plus Jakarta Sans` (400) 或 `Inter` (400)

**Color Palette:**
```css
:root {
    --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --card-bg: rgba(255, 255, 255, 0.15);
    --card-bg-solid: #ffffff;
    --text-primary: #ffffff;
    --text-on-card: #333333;
    --accent: #00d2ff;
    --shadow: rgba(0, 0, 0, 0.1);
}
```

**Signature Elements:**
- 现代卡片设计（圆角 + 毛玻璃效果）
- 渐变背景（紫色到蓝色系）
- 圆角元素 (border-radius: 16px-24px)
- 柔和阴影
- 彩色主题，充满活力
- 动态布局，不对称网格

**Best Use Cases:** 现代创意展示, 年轻品牌, 动态内容, 社交/活动推广

---

### 18. Consulting

**气质**: 咨询风格, data-heavy, structured, professional

**布局:** 文字密度高，表格和图表，结构化多栏布局。

**Font Pairing:**
- Display: `Georgia` (700) 或 `Playfair Display` (700)
- Body: `Arial` (400) 或 `Source Sans 3` (400)

**Color Palette:**
```css
:root {
    --bg-primary: #ffffff;
    --bg-header: #1b2a4a;
    --text-primary: #333333;
    --text-header: #ffffff;
    --text-secondary: #666666;
    --accent-navy: #1b2a4a;
    --accent-teal: #00838f;
    --accent-gold: #c6930a;
    --border: #dee2e6;
    --table-stripe: #f8f9fa;
}
```

**Signature Elements:**
- 高文字密度布局
- 专业表格和数据可视化
- 多栏信息架构（2-3 栏）
- 页眉品牌色条
- 结构化标题层级
- 数据图表（柱状图、饼图、折线图）
- 页脚页码 + 公司标识

**Best Use Cases:** 商业咨询, 数据分析报告, 研究报告, 战略提案

---

## 编辑出版 (Editorial)

---

### 19. Editorial Magazine

**气质**: 杂志排版, high-quality, visual storytelling

**布局:** 杂志风格排版，图文混排，多栏布局，大标题。

**Font Pairing:**
- Display: `Playfair Display` (700/900) 或 `Bodoni Moda` (700)
- Body: `Source Sans 3` (400) 或 `Lora` (400)

**Color Palette:**
```css
:root {
    --bg-primary: #ffffff;
    --bg-feature: #f8f6f1;
    --text-primary: #1a1a1a;
    --text-secondary: #555555;
    --accent: #e63946;
    --accent-secondary: #457b9d;
    --rule-color: #cccccc;
}
```

**Signature Elements:**
- 杂志式大标题（特大字号 + 粗体）
- 图文混排（文字环绕图片）
- 多栏布局（2-3 栏内容区）
- Pull quotes 和 callout 框
- 精美排版节奏
- 高质感色彩搭配
- 章节分隔设计

**Best Use Cases:** 杂志风格展示, 内容编辑, 视觉故事, 品牌期刊

---

### 20. Newspaper

**气质:** 报纸风格, multi-column, dense, journalistic

**布局:** 多栏排版，清晰标题层级，紧凑布局，黑白配色。

**Font Pairing:**
- Display: `Merriweather` (700/900) 或 `Georgia` (700)
- Body: `Source Serif 4` (400) 或 `Georgia` (400)

**Color Palette:**
```css
:root {
    --bg-primary: #f5f5f0;
    --text-primary: #1a1a1a;
    --text-secondary: #444444;
    --text-light: #777777;
    --rule-thick: #1a1a1a;
    --rule-thin: #cccccc;
    --accent: #8b0000;
}
```

**Signature Elements:**
- 多栏排版（3-4 栏）
- 清晰的标题层级（H1 > H2 > H3）
- 新闻感十足的紧凑布局
- 黑白为主，少量强调色
- 粗细线条分隔
- 日期线/来源标注
- 高易读性（充足行高和段落间距）

**Best Use Cases:** 新闻发布, 报告总结, 信息密集内容, 年报/简报

---

## 设计艺术 (Design & Art)

---

### 21. Bauhaus Web

**气质**: 几何图形, primary colors, 艺术感, bold

**布局:** 大胆构图，几何色块分割，原色组合。

**Font Pairing:**
- Display: `Archivo Black` (900) 或 `Bebas Neue` (400)
- Body: `Archivo` (400) 或 `Montserrat` (400)

**Color Palette:**
```css
:root {
    --bg-primary: #f5f0eb;
    --color-red: #e63946;
    --color-blue: #1d3557;
    --color-yellow: #f4d35e;
    --color-black: #1a1a1a;
    --color-white: #ffffff;
    --text-primary: #1a1a1a;
}
```

**Signature Elements:**
- 三原色色块（红、黄、蓝）+ 黑白
- 几何图形（圆、三角、方块）
- 大胆不对称构图
- 高对比度
- 现代艺术感
- 无衬线字体
- 粗线条和硬边缘

**Best Use Cases:** 艺术展示, 创意设计, 历史回顾, 设计教育

---

### 22. Kinfolk

**气质**: 自然色调, warm, organic, 生活方式

**布局:** 大量留白，温暖自然色调，有机形状装饰。

**Font Pairing:**
- Display: `Cormorant Garamond` (400/600)
- Body: `Nunito Sans` (300/400) 或 `Source Sans 3` (300)

**Color Palette:**
```css
:root {
    --bg-primary: #f8f5f0;
    --bg-warm: #f0ebe4;
    --text-primary: #3d3229;
    --text-secondary: #7a6e5d;
    --accent-terracotta: #c47a5a;
    --accent-sage: #7a8b6f;
    --accent-sand: #d4c4a8;
    --accent-cream: #e8ddd0;
}
```

**Signature Elements:**
- 自然色调（米色、棕色、绿色系）
- 大量留白（类似日式美学）
- 温暖舒适感
- 有机形状和自然纹理
- 淡雅的色彩过渡
- 手写体签名式装饰（可选）
- 纸张质感背景

**Best Use Cases:** 生活方式, 自然主题, 温暖品牌, 健康/食品/家居

---

### 23. MUJI

**气质**: 无印良品极简, functional, 日式美学, restraint

**布局:** 极致极简，中性色调，功能至上，无装饰。

**Font Pairing:**
- Display: `Noto Sans JP` (300/500) 或 `Helvetica Neue` (300)
- Body: `Noto Sans JP` (300) 或 `Helvetica Neue` (300)

**Color Palette:**
```css
:root {
    --bg-primary: #f5f5f0;
    --bg-secondary: #ececea;
    --text-primary: #333333;
    --text-secondary: #888888;
    --accent-brown: #8b7355;
    --accent-kraft: #c4a882;
    --line: #cccccc;
}
```

**Signature Elements:**
- 极简设计（零装饰）
- 中性色（白、灰、黑、米色）
- 功能性驱动布局
- 清晰易读的信息层级
- 超细字重（font-weight: 200-300）
- 棕色/米色强调（接近自然纤维色）
- 日式留白美学
- 无阴影，无渐变，无特效

**Best Use Cases:** 极简主义, 日式品牌, 功能性展示, 生活美学

---

### 24. Brutalist Web

**气质:** 粗野主义, thick borders, high contrast, raw

**布局:** 大胆排版，粗边框，不规则形状，高对比度。

**Font Pairing:**
- Display: `Space Mono` (700) 或 `Courier New` (700)
- Body: `Space Mono` (400) 或 `IBM Plex Mono` (400)

**Color Palette:**
```css
:root {
    --bg-primary: #fffffe;
    --bg-accent: #ff6b35;
    --text-primary: #000000;
    --text-secondary: #333333;
    --border-thick: #000000;
    --accent-yellow: #ffd60a;
    --accent-red: #e63946;
}
```

**Signature Elements:**
- 粗边框（3-5px 黑色实线）
- 高对比度配色
- 大胆排版（超大字号 + 混合字重）
- 不规则形状和不对称布局
- 工业感/原始感
- 等宽字体
- 鲜明色块碰撞
- 故意"不完美"的对齐

**Best Use Cases:** 艺术展示, 实验性设计, 独特品牌, 反主流文化

---

## 科技 (Tech)

---

### 25. Red-Black-White

**气质:** 高对比科技感, intense, powerful, sharp

**布局:** 红色强调 + 黑白对比，锐利的几何元素。

**Font Pairing:**
- Display: `Oswald` (700) 或 `Montserrat` (900)
- Body: `Roboto Condensed` (400) 或 `Source Sans 3` (400)

**Color Palette:**
```css
:root {
    --bg-primary: #0a0a0a;
    --bg-secondary: #1a1a1a;
    --text-primary: #ffffff;
    --text-secondary: #cccccc;
    --accent-red: #ff0033;
    --accent-red-dark: #cc0029;
    --border: #333333;
    --glow-red: rgba(255, 0, 51, 0.3);
}
```

**Signature Elements:**
- 红色作为唯一强调色
- 黑白为主基调
- 高对比度科技感
- 锐利的几何线条和形状
- 红色光效/发光边框
- 极简但有力量的排版
- 对角线/斜切元素

**Best Use Cases:** 科技公司, 创新展示, 安全/网络安全, 专业演示

---

## 教育创意 (Educational)

---

### 26. Cartoon 2.5D

**气质:** 立体插图, playful, 活泼, fun

**布局:** 立体插图元素，活泼配色，圆润边角，趣味图标。

**Font Pairing:**
- Display: `Baloo 2` (700/800) 或 `Fredoka One` (400)
- Body: `Nunito` (400/600) 或 `Quicksand` (400/500)

**Color Palette:**
```css
:root {
    --bg-primary: #eef6ff;
    --bg-secondary: #fff8e7;
    --text-primary: #2d3748;
    --text-secondary: #718096;
    --color-blue: #4299e1;
    --color-green: #48bb78;
    --color-yellow: #ecc94b;
    --color-pink: #ed64a6;
    --color-purple: #9f7aea;
    --color-orange: #ed8936;
    --shadow-soft: rgba(0, 0, 0, 0.1);
}
```

**Signature Elements:**
- 2.5D 等轴测插图（等距视角）
- 活泼多彩配色
- 大圆角元素 (border-radius: 20px+)
- 卡通图标和表情
- 柔和阴影（偏移 + 模糊）
- 儿童友好设计
- 游戏化元素（星星、徽章、进度条）

**Best Use Cases:** 教育内容, 儿童演示, 趣味展示, 培训材料

---

### 27. Education

**气质:** 知识结构化, icons, clear hierarchy, 学习友好

**布局:** 知识点结构化呈现，图标辅助理解，清晰层级。

**Font Pairing:**
- Display: `Nunito` (700/800) 或 `Poppins` (600/700)
- Body: `Nunito` (400) 或 `Open Sans` (400)

**Color Palette:**
```css
:root {
    --bg-primary: #ffffff;
    --bg-section: #f7fafc;
    --text-primary: #2d3748;
    --text-secondary: #718096;
    --accent-blue: #4299e1;
    --accent-green: #48bb78;
    --accent-orange: #ed8936;
    --accent-purple: #9f7aea;
    --border: #e2e8f0;
    --icon-bg: #ebf8ff;
}
```

**Signature Elements:**
- 知识点结构化卡片
- 图标辅助（每项配图标）
- 清晰的层级和编号
- 步骤/流程可视化
- 学习友好的色彩区分
- 信息图表风格
- 进度指示和章节标记

**Best Use Cases:** 教学演示, 知识讲解, 培训内容, 学习课件, 操作指南

---

## 快速参考表

### 按情绪选择风格

| 情绪 | 推荐风格 |
|------|----------|
| 自信/专业 | Bold Signal, Electric Studio, TED, Swiss Modern |
| 创意/活力 | Creative Voltage, Split Pastel, Gamma Modern |
| 优雅/高级 | Dark Botanical, Paper & Ink, Kinfolk |
| 未来/科技 | Neon Cyber / Neo-Tokyo, Terminal Green, Red-Black-White |
| 温暖/友好 | Pastel Geometry, Notebook Tabs, Kinfolk |
| 极简/克制 | Apple Keynote, MUJI, Swiss Modern |
| 教育/清晰 | Education, Typical, Consulting |

### 按内容密度选择风格

| 密度 | 推荐风格 |
|------|----------|
| 低（大图+少文字） | TED, Apple Keynote, Dark Botanical |
| 中（图文平衡） | Neon Cyber, Vintage Editorial, Editorial Magazine |
| 高（信息密集） | Consulting, Newspaper, Typical, Education |

### Font Source 快速参考

| Source | 可用字体 | 本地路径 |
|--------|---------|-----|
| Local vendor fonts | Playfair Display, Source Serif 4, IBM Plex Mono, Noto Serif SC, Noto Sans SC, plus system fallbacks | `assets/vendor/google-fonts-local.css` |
| Fontshare | Clash Display, Satoshi | `api.fontshare.com` |
| System | -apple-system, SF Pro, Segoe UI, Calibri, Georgia, Arial | 系统内置 |

---

## 禁止使用的通用模式 (DO NOT USE)

**字体:** Inter, Roboto, Arial 作为 Display 字体（仅 Body 可接受系统字体）

**配色:** `#6366f1`（通用靛蓝）、紫色渐变白底、默认蓝色作为主色

**布局:** 万物居中、千篇一律的 Hero Section、完全相同的卡片网格

**装饰:** 写实插图（除非风格要求）、无目的的毛玻璃效果、无目的的阴影

**替代方案:** 使用每个风格独特的 Font Pairing 和 Color Palette，确保每份演示文稿有辨识度。
