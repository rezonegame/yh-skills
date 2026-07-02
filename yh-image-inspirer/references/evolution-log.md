# Evolution Log

记录 `yh-image-inspirer` 的来源、设计取舍和后续进化线索。每次对 skill 的能力、偏好、案例库或 recipe 做重要调整，都追加一条记录。

## 目录

- v0.1：初始融合与能力补齐
- v0.2：桌游、规则书和众筹增强
- v0.3：模板、案例库和自检
- v0.4：来源治理与升级体检
- 后续：海报、电商、构图与执行边界整合

## 2026-05-01 v0.1.0 初始融合版

### 目标

创建一个可独立运行的通用视觉生成工作流 skill。它内置本地图片提示词案例库，吸收 `awesome-gpt-image-2` 的结构化提示词能力，并加入用户自己的作图偏好。

### 来源

- 本地图片提示词案例库
  - 内置完整 `db/` 案例库。
  - 内置 13 大类路由：UI、海报、信息图、插画、摄影、电商、古风、品牌、建筑、角色、文档、场景、创意应用。
  - 内置搜索案例、模糊启发、二次创作的基本工作流。

- `awesome-gpt-image-2`
  - 吸收 Prompt-as-Code 思路。
  - 将视觉生成任务拆成结构化槽位：类型、主体、布局、比例、文案、风格、材质、约束。
  - 提炼成 `references/structured-templates.md`，覆盖 UI、海报、电商、信息图、卡牌、品牌、摄影、出版物、空间、场景、创意、插画。

- 用户实测反馈
  - 卡牌场景中，“卡牌”默认应优先理解为牌面正面图，而不是桌面摆拍或产品效果图。
  - 卡牌牌面信息默认使用简体中文。
  - 同系列卡牌必须锁定统一视觉系统，每张只改变有限变量。
  - 参考产品图用于电商海报时，必须保留产品识别，不要改成其他产品。
  - 电商展示海报应包含标题、副标题、卖点、行动区和商品主体，而不是只生成商品效果图。

### 新增文件

- `SKILL.md`：替代版总控工作流。
- `references/structured-templates.md`：结构化模板库。
- `references/personal-preferences.md`：用户偏好规则。
- `references/output-checklists.md`：出图前检查表。
- `recipes/boardgame-card.md`：桌游卡牌工作流。
- `recipes/ecommerce-poster.md`：电商海报工作流。
- `recipes/series-generation.md`：同风格批量生成工作流。
- `recipes/infographic.md`：信息图工作流。

### 设计取舍

- 不直接把 `awesome-gpt-image-2` 的 367 个案例全部并入 `db/`，避免案例库膨胀和重复。
- 优先吸收它的结构化模板与防坑逻辑，用作内置本地案例库上方的“模板引擎”。
- 将本地案例库作为稳定案例基础，确保 skill 不依赖外部 skill 目录即可运行。

## 2026-05-01 v0.1.1 完整替代补齐

### 触发原因

对比独立版目标和早期版本后发现两个小缺口：

1. 原版有“补充案例”能力，新版未明确写入。
2. 原版搜索案例会展示参考图，新版只写参考图路径。

### 更新

- 在 `SKILL.md` 增加“用户要补充或沉淀案例”流程。
- 在案例搜索输出模板中要求尽量用 Markdown 图片语法展示参考图。
- 在资源地图中加入本文件，明确后续演进记录位置。

### 后续观察点

- 是否需要把 `awesome-gpt-image-2` 中高价值案例按类别精选并加入 `db/`，而不只是保留模板。
- 是否需要建立 `evals/`，用固定测试提示评估 skill 触发和输出质量。
- 是否需要增加更多专用 recipe，例如包装设计、品牌视觉板、社媒截图、中文课程封面、公众号首图。

## 2026-05-01 v0.2.0 桌面游戏专题增强

### 触发原因

用户明确主要工作方向是桌面游戏相关视觉：

- 桌面游戏卡牌设计
- 桌面游戏 UI 设计
- 桌面游戏封面设计
- 桌面游戏电商图设计
- 桌面游戏宣传海报设计

因此对 `awesome-gpt-image-2` 做面向桌游工作的精选整合，而不是全量导入。

### 整合方式

新增 `references/awesome-boardgame-cases.md`，把 awesome 中适合桌游迁移的案例抽象成结构专题。

重点吸收的案例结构：

