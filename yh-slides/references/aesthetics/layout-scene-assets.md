# Layout and Scene Asset Guide

> 用途：说明 `assets/layout-samples/` 与 `assets/scene-templates/` 何时进入工作流，以及如何避免把外部资产误用成最终内容。

## 何时读取

| 用户意图 | 读取资产 | 推荐路径 |
|---|---|---|
| “版式更稳 / 页面结构丰富 / 高密度但不乱” | `assets/layout-samples/kami-diagrams/`、`open-design-systems/` | `2A` 或 `2D` |
| “正式纸面感 / 报告感 / 编辑设计” | `kami-slides/`、`open-slide-themes/paper-press.md`、`open-design-systems/editorial.md` | `2A`、`2D / Path C` |
| “暗黑杂志 / 发布会 / 强演讲视觉” | `open-slide-themes/editorial-noir.md`、`open-design-systems/neon.md` | `2B`、`2C`、`2D` |
| “产品界面 / App / 多设备展示” | `assets/scene-templates/device-frames/` | `2D / Path C-D-E` |
| “游戏感 / 分镜 / 视觉底图” | `assets/scene-templates/open-design-prompt-gallery/` | `2B`、`2C`、`Path D` |

## 转译规则

- `2A`：把样例拆成 PPT 原生文本、形状、图表和局部图片。不要把完整 HTML 截图贴成一张图。
- `2B`：可把样例作为整页视觉方向，但图中文字不可编辑，需提前提醒。
- `2C`：样例只用于底图构图和留白。所有正文、标题、互动题、答案必须在 PPT 文本框层。
- `2D`：可以更直接复用 HTML 结构，但仍要本地化依赖并按截图 QA 检查。

## 来源

- `tw93/Kami`：MIT。用于图表布局、纸面 slides 参考。
- `1weiho/open-slide`：MIT。用于 agent-facing slide theme 参考。
- `nexu-io/open-design`：Apache-2.0。用于设计系统、设备 frame、prompt gallery。
- `OpenCoworkAI/open-codesign`：MIT。本轮只审计理念与运行时结构，未复制运行时代码。

许可证快照见 `assets/external-licenses/`。
