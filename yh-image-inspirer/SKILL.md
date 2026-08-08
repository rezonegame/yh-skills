---
name: yh-image-inspirer
description: |
  This skill should be used for visual-first creation and exploration: finding image references or inspiration, reverse-engineering or improving prompts, exploring styles, or creating standalone posters, photography, illustrations, product imagery, board-game visuals, UI concepts, infographics, brand visuals, and coherent image series. It searches the local case library, applies structured Prompt-as-Code templates and personal preferences, then uses runtime-native image generation when the user requests a final image. Do not use it when an article, post, publishing platform, or content-distribution goal comes first—including article illustrations, any platform-specific social cover or card, social carousels or packages, and cross-platform adaptation; use `yh-social-visual` for those content-first tasks.
---

# YH Image Inspirer

这是一个可独立运行的图片创作 skill。它内置 14 类本地图片提示词案例库和启发式创作流程，同时吸收 `awesome-gpt-image-2` 的结构化模板、变量槽位、防坑约束和 Agent 友好的 Prompt-as-Code 思路。

定位说明：这是一个视觉目标驱动的通用创作工作流。桌面游戏视觉是当前重点强化的专项能力之一，但不是唯一身份；其他专项包括教育图解、品牌营销、出版物、课程封面和独立海报等视觉作品。

核心原则：不要只堆风格词。先确定任务类型和输出形态，再组合案例结构、模板协议、用户偏好和出图约束。

## 与社媒内容视觉的边界

- 当任务从“想做一张什么样的图”出发时，使用本 skill。
- 当任务从“已有内容要发布到哪个平台”出发时，使用 `yh-social-visual`。
- 文字多少不决定路由。独立文字海报仍属于本 skill；无文字的文章插图仍属于 `yh-social-visual`。
- 不从本 skill 调用 `yh-social-visual`，也不接管文章拆解、社媒分页或跨平台内容适配。

## 资源地图

优先按需读取，不要一次性加载所有资源。

