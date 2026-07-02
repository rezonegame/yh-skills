# Style Samples Index

> 用途：把 `assets/style-samples/` 中的风格样例图接入 Step 4 风格选择流程。图片用于“给用户看风格长什么样”和“帮助 Agent 校准视觉语言”，不是生成 PPTX/HTML 时自动引用的内容素材。

## 使用规则

- 当用户说“打开风格库 / 看看例子 / 有哪些风格 / 不确定想要什么风格”时，优先读取本文件。
- 推荐 3 个风格时，如果其中风格有样例图，可以把样例图路径一并给出，方便在 Codex 桌面中用 Markdown 图片展示。
- 样例图只作为视觉参考，不作为最终 deck 的图片素材；不要直接把这些图塞进用户 PPT。
- 这些样例大多来自同一页内容的多风格对比，适合横向比较风格 DNA，不适合判断完整 deck 的页型丰富度。
- 若风格用于 `2A / Path A`，需要把视觉语言翻译成可编辑 HTML/PPTX 元素；若用于 `2B / Path B` 或 `2C / Path H`，可作为整图/底图 prompt 的视觉参考。

## 样例图总表

| 风格 | 样例图 | 对应风格文档 | 适合产物 | 用途提示 |
|---|---|---|---|---|
| Snoopy 温暖漫画 | `assets/style-samples/slide04-snoopy.png` | `proven-styles-gallery.md` #1；`proven-styles-snoopy.md` | `2A` / `2B` / `2C` | 教育、品牌、温暖叙事；2C 时底图必须去文字，保留角色和留白 |
| 学習漫画 Manga | `assets/style-samples/slide04-manga.png` | `proven-styles-gallery.md` #2 | `2B` / `2C`；2A 可局部借鉴 | 教程、培训、知识科普；注意不要让底图承担正文 |
| Ligne Claire 清线漫画 | `assets/style-samples/slide04-ligne-claire.png` | `proven-styles-gallery.md` #3 | `2A` / `2B` / `2C` | 流程说明、产品解释；适合高可读插图和清晰留白 |
| Neo-Pop 新波普 | `assets/style-samples/slide04-neo-pop.png` | `proven-styles-gallery.md` #4 | `2B` / `2D`；2A 可弱化 | 年轻受众、活动、产品发布；注意信息密度不要过载 |
| xkcd 白板手绘 | `assets/style-samples/slide04-xkcd.png` | `proven-styles-gallery.md` #5 | `2A` / `2B` | 技术解释、课堂讲解；2A 可用线条、箭头、手绘图表实现 |
| Ian 中文手绘技术解释 | `assets/style-samples/ian-handdrawn-technical-anchor.png` | `ian-handdrawn-technical.md`；`proven-styles-gallery.md` #24 | `2B` / `2C` | 技术解释、教学和方法论；2B 用短而准确的图片文字，精确文字优先 2C |
| 苏联构成主义 | `assets/style-samples/slide04-01-苏联构成主义-constructivism.png` | `proven-styles-gallery.md` #6 | `2B`；2A 可做海报式封面 | 宣言、发布会、强观点；视觉强但不适合长正文 |
| 温暖叙事 | `assets/style-samples/slide04-13-温暖叙事-warm-narrative.png` | `proven-styles-gallery.md` #7 | `2A` / `2B` / `2C` | 品牌故事、服务介绍、用户案例；适合柔和留白 |
| The Oatmeal 信息图漫画 | `assets/style-samples/slide04-oatmeal.png` | `proven-styles-gallery.md` #8 | `2B` / `2C`；2A 可借鉴信息图结构 | 轻松科普、内部分享；注意幽默感不要压过正文 |
| 敦煌壁画 | `assets/style-samples/slide04-10-敦煌壁画-dunhuang.png` | `proven-styles-gallery.md` #9 | `2B` / `2C` | 国风、文化、东方哲学；2C 底图必须预留正文区 |
| 浮世绘 | `assets/style-samples/slide04-02-浮世绘-ukiyo-e.png` | `proven-styles-gallery.md` #10 | `2B` / `2C` | 东方美学、艺术主题；适合强视觉背景或封面 |
| Risograph 孔版印刷 | `assets/style-samples/slide04-04-孔版印刷-risograph.png` | `proven-styles-gallery.md` #11 | `2A` / `2B` / `2D` | 独立出版、年轻品牌；2A 中用色块、颗粒、叠印感近似 |
| Isometric 等轴测 | `assets/style-samples/slide04-05-等轴测-isometric.png` | `proven-styles-gallery.md` #12 | `2A` / `2B` / `2C` | 系统、流程、技术架构；适合做局部示意图或底图 |
| Bauhaus 包豪斯 | `assets/style-samples/slide04-03-包豪斯-bauhaus.png` | `proven-styles-gallery.md` #13 | `2A` / `2B` / `2D` | 设计教育、几何秩序；2A 可用原生形状实现 |
| Blueprint 工程蓝图 | `assets/style-samples/slide04-06-工程蓝图-blueprint.png` | `proven-styles-gallery.md` #14 | `2A` / `2B` / `2C` | 工程、建筑、系统设计；注意投影环境可读性 |
| Vintage Ad 复古广告 | `assets/style-samples/slide04-07-复古广告-vintage-ad.png` | `proven-styles-gallery.md` #15 | `2B` / `2C` | 品牌历史、营销提案、生活方式；不适合严肃数据页 |
| Collage 达达拼贴 | `assets/style-samples/slide04-08-达达拼贴-collage.png` | `proven-styles-gallery.md` #16 | `2B` / `2D`；2A 可局部借鉴 | 创意、文化批评、反常规表达；风险是信息焦点分散 |
| Pixel Art 像素画 | `assets/style-samples/slide04-09-像素画-pixel-art.png` | `proven-styles-gallery.md` #17 | `2B` / `2D` | 游戏、科技、年轻受众；不适合需要细腻中文正文的页面 |