- case 166：多卡面统一系列 -> 桌游卡牌套组、卡牌合集图。
- case 323：实体化 UI -> 玩家面板、资源盘、实体 UI 组件。
- case 333：爆炸拆解图 -> 桌游组件拆解、盒内物料展示。
- case 334：技术详解图 -> 桌游机制讲解、回合流程图。
- case 342：四季包装 Campaign 宫格 -> 扩展包、阵营盒、系列包装。
- case 344：单产品 Campaign 海报 -> 桌游盒主视觉宣传图。
- case 347：4x4 动作分解表 -> 玩家帮助卡、动作说明表。
- case 354：Logo 与品牌身份系统 -> 桌游品牌、LOGO、系列视觉。
- case 355：概念字体海报 -> 桌游标题主导封面。
- case 362：品牌触点系统视觉板 -> 桌游产品线视觉板。
- case 365：收藏级玩具发布板 -> 豪华版、组件、开箱发布图。
- case 367：奢华产品广告 -> 高端桌游盒广告。

### 新增 recipe

- `recipes/boardgame-ui.md`
  - 玩家面板、资源盘、行动面板、回合轨、帮助卡。
  - 默认区分可印刷正面图、实体组件效果图、数字 App UI、规则信息 UI。

- `recipes/boardgame-cover.md`
  - 桌游盒面、封面主视觉、扩展包封面、系列包装。
  - 默认区分盒面正面设计图、完整盒子效果图、宣传封面海报、系列包装宫格。

- `recipes/boardgame-promo.md`
  - 宣传海报、众筹首图、电商详情页首屏、小红书种草图、发行 Campaign。
  - 支持单盒强主视觉、组件铺陈、豪华版发布、玩法卖点、众筹首图。

### SKILL.md 更新

- 在资源地图加入 `awesome-boardgame-cases.md` 和 3 个桌游 recipe。
- 在类型路由表加入桌游总入口。
- 增加“用户做桌面游戏相关视觉”流程，要求先读桌游精选索引，再读对应 recipe，最后检索原 `db/` 案例。

### 设计取舍

- 不把 awesome 案例原文和图片全量复制进 `db/`。
- 只抽取适合桌游工作的结构模式，避免案例库噪音变大。
- 桌游任务优先以“输出形态”路由：卡牌、UI、封面、电商、宣传、规则机制图。

### 后续观察点

- 可以继续补 `recipes/boardgame-rulebook.md`，用于规则书页面、玩家帮助卡和说明书视觉。
- 可以补 `recipes/boardgame-crowdfunding.md`，用于 Kickstarter/摩点/众筹详情页长图。
- 如果某些 awesome 案例在实战中反复使用，再将其精选图文沉淀到本地 `db/`。

## 2026-05-01 v0.2.1 规则书与众筹长图补齐

### 触发原因

延续 v0.2.0 的后续观察点，补齐桌游生产中两类常见但容易被普通“海报/信息图”混淆的任务：

- 规则书页面、玩家帮助卡、组件说明页。
- 众筹首屏、详情页长图、版本对比图。

### 新增 recipe

- `recipes/boardgame-rulebook.md`
  - 覆盖规则书单页、玩家帮助卡、规则摘要海报、组件说明页、教学流程图。
  - 默认输出可印刷的正面页面设计图，不做桌面摆拍。
  - 强调规则书服务“理解”，而不是追求海报冲击力。
  - 使用短句、编号、图标、模块化布局，避免把规则书正文塞进图片。

- `recipes/boardgame-crowdfunding.md`
  - 覆盖众筹首屏、详情页长图、豪华版发布页、玩法解释长图、版本对比图。
  - 将众筹页结构定义为“吸引 -> 可信 -> 会玩 -> 有料 -> 想买”。
  - 强调组件图和玩法图比单纯氛围图更能转化。

### SKILL.md 更新

- 在资源地图加入 `boardgame-rulebook.md` 与 `boardgame-crowdfunding.md`。
- 在桌游路由中加入规则书、帮助卡、详情页。
- 在桌游工作流中明确：
  - 规则书/帮助卡/组件说明 -> `boardgame-rulebook.md`
  - 众筹首屏/详情页长图/版本对比 -> `boardgame-crowdfunding.md`

### 后续观察点

- 可以补 `recipes/boardgame-components.md`，专门处理 token、米宝、棋盘、收纳、3D 组件和 punchboard。
- 可以补 `recipes/boardgame-localization.md`，专门处理中文化、美术字、规则文本压缩和双语版式。

## 2026-05-01 v0.2.2 主身份澄清

### 触发原因

用户指出：`yh-image-inspirer` 不是一个专门的桌游视觉生成工作流 skill。它首先是一个通用视觉生成工作流 skill，只是当前强化了“桌游视觉”这个专项能力。

### 定位修正

- 主身份：通用视觉生成工作流 skill。
- 基础能力：案例检索、结构化提示词、作图引导、参考图保真、批量同风格生成、案例沉淀。
- 专项能力：桌游视觉只是当前最重要的垂直模块之一。
- 后续演进：可以继续添加其他专项模块，例如教育可视化、品牌营销图、电商详情页、公众号封面、出版物版式、课程视觉等。

### SKILL.md 更新

- 在开头加入定位说明，明确桌游不是唯一身份，避免后续迭代把通用视觉生成能力收窄成桌游专用能力。

