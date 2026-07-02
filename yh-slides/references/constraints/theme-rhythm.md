# 主题节奏规划（Theme Rhythm）

> **适用路径**：Path C、Path D（需要主题切换的 HTML 路径）；Path A/B 的审美节奏参考 [quality-checklist.md](./quality-checklist.md) 的 P2 规则
> **强制级别**：P0（违反会导致视觉疲劳、叙事死板）

## 为什么需要节奏

**失败例子**：一份 12 页的 deck，除封面外全是 `light` 白色背景，正文衬线字体，chrome/foot 一个样。
结果：观众第 3 页就开始走神，没有任何视觉呼吸感。

**guizang 原话**：
> 连续 3 页同主题 = 视觉疲劳  
> 8 页以上必须有 ≥1 个 `hero dark` + ≥1 个 `hero light`

这不是"建议"，是硬规则。

---

## 4 种主题标记

每一页的 `<section>` **必须**带一个主题 class：

| 标记 | 适用 | WebGL 背景 | 文字颜色 | 遮罩 |
|------|------|-----------|---------|------|
| `light` | 正文页（数据、列表、图文） | 半透（隐约可见） | 深色（--ink） | 78% 纸色 |
| `dark` | 正文页（强反差、对比、思考） | 半透 | 浅色（--paper） | 78% 墨色 |
| `hero light` | 章节分割、金句、转场 | **明显可见**（浅色流动） | 深色 | 16% 纸色 |
| `hero dark` | 封面、开场、结尾、重要问题 | **强烈可见**（钛金色散） | 浅色 | 12% 墨色 |

**禁止**：
- 只写 `hero` 不带主题色（会导致 WebGL 切换失败）
- 使用自定义主题名（如 `midnight` / `sunny`）
- 一个 deck 内混用两套色系

---

## 节奏规划流程（强制）

### Step 1: 写代码前，先画节奏表

在开始生成 slide 代码之前，**先列出每一页的主题标记**：

例（12 页 deck）：
```
Page 01: hero dark     ← 封面
Page 02: dark          ← 开场叙事
Page 03: light         ← 数据呈现
Page 04: light         ← 数据延展
Page 05: hero light    ← 章节转场 (Act II)
Page 06: dark          ← 深度分析
Page 07: light         ← 对比页
Page 08: dark          ← 案例引用
Page 09: hero dark     ← 核心问题
Page 10: light         ← 解决方案
Page 11: dark          ← 行动号召
Page 12: hero light    ← 收束致谢
```

### Step 2: 对照硬规则自检

| 规则 | 检查方法 |
|------|---------|
| **不允许连续 3 页同主题** | 看节奏表，任何 3 连续行不能都是同一标记 |
| **8 页以上必须有 ≥1 hero dark + ≥1 hero light** | 总数 count(hero dark) ≥ 1 AND count(hero light) ≥ 1 |
| **至少 1 个 dark 正文页（非 hero）** | count(dark 但非 hero) ≥ 1 |
| **不能全是 light 正文页** | 除 hero 外，混合使用 light 和 dark |

### Step 3: 节奏符合后再写代码

节奏表过关后，再开始挑布局、填内容。

---

## 常见节奏模板

### 短 deck（5-8 页）

```
01: hero dark      ← 封面
02: light          ← 核心信息
03: dark           ← 反差 / 对比
04: hero light     ← 转场或金句
05: light          ← 数据 / 细节
06: dark           ← 案例
07: hero dark      ← 问题 / 结论
08: light          ← 致谢
```

### 中等 deck（10-15 页）

按 3 幕结构：
```
Act I (开场): hero dark → light → dark → light
Act II (展开): hero light → light → dark → light → dark
Act III (收束): hero dark → light → hero light
```

### 长 deck（20-30 页）

按 3-4 幕，每幕 5-8 页：
```
Act I:   hero dark + 4 页正文（light/dark 交替）+ hero light (转场)
Act II:  hero dark + 5 页正文 + hero light (转场)
Act III: hero dark + 6 页正文 + hero light (转场)
收束:    hero dark (总结) + 1-2 页致谢
```

