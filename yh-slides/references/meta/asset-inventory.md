# Asset Inventory and Legacy Notes

> 用途：说明 `yh-slides` 中本地资产、占位目录和历史遗留内容的当前状态。遇到“这个文件/目录是不是被使用”的问题，先查本文件。

## 已接入资产

| 位置 | 状态 | 使用方式 |
|---|---|---|
| `assets/seeds/path-a-seed.html` | 已接入 | `2A / Path A` 的 HTML -> PPTX 起点；固定 720pt x 405pt |
| `assets/seeds/path-c-magazine-seed.html` | 已接入 | `2D / Path C magazine` 单文件网页演示起点 |
| `assets/seeds/path-c-minimal-seed.html` | 已接入 | `2D / Path C minimal` 轻量单文件网页演示起点 |
| `assets/seeds/path-d-animated-seed.html` | 已接入 | `2D / Path D` 动画 + TTS HTML 起点 |
| `assets/style-samples/` | 已接入 | Step 4 风格选择时展示视觉样例；索引见 `references/aesthetics/style-samples.md` |
| `assets/layout-samples/` | 已接入 | 图表布局、主题约束、设计系统样例；索引见 `references/aesthetics/layout-scene-assets.md` |
| `assets/scene-templates/` | 已接入 | 设备 frame、视觉 prompt gallery；索引见 `references/aesthetics/layout-scene-assets.md` |
| `assets/external-licenses/` | 已接入 | 外部资产来源许可证快照：Kami、open-slide、open-design、open-codesign |
| `assets/vendor/` | 已接入 | `2D / Path C-D-E` 输出时复制到 `output/assets/vendor/`，提供本地字体、Lucide、GSAP、Motion |
| `assets/placeholders/image-not-available.svg` | 已接入 | 缺图或素材未就绪时的本地占位图 |
| `scripts/html2pptx.js` | 已接入 | `2A / Path A` HTML -> PPTX；依赖技能根目录 `package.json` |
| `scripts/create_slides.py` | 已接入 | `2B / Path B` 图片型 PPTX 组装 |
| `scripts/figedit_batch.py` | 已接入 | `2B-R / FigEdit Reconstruction` 独立技能联动、批处理与质量门 |
| `scripts/generate_image.py` | 已接入但非默认 | API 生图 fallback；默认仍优先当前 runtime 原生生图 |

## 当前占位 / 空目录

当前没有空的 `assets/` 子目录。原 `assets/layout-samples/` 与 `assets/scene-templates/` 已接入外部精选资产。

| 位置 | 当前状态 | 建议 |
|---|---|---|
| `references/scripts/` | 已放入 README，占位不再为空 | 未来用于脚本文档；当前脚本说明仍集中在 `references/_INDEX.md` 和 `references/paths/path-workflows.md`。 |

## 历史遗留说明

- 旧称 `Path B 高级版` 和旧的文字覆盖补救已移除；当前为 `2B-R / FigEdit Reconstruction`。
- 旧称 `Path B Standard` 已统一为 `2B / Path B`。
- 旧称 `Path Hybrid / 2C` 已统一为 `2C / Path H`。
- `2A/2B/2C/2D` 是用户侧产物选项，`Path A/B/H/C/D/E` 是内部执行路径。

## 检查建议

新增资产时必须同时完成三件事：

1. 在本文件登记状态和用途。
2. 在 `references/_INDEX.md` 或对应 reference 中添加入口。
3. 在 `SKILL.md` 的相关 Step 中说明何时读取或展示。