## 2026-05-01 v0.2.3 独立本地参考库

### 触发原因

用户要求：本地参考库也一同放入此技能，需要完整脱离外部 `image-inspirer` skill。

### 更新

- 确认 `db/` 已完整内置 13 个分类目录和对应参考图。
- 将 `SKILL.md` 中“替代/原库”一类表述改为“可独立运行/内置本地案例库”。
- 新增 `references/source-attribution.md`，记录内置案例库和结构化模板的来源与维护边界。
- 移除 `README-image-inspirer-origin.md` 备份文件，避免 skill 内部继续出现外部安装命令和原项目说明造成依赖感。

### 设计取舍

- 保留来源归因，但不保留原项目 README 作为运行资源。
- 运行时所有案例检索都指向当前 skill 内部的 `db/`。
- 后续新增案例应直接沉淀到当前 skill 的 `db/`、`references/` 或 `recipes/`，不再写回外部 skill。

## 2026-05-11 v0.3.0 新模板吸收与结构化增强

### 触发原因

对比 `awesome-gpt-image-2` 上游仓库（4.9k stars，420 案例，22+ 模板）发现上游在上次吸收后新增了多个高价值模板，并将每个模板从"纯槽位"升级为带 `useWhen`/`guidance`/`pitfalls` 的智能模板。

### 更新内容

**新增 13 个模板**（structured-templates.md）：

- UI 类（+2）：截图生成模板（平台专属 UI 特征）、直播界面模板（电商 vs 才艺）
- 海报类（+5）：中文概念字体海报、运动商业 Campaign 海报、自然科普海报（Apple keynote 风格）、水墨双重曝光肖像海报、签名设计系统（三合一）
- 品牌类（+3）：品牌触点系统视觉板、品牌信封产品广告（四阶段流水线）、品牌人设漫画信息图
- 摄影类（+1）：街拍抓拍摄影（手机视角、禁止 CGI）
- 角色类（+2）：动作分解参考表（4×4 网格）、3D 收藏玩具
- 信息图类（+1）：科学比例尺缩放信息图（6-8 级微观→宏观）

**现有 12 个模板结构化增强**：

为每个现有 JSON 模板增加 `useWhen`、`guidance`、`pitfalls` 三个字段，内容来自上游 style-library.json 和 output-checklists.md。

**output-checklists.md 新增检查表**：

- UI 截图检查（平台特征、中文文字、UI 层级）
- 直播界面检查（主播完整性、UI 不遮挡、平台特征）
- 概念字体海报检查（标题拼写、字体作为主角、禁止项）
- 街拍摄影检查（自然感、禁止 CGI、手机视角）

**SKILL.md 路由表扩展**：

- 从 16 行扩展到 32 行，覆盖所有新模板的关键词映射
- 资源地图更新：structured-templates.md 描述更新为"25 个模板"

### 设计取舍

- 只做模板扩充和结构化增强，不动索引体系和架构。
- 不引入 style-library.json 全局索引、style/scene 标签系统、双语元数据——这些是代码组织优化，对使用方法和产出效果影响很小，但改动成本高。
- 保持自包含设计：所有内容完整内嵌，零外部依赖。
- 暂不吸收 P2 长尾模板（美妆推荐报告、产品研发拆解板），后续按需补充。

### 后续观察点

- P2 模板（美妆推荐报告、产品研发拆解板）是否有实际使用场景。
- 新模板的 guidance/pitfalls 在实战中是否有效减少翻车。
- 是否需要为新模板补充对应的 recipe 工作流。
- 是否需要将部分新模板的典型案例沉淀到 `db/` 中。

## 2026-05-11 v0.3.1 桌游卡牌与版图专题库接入

### 触发原因

用户在 `db/` 中新增了“桌游卡牌与版图”文件夹，并放入 30 张桌游卡牌、玩家面板和版图参考图，需要按现有案例库结构补全索引，并让技能路由优先使用该专题库。

### 更新内容

- 新增 `db/桌游卡牌与版图/prompt.md`，包含库级 Metadata、30 个案例条目和使用提示。
- 案例覆盖：角色职业卡矩阵、技能卡、怪物/事件/法术/资源牌、玩家面板、儿童路径板、复古路径板、叙事地图、迷宫、六边形地形、科幻设施、地牢、村庄、城市路线、海岛、奇幻大陆和大型乐园路线版图。
- 更新 `SKILL.md` 的资源地图、桌游常见组合、类型路由表和桌游专项流程，让桌游相关需求先检索 `db/桌游卡牌与版图/`，再按交付物补读人物、UI、海报、电商或信息图库。
- 更新 `references/source-attribution.md`，将内置案例库数量从 13 类改为 14 类，并加入“桌游卡牌与版图”。

### 设计取舍