**关键平衡**：
- Hero 页占比 15-25%（太少无节奏，太多会疲劳）
- dark 和 light 页比例约 1:1（可以 4:6 或 6:4，但不能 1:9）

---

## 按布局选主题的建议

从 guizang 原版 checklist 整理：

| 布局类型 | 推荐主题 | 理由 |
|---------|---------|------|
| 左文右图（Layout 4） | `light` / `dark` 交替 | 图文混排需要清爽背景 |
| 大引用（Layout 8） | `light` / `dark` 交替 | 金句需要干净底 |
| 图文混排（Layout 10） | `light` / `dark` 交替 | 图片优先 |
| 大字报（数据矩阵） | `light` | 大数字需要亮底突出 |
| 图片网格 | `light` | 截图需要亮底 |
| Pipeline / 流程 | `light` | 流程需要清晰 |
| 对比页 | `light` | 双栏对比亮底最清 |
| 封面 | `hero dark` | 视觉冲击 |
| 章节幕封 | `hero dark` 与 `hero light` 交替 | 主题切换标志 |
| 问题页（Q） | `hero dark` | 聚焦提问 |
| 结尾致谢 | `hero light` 或 `hero dark` | 收束仪式感 |

---

## 自动化自检命令

### 列出所有 slide 的主题标记

```bash
grep -oE 'class="slide [^"]+"' output.html
```

### 统计各主题数量

```bash
grep -oE 'class="slide [^"]+"' output.html | sort | uniq -c
```

### 检查连续 3 页同主题

```bash
grep -oE 'class="slide ([^"]+)"' output.html \
  | sed 's/class="slide //;s/"//' \
  | awk 'prev==$0 && prev2==$0 {print NR": 3+ consecutive "$0} {prev2=prev; prev=$0}'
```

如输出任何行，就有违规。

---

## 反例

### ❌ 全白 deck

```
Page 01: hero dark
Page 02-12: light (连续 11 页)
```

**问题**：连续 11 页 light，违反"不超过连续 3 页同主题"。

**修复**：
```
Page 01: hero dark
Page 02: light
Page 03: dark       ← 加入 dark 打破连续
Page 04: light
Page 05: hero light  ← 加入 hero 变化
Page 06-08: light / dark 交替
...
```

### ❌ 无 hero 节奏

```
Page 01-30: 全部 light + dark 交替，没有 hero
```

**问题**：30 页完全没有 hero，观众没有喘息的视觉锚点。

**修复**：每 4-6 页插入 1 个 `hero dark` 或 `hero light`。

### ❌ hero 过密

```
Page 01: hero dark
Page 02: hero light
Page 03: hero dark
Page 04: hero light
```

**问题**：连续 4 页 hero，WebGL 背景抢戏，观众视觉疲劳。

**修复**：hero 之间至少插 2-3 页正文。

---

## Path A / Path B 的审美节奏

Path A/B 是 PPTX 路径，没有"主题 class"的概念，但审美节奏原则类似：

**Path A（HTML → PPTX）**：
- Hero 页用深色背景 + 大字
- 正文页用白色背景 + 信息密集
- 连续 3 页同风格 = 审美疲劳

**Path B（AI 整页图片）**：
- 视觉强度交替：封面冲击 → 信息页克制 → 案例页强视觉 → 引用页克制
- 构图交替：左图右文 / 居中 / 全屏 / 分屏

详见 [quality-checklist.md](./quality-checklist.md) 的 P2 视觉节奏部分。

---

## 自检清单

生成 deck 前：
```
□ 已画节奏表（每页标记 light/dark/hero light/hero dark）
□ 没有连续 3 页同主题
□ 8 页以上有 ≥1 hero dark + ≥1 hero light
□ 至少 1 个 dark 正文页（非 hero）
□ 不是全 light 或全 dark
```

生成 deck 后：
```
□ grep 'class="slide' output.html 结果符合节奏表
□ 浏览器打开后，翻页有视觉呼吸感
□ WebGL 背景能根据主题切换（body.light-bg 类在浅色页生效）
```
