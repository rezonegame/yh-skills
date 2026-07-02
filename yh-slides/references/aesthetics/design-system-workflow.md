# DESIGN.md 品牌系统工作流

用于需要贴合品牌、公司模板、参考网站、旧版 PPT 或长期系列演示的项目。灵感来自 Open Design 的 `DESIGN.md` 机制：把风格判断沉淀成文件，而不是每次靠临场描述。

---

## 何时启用

满足任一条件就启用：

- 用户说有品牌规范、公司模板、VI、字体、品牌色
- 用户要求匹配某个网站、产品、旧 PPT、截图
- 同一客户 / 同一课程 / 同一专栏会反复生成多份 PPT
- 用户不想要 guizang magazine 默认风格，而想要自己的系统

不启用的情况：

- 用户只要一次性快速成稿
- 2B / Path B 只追求整图视觉冲击
- 用户明确说“不用管品牌”

---

## 9 段结构

在项目目录创建 `DESIGN.md`：

```markdown
# <品牌 / 项目名>

## Visual Theme & Atmosphere
## Color Palette & Roles
## Typography Rules
## Component Stylings
## Layout Principles
## Depth & Elevation
## Do's and Don'ts
## Responsive Behavior
## Agent Prompt Guide
```

### 每段写什么

| 段落 | 内容 |
|---|---|
| Visual Theme & Atmosphere | 一句话视觉气质 + 适合/不适合的场景 |
| Color Palette & Roles | 背景、前景、强调色、弱化色、边框色、surface 的角色 |
| Typography Rules | 标题/正文/等宽字体，字号层级，行高和字距 |
| Component Stylings | 卡片、按钮、表格、图框、引用、标签等组件姿态 |
| Layout Principles | 栅格、留白、页面密度、hero/正文比例 |
| Depth & Elevation | 阴影、边框、层级、玻璃/拟物/平面策略 |
| Do's and Don'ts | 具体可执行的做/不做 |
| Responsive Behavior | HTML 路径的桌面/移动适配策略 |
| Agent Prompt Guide | 之后生成时必须遵守的短规则 |

---

## 提取流程

### A. 用户给品牌资料

1. 读取用户给的品牌规范、模板、截图或旧 PPT。
2. 提取真实颜色、字体、版式姿态；不要凭记忆猜品牌色。
3. 写入项目目录 `DESIGN.md`。
4. 用一句话复述将采用的设计系统，让用户有机会纠偏。

### B. 用户给参考网站

1. 访问品牌官网、press、brand、about 页面。
2. 记录主背景、正文色、强调色、字体、按钮/卡片/图框风格。
3. 如果只能看到近似值，写“近似提取”，不要装作官方规范。
4. 生成 `DESIGN.md` 后再进入内容结构化。

### C. 用户只有抽象描述

优先使用 `references/aesthetics/magazine/directions.md` 或 `web-styles-gallery.md` 的方向包，不要从零发明风格。若仍需生成 `DESIGN.md`，把它标记为“项目自定义设计系统”。

---

## 映射到 yh-slides

### Path A

- 将 `DESIGN.md` 的颜色和字体映射到 720pt HTML seed。
- 仍保持绝对定位和可编辑 PPTX 优先。

### Path C magazine

- 如果用户选择 magazine 方向，优先用 `directions.md`。
- 如果用户提供品牌系统，则用 `DESIGN.md` 覆盖主题色、字体和 chrome 语气，但保留 class 体系、主题节奏和质量检查。
- 不要混搭多个方向；如果品牌系统和 magazine 方向冲突，优先品牌系统。

### Path C minimal / Path D

- 用 `DESIGN.md` 作为 CSS token 和排版规则来源。
- 若没有 `DESIGN.md`，使用 `web-styles-gallery.md` 或默认安全风格。

---

## 交付检查

- [ ] 项目目录存在 `DESIGN.md`
- [ ] `DESIGN.md` 有 9 个 section
- [ ] 颜色来自用户资料、参考网站或明确方向包，不是临时猜测
- [ ] 字体策略明确：display / body / mono
- [ ] 至少 5 条 Do's and Don'ts
- [ ] `Agent Prompt Guide` 能直接指导后续生成
- [ ] 在最终说明里标明本 deck 使用了哪个设计系统