- 不为 30 张图虚构外部来源，统一标注为“用户新增本地参考图”。
- 每个案例提供可迁移的结构化复刻提示词，而不是只描述图片外观。
- 将“版图”明确约束为可玩结构：俯视正交、路径/节点/格子/区域边界清楚，避免生成普通奇幻地图或氛围插画。

### 后续观察点

- 是否需要继续拆分更细的 `recipes/boardgame-board.md`，专门处理版图、地图板、路径板和区域控制板。
- 是否需要为卡牌尺寸、出血线、安全边距、图标槽位建立印刷专用检查表。

## 2026-05-12 v0.3.2 桌游封面案例补强

### 触发原因

用户在 `db/桌游卡牌与版图/images/` 中继续新增 4 张桌游封面参考图，需要把盒面/封面/扩展包包装纳入该专题库，而不是只覆盖卡牌、版图和玩家面板。

### 更新内容

- 将 `db/桌游卡牌与版图/prompt.md` 案例数从 30 个更新为 34 个。
- 新增例 930-933：高能邪典喜剧盒面、宁静自然绘本盒面、周年纪念角色群像封面、横版扩展包叙事封面。
- 扩展 Metadata：新增桌游封面、盒面、包装、扩展包封面等关键词与默认比例。
- 更新使用提示：封面/盒面任务优先检索例 930-933，并补读 `recipes/boardgame-cover.md`。
- 更新 `SKILL.md` 路由关键词，让桌游封面、盒面、包装、扩展包封面优先命中 `db/桌游卡牌与版图/`。

### 设计取舍

- 新增案例只提炼构图、标题区、角色群像、场景叙事和封面信息层级，不要求复刻真实游戏名、商标或角色。
- 封面案例与 `recipes/boardgame-cover.md` 协作：案例库提供视觉参考结构，recipe 负责输出形态判定和槽位完整性。

### 后续观察点

- 是否需要为“盒面正面图”和“完整盒子效果图”分别补充更多参考图。
- 是否需要建立桌游包装印刷检查表：出血、安全边距、标题可读性、年龄/人数/时长信息区、出版社标识占位等。

## 2026-05-12 v0.3.3 全库自检与链接修复

### 触发原因

用户要求完整自检 `yh-image-inspirer` skill。检查范围包括根目录结构、14 个 `db/` 案例库、图片引用、资源地图、recipe/reference 路径和新增“桌游卡牌与版图”专题库。

### 修复内容

- 修正 `SKILL.md` 常见组合中断行导致的 `ecipes/...` 路径错误，恢复为可读的 `recipes/...` 路径。
- 将 `SKILL.md` 中卡牌默认比例从 `1:1` 调整为 `2:3 或 3:4`，与 `recipes/boardgame-card.md` 和 `db/桌游卡牌与版图/prompt.md` 保持一致。
- 对老案例库中不存在的本地图片引用改为“参考图：暂缺”文本，避免运行时输出坏的 Markdown 图片：UI与界面 3 个、插画与艺术 4 个、海报与排版 1 个、商品与电商 1 个、摄影与写实 1 个、图表与信息可视化 2 个。

### 自检结论

- 根目录必要文件和目录存在：`SKILL.md`、`LICENSE`、`db/`、`recipes/`、`references/`。
- 14 个 `db/` 分类均有 `prompt.md` 与 `## Metadata`。
- 新增 `db/桌游卡牌与版图/` 通过一致性检查：34 个案例、34 张图片、0 缺失引用。
- 资源地图中列出的主要 recipe/reference 文件均存在。

### 后续观察点

- 部分旧库仍有未被 Markdown 正文引用的图片文件，主要是 Mondo 专题图和历史导入冗余，不影响运行，可后续按专题整理。
- `references/evolution-log.md` 中提到的 `recipes/boardgame-components.md`、`recipes/boardgame-localization.md`、`recipes/boardgame-board.md` 属于历史规划项，不是当前运行依赖。

## 2026-05-16 v0.4.0 来源治理层与升级体检流程

### 触发原因

用户要求把 `yh-image-inspirer` 从“内容强的本地图片工作流 skill”升级为“可持续演进的技能系统”，重点补足：

- GPT-Image-2 专项决策能力
- 来源治理与吸收台账
- 升级前自动体检能力

### 更新内容

- 新增来源治理文件：
  - `references/source-registry.md`
  - `references/absorption-map.md`
  - `references/upstream-gap-tracker.md`
  - `references/fossil-record.md`
- 新增升级与方法文件：
  - `references/upgrade-playbook.md`
  - `references/gpt-image2-decision-rules.md`
  - `references/edit-workflows.md`
  - `references/template-index.md`
  - `references/featured-cases.md`
  - `references/learning-capture-rules.md`