| 资源 | 用途 |
| --- | --- |
| `db/INDEX.md` | 14 类本地案例库总索引；先选主库，再按关键词检索对应 `prompt.md` |
| `db/<类型名>/prompt.md` | 内置本地案例库，按类型检索相似案例；优先用 `rg -n "<关键词>"` 定向读取 |
| `db/桌游卡牌与版图/prompt.md` | 桌游卡牌、版图、盒面封面、玩家面板、资源板、组件与规则视觉专题案例库 |
| `references/structured-templates.md` | awesome-gpt-image-2 风格的结构化模板库（29 个模板条目，含 useWhen/guidance/pitfalls） |
| `references/style-library.json` | 可机器读取的风格族与参数注册表；需要结构化选择时读取 |
| `references/variation-engine.md` | 系列图或多方案探索的 5 轴变量设计，避免只换颜色的伪变体 |
| `references/color-engine.md` | 角色化配色、锚色面积和对比度规则 |
| `references/prompt-compiler.md` | 把 brief 编译为可渲染 prompt 的字段与四段式结构 |
| `references/style-avoids.md` | 按风格族选择 Hard Avoids，避免通用负面词堆砌 |
| `references/template-negative-prompts.md` | 模板专项负面约束；只在对应模板命中时读取 |
| `references/ecommerce-scene-templates.md` | 电商全场景结构化 prompt 模板库（25 个场景模板，含触发词、变量槽位、风格变体、品类适配） |
| `references/ecommerce-prompt-methodology.md` | 电商 Prompt 写法五原则、Anti-AI 防坑规则、桌游与文创业品类适配、通用组装公式 |
| `references/awesome-boardgame-cases.md` | 从 awesome-gpt-image-2 精选出的桌游可迁移案例结构 |
| `references/personal-preferences.md` | 用户偏好与本轮测试沉淀的默认规则 |
| `references/output-checklists.md` | 出图前质量检查与常见翻车点 |
| `references/evolution-log.md` | 本 skill 的来源、设计取舍和后续进化记录 |
| `references/source-attribution.md` | 内置参考库与模板来源说明 |
| `references/source-registry.md` | 知识来源主表，升级前先看 |
| `references/absorption-map.md` | 外部来源到本地落点的映射 |
| `references/upstream-gap-tracker.md` | 已吸收 / 未吸收 / 暂不吸收的差距台账 |
| `references/fossil-record.md` | 已否决或被替代方案归档 |
| `references/upgrade-playbook.md` | 升级前自动体检流程 |
| `references/gpt-image2-decision-rules.md` | GPT-Image-2 专项决策规则 |
| `references/gpt-image2-advanced-patterns.md` | GPT-Image-2 高级模式：GST+NP 模式、HUD 叠加规范、拆解图结构、pose grid、storyboard 序列、相机参数、Anti-AI-Slop 清单 |
| `references/edit-workflows.md` | 参考图改造与 edit 工作流模板 |
| `references/template-index.md` | 29 个模板条目的统一元信息索引 |
| `references/featured-cases.md` | 高复用案例快速入口 |
| `references/learning-capture-rules.md` | 会话经验何时落档、落到哪里 |
| `recipes/boardgame-card.md` | 桌游卡牌、实体卡牌、系列卡牌流程 |
| `recipes/boardgame-ui.md` | 桌游玩家面板、资源盘、行动面板、帮助卡流程 |
| `recipes/boardgame-cover.md` | 桌游盒面、封面、扩展包包装流程 |
| `recipes/boardgame-promo.md` | 桌游宣传海报、众筹首图、电商发布图流程 |
| `recipes/boardgame-rulebook.md` | 桌游规则书、玩家帮助卡、组件说明页流程 |
| `recipes/boardgame-crowdfunding.md` | 桌游众筹首屏、详情页长图、版本对比流程 |
| `recipes/ecommerce-poster.md` | 电商展示海报、商品主图、详情页流程 |
| `recipes/series-generation.md` | 同风格批量生成流程 |
| `recipes/infographic.md` | 信息图、科普图、拆解图流程 |
| `recipes/retro-print.md` | 复古版画、图章、旧报纸质感流程；后处理脚本为 `scripts/retro_print.py` |
| `references/poster-design-fundamentals.md` | 海报设计底层原理：视觉层级（3秒法则）、网格系统、排版规范、色彩策略（60-30-10）、印刷制作规范（DPI/CMYK/出血/纸张）|
| `references/poster-artist-styles.md` | 20 位海报设计大师风格指南，含完整 Prompt Modifiers |
| `references/poster-composition-patterns.md` | Mondo 构图模式库（负空间/居中对称/几何框架/层次景深等）|
| `references/poster-genre-templates.md` | 按题材分类的海报 prompt 模板（恐怖/科幻/黑色/公众号/书籍/专辑/旅行/国潮/奢品/食品饮料等）|
| `references/layout-composition-patterns.md` | 100 种排版构图文字化模式库（分法/九宫格/黄金分割/框架/网格/透视/动线/对比等），用于把参考图转成 Agent 可调用的版式骨架 |
| `references/layout-composition-images/` | `nevertoday/100-layout-compositions` 的完整本地参考图：100 张高清原图、100 张缩略图、索引和总览图，CC BY 4.0 |
| `references/awesome-images/` | 精选离线参考图（61 张），按模板分类：travel/guochao/luxury/food-bev/beauty/breakdown/history + open-design（22 张：game-screenshot/exploded-view/choreography/social-media/cultural/anime），含 INDEX.md 索引 |
| `references/adoption-decisions.md` | 维护时审查外部方法吸收、测试和回滚边界 |


## 升级前体检与来源治理

未来维护者升级本 skill 时，默认先查看：

- `references/source-registry.md`
- `references/absorption-map.md`
- `references/upstream-gap-tracker.md`
- `references/fossil-record.md`

如果只是上游已有知识的本地重复表达，优先更新台账、索引和 gap 状态，而不是重复新增文档。

涉及 GPT-Image-2 专项任务时，优先补读 `references/gpt-image2-decision-rules.md`；涉及参考图改造时，优先补读 `references/edit-workflows.md`。

## 导演阶段：从 brief 到 prompt

在真正生成或编辑图片前，按需完成以下编译链；简单任务可以合并步骤，但不能丢掉约束：

1. 读取 `references/contracts/asset-intent.md`，锁定 generate/edit 模式、目标路径、保留项与覆盖权限。
2. 多方案或系列任务读取 `references/variation-engine.md`，明确哪些轴锁定、哪些轴允许变化。
3. 需要精确配色时读取 `references/color-engine.md`，为颜色分配功能角色和面积，而不是只写“高级感配色”。
4. 使用 `references/prompt-compiler.md` 把画布、注意力结构、主体锚点、排版、色彩、质感、情绪和 Hard Avoids 编译成连续的画面描述。
5. 从 `references/style-avoids.md` 选择对应风格族的避免项；不要把所有负面词一次性塞进 prompt。

