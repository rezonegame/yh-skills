# Magazine 电子杂志设计系统（移植自 guizang-ppt-skill）

## 身份与出处

本设计系统吸收自 guizang-ppt-skill 的电子杂志工作流，并已本地化为 yh-slides **Path C 的精品预设路径**，追求"电子杂志 × 电子墨水"美学。使用时只读取本技能目录内文件，不访问外部仓库。

### 核心哲学
- **约束优于自由**：只允许 5 套预设主题色，不允许用户自定义 hex 值
- **克制优于炫技**：WebGL 只用在 hero 页面，信息层级靠排版和留白
- **设计驱动**：幻灯片 = 一期杂志，每页有明确定位（hero / 章节 / 正文）

---

## 资产清单

整套 magazine 设计系统由 5 份文件组成：

| 文件 | 作用 | 位置 |
|------|------|------|
| 种子模板 | 完整可跑的单 HTML 文件 | [assets/seeds/path-c-magazine-seed.html](../../assets/seeds/path-c-magazine-seed.html) |
| 组件手册 | 所有 CSS class 的用法和样本 | [references/aesthetics/magazine/components.md](./magazine/components.md) |
| 布局库 | 10 种完整可复制的 slide 骨架 | [references/aesthetics/magazine/layouts.md](./magazine/layouts.md) |
| 主题色预设 | 5 套精选色板（墨水经典/靛蓝瓷/森林墨/牛皮纸/沙丘） | [references/aesthetics/magazine/themes.md](./magazine/themes.md) |
| 质量清单 | P0-P3 分级检查（guizang 原版） | [references/aesthetics/magazine/checklist.md](./magazine/checklist.md) |

---

## 使用流程（Path C · Magazine 路径）

### Step 1: 复制种子
```bash
cp assets/seeds/path-c-magazine-seed.html "C:\PPTX\{项目名}\index.html"
```

### Step 2: 选主题
阅读 [themes.md](./magazine/themes.md)，从 5 套里选一套：
- 🖋 **墨水经典**：通用、商业、科技（默认推荐）
- 🌊 **靛蓝瓷**：AI、研究、技术发布
- 🌿 **森林墨**：自然、可持续、文化
- 🍂 **牛皮纸**：怀旧、人文、阅读
- 🌙 **沙丘**：艺术、设计、创意

整体替换种子里 `:root{` 块的 `--ink` / `--paper` 等变量。

### Step 3: 规划主题节奏（强制）
在写代码前，为每页画节奏表：

```
Page 01: hero dark     ← 封面
Page 02: dark          ← 开场叙事
Page 03: light         ← 数据呈现
Page 04: hero light    ← 章节转场
...
```

硬规则（详见 [checklist.md §2b-2](./magazine/checklist.md)）：
- 连续 3 页同主题 = 禁止
- 8 页以上必须有 ≥1 `hero dark` + ≥1 `hero light`
- 至少 1 个 `dark` 正文页（非 hero）

### Step 4: 类名预检（强制）
对照 [components.md](./magazine/components.md) 和 [layouts.md](./magazine/layouts.md)，列出你要用的所有 class，**逐个在种子的 `<style>` 块里确认已定义**。

参考 yh-slides 自己的预检文档：[references/constraints/class-preflight.md](../constraints/class-preflight.md)

### Step 5: 粘贴布局
从 [layouts.md](./magazine/layouts.md) 挑选 10 种布局中合适的骨架，粘贴到种子的 `#deck` 容器中。

10 种布局概览：
1. **封面 hero** — 品牌/项目大字报
2. **章节分割 hero** — Act I/II/III 过渡
3. **大字报数据** — big-num 矩阵
4. **左文右图** — Layout 4（主力布局）
5. **图片网格** — 多图并列
6. **Pipeline** — 流程 / 步骤
7. **Callout 金句** — 大引用
8. **对比页** — 双栏 vs
9. **Q&A / 问题页** — hero 提问
10. **图文混排** — 正文+插图

### Step 6: 填充内容
每页需要 3 级信息清晰：
- `.kicker`（等宽小提示，独一份）
- 大标题（衬线字体）
- 正文（非衬线字体）

详见 [components.md](./magazine/components.md)。

### Step 7: 自检
走一遍 [checklist.md](./magazine/checklist.md) 的 P0-P3 分级：
- P0：类名齐全、字体分工、图片裁剪规范、主题节奏
- P1：Hero 节奏、术语一致、页码统一
- P2：WebGL 遮罩、圆角、对齐
- P3：路径、页码同步

---

## 与 yh-slides 其他路径的关系

| 路径 | 何时用 Magazine |
|------|----------------|
| **Path A** (HTML→PPTX) | ❌ 不适用（magazine 是 HTML 原生，非 PPTX 路径） |
| **Path B** (AI 图片) | ❌ 不适用（magazine 的核心是 CSS 排版，不是整页 AI 图） |
| **Path C** (单文件 HTML) | ✅ **Magazine 是 Path C 的推荐快路径** |
| **Path D** (多文件 HTML) | ⚠️ 部分借鉴（但 Path D 用 GSAP 动画，magazine 是 scroll-snap） |

### Path C 的两种子路径
- **Path C · Magazine**：用 magazine-seed，直接粘布局改文字（10 分钟出稿）
- **Path C · Custom**：从零生成，走 `references/integrations/slide-presentation-js.md` + `web-styles-gallery.md`

选择建议：
- 不知道选什么、想快速出稿、喜欢杂志风 → Magazine
- 有明确自定义风格需求、需要非典型布局 → Custom

---

## 约束能力（迁移到 yh-slides 全部路径）

Magazine 的 3 大约束思想已被抽取到 yh-slides 的顶层 constraints/ 目录，适用于所有相关路径：

| guizang 原规则 | yh-slides 通用规则 |
|---------------|-------------------|
| 类名必须预定义 | [class-preflight.md](../constraints/class-preflight.md) |
| 主题节奏硬规则 | [theme-rhythm.md](../constraints/theme-rhythm.md) |
| 禁止 emoji / 自创颜色 | [anti-patterns.md](../constraints/anti-patterns.md) |
| P0-P3 分级质检 | [quality-checklist.md](../constraints/quality-checklist.md) |

---

## 版权与来源

本目录下的 `magazine/components.md`、`layouts.md`、`themes.md`、`checklist.md` 均为 guizang-ppt-skill 方向的本地化吸收资产，作者保留原版权。

`path-c-magazine-seed.html` 是 guizang 原始 `template.html` 的完整副本，仅在头部添加 yh-slides 集成注释。

如有版权冲突，请联系原作者。