- 更新 `SKILL.md` 资源地图，并新增“升级前体检与来源治理”说明。
- 更新 `SKILL.md` 的 prompt / 出图 / 沉淀流程，使 GPT-Image-2 专项规则与 edit workflow 成为显式入口。
- 重构 `references/personal-preferences.md` 为固定章节。
- 扩展 `references/output-checklists.md`，新增 edit、系列图、GPT-Image-2 与升级后自测检查。

### 设计取舍

- 坚持本地台账优先：先用 markdown 台账解决“升级前查什么”的问题，不引入脚本或数据库。
- 不全量镜像 `awesome-gpt-image-2`，只增强本地索引、精选入口和差距台账。
- 不直接复用 `continuous-learning` 的全局 Hook，而是把学习规则显式写入 skill 自身。
- 不把 `yinyo-image2-prompt` 变成依赖，而是抽取其最有价值的 GPT-Image-2 决策层。

### 后续观察点

- 如果未来升级频率足够高，可考虑增加第二阶段“本地+在线比对”流程。
- 若案例量继续扩大，可能需要把 `featured-cases.md` 进一步拆成按任务类型的多个入口文件。
- 若 edit 任务占比继续提升，可考虑把 `edit-workflows.md` 升级为独立 recipe 集合。

## 2026-05-25 海报设计原理整合

### 触发原因

独立的 `poster-design` 技能（806 行）与本 skill 存在能力重叠，但其底层设计原理（视觉层级、网格系统、排版规范、色彩策略、印刷制作）恰好是本 skill 缺少的通用知识层。本 skill 强在案例驱动的 prompt 生成，但缺少这些设计基础。

### 更新

- 整合 `poster-design` 技能的核心知识为 `references/poster-design-fundamentals.md`，覆盖：
  - 视觉层级（3 秒法则、层级结构、字号参考、视觉距离）
  - 网格系统（单栏/双栏/三分法/Z 型动线/经典图像布局）
  - 排版规范（字体分类与用途、配对原则、行距、对齐）
  - 色彩策略（心理学速查、60-30-10 法则、配色方案）
  - 印刷制作规范（DPI、CMYK、文件格式、出血与安全区、纸张选择）
  - 海报类型速查、常见错误清单
- 更新 `SKILL.md` 资源地图，新增 `poster-design-fundamentals.md` 条目。
- 更新类型路由表，海报相关任务优先读取设计原理。
- 更新线下与印刷海报专项流程，显式引用印刷制作规范。
- 删除独立的 `poster-design` 技能。

### 设计取舍

- 不把 poster-design 全文照搬，而是提炼为与现有海报资源互补的底层原理层。
- 保留 poster-design 中的通用设计法则（层级、网格、排版、色彩），去掉与本 skill 已有内容重复的部分（如模板、案例）。
- 明确四份海报资源的分工：原理（fundamentals）→ 构图（composition-patterns）→ 风格（artist-styles）→ 题材模板（genre-templates）。

### 后续观察点

- 海报任务中设计原理的引用频率，是否需要进一步细化。
- 是否需要为其他垂直领域（如 UI、信息图）补充类似的底层原理文件。

## 2026-05-25 海报与电商模板库扩充

### 触发原因

用户要求从两个 GitHub 仓库吸收海报和电商相关的提示词内容和更强功能：
- `freestylefly/awesome-gpt-image-2`（466 案例、22 模板）
- `buluslan/gpt-image2-ecommerce`（25 个结构化电商场景模板）

对比本地 skill 后发现：structured-templates.md 已覆盖 awesome 的 5 个海报模板（运动 Campaign、概念字体、水墨双重曝光、自然科普、签名设计），但缺少 3 个模板和 4 个海报题材；ecommerce 仓库的 25 个场景模板完全是新内容。

### 更新内容

**新增 `references/ecommerce-scene-templates.md`**：
- 25 个结构化电商场景模板，来自 gpt-image2-ecommerce
- 每个模板含触发词、prompt 结构、变量槽位、风格变体、品类适配建议
- 覆盖：白底主图、生活方式场景、平铺俯拍、细节微距、促销海报、社媒内容、UGC 买家秀、模特展示、对比图、包装设计、信息图 A+、创意概念、尺寸规格、多件组合、直播间、虚拟试穿、技术拆解、隐形模特、多角度网格、杂志编辑、季节营销、奢华氛围、设备 Mockup、店铺门面、运动 Campaign
- 包含 Anti-AI 处理要点和品类通用适配建议

**`references/structured-templates.md` 新增 3 个模板**：
- 个性化美妆报告：诊断报告/推荐卡片/导购助手布局
- 概念产品研发拆解：爆炸拆解图/研发板/组件展示
- 历史与古风题材：朝代/时期/视觉风格/传统色谱

**`references/poster-genre-templates.md` 新增 4 个题材模板**：
- Travel Poster：复古矢量/等距鸟瞰/城市文字/水彩拼贴四种风
- 国潮/新中式：双重曝光城市风/新中式山水画风
- Luxury Product Campaign：香水美妆/时尚服装
- Food & Beverage Commercial：飞溅动态/产品宣传