不要复制压缩包中的原始上游图片集：本地 `db/` 已按语义分类且包含大量同源素材。新增案例只有完成来源、用途和分类登记后才进入本地库。


## 库级 Metadata 与多库交叉规则

检索任何 db/<分类名>/prompt.md 前，先读取文件顶部的 ## Metadata，确认该库是否适合当前任务。Metadata 是库级路由索引，不替代案例正文；它用于判断主库、辅助库、必要槽位、默认值和必须确认项。

多库交叉默认采用 **1 个主库 + 最多 2 个辅助库 + 必要 recipe**：

1. **主库** 由最终交付物决定。例如最终要海报，就以 db/海报与排版/ 为主库；最终要 UI，就以 db/UI与界面/ 为主库。
2. **第一辅助库** 由画面主体决定。例如主体是商品、人物、空间、历史题材或图表结构。
3. **第二辅助库** 由风格来源或信息结构决定。例如插画风格、摄影质感、品牌系统、信息图模块。
4. **必要 recipe** 不计入辅助库数量。涉及卡牌、系列图、电商图、信息图、桌游宣传图、桌游封面、规则书等固定流程时，必须读取对应 recipe。

常见组合：

- 游戏外盒做线下宣传海报：主库 `db/海报与排版/`；辅助库 `db/桌游卡牌与版图/`；recipe 使用 `recipes/boardgame-promo.md`、`recipes/boardgame-cover.md`，必要时补 `recipes/ecommerce-poster.md`。
- 桌游卡牌系列：主库 `db/桌游卡牌与版图/`；recipe 使用 `recipes/boardgame-card.md` + `recipes/series-generation.md`；按主体补 `db/人物与角色/`、`db/UI与界面/` 或 `db/海报与排版/`。
- 商品参考图做电商海报：主库 `db/商品与电商/`；recipe 使用 `recipes/ecommerce-poster.md`；必要时补 `db/海报与排版/` 或 `db/图表与信息可视化/`。
- 产品详情页信息图：主库 `db/商品与电商/` 或 `db/图表与信息可视化/`，按最终交付物决定；recipe 使用 `recipes/ecommerce-poster.md` + `recipes/infographic.md`。
- 古风人物设定：主库 db/人物与角色/；辅助库 db/历史与古风题材/、db/插画与艺术/。
## 类型路由表
根据用户关键词定位案例库和可能的 recipe。

