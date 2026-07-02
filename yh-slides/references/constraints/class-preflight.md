# 类名预检机制（Class Preflight）

> **适用路径**：Path A、Path C、Path D（所有基于 HTML 的路径）
> **强制级别**：P0（必须通过，否则页面样式全塌）

## 为什么需要预检

**最常见的 LLM 生成翻车**：发明不存在的 class 名。

例子：Claude 写了 `.stat-card`，但种子文件的 `<style>` 里只定义了 `.stat`。结果：
- 浏览器 fallback 到默认样式
- 大标题变成非衬线字体
- 布局全塌，元素堆叠
- 用户以为是种子文件问题，实际是类名没对上

这种错误**在浏览器打开前完全看不出来**，是所有 HTML 生成类任务的头号风险。

---

## 强制预检流程（Path C / Path D）

### Step 1: 读种子文件

在写任何 slide 代码之前，**必须先 Read 种子文件**：

```
Read: assets/seeds/path-c-magazine-seed.html
或
Read: assets/seeds/path-c-minimal-seed.html
或
Read: assets/seeds/path-d-animated-seed.html
```

**至少读到 `<style>` 块末尾**（通常在文件前 40% 的位置）。

### Step 2: 列出要用的所有 class 名

在生成 slide 代码前，**先文字列出你打算使用的所有 class**。

例如：
```
本次生成将使用以下 class:
- .slide, .slide.light, .slide.dark, .slide.hero
- .chrome, .foot, .kicker, .tag
- .h1-zh, .h2-zh, .body-zh, .meta
- .grid-6, .grid-4, .grid-3, .split
- .stat (.n / .l / .m), .callout, .pillar
- .frame-img, .frame-cap
```

### Step 3: 对照种子的 `<style>` 块逐项确认

**✅ 类名都已定义** → 继续生成  
**❌ 缺失某些类**：
- 优先方案：在种子的 `<style>` 块里补上新 class 定义
- 次选方案：在 slide 里用 inline `style="..."` 替代
- **绝不允许**：发明一个新 class 名然后当它存在

### Step 4: 生成代码

只在 `<main id="deck">` 或 slide 容器内写内容。**不要重写 CSS 结构**。

---

## 预检的自动化辅助

### 列出种子里已定义的 class

```bash
grep -oE '\.[a-z][a-z0-9-]+' assets/seeds/path-c-magazine-seed.html | sort -u
```

### 列出输出 HTML 中使用的 class

```bash
grep -oE 'class="[^"]+"' output.html | grep -oE '[a-z][a-z0-9-]+' | sort -u
```

### 找出未定义的 class（diff）

```bash
diff <(grep -oE 'class="[^"]+"' output.html | grep -oE '[a-z][a-z0-9-]+' | sort -u) \
     <(grep -oE '\.[a-z][a-z0-9-]+' assets/seeds/path-c-magazine-seed.html | grep -oE '[a-z][a-z0-9-]+' | sort -u)
```

输出 `<` 开头的行就是「使用了但未定义」的类。

---

## 常见易漏类名（Magazine Seed）

以下类名是 `path-c-magazine-seed.html` 中预定义的，但 layouts.md 示例里用到的 class 可能与种子不完全对齐。**生成前必查**：

### 标题与正文
`.display` `.display-zh` `.h1-zh` `.h2-zh` `.h3-zh` `.lead` `.body-zh` `.body-serif` `.kicker` `.meta` `.big-num` `.mid-num` `.ghost`

### 布局
`.col` `.row` `.grid-6` `.grid-9` `.grid-4` `.grid-3` `.split` `.split-55` `.fill` `.center`

### 组件
`.chrome` `.foot` `.tag` `.rule` `.callout` `.callout .cite` `.callout .q-big`
`.stat .n / .l / .m` `.plat .name / .nb / .sub` `.rowline .k / .v / .m`
`.pillar .ic / .t / .d`

### 图片
`.frame-img` `.frame-cap` `.frame-cap .pf / .nb / .idx` `figure.tile` `.img-slot`

### 高级布局（layouts.md 里可能额外定义）
`.frame.grid-2-7-5` `.frame.grid-2-6-6` `.frame.grid-2-8-4` `.frame.grid-3-3`

**注意**：最后一组（`grid-2-*`）需要检查种子的 `<style>` 里是否真的定义了；如果没有，要先补上。

---

## 反例：禁止的做法

### ❌ 反例 1：发明新类
```html
<!-- 错误：种子里没有 .stat-card -->
<div class="stat-card">
  <div class="stat-label">Users</div>
  <div class="stat-nb">1.2M</div>
</div>
```

```html
<!-- 正确：用种子里已有的 .stat -->
<div class="stat">
  <span class="m">Users</span>
  <span class="n">1.2M</span>
</div>
```

### ❌ 反例 2：Inline 重写基础架构
```html
<!-- 错误：重写了 .slide 的 flex 行为 -->
<section class="slide light" style="display:block;padding:0">
```

```html
<!-- 正确：保持 .slide 原语义，在子元素里调整 -->
<section class="slide light">
  <div style="padding:4vh 4vw">内容</div>
</section>
```

### ❌ 反例 3：删除种子的 class
```html
<!-- 错误：把 .frame-img 改成 .image -->
<figure class="image">
```

```html
<!-- 正确：保留 .frame-img，图片尺寸用内联控制 -->
<figure class="frame-img" style="height:26vh">
```

---

## 与 Path A 的差异

Path A（HTML → PPTX）也需要预检，但规则略有不同：

| 维度 | Path C / D | Path A |
|------|-----------|--------|
| 种子文件 | `path-c-*-seed.html` | `path-a-seed.html` |
| 核心检查 | class 是否定义 | `position: absolute` 是否应用到每个元素 |
| 常见错误 | 发明新 class | 忘记写 `position: absolute` / 尺寸不是 720×405pt |

Path A 的详细预检见 [quality-checklist.md](./quality-checklist.md) 的 Path A 段落。

---

## 自检清单

生成完 HTML 后，按以下顺序检查：

```
□ 对照种子 <style> 块，确认用到的 class 都有定义
□ 没有 inline 重写 .slide / .frame / .chrome / .foot 这些基础架构
□ 如果扩展了新 class，已写入 <style> 块（不是 inline）
□ 浏览器打开后没有"字体全塌 / 布局错位 / 图片堆叠"
```

如果任意一条打不上勾，**回到 Step 1 重做预检**。