**更新 `SKILL.md`**：
- 资源地图新增 `ecommerce-scene-templates.md` 条目
- 结构化模板数从 25 更新为 28
- 类型路由表新增 6 行（旅行/奢品/食品饮料/美妆报告/研发拆解）+ 更新 2 行（电商+古风）

**更新 `references/source-registry.md`**：
- 更新 awesome-gpt-image-2 条目，吸收数从 25 模板扩展到 28
- 新增 `src-gpt-image2-ecommerce` 条目，状态 `absorbed`

### 设计取舍

- 不全量镜像 awesome 的 466 个案例到 db/，只增强模板和题材库。
- awesome 的 poster-layout-system 和 product-commerce-visual 模板与本地已有模板重叠，不重复添加。
- e-commerce 场景模板独立成文件，与 recipes/ecommerce-poster.md 互补：recipe 负责流程，scene templates 负责场景匹配。
- 海报题材模板（genre-templates）专注于 Mondo 之外的新题材，避免与现有电影/书籍/专辑模板重复。

### 后续观察点

- 个性化美妆报告和产品研发拆解模板的实际使用频率。
- 旅行海报和国潮题材是否需要进一步细化为独立 recipe。
- 是否需要将 awesome 中的 Featured 案例精选沉淀到 db/ 对应分类。
- ecommerce-scene-templates.md 的 Anti-AI 处理是否有效减少社媒/UGC 场景的翻车。

## 2026-05-26 电商 Prompt 方法论深度吸收

### 触发原因

用户做桌游和文创电商，要求分析 `gpt-image2-ecommerce` 除场景模板外的剩余价值并融合。分析发现该仓库的 SKILL.md 包含三层面尚未吸收的内容：

1. Prompt 写法五原则（简洁为王、自然语言优先、材质描述、光照、善用参考图）
2. Anti-AI 防坑规则（iPhone 型号、噪点、Kodak Portra 400、"NOT retouched"）
3. 25 个 JSON 模板中的 `category_tips`、`examples`、`variants` 针对桌游/文创的适配

### 更新内容

**新增 `references/ecommerce-prompt-methodology.md`**：
- Prompt 写法五原则：简洁为王、自然语言优先、材质描述要具体、光照很重要、善用参考图
- 桌游/文创常用材质词和光照词速查表
- Anti-AI 防坑规则：7 条核心规则 + CCD 复古胶片感 + 小红书种草风示例
- 桌游与文创业品类适配：为 12 个最相关的电商场景模板（主图/场景/平铺/微距/海报/社媒/UGC/包装/信息图/创意/尺寸/套装/直播/拆解/多角度/季节营销）补充桌游专属提示和示例 prompt
- 通用 Prompt 组装公式

**更新 `SKILL.md`**：
- 资源地图新增 `ecommerce-prompt-methodology.md` 条目
- 类型路由表"电商"行新增 `ecommerce-prompt-methodology.md` 引用

**更新 `references/source-registry.md`**：
- `src-gpt-image2-ecommerce` 条目扩展吸收范围，新增 Prompt 写法和桌游文创品类适配

### 设计取舍

- 不把 25 个 JSON 模板的完整 examples 原文搬入（已在 ecommerce-scene-templates.md 中有文字描述），只提取方法论和桌游专属适配。
- Anti-AI 规则独立成节而不是嵌入每个模板，因为它是跨场景的通用规则。
- 桌游品类适配选取了 12 个最相关的场景，跳过了与桌游无关的（模特展示/虚拟试穿/隐形模特/设备 Mockup/店铺门面/运动 Campaign）。

### 后续观察点

- Prompt 写法五原则在实际电商作图中是否被正确引用。
- Anti-AI 规则在小红书/UGC 场景中是否有效减少"AI 感"。
- 是否需要为文创品类（非桌游）单独补充更多品类适配。

## 2026-05-26 Open Design 高级 Prompt 模式吸收

### 触发原因

用户要求分析 `nexu-io/open-design` 的 image gallery（43 个 gpt-image-2 prompt-templates）中可增强当前技能的内容。对比后发现该仓库有 10 种超出常规模板的高级模式。

### 更新内容

**新增 `references/gpt-image2-advanced-patterns.md`**（10 种高级模式）：
1. **GST+NP 模式**：Global Style Tokens + Negative Prompt 三段拼合，确保系列图风格统一
2. **HUD 叠加规范**：3D 场景 + UI 叠加层分离描述，适用于游戏截图、桌游数字版 UI
3. **拆解图结构化规范**：JSON 结构定义拆解层级、标注线、图例位置
4. **Pose Grid 动作分解表**：4×4 / 3×3 网格，角色一致性锁定，纯色背景
5. **Storyboard 序列**：6-8 连拍，共享角色锁定，每帧独立姿态
6. **相机参数指定**：85mm f/2.0、50mm f/1.4 等精确控制景深和质感
7. **Anti-AI-Slop 清单**：五道防线（Question Form、Brand-Spec、Five-Dim Critique、P0/P1/P2、Slop Blacklist）
8. **2×2 编辑拼贴**：四格一致造型展示
9. **品牌发布会海报**：大字标题 + 人物主视觉 + 品牌标识层次结构
10. **12 格旅行拼贴**：手机随拍风不规则网格