| 用户关键词 | 案例目录 | 优先补充模板 |
| --- | --- | --- |
| 桌游/桌面游戏/Board game/卡牌游戏/实体卡牌/牌面/版图/地图板/桌游封面/盒面/包装/扩展包封面/游戏组件/玩家面板/资源板/游戏盒/规则书/帮助卡/众筹首图/详情页 | `db/桌游卡牌与版图/`；宣传、电商、规则书再按交付物补 `db/海报与排版/`、`db/商品与电商/`、`db/图表与信息可视化/` | `references/awesome-boardgame-cases.md` + 对应桌游 recipe |
| 界面/App/网页/UI/手机 | `db/UI与界面/` | `structured-templates.md#ui` |
| 截图/社媒截图/App截图/小红书截图/抖音截图 | `db/UI与界面/` | `structured-templates.md#ui-截图生成` |
| 直播/直播间/电商直播/才艺直播 | `db/UI与界面/` | `structured-templates.md#ui-直播界面` |
| 海报/排版/封面/Campaign/宣传/构图/版式 | `db/海报与排版/` | `references/poster-design-fundamentals.md` + `structured-templates.md#poster` + `references/layout-composition-patterns.md` + `references/poster-artist-styles.md` |
| 概念字体海报/字体设计海报/文字海报/typography poster | `db/海报与排版/` | `structured-templates.md#概念字体海报` |
| 运动海报/运动品牌/运动员海报/体育Campaign | `db/海报与排版/` | `structured-templates.md#运动商业campaign-海报` |
| 自然科普/物种海报/Apple keynote风格科普 | `db/海报与排版/` + `db/图表与信息可视化/` | `structured-templates.md#自然科普海报` |
| 水墨双重曝光/水墨人像/诗意肖像海报 | `db/海报与排版/` + `db/插画与艺术/` | `structured-templates.md#水墨双重曝光肖像海报` |
| 签名设计/签名选择/签名练习 | `db/海报与排版/` | `structured-templates.md#签名设计系统` |
| Mondo/丝网印刷/限量版/Olly Moss/Tyler Stout/复古海报/电影海报/书籍封面/专辑封面 | `db/海报与排版/`（Mondo专题案例）| `references/poster-artist-styles.md` + `references/poster-composition-patterns.md` + `references/poster-genre-templates.md` |
| 信息图/图表/可视化/拆解/图解/科普 | `db/图表与信息可视化/` | `recipes/infographic.md` |
| 科学缩放/比例尺缩放/微观到宏观/scale diagram | `db/图表与信息可视化/` | `structured-templates.md#科学比例尺缩放信息图` |
| 插画/漫画/二次元/动漫/手绘/水墨/水彩 | `db/插画与艺术/` | `structured-templates.md#illustration` |
| 摄影/写实/人像/写真/自拍/时尚大片 | `db/摄影与写实/` | `structured-templates.md#photo` |
| 街拍/抓拍/街头摄影/手机摄影/candid/street photo | `db/摄影与写实/` | `structured-templates.md#街拍抓拍摄影` |
| 电商/商品/详情页/淘宝/产品图/广告/展示海报 | `db/商品与电商/` | `recipes/ecommerce-poster.md` + `references/ecommerce-scene-templates.md` + `references/ecommerce-prompt-methodology.md` |
| 古风/历史/朝代/国潮/汉服/新中式 | `db/历史与古风题材/` | `structured-templates.md#历史与古风题材` + `references/poster-genre-templates.md` → `## 国潮/新中式（Chinese Modern）` |
| Logo/品牌/标志/VI/字体/图标 | `db/品牌与标志/` | `structured-templates.md#brand` |
| 品牌触点/品牌应用/VI应用/品牌视觉板 | `db/品牌与标志/` | `structured-templates.md#品牌触点系统视觉板` |
| 品牌广告/品牌信封/同品牌不同产品 | `db/品牌与标志/` | `structured-templates.md#品牌信封产品广告` |
| 品牌人设/品牌性格/品牌漫画 | `db/品牌与标志/` | `structured-templates.md#品牌人设漫画信息图` |
| 建筑/室内/空间/城市/地标 | `db/建筑与空间/` | `structured-templates.md#space` |
| 角色/人物/卡牌/动作分解/设定/游戏卡/资源卡/事件卡 | `db/人物与角色/` | `recipes/boardgame-card.md` |
| 动作分解/姿势参考/动作参考表/pose grid | `db/人物与角色/` | `structured-templates.md#动作分解参考表` + `references/gpt-image2-advanced-patterns.md#4-pose-grid` |
| 游戏截图/游戏UI/HUD/游戏界面/ARPG/MMO | `db/UI与界面/` + `db/桌游卡牌与版图/` | `references/gpt-image2-advanced-patterns.md#2-hud-叠加规范` |
| 组件拆解/爆炸图/盒内物料/组件展示 | `db/桌游卡牌与版图/` + `db/图表与信息可视化/` | `references/gpt-image2-advanced-patterns.md#3-拆解图结构化规范` |
| 连拍/分镜/8连拍/storyboard/系列姿态 | `db/人物与角色/` | `references/gpt-image2-advanced-patterns.md#5-storyboard-序列` |
| 潮玩/3D玩具/收藏玩具/blind box/公仔 | `db/人物与角色/` + `db/商品与电商/` | `structured-templates.md#3d-收藏玩具` |
| 文档/杂志/菜单/报纸/课本/药方/笔记 | `db/文档与出版物/` | `structured-templates.md#publication` |
| 场景/叙事/电影感/分镜/故事 | `db/场景与叙事/` | `structured-templates.md#scene` |
| 旅行海报/travel poster/复古旅行/城市海报/vintage travel | `db/海报与排版/` + `db/建筑与空间/` | `references/poster-genre-templates.md` → `## Travel Poster（旅行海报）` |
| 奢品广告/奢华海报/luxury campaign/高端品牌/香水广告/时尚大片 | `db/商品与电商/` + `db/海报与排版/` | `references/poster-genre-templates.md` → `## Luxury Product Campaign（奢品广告）` |
| 食品饮料海报/food poster/飞溅/商业美食/产品宣传 | `db/商品与电商/` + `db/海报与排版/` | `references/poster-genre-templates.md` → `## Food & Beverage Commercial（食品饮料商业海报）` |
| 美妆推荐/肤质报告/美妆报告/beauty report/导购卡片 | `db/商品与电商/` | `structured-templates.md#个性化美妆报告` |
| 产品研发/拆解图/breakdown/研发板/组件展示 | `db/图表与信息可视化/` + `db/商品与电商/` | `structured-templates.md#概念产品研发拆解` |
| 创意合成/趣味/跨界/搞笑/混搭 | `db/其他应用场景/` | `structured-templates.md#creative` |


