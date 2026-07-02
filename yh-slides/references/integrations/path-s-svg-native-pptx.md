# Path S: SVG -> Native Editable PPTX

> 用途：`2A-S 高保真原生可编辑 PPTX` 的执行规范。Path S 吸收 PPT Master 的 SVG -> DrawingML 转换链路，用于复杂图表、咨询级版式、强原生可编辑和避免 HTML 转换偏移的 PPTX。

## 定位

Path S 是 `2A` 的高级分支，不替代 `Path A`。

| 路线 | 适合 | 风险 |
|---|---|---|
| `2A / Path A` | 正式汇报、企业材料、后期改字、最快稳定落地 | HTML -> PPTX 有坐标/文本渲染偏移风险，复杂图表表达有限 |
| `2A-S / Path S` | 复杂图表、咨询级版式、原生形状/路径/文本可编辑、希望避开 HTML 转换偏移 | 流程更重、更慢，SVG 子集约束严格，需要逐页质量门 |

推荐规则：

- 用户只说“正式可编辑 PPTX / 最稳 / 企业汇报”时，默认推荐 `2A / Path A`。
- 用户强调“复杂图表 / 原生形状 / 矢量可编辑 / 不要 HTML 偏移 / 咨询级图表”时，推荐 `2A-S / Path S`。
- 用户想要“好看且文字能改”，但不要求所有形状原生可编辑时，仍优先 `2C / Path H`。

## 项目结构

```text
C:\PPTX\{项目名}\
├── design_spec.md
├── spec_lock.md
├── sources\
├── images\
├── svg_output\
│   ├── 01_cover.svg
│   ├── 02_context.svg
│   └── ...
├── svg_final\
├── notes\
│   ├── total.md
│   └── ...
├── exports\
└── backup\
```

## 执行流程

1. 完成 `SKILL.md` Step 0-4：需求、内容大纲、页型覆盖、设计方向。
2. 写出 `design_spec.md`：人类可读的设计说明，包含受众、页数、风格目标、内容大纲、图片策略。
3. 写出 `spec_lock.md`：机器执行锁，包含画布、颜色、字体、图片资源、页型节奏、图表/版式引用。
4. 逐页生成 SVG 到 `svg_output/`。生成每页前必须重读 `spec_lock.md`。
5. 运行 SVG 质量检查，0 error 后才进入后处理。
6. 生成演讲者备注 `notes/total.md`，再拆分为逐页 notes。
7. 后处理 SVG，输出 `svg_final/`。
8. 导出 native PPTX 与 SVG preview PPTX。

## 本地模板库

Path S 已全量内置 PPT Master 模板库到 `templates/`，运行时不依赖外部仓库。

```text
templates/
├── design_spec_reference.md
├── spec_lock_reference.md
├── layouts/
│   ├── layouts_index.json
│   └── <layout_id>/
├── charts/
│   ├── charts_index.json
│   ├── CHART_STYLE_GUIDE.md
│   └── *.svg
└── icons/
    ├── README.md
    ├── tabler-outline/
    ├── tabler-filled/
    ├── phosphor-duotone/
    ├── simple-icons/
    └── chunk-filled/
```

使用规则：

- 用户明确给出布局模板目录时，读取该目录下的 `design_spec.md` 和页面 SVG，把它作为 Path S 的页面骨架来源。
- 用户只说“有哪些模板”时，读取 `templates/layouts/layouts_index.json` 和 `templates/layouts/README.md`，只列路径和适用场景，不自动套用。
- 涉及数据图表、流程、架构、系统关系、战略框架时，读取 `templates/charts/charts_index.json`，按每页内容形状匹配 SVG 模板；不要把所有结构页都做成普通文本页。
- 图标只从 `templates/icons/` 选择，优先使用 `tabler-outline`；品牌 logo 才使用 `simple-icons`。图标必须在 `spec_lock.md` 中记录库名或具体文件。
- 模板 SVG 是骨架，不是最终页；必须改写文本、数据、配色和层级，使其匹配当前 `spec_lock.md`。

```bash
python scripts/svg_quality_checker.py "C:\PPTX\{项目名}"
python scripts/total_md_split.py "C:\PPTX\{项目名}"
python scripts/finalize_svg.py "C:\PPTX\{项目名}"
python scripts/svg_to_pptx.py "C:\PPTX\{项目名}"
```

