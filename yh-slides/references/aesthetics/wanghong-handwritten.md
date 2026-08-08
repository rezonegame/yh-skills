# 王虹学术手写风（Wanghong Handwritten）

> 2026-08-07 从 z-wanghong-handwritten-ppt（tjxj/z-skills，MIT）深度学习吸收。本页为该风格的视觉 DNA、提示词、时间轴动画运行时和落地方法。

## 一、适用场景

- 技术文章 / 论文 / 模型 / 工具 / 产品原理讲解
- 数学学术报告气质、Notability 数字手写页
- 需要 16:9 HTML 幻灯片 + 逐页 PNG + 时间轴逐步动画演示
- 要求保留手写温度，同时中文清楚可读

## 二、视觉 DNA（五要素）

1. **封面极简**：单行标题放画面上方约 1/3，深蓝细笔，下方一条玫红手绘横线；作者/场合/日期三行居中；下半页大面积留白。
2. **正文像数字白板笔记**：淡暖白背景（近纯白、纹理弱），深蓝黑主体笔迹，字小而工整，行距宽松；无页眉页脚页码品牌装饰。
3. **颜色承担逻辑功能**（每色必有意）：
   - 蓝 `#2f6cf6`：标题下划线、公式、坐标轴、推导主线
   - 玫红 `#ec3f79`：结论、警告、重点框、推荐项
   - 绿 `#56dc38`：正向定义、成立条件、关键结构
   - 荧光黄 `#fff04f`：一个词/短语瞬时强调（极少）
   - 珊瑚粉 `#ffaaa4`：例外、损失、剩余部分
   - 主体墨水 `#18224d`、纸张 `#f7f5ed`
4. **图文排布自由、逻辑规整**：左文右图、上公式下推论；直线/坐标轴/框/箭头保留手画不均匀感（SVG feTurbulence wobble 滤镜 + stroke-linecap round + 轻微 rotate）。
5. **强调克制**：定理/目标/结论用细线框；关键词窄条高亮；短下划线代替粗体大字号。禁止圆角卡片、渐变、阴影、照片背景、装饰图标、统一网格。

## 三、字体

- 原版：HanziPen SC（macOS「翩翩体-简」，非自由分发）
- **Linux/Windows 替代：LXGW WenKai（霞鹜文楷），OFL 许可**，已在 `assets/wanghong/template.css` 的 `--hand` 变量默认启用。安装：下载 Regular TTF 到 `~/.local/share/fonts/` 后 `fc-cache -f`。
- 渲染前确认字体已安装；`render_wanghong.sh` 会用 `fc-match` 预检。

## 四、页面类型（优先选用）

- 极简封面
- 左文右图（3-5 行解释 + 手绘示意图）
- 流程页（三个框和箭头，最重要一步荧光色）
- 坐标页（双轴解释成本/质量/速度/规模）
- 对比页（两列/三列/紧凑表格）
- 结论页（公式式收束 + 底部玫红结论框）
- 结束页（一句感谢 + 署名，安静）

## 五、时间轴动画版（核心增量，Office-PPT 式逐步播放）

同一份 HTML 可生成 `index-timeline.html` 单文件：自动把每页拆成步骤（标题、框、箭头、文字行、图表），空格/点击逐步出现，可自动连播。

```bash
python3 scripts/build_timeline.py \
  --source "/path/to/deck/index.html" \
  --out "/path/to/deck/index-timeline.html"
```

**运行时机制**（`assets/wanghong/timeline.js` + `timeline.css`，MIT）：
- 固定 1920×1080 画布，`--tl-scale` 等比缩放适配窗口
- `flatten()` 递归把内容容器拆成叶子步骤（深度≥2 或 SVG 停止拆分；行内 span/b/i 不拆）
- 标题组识别：`.page-heading` 或含 `.hand-title/.slide-title/h1/h2` 的容器
- SVG 描边动画：`pathLength=1` + `stroke-dasharray:1` + `dashoffset` 过渡（1.3s，线条间 70ms 交错）
- 荧光标记：`clip-path: inset(0 100% 0 0)` → `0` 横向揭示（0.7s）
- 标题线：`clip-path` 横向写入（0.55s）
- 纸张翻页转场 `#tl-wipe`：`scaleX(0→1)` 330ms
- 底部控制条（首页/上一步/重播/下一步/自动连播/全屏）+ 顶部进度条
- 操作：`→/空格/回车/点击` 下一步，`←/Backspace` 上一步，`Home/End` 首页末页，`F` 全屏
- 渐进增强：`.tl-ready` 前缀下 JS 未运行时页面完整可见
- 键盘事件用 capture 阶段，输入框内不劫持

