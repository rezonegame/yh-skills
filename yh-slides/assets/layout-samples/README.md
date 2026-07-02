# Layout Samples

用途：为 `yh-slides` 提供可读、可复用的布局参考。这里的文件不是默认运行入口；只有在需要图表页型、主题约束、杂志/纸面/终端/仪表盘等布局语言时读取。

## 子目录

| 目录 | 来源 | 用途 |
|---|---|---|
| `kami-diagrams/` | `tw93/Kami` | 14 个单页 HTML 图表/结构布局：architecture、timeline、quadrant、tree、swimlane 等。适合 `2A` 页型拆解和 `2D` HTML 组件参考。 |
| `kami-slides/` | `tw93/Kami` | 纸面感 slides 模板参考。适合正式分享、研究报告、讲稿型幻灯片的节奏参考。 |
| `open-slide-themes/` | `1weiho/open-slide` | 3 个 agent-facing slide theme：Paper Press、Editorial Noir、Neon Terminal。适合 Step 4 风格选择。 |
| `open-design-systems/` | `nexu-io/open-design` | 精选设计系统说明：editorial、publication、paper、dashboard、bento、neon、brutalism、xiaohongshu。适合把风格词转成 token 与组件约束。 |

## 使用规则

- `2A / Path A`：优先把这些样例转译为 720pt x 405pt、absolute 定位、可编辑文本/形状，而不是直接嵌整页截图。
- `2C / Path H`：可借鉴布局留白和视觉节奏，但正文、题目、答案仍必须用 PPT 文本框承担。
- `2D / Path C-D-E`：可复用 HTML/CSS 结构，但必须本地化资源并做截图 QA。
- 外部来源和许可证见 `assets/external-licenses/`。