## 全局出图标准流程门禁

凡是用户要求“作图”“出图”“生成图片”“输出图像”“直接画”“设计图片”“生成海报”“生成卡牌”“生成界面”“生成信息图”等任何图像结果时，必须先走标准流程，不允许直接跳到图像生成、脚本拼版或素材重排。

出图前必须完成以下 7 个检查点，并在内部或简短对用户说明中明确落实：

1. **任务类型判定**：先判断输出属于海报、卡牌、UI、信息图、商品图、包装、封面、插画、摄影图、系列图或其他类型；根据类型读取对应 recipe 或结构化模板。
2. **信息槽位填充**：明确主题、主体、用途、比例、语言、画面文字、必须保留元素、允许变化元素、禁止事项；如果关键信息不足且没有合理默认值，最多问 1-3 个问题。
3. **参考结构选择**：读取并迁移相应案例库、recipe、structured template 或参考文件中的“结构”和“约束”，不得只堆风格词。
4. **视觉系统锁定**：确定构图、层级、配色、字体/字感、材质、边框、标签、留白、主体位置；系列图必须先锁定统一视觉系统，再改变有限变量。
5. **结构化 prompt 或制作 brief**：在实际出图前，先形成完整的结构化 prompt / design brief，包含主体、版式、文字、风格、质量要求和避免项。
6. **输出检查表自检**：调用 `references/output-checklists.md` 中对应类型检查，确认中文可读、文字不过量、主体识别保留、比例正确、没有样机/水印/二维码/价格等未要求元素。
7. **用户确认 brief**：凡是最终要作图、出图或生成图片，默认先输出用户可读 brief，展示任务、保留锚点、画面结构、文案、风格、禁忌和待确认项；用户最多调整 2 轮，确认后再生成最终 prompt 快照并调用图像生成。用户明确说“直接生成/不用确认”且信息足够时，可以跳过。

硬性规则：

- 未完成以上流程，不得调用图像生成能力，也不得直接用脚本拼版作为最终交付。
- 用户提供参考图时，必须把参考图当作严格参考；先列出必须保留的 3-5 个识别锚点。
- 如果因为时间或工具限制只能做快速草稿，必须明确标注“草稿/快速拼版”，不能把它等同于标准流程产物。
- 默认简体中文画面文字；除非用户明确要求，不主动加入英文标题、英文标签、价格、二维码、水印、平台 logo。

## 工作流总控

### 1. 用户要找灵感或案例

当用户说“有没有案例”“找灵感”“类似图片怎么写”“参考一下”：

1. 根据类型路由表选择 `db/<类型名>/prompt.md`。
2. 用关键词检索 3-5 个相近案例。
3. 输出案例标题、来源路径、参考图、核心结构、可迁移点。
4. 参考图应尽量用 Markdown 图片语法展示；在本地环境中使用绝对路径，避免相对路径无法渲染。
5. 不要直接长篇复制所有案例。只摘取必要提示词片段，并说明如何迁移到用户需求。

### 2. 用户要写提示词或优化提示词

当用户说“帮我写提示词”“优化 prompt”“这张图怎么生成”：

1. 识别任务类型、输出形态、比例、语言、主体、用途。
2. 读取相应案例库和结构化模板。
3. 如果任务明确面向 GPT-Image-2 或高度依赖该模型特性，同时读取 `references/gpt-image2-decision-rules.md`。
4. 如果任务属于参考图修改、局部替换、保主体改风格或重组，则转入 `references/edit-workflows.md` 对应模板。
5. 输出一个可直接用于图像模型的完整 prompt。
6. 说明参考了哪些案例结构和模板槽位。