**时序参数**（`CFG` 常量）：stepDur 450 / titleDur 520 / svgDur 1300 / svgStagger 70 / markerDelay 420 / markerDur 700 / autoStepDelay 1300 / autoNextDelay 2200 / wipeDur 330 / barHideDelay 2800。

## 六、neat-annotations 中文标注

`assets/wanghong/neat-annotations.css`（MIT）已本地保存，手写箭头把短注释指向目标词，支持八个方向、颜色、自定义颜色。

```css
:root {
  --ann-font: "LXGW WenKai";
  --ann-label-max-width: 220px;
}
```

```html
<span class="ann ann-n ann-green" data-note="甜点档">Q4_K_XL</span>
```

- `data-note` 直接写中文
- 标注绝对定位，目标四周预留空间；长中文结论仍写在正文中

## 七、落地工作流（在 yh-slides 内）

1. **触发**：用户说「王虹手写PPT」「Notability学术手写风」「手写网页PPT」「数学报告风」，或文章/讲稿需要手写学术气质 → 推荐 2D / Path C 或 Path D，视觉方向选本风格。
2. **模板**：从 `assets/wanghong/deck-template.html` 复制，引用本地资源：
   ```html
   <link rel="stylesheet" href="wanghong/base.css">
   <link rel="stylesheet" href="wanghong/animations.css">
   <link rel="stylesheet" href="wanghong/neat-annotations.css">
   <link rel="stylesheet" href="wanghong/template.css">
   <script src="wanghong/runtime.js"></script>   <!-- 如需 presenter/overview -->
   ```
   注意：从技能目录复制到项目时，相对路径指向技能内 `assets/wanghong/`；或整体复制 `assets/wanghong/` 到项目 `assets/` 下并改引用。
3. **页面结构**：
   ```html
   <section class="slide" data-title="页面名称">
     <div class="page-heading"><h2 class="hand-title">问题</h2><div class="title-line"></div></div>
     <!-- 内容 -->
     <div class="notes">演讲补充一两句</div>
   </section>
   ```
4. **图表**：SVG 手绘，`stroke-linecap="round"` + wobble 滤镜（`feTurbulence baseFrequency≈0.018 + feDisplacementMap scale≈1.4`），轻微位移保留手画感。
5. **检查**：`python3 scripts/check_deck.py <index.html>`（无此脚本时人工核对：slide 数=notes 数、必需资源齐全）。
6. **渲染 PNG**：运行 `scripts/render_wanghong.sh` 传入 `index.html`、`all` 和输出目录三个参数（Linux/google-chrome）。
7. **时间轴版**：`python3 scripts/build_timeline.py --source <index.html>` → 同目录 `index-timeline.html`，浏览器打开实际翻页测试。

## 八、许可与来源

- HTML/PPT 运行时（base.css/animations.css/runtime.js/timeline.*）：MIT，© 2026 lewis (sudolewis@gmail.com)，许可文本存 `assets/wanghong/HTML-PPT-LICENSE`
- neat-annotations：MIT，© 2026 Maxim Syabro，许可文本存 `assets/wanghong/NEAT-ANNOTATIONS-LICENSE`
- 原始 Skill：`tjxj/z-skills` 仓库 `z-wanghong-handwritten-ppt`，安装命令 `npx -y skills@latest add tjxj/z-skills --skill z-wanghong-handwritten-ppt`
- 风格来源：王虹（21 世纪经济报道 2026-07-28 现场报告），AI 复刻作者「老章很忙」
- 吸收原则：方法论 + 资产吸收，保留 MIT 版权声明，不声明为原创