**下载 22 张精选参考图**到 `references/awesome-images/open-design/`：
- 游戏截图 5 张（三国 ARPG、古风 MMO HUD、动漫格斗）
- 拆解图 2 张（VR 头显、3D 石阶信息图）
- 动作分解 2 张（16 格 pose grid、8 连拍 storyboard）
- 社媒内容 6 张（城市地图、旅行拼贴、时尚拼贴、直播 UI、发布海报、店铺预告）
- 文化复古 3 张（杂志封面、图解混搭、手绘字体）
- 动漫肖像 4 张（武术对决、赛博朋克头像、时尚摄影）

**更新 `references/awesome-images/INDEX.md`**：新增 Open Design 分类索引

**更新 `SKILL.md`**：
- 资源地图新增 `gpt-image2-advanced-patterns.md` 条目
- 资源地图更新 `awesome-images/` 条目（39→61 张）
- 类型路由表新增 3 行：游戏截图/HUD、组件拆解/爆炸图、连拍/分镜/storyboard

**更新 `references/source-registry.md`**：
- 新增 `src-open-design` 条目，状态 `partially_absorbed`

### 设计取舍

- 不全量导入 43 个模板，只提取 10 种可迁移的高级模式。
- 参考图精选 22 张（非全量 43 张），优先选择与桌游/文创相关的场景。
- GST+NP 模式和 Pose Grid 模式是最具操作价值的增量，直接解决系列卡牌和角色卡设计的一致性问题。
- HUD 叠加规范补充了当前 skill 在"游戏 UI 截图"场景的空白。
- Anti-AI-Slop 清单与已有的 Anti-AI 防坑规则互补：前者是设计流程层面的防线，后者是 prompt 措辞层面的技巧。

### 后续观察点

- GST+NP 模式在系列卡牌设计中的实际效果是否优于单图独立 prompt。
- Pose Grid 是否需要进一步细化为独立 recipe（如 `recipes/pose-grid.md`）。
- HUD 叠加规范是否需要扩展到桌游 App 的完整 UI 规范。
- 是否需要将 open-design 中剩余的 21 个模板按需吸收。

## 2026-05-26 全库自检（skill-creator 框架）

### 触发原因

用户要求使用 skill-creator 框架对 `yh-image-inspirer` 进行全面自检，覆盖结构完整性、内容一致性和案例库健康度。

### 检查范围

根目录结构、14 个 `db/` 案例库、`recipes/`、`references/`、`awesome-images/`、SKILL.md 资源地图、source-registry、template-index、evolution-log。

### 结构完整性检查

- 根目录必要文件和目录存在：`SKILL.md`、`LICENSE`、`agents/`、`db/`、`recipes/`、`references/`。
- SKILL.md 资源地图列出的 32 个文件/目录全部存在，0 个缺失。
- `recipes/` 包含 9 个 recipe 文件，全部在 SKILL.md 中被引用。
- `references/` 包含 26 个文件 + 1 个子目录（awesome-images/），全部在 SKILL.md 中被引用。
- `agents/openai.yaml` 存在但未在 SKILL.md 资源地图中列出（非运行依赖，低优先级）。

### 内容一致性检查

- **模板数量**：SKILL.md 原写"28 个模板"，实际 `structured-templates.md` 有 29 个 `### ` 子节（28 个模板 + 1 个风格扩展附录），`template-index.md` 有 29 个条目。已修正为"29 个模板条目"。
- **参考图数量**：SKILL.md 写"61 张"，实际 `awesome-images/` 下 8 个子目录合计 61 张图片文件，一致。
- **路由表**：39 个路由行，覆盖 14 个 db 分类 + 28 个模板 + 6 个桌游 recipe + 3 个通用 recipe + 高级模式引用。
- **source-registry**：11 个来源条目，状态和日期与 evolution-log 一致。
- **awesome-images 子目录分布**：open-design 22 张、history 16 张、guochao 8 张、travel 7 张、luxury 3 张、food-bev 2 张、breakdown 2 张、beauty 1 张，与 INDEX.md 索引一致。

### 案例库完整性检查