### 3. 用户要作图、生成图片或输出图像

当用户明确说“作图”“出图”“生成图片”“输出图像”“直接画”：

1. 判断信息是否足够。
2. 如果缺少会显著影响结果的关键信息，最多问 1-3 个问题；如果已有合理默认值，就直接补齐。
3. 按库级 Metadata 判断主库、辅助库和必要 recipe，读取相应案例结构与检查表。
4. 如果任务明确依赖 GPT-Image-2 的文字控制、镜头参数、模板适配判断或 A/B 策略，额外读取 `references/gpt-image2-decision-rules.md`。
5. 如果任务本质是“改图”而不是“重新作图”，先读取 `references/edit-workflows.md`，列出识别锚点，再写 `Change` / `Preserve`。
6. 先形成用户可读 brief；默认等待用户确认，允许最多 2 轮调整。
7. 用户确认后，生成最终结构化 prompt 快照。
8. 调用运行时原生图像生成能力直接出图（无需脚本、无需 API key）。
9. 如果原生能力不可用或生成失败，保留完整 prompt 并如实说明失败；不要自动切换到 API、CLI 或其他本地生图 skill。
10. 不要在图像生成后追加多余说明，除非用户要求复盘或改图。

必要信息通常包括：

- 输出形态：正面设计图、效果图、海报、详情页、信息图、UI 截图、摄影图等。
- 主体：产品、人物、卡牌、图标、场景、概念。
- 语言：默认简体中文，除非用户要求英文或双语。
- 比例：若未指定，按场景默认。电商海报 4:5 或 3:4，卡牌正面 2:3 或 3:4，信息图 9:16，社媒海报 4:5。
- 约束：是否保留参考图、是否禁止样机、是否需要统一系列风格。

### 4. 用户要批量生成同系列

当用户说“同风格生成 N 张”“不同名字生成一组”“系列卡牌/系列海报”：

1. 读取 `recipes/series-generation.md`。
2. 先锁定统一视觉系统：画幅、配色、字体、边框、材质、构图、信息层级。
3. 为每张图改变有限变量：名称、主体图标、数值、规则、卖点或场景。
4. 每张图都重复核心一致性约束，避免风格漂移。

### 5. 用户做桌面游戏相关视觉

当用户需求涉及桌游、桌面游戏、卡牌游戏、游戏盒、桌游封面、盒面、扩展包包装、玩家面板、游戏组件、规则说明、众筹首图、电商图时：

1. 先读取 `references/awesome-boardgame-cases.md`，选择可迁移专题。
2. 根据具体对象读取对应 recipe：
   - 卡牌：`recipes/boardgame-card.md`
   - UI/玩家面板/帮助卡：`recipes/boardgame-ui.md`
   - 盒面/封面/扩展包：`recipes/boardgame-cover.md`
   - 宣传海报/电商/众筹图：`recipes/boardgame-promo.md`，必要时再读 `recipes/ecommerce-poster.md`
   - 规则书/玩家帮助卡/组件说明：`recipes/boardgame-rulebook.md`
   - 众筹首屏/详情页长图/版本对比：`recipes/boardgame-crowdfunding.md`
   - 规则机制图：`recipes/infographic.md`
3. 再检索 `db/桌游卡牌与版图/prompt.md` 中相近案例；如果主体或交付物需要，再补读人物、UI、海报、电商或信息图库。
4. 默认中文画面文字。默认区分牌面正面图、版图俯视图、玩家面板、效果图、宣传海报，不混用。

### 6. 用户要补充或沉淀案例

当用户说“把这个加入案例库”“保存成案例”“沉淀到 skill”“以后也这样做”：

1. 先确认案例归属类型，对照类型路由表选择 `db/<类型名>/`。
2. 如果是图片案例，确认图片文件来源和可保存路径；不要移动或删除用户原图。
3. 追加写入对应 `db/<类型名>/prompt.md`，包含案例标题、来源说明、提示词、可迁移结构和注意事项。
4. 如果有参考图，复制到对应 `images/` 目录，使用下一个合理编号或语义化文件名，避免覆盖已有图片。
5. 如果案例体现的是用户偏好或流程规则，优先更新 `references/personal-preferences.md`、`references/output-checklists.md` 或相关 `recipes/`，而不是只塞进 prompt 案例。
6. 如果这次沉淀涉及外部来源吸收或已吸收差异，优先同步更新 `references/source-registry.md`、`references/absorption-map.md` 或 `references/upstream-gap-tracker.md`。
7. 如果这次沉淀是否决了某种旧思路，更新 `references/fossil-record.md`。
8. 追加 `references/evolution-log.md`，记录这次沉淀的原因、来源、变更文件和下一步观察点。


