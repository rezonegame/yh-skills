# Path E: Local React Deck

> 用途：定义 `yh-slides` 的本地 React/TSX 网页演示路径。Path E 吸收固定画布和组件化 authoring 方法，但不默认依赖 Open-Slide、Open-Design 或任何外部 slide runtime。

## 适用场景

优先选择 Path E，当用户需要：

- 长期维护的网页演示，而不是一次性交付 HTML。
- 复杂交互、可复用组件、状态切换、可展开内容或演示控制。
- 静态部署、版本管理、截图 QA、contact sheet。
- 固定 1920×1080 视觉画布，并希望预览、导出和演示保持一致。

不优先选择 Path E，当用户需要：

- 纯 PPTX 可编辑文件：选 Path A。
- 最快出强视觉图片型 PPTX：选 Path B。
- 单文件离线 HTML：选 Path C。
- TTS 和 GSAP 主导的多媒体课件：选 Path D。

## 独立运行原则

- 默认不使用 `@open-slide/core`、Open-Slide CLI 或外部 runtime。
- 可以用 React/TSX，也可以用等价本地前端工程，只要固定画布、静态输出和 QA 可执行。
- 不自动改写全局 `package.json`、全局配置或其他项目文件。
- 如果当前工作区没有前端工程，先向用户说明将创建一个本地工程目录；若用户只要单文件输出，改走 Path C。

## 推荐目录

在项目目录中创建局部工程：

```text
C:\PPTX\{项目名}\
├── react-deck\
│   ├── src\
│   │   ├── App.tsx
│   │   ├── slides.tsx
│   │   └── theme.ts
│   ├── public\
│   └── package.json
├── images\
├── output\
├── DESIGN.md
└── 项目记录.md
```

如果已有前端工程，则遵守现有结构，不另起无关框架。

## 画布规则

- 每页根节点固定为 1920×1080。
- 预览容器负责等比缩放，不在 slide 内写响应式断点。
- 主要布局可用 absolute 坐标、CSS grid 或 flex，但最终视觉必须在 1920×1080 下稳定。
- 字体不要随视口缩放；所有层级基于固定画布设计。

建议 type scale：

| Role | Size |
|---|---:|
| Display | 160-190px |
| H1 | 104-132px |
| H2 | 72-92px |
| Body | 28-38px |
| Caption / Mono | 14-20px |

## Authoring 规则

- 每个 page 是一个独立组件或清晰的数据驱动渲染单元。
- 页面内容来自 Step 3 的大纲和页型 archetype，不在组件中临时发明结构。
- 主题 tokens 来自 `DESIGN.md`，不要在每页重复散落颜色和字号。
- 复杂图表先按 `references/integrations/diagram-chart-routing.md` 判断类型，再实现。
- 资源使用本地相对路径，不能把远程图片、字体、脚本作为必需资源。

## 构建与输出

推荐输出：

```text
C:\PPTX\{项目名}\output\react-deck\
├── index.html
├── assets\
└── screenshots\
```

构建命令取决于现有工程。如果新建 Vite/React 工程，使用本地 `npm` / `pnpm` / `bun` 命令即可；不要在技能中硬编码唯一包管理器。

## QA 要求

Path E 必须执行：

- 本地构建或预览命令通过。
- 每页截图。
- 检查白屏、空页、截断、低方差近空白页、异常重复 hash。
- 生成 contact sheet。
- 交付前说明预览路径和输出路径。

详细规则见 `references/constraints/visual-qa.md`。

## 常见失败

- 构建通过但路由白屏：必须用浏览器截图检查，不要只信 build。
- 组件里散落样式：回到 `DESIGN.md` 提取 theme tokens。
- 画布内写响应式断点：会导致导出和演示不一致。
- 为了兼容外部 runtime 改全局配置：违反独立技能原则。
