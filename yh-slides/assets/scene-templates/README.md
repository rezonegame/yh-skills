# Scene Templates

用途：为需要“场景构图、设备展示、AI 底图提示词”的演示提供本地参考。这里的素材不应自动塞进每个 deck；只有当用户要产品界面、游戏/故事板、视觉底图或多设备展示时读取。

## 子目录

| 目录 | 来源 | 用途 |
|---|---|---|
| `device-frames/` | `nexu-io/open-design` | 浏览器、iPhone、Android、iPad、MacBook HTML frame。适合 `2D / Path C-D-E` 做网页/产品/移动端展示。 |
| `open-design-prompt-gallery/` | `nexu-io/open-design` | 图像/视频 prompt 的 JPG 参考图。适合 `2B` 整图、`2C` 无字底图、Path D 视频感分镜。 |

## 使用规则

- `2B`：可用 prompt-gallery 作为构图灵感，允许图中承载文字，但必须校验文字准确性。
- `2C`：只借鉴构图、镜头、风格；生成底图 prompt 必须写明“无标题、无正文、无题目、无答案、无可读文字”。
- `2D`：device frame 只能作为展示壳，正文内容仍由当前项目 HTML 承担。
- 外部来源和许可证见 `assets/external-licenses/`。
