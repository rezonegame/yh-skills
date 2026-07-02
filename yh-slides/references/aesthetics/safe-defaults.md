# 精选默认组合（Safe Defaults）

> 不知道怎么选？从这里找你的场景，直接用。

---

## 理念

来自 guizang 的经验教训：

> **给用户默认，不是唯一。** 精心挑选的默认组合，能让 80% 的用户不需要纠结，直接出高质量作品。深度定制路径依然保留，但需要主动申请。

---

## Path A 精选默认

### 企业产品介绍（对外）

- **种子**：`assets/seeds/path-a-seed.html`
- **插画风格**：Snoopy 线稿（`references/aesthetics/proven-styles-snoopy.md`）
- **配色**：深色封面（`background: #1a1a1a`），白色正文
- **布局**：图文 7:5（右图左文），数据页大数字居中
- **字体**：Playfair Display（标题）+ Noto Sans SC（正文）

```html
<!-- 封面参考 -->
<div class="slide dark">
  <h1 class="t-display" style="position:absolute;top:150pt;left:60pt;font-size:64pt;color:#fff">产品名</h1>
</div>
```

### 学术研究汇报（学术会议）

- **种子**：`assets/seeds/path-a-seed.html`
- **插画**：无插画（降低干扰）
- **配色**：纯白正文，深蓝强调（`accent: #2a6db5`）
- **布局**：文字为主，数据图（表格 / 公式）用图片嵌入
- **字体**：Noto Serif SC（标题）+ Noto Sans SC（正文）

---

## Path B精选默认

### 产品发布会

- **风格**：Snoopy 线稿（最稳定，不乱码）
- **尺寸**：2K（`--image-size 2K`）
- **构图节奏**：封面全屏冲击 → 信息页克制留白 → 案例页强视觉交替
- **prompt 前缀**：`in Snoopy Schulz line art style, clean white background, no text in image,`

### 创意展示 / 艺术项目

- **风格**：`references/aesthetics/proven-styles-gallery.md` 的 **Ligne Claire** 或 **日本现代版画**
- **尺寸**：2K
- **构图**：封面大面积留白 + 单一主体，正文局部特写 + 说明文字

### 初创公司融资路演

- **风格**：**Bauhaus + 构成主义**（几何感强，显"高端简约"）
- **尺寸**：2K
- **配色**：黑白为主，单色强调（纯红或纯蓝）

---

## Path C 精选默认

### 个人年度总结 / 个人品牌

- **种子**：`path-c-magazine-seed.html`
- **主题**：沙丘（`references/aesthetics/magazine/themes.md` → 沙丘）
  ```css
  --ink: #3d2817; --paper: #f6ede0; --accent: #d4a574;
  ```
- **节奏**：hero-dark（封面）→ light × 3 → hero-light（转折）→ dark × 2 → hero-dark（结尾）
- **字体**：Noto Serif SC（标题）+ Noto Sans SC（正文）

### 技术分享 / 开源项目介绍

- **种子**：`path-c-magazine-seed.html`
- **主题**：靛蓝瓷
  ```css
  --ink: #0a1f3d; --paper: #f1f3f5; --accent: #2a6db5;
  ```
- **节奏**：封面 hero-dark → 问题 dark → 解决 light × N → 演示 hero-light → 结论 dark
- **布局**：代码块用 `.callout` + mono 字体，数据用 `.stat`

### 学术讲座 / 会议演讲

- **种子**：`path-c-magazine-seed.html`
- **主题**：墨水经典（最严肃，适合学术）
  ```css
  --ink: #1a1a1a; --paper: #f5f1ed; --accent: #c4302b;
  ```
- **节奏**：严格执行 light/dark 交替，hero 只在章节转场出现

### 快速原型 / 5 分钟 Demo

- **种子**：`path-c-minimal-seed.html`
- **主题**：墨水经典（极简种子默认）
- **节奏**：不超过 8 页，不追求复杂布局，内容优先

---

## Path D 精选默认

### 产品 Demo 视频（展会 / 官网）

- **种子**：`path-d-animated-seed.html`
- **动画风格**：`fade`（淡入）主导，偶尔 `slide-up`
- **TTS**：中文配音，语速适中
- **循环**：最后一页结束后自动回到第一页（JS 实现）
- **节奏**：hero-dark 封面 → light × 3 → hero-light 转场 → dark × 2 → hero-dark 结尾

### 教学课件（逐条讲解）

- **种子**：`path-d-animated-seed.html`
- **动画风格**：`slide-up`（每个要点逐条入场）
- **TTS**：启用，每页配完整解说
- **布局**：`.points` 列表 + `.pillar` 卡片（逐条动画）
- **节奏**：light 为主（清晰背景利于阅读），dark 只用于"提问"和"总结"页

---

## 当你完全不确定时

按以下顺序决策：

```
1. 用户最终在哪播放？
   → PPT/Keynote：Path A
   → 浏览器：Path C 或 D

2. 需要 AI 图片吗？
   → 是，不需要改字：Path B
   → 是，需要改字：Path A + AI 插画

3. Path C 的种子？
   → 不知道：用 magazine-seed + 墨水经典

4. 颜色方案？
   → 不知道：墨水经典（万金油）
```

---

## 反模式：不要这样选

- ❌ 在源文件仍可正向制作时滥用 2B-R；它只用于已经存在的位图资产
- ❌ 没有品牌色却让 Claude 随意选 hex（用 5 套主题色之一）
- ❌ Path C 不用种子从空白开始（必须从种子开始）
- ❌ 用户说"随便"就真的随便（最少也要确认受众和时长）