## 出图前强确认流程

强确认默认只用于最终要生成图片的任务，不用于纯案例检索或纯提示词编写。确认目标是提高成图方向命中率，而不是把内部检索细节全部交给用户。

### 用户可读 brief

`markdown
## 出图前确认 brief

任务类型：
输出形态：
比例：
语言：

需要保留：
1.
2.
3.

画面结构：
- 主视觉：
- 背景：
- 信息层级：
- 文案区域：

画面文字：
- 主标题：
- 副标题：
- 卖点：
- 行动信息：

风格方向：

禁止事项：

待确认：
1.
2.
`

规则：

- 用户可读 brief 保持一屏内可确认，不要长篇解释内部推理。
- 内部可以保留主库、辅助库、recipe、metadata 槽位和检查表，但无需全部展示给用户。
- 用户最多调整 2 轮 brief；第二轮后应收敛为最终 prompt 快照。
- 用户确认后，必须基于确认内容生成最终 prompt，不临时加入新的方向。
- 用户明确说“直接生成/不用确认/不要问我”且信息足够时，可以跳过强确认。

### 线下与印刷海报专项

当用户提到线下宣传、张贴、展会、印刷、A3、A2、传单、易拉宝等场景：

- 先读取 `references/poster-design-fundamentals.md` 中的印刷制作规范（DPI、CMYK、出血、纸张）和视觉层级法则。
- 默认应用 `references/output-checklists.md` 中的 3 秒法则和印刷意图检查。
- 未指定尺寸时，默认竖版 A3/A2 海报感，比例 3:4 或 4:5。
- 文字控制为 1 个主标题、1 个副标题、3 个短标签或少量活动信息。
- 高对比、远距离可读，避免小字号密集说明。
- 二维码默认不生成。用户未提供二维码素材时，只预留“二维码占位区”；用户提供二维码图时，作为严格参考素材保留；用户不要求二维码时，不主动加入。
## 输出格式
### 案例搜索输出

```markdown
## 搜索结果：[类型]

找到 [N] 个可迁移案例：

### 例 [编号]：[标题]
来源：`db/<类型>/prompt.md`
参考图：
![参考图](/absolute/path/to/db/<类型>/images/caseXX.jpg)
可迁移结构：[一句话]
适合迁移到：[用户场景]

下一步建议：[基于某案例二次创作 / 继续缩小方向]
```

### 提示词输出

```markdown
## 定制提示词

类型：[类型]
输出形态：[正面设计图/海报/详情页/信息图等]
比例：[比例]
语言：[简体中文/英文/双语]

```text
[完整提示词]
```

参考结构：
- 案例：[db 路径和例号]
- 模板：[reference 或 recipe]

质量约束：
- [关键约束 1]
- [关键约束 2]
```

## 默认偏好

读取 `references/personal-preferences.md`。尤其注意：

- 默认使用简体中文作为画面文字。
- 用户说卡牌时，先区分“牌面正面图”和“产品效果图”；没有说明时优先牌面正面图。
- 用户给参考产品图时，必须保留产品识别，不要改成其他产品。
- 电商展示海报要有信息层级，而不是只做产品摆拍。
- 批量系列图要强制锁定统一视觉系统。

## 出图前自检

生成 prompt 或调用图像生成前，读取 `references/output-checklists.md` 中对应类型检查表。至少检查：

- 类型和输出形态是否明确。
- 画面语言是否符合用户要求。
- 文字是否少量、清晰、可读。
- 是否禁止了不想要的形态，比如样机、桌面摆拍、手机界面、英文文字。
- 参考图中的产品、角色、包装识别是否被保留。

对于高价值视觉方向、系列图系统、品牌图、桌游视觉或多轮 brief 后仍不确定的方案，可在出图前调用 `autoreason-review` 做方向质量门：将当前 brief/prompt 作为 `A`，只针对真实问题生成 `B`，再生成综合稿 `AB`；重点评审主体识别、画面结构、风格一致性、文字克制和用户约束。不要用它替代参考图识别、输出检查表或实际成图 QA。