## 推荐展示方式

在 Codex 桌面中可以直接用绝对路径 Markdown 图片展示，例如：

```markdown
![Snoopy 温暖漫画](C:/Users/wudao/.codex/skills/yh-slides/assets/style-samples/slide04-snoopy.png)
```

一次不要展示全部 17 张。推荐流程：

1. 根据主题先选 3 个候选风格。
2. 展示这 3 张样例图。
3. 用户确认方向后，再用该风格做 1-2 页样稿。

## 风格库展开分组

### 教学 / 解释类

- Snoopy 温暖漫画
- 学習漫画 Manga
- Ligne Claire 清线漫画
- xkcd 白板手绘
- The Oatmeal 信息图漫画

### 强视觉 / 发布类

- 苏联构成主义
- Neo-Pop 新波普
- Collage 达达拼贴
- Pixel Art 像素画

### 东方 / 文化类

- 敦煌壁画
- 浮世绘

### 技术 / 系统类

- Isometric 等轴测
- Blueprint 工程蓝图
- Bauhaus 包豪斯

### 品牌 / 叙事类

- 温暖叙事
- Vintage Ad 复古广告
- Risograph 孔版印刷

## 与产物路径的关系

- `2A / Path A`: 样例图用于提取版式、色彩、形状和插画策略；最终应转译为可编辑 HTML/PPTX 元素。
- `2B / Path B`: 样例图用于确定整页图 prompt 的视觉语言；文字可在图里，但必须检查准确性。
- `2C / Path H`: 样例图用于确定无正文文字底图的视觉语言；标题、正文、题目、答案仍由 PPT 文本框承担。
- `2D / Path C-D-E`: 样例图可作为网页视觉方向参考；但 Web/CSS 风格优先参考 `web-styles-gallery.md` 和 magazine 方向包。