- 14 个 `db/` 目录全部包含 `prompt.md` 和 `images/` 目录。
- 所有 `prompt.md` 均包含 `## Metadata` 段落。
- 图片引用检查：所有 `prompt.md` 中的 `images/` 引用均指向存在的文件，0 个断链。
- 总计 405 张 db 图片，23 张（5.7%）未被 `prompt.md` 正文引用：
  - 海报与排版 11/75、UI与界面 4/59、插画与艺术 4/55、图表与信息可视化 2/55、商品与电商 1/15、摄影与写实 1/38。
  - 这些主要是 Mondo 专题图和历史导入冗余，不影响运行。

### 修复内容

- 修正 SKILL.md 资源地图中 `structured-templates.md` 描述：从"28 个模板"改为"29 个模板条目"。
- 修正 SKILL.md 资源地图中 `template-index.md` 描述：从"28 个模板"改为"29 个模板条目"。

### 自检结论

- 结构完整性：通过。所有资源地图路径存在，无断链。
- 内容一致性：通过（修正模板计数后）。路由表、source-registry、INDEX.md 均与实际内容一致。
- 案例库健康度：通过。14 类库均有完整 Metadata 和图片引用，断链率为 0。
- 整体评价：skill 在连续吸收 poster-design、gpt-image2-ecommerce、open-design 三个来源后，结构保持良好，无重大缺口。

### 后续观察点

- 是否需要清理 23 张未引用的 db/ 图片以减小 skill 体积。
- 是否需要将 `agents/openai.yaml` 纳入资源地图或移除。
- 是否需要建立 `evals/` 目录，用固定测试提示评估 skill 触发和输出质量。

## 2026-05-26 桌游宣传海报参考集合沉淀

### 触发原因

用户整理了两组桌游宣传海报参考图，希望加入 `yh-image-inspirer` 作为后续桌游宣传海报生成与提示词编写的本地参考。

### 变更内容

- 将 15 张意向风格桌游宣传海报复制到 `db/海报与排版/images/boardgame-promo-concept-001..015`。
- 将 15 张写实风格桌游宣传海报复制到 `db/海报与排版/images/boardgame-promo-realistic-001..015`。
- 在 `db/海报与排版/prompt.md` 追加两个集合型案例：
  - `例 387：桌游宣传海报｜意向主视觉参考集合`
  - `例 388：桌游宣传海报｜写实主视觉参考集合`

### 分类规则

- 意向主视觉：装饰性插画、符号化中心主体、大色块、明确标题、概念海报感；避免照片、产品实拍、规则说明图。
- 写实主视觉：电影感场景、具象角色/空间、真实光影体积、故事张力；避免真实桌面摆拍、样机、平面符号海报。

### 后续观察点

- 后续桌游宣传海报任务中，优先按用户指定的“意向/写实”路由到对应集合。
- 如果继续增加桌游宣传参考，保持 `boardgame-promo-concept-*` 与 `boardgame-promo-realistic-*` 命名，并同步更新 `prompt.md` 中的集合引用。

## 2026-05-26 100 Layout Compositions 构图模式库吸收

### 触发原因

用户提出 `nevertoday/100-layout-compositions` 可能有助于提升 `yh-image-inspirer` 的排版构图能力，但担心该来源主要是图片，通用 Agent 不能稳定依赖现场读图。用户要求处理成完整本地可用版本。

### 调研结论

该来源是 100 张中文排版构图参考图，适合作为“版式骨架/构图语法”来源，而不是普通风格案例库。直接导入图片价值有限，必须转写为文字化构图规则。

### 变更内容

- 完整下载 100 张高清原图到 `references/layout-composition-images/originals/`。
- 完整下载 100 张缩略图到 `references/layout-composition-images/thumbnails/`。
- 生成 4 张总览图：`references/layout-composition-images/contact-sheet-1..4.jpg`。
- 新增 `references/layout-composition-images/INDEX.md`，记录 100 个图号、构图名和本地路径。
- 新增 `references/layout-composition-patterns.md`，包含：
  - 使用原则
  - 快速路由
  - 高频模式卡
  - 完整 100 构图词表
  - 桌游宣传海报 / 信息型海报 / Mondo 概念海报组合建议
  - 防坑规则
- 更新 `SKILL.md`，在资源地图和海报/排版/构图路由中加入该库。
- 更新 `source-registry.md`、`absorption-map.md`、`upstream-gap-tracker.md`、`source-attribution.md`。

### 设计取舍

- 图片完整本地化，但运行时优先使用文字化规则，降低对图像读取的依赖。
- 不放入 `db/海报与排版/images/`，避免和具体海报风格案例混在一起。
- 不为 100 个构图逐一写长篇模板；先为高频构图写详细模式卡，其余通过完整索引和词表保留。

### 后续观察点

- 后续海报生成任务中，检查 `layout-composition-patterns.md` 是否能显著提高版式稳定性。
- 如果某些构图被频繁使用，可继续扩写为完整模式卡。
- 可考虑为 `layout-composition-images/INDEX.md` 增加标签字段或机器可读 JSON 索引。