输出：

```text
exports/{project_name}_{timestamp}.pptx
backup/{timestamp}/{project_name}_svg.pptx
backup/{timestamp}/svg_output/
```

依赖说明：native DrawingML 主 PPTX 需要 `python-pptx`。SVG preview PPTX 的旧版 Office 兼容 PNG fallback 需要 `cairosvg`，或 `svglib reportlab`；缺失时导出器会退回 pure SVG preview，主 native PPTX 不受影响。生产交付如果需要 preview PPTX 兼容旧版 Office，优先运行：

```bash
pip install -r requirements-optional.txt
```

若 `cairosvg` 在 Windows 目标环境不可用，可改装：

```bash
pip install svglib reportlab
```

注意：Windows 上 Python 包装好后仍可能缺系统 Cairo DLL，导致 PNG renderer 无法加载。此时 `svg_to_pptx.py` 会退回 pure SVG preview；native DrawingML PPTX 仍正常生成。生产环境如要求旧版 Office preview 兼容，建议使用已带 Cairo 的 conda/WSL/CI 镜像，或单独安装系统 Cairo runtime。

## spec_lock.md 最小结构

`svg_quality_checker.py` 和 `update_spec.py` 读取的是 Markdown section + list item 格式：

```markdown
# Execution Lock

## project
- name: demo
- format: ppt169

## canvas
- viewbox: 0 0 1280 720
- width: 1280
- height: 720

## colors
- primary: #1D4ED8
- accent: #F59E0B
- background: #FFFFFF
- text: #111827

## typography
- font_family: Noto Sans SC
- body: 30
- title: 56
- caption: 18

## icons
- library: tabler-outline

## page_rhythm
- 01_cover: anchor
- 02_context: dense
- 03_framework: breathing

## page_layouts
- 01_cover: null
- 02_context: null

## page_charts
- 03_framework: null
```

规则：

- `colors.*` 和 `typography.font_family` 是逐页 SVG 的字面来源，不要凭记忆改写。
- `page_rhythm` 用于避免每页同构：`anchor` 承载关键判断，`dense` 承载信息密度，`breathing` 留白降噪。
- `page_layouts` 和 `page_charts` 可为空；为空代表本页自由设计，不是缺失。
- 默认 `ppt169` viewBox 使用 `0 0 1280 720`；如果未来扩展其他尺寸，先同步 `scripts/project_utils.py` / `scripts/svg_to_pptx/pptx_dimensions.py` 的 canvas format。

## SVG 生成纪律

- 每页一个完整 SVG 文件，`viewBox` 必须匹配 `spec_lock.canvas`。
- 逐页生成，不批量脚本生成，不一次性模板循环吐出所有页。
- 每页生成前重读 `spec_lock.md`，颜色、字体、图片文件名必须来自锁文件。
- 顶层逻辑块使用 `<g id="...">`，便于导出后成为动画和选择粒度。
- 复杂图表优先用 SVG 原生几何表达，不用整图截图。

## SVG 技术约束

禁用或避免：

- `<style>` / CSS class 作为视觉来源；使用内联属性。
- `foreignObject`、`script`、`iframe`、`animate*`。
- `<mask>`、`textPath`、`symbol + use` 的非图标用法。
- HTML 命名实体如 `&mdash;`；SVG XML 中应使用裸 Unicode 或标准 XML 转义。
- 未约束的 `clipPath`；只在图片裁剪场景中使用可转换写法。

允许并推荐：

- `<rect>`、`<circle>`、`<ellipse>`、`<line>`、`<path>`、`<polygon>`、`<polyline>`、`<text>`、`<image>`。
- `linearGradient` / `radialGradient`，但要跑 `svg_quality_checker.py` 验证。
- 顶层 `<g id="content_block">` 组织语义块。

## 失败处理

- `svg_quality_checker.py` 出现 error：回到对应页重写 SVG，不要直接后处理。
- PPTX 可打开但对象不可编辑：检查该页是否被图片化或使用了不可转换 SVG 特性。
- native PPTX 与 preview PPTX 差异明显：优先检查 `svg_output/` 中的图片引用、`<use>` 图标、`tspan` 和裁剪。
- 图表数值错位：回到 SVG 源文件修正坐标，再重跑质量检查和导出。
