# Structured Templates

这些模板吸收 `awesome-gpt-image-2` 的 Prompt-as-Code 思路：把散文式提示词拆成可控槽位。使用时不要机械照抄，先填槽位，再改写成自然 prompt。

每个模板包含：
- `useWhen`：何时使用此模板
- `guidance`：分步填写指导
- `pitfalls`：常见翻车点

## 目录

- UI、截图和直播界面
- 海报、字体、Campaign 与科普视觉
- 电商、信息图和编辑工作流
- 角色、摄影、场景、品牌与系列生成
- 桌游、出版物和其他专项模板

---

## UI

```json
{
  "type": "UI Screenshot or UI Object",
  "platform": "iOS / Android / Web / physical UI object",
  "product": "[产品或系统]",
  "layout": "[顶部导航/卡片流/仪表盘/双栏/社媒截图]",
  "content": {
    "title": "[必须显示的标题]",
    "sections": ["[模块1]", "[模块2]", "[模块3]"],
    "actions": ["[按钮或图标]"]
  },
  "style": {
    "theme": "[明亮/暗黑/科技/拟物/极简]",
    "colors": "[主色 + 强调色]",
    "typography": "clean readable typography"
  },
  "constraints": "readable text, correct layout, no gibberish, aspect ratio [x:y]",
  "useWhen": "用于 App 界面、网页、仪表盘、组件库、物理 UI 对象等通用 UI 场景。",
  "guidance": [
    "锁定平台、比例、布局层级和画面文字。",
    "明确状态栏、Tab、操作区等 UI 元素。",
    "指定产品类型和核心功能模块。"
  ],
  "pitfalls": [
    "避免平台描述过泛，需指定具体平台。",
    "约束文字可读性，防止乱码和占位文本。",
    "非手机屏幕需锁定比例（如车载 21:9）。"
  ]
}
```

## UI 截图生成

```json
{
  "type": "UI Screenshot",
  "platform": "[小红书 / 抖音 / 微信 / X / 微博 / Instagram]",
  "color_scheme": "[深色/浅色]",
  "aspect_ratio": "[9:16 / 16:9 / 1:1]",
  "profile": {
    "avatar": "[头像描述]",
    "username": "[用户名]",
    "verified_badge": "[认证标识或无]"
  },
  "content_layers": {
    "top_bar": "[顶部状态栏/导航]",
    "main_content": "[主要内容区域描述]",
    "interaction_bar": "[点赞/评论/转发/收藏数量]",
    "bottom_nav": "[底部 Tab 栏]"
  },
  "exact_text": "[画面中必须显示的中文文字，逐字写明]",
  "constraints": "platform-specific UI features, Chinese text accuracy, no gibberish, no placeholder text",
  "useWhen": "用于生成平台专属 App 截图，如小红书笔记、抖音视频页、微信对话、X 推文等。",
  "guidance": [
    "锁定平台 + 比例 + 布局层级。",
    "指定平台专属 UI 特征：X 蓝勾、抖音音乐碟、小红书瀑布流、微信对话气泡。",
    "头像/用户名/认证标识需具体描述。",
    "所有画面中文文字必须逐字写明，禁止模型自创。"
  ],
  "pitfalls": [
    "禁止乱码和占位文本，中文必须准确。",
    "必须指定平台，不能模糊说做个截图。",
    "不同平台 UI 差异大，需显式锁死平台特征。",
    "互动数据（点赞/评论数）需显式指定。"
  ]
}
```

## UI 直播界面

```json
{
  "type": "Live Stream Interface",
  "platform": "[抖音/快手/淘宝直播/小红书/B站]",
  "stream_type": "[电商直播/才艺直播/游戏直播]",
  "streamer": {
    "appearance": "[主播人物描述]",
    "pose": "[姿态]",
    "outfit": "[服装]",
    "background": "[背景]"
  },
  "lighting": "[自然光/暖色补光/冷色科技感]",
  "overlay_layers": {
    "top": "[顶部信息栏：在线人数/直播标题]",
    "left_bottom": "[左下角：弹幕/评论]",
    "right_bottom": "[右下角：点赞/分享]",
    "bottom_bar": "[底部商品栏/礼物栏]"
  },
  "style": "[写实/商业/娱乐]",
  "constraints": "no UI elements blocking streamer face, platform-specific features, readable Chinese text",
  "useWhen": "用于生成直播间界面截图，包括电商直播、才艺直播、游戏直播等场景。",
  "guidance": [
    "先确定直播类型（电商/才艺/游戏），不同类型 UI 布局差异大。",
    "主播人物描述需具体：姿态、服装、背景、灯光。",
    "覆盖层分层描述：顶部、左下、右下、底部。",
    "电商直播强调商品栏，才艺直播强调礼物栏。"
  ],
  "pitfalls": [
    "禁止 UI 元素遮挡主播面部。",
    "必须指定平台和直播类型。",
    "弹幕文字需使用中文，且内容合理。",
    "避免把直播界面做成海报或静态展示。"
  ]
}
```

## Poster

```json
{
  "type": "Poster",
  "topic": "[活动/产品/电影/品牌/概念]",
  "hero": "[主视觉主体]",
  "copy": {
    "headline": "[标题]",
    "subhead": "[副标题]",
    "small_text": "[少量辅助文字]"
  },
  "layout": "[居中/左对齐/对角线/强主视觉/留白]",
  "style": {
    "aesthetic": "[复古/未来/极简/国风/商业 campaign]",
    "colors": "[主色 + 辅色]",
    "mood": "[情绪]"
  },
  "constraints": "single finished poster, readable title, no mockup, no extra captions",
  "useWhen": "用于活动海报、电影海报、封面和社媒传播视觉。",
  "guidance": [
    "锁定主体、标题、版式、配色和比例。",
    "突出标题层级和主视觉。",
    "先确定主视觉到底是什么，再构建画面。"
  ],
  "pitfalls": [
    "需要成品海报时，避免生成拼贴展示板或情绪板。",
    "标题和副标题文字必须硬编码在 prompt 中。",
    "约束多余文字和装饰符号。"
  ]
}
```

## 概念字体海报（中文）

```json
{
  "type": "Conceptual Typography Poster (Chinese)",
  "title_text": "[标题/词语/短句，必须精确]",
  "interpretation": "[对标题含义的视觉隐喻解读]",
  "typography_style": {
    "weight": "[字重：粗/中/细]",
    "width": "[字宽：紧/正常/宽]",
    "contrast": "[笔画对比度]",
    "spacing": "[字间距：紧/正常/宽松]",
    "rhythm": "[节奏感：平稳/跳跃/流动]",
    "deformation": "[变形程度：无/轻微/夸张]",
    "negative_space": "[负空间处理]"
  },
  "interaction": "[人物/物体/风景与字体的交互方式]",
  "palette": "[4-6 色系统]",
  "texture": "[丝网印刷/石版画/孔版画质感]",
  "constraints": "title must be exact, typography is hero, no moodboard, no grid, no mockup, no captions, no process sheet",
  "useWhen": "用于标题文字需要成为主视觉结构的中文海报，特别是概念化、艺术化的字体设计海报。",
  "guidance": [
    "让字体成为画面主角，标题拼写必须精确。",
    "沉默式解读标题含义，转化为一个视觉隐喻。",
    "指定字重、字宽、对比度、间距、节奏、变形、负空间。",
    "若标题=知名人物：40-70% 构图作为编辑式肖像与字体交互。",
    "使用 4-6 色系统，保持克制。",
    "质感：丝网印刷/石版画/孔版画颗粒、纸纤维、轻微墨迹不完美。"
  ],
  "pitfalls": [
    "禁止：情绪板、网格、样机、说明文字、过程图、样本标签。",
    "避免默认字效、无关图标和标题错字。",
    "标题拼写是第一优先级视觉，错一个字全图报废。",
    "配色数量控制在 4-6 色，避免花哨。"
  ]
}
```

## 运动商业 Campaign 海报

```json
{
  "type": "Sports Commercial Campaign Poster",
  "sport": "[运动项目：篮球/足球/跑步/健身/网球/滑板...]",
  "athlete": {
    "description": "[运动员/模特描述]",
    "pose": "[动态姿态]",
    "equipment": "[核心运动器材]"
  },
  "layout_mode": "[单张强主视觉 / 三联画 / 数据涂鸦]",
  "copy": {
    "headline": "[主标题]",
    "supporting": "[辅助文案]"
  },
  "brand_palette": "[品牌化配色方案]",
  "lighting": "[强光影/逆光/侧光/戏剧性]",
  "constraints": "correct sports equipment, clean composition, readable data overlays, no wrong gear",
  "useWhen": "用于运动品牌 Campaign、运动员海报、运动产品宣传视觉。",
  "guidance": [
    "先锁定版式结构（单张/三联画/数据涂鸦），再填主体和文案。",
    "定义运动项目、运动员姿态、核心道具、标题和品牌色。",
    "使用强光影、干净构图和可读数据层。",
    "运动器材必须渲染正确（球拍角度、鞋子比例等）。"
  ],
  "pitfalls": [
    "避免错误运动器材和杂乱拼贴。",
    "让运动员和核心道具占据视觉主导。",
    "先锁版式再填内容，防止拼贴混乱。",
    "道具需指定角度、比例、位置。"
  ]
}
```

## 自然科普海报

```json
{
  "type": "Nature Science Poster",
  "subject_cn": "[中文物种名]",
  "subject_en": "[英文物种名]",
  "distribution": "[分布区域]",
  "features": [
    {"title": "[特征1标题]", "description": "[特征1说明]"},
    {"title": "[特征2标题]", "description": "[特征2说明]"},
    {"title": "[特征3标题]", "description": "[特征3说明]"},
    {"title": "[特征4标题]", "description": "[特征4说明]"}
  ],
  "summary": "[总结句]",
  "subtitle": "[物种定位副标题]",
  "design_system": {
    "subject_ratio": "50-70%",
    "info_zone": "四栏极简信息区，细线分隔",
    "background": "纯白/浅灰",
    "typography": "大中文标题 + 灰色副标 + 小英文名",
    "color_usage": "颜色仅用于图标和小标题，无大色块"
  },
  "palette": "[暖棕/冷蓝/松石绿/紫色/橙色]",
  "constraints": "Apple keynote aesthetic, subject 50-70%, minimal copy, no heavy advertising, no encyclopedia blocks",
  "useWhen": "用于自然主题的高级、干净科普海报，Apple keynote 风格。",
  "guidance": [
    "主体必须占视觉面积 50-70%。",
    "四栏极简信息区，细线分隔，纯白/浅灰背景。",
    "排版层级：大中文标题、灰色副标、小英文名。",
    "颜色仅用于图标和小标题，无大色块。",
    "使用清晰主体、少量文案、柔和阴影和充足留白。"
  ],
  "pitfalls": [
    "避免广告感太重。",
    "避免密集百科正文。",
    "主体必须放大，不能做小图鉴。",
    "信息极简：少而准。"
  ]
}
```

## 水墨双重曝光肖像海报

```json
{
  "type": "Ink Double Exposure Portrait Poster",
  "subject": "[人物/角色]",
  "pose": "[站姿/动作姿态/凝视镜头]",
  "key_scene": "[双重曝光内部的关键场景]",
  "symbol": "[象征物]",
  "narrative": "[叙事片段]",
  "texture": "[环境纹理：云雾/墨痕/宣纸]",
  "text": "[标题/姓名/短句，可选]",
  "composition": {
    "upper": "放大头像剪影",
    "internal": "双重曝光叙事场景",
    "lower": "全身/半身主体"
  },
  "connection": "[云/雾/墨水扩散/飞白边缘]",
  "style": "东方水墨美学 + 电影写实混合",
  "constraints": "premium ink aesthetic, no cheap fantasy collage, no overloaded scenery, subtle text",
  "useWhen": "用于诗意人像海报、水墨氛围、文化主题视觉、双重曝光效果。",
  "guidance": [
    "三区域垂直结构：上部放大头像剪影、内部双重曝光叙事、下部全身主体。",
    "通过云/雾连接，墨水扩散、飞白边缘。",
    "融合人像剪影、水墨质感、氛围和留白。",
    "保持构图克制、高级、可读。"
  ],
  "pitfalls": [
    "避免廉价奇幻拼贴和景物堆叠。",
    "非必要时减少文字。",
    "水墨质感要自然，不能像 PS 滤镜。",
    "双重曝光的内部场景需与人物有叙事关联。"
  ]
}
```

## 签名设计系统

```json
{
  "type": "Signature Design System",
  "mode": "[多风格选择 / 单签名提取 / 练习分解]",
  "name": "[姓名/昵称]",
  "style_preference": "[若有偏好]",
  "multi_style_grid": {
    "layout": "2x3 卡片网格",
    "styles": [
      "1. 极简理性",
      "2. 狂野张力",
      "3. 松弛随性",
      "4. 东方行楷",
      "5. 锐利结构",
      "6. 实验性"
    ],
    "card_content": "编号 + 风格名 + 大签名 + 一行气质描述 + 一个强调色"
  },
  "extraction": {
    "source": "[输入图片或风格编号]",
    "preserve": ["笔触动势", "墨色", "压力变化"],
    "no_decoration": true
  },
  "practice_breakdown": {
    "steps": "8-12 步",
    "markers": ["方向箭头", "起/止/续点", "快/慢", "轻/重", "转折", "钩挑", "飞白", "长拖"],
    "aesthetic": "教学笔记本，红蓝教学箭头"
  },
  "constraints": "exact name spelling, character analysis before style generation, no random fonts",
  "useWhen": "用于签名设计、签名选择、签名练习图等场景。",
  "guidance": [
    "多风格模式：隐藏式字形分析 → 2×3 网格展示 6 种风格。",
    "提取模式：纯提取，保留笔触动势和墨色。",
    "练习分解模式：8-12 步笔画分解，标注方向和力度。",
    "先分析字形结构（密度、笔画比、重心），再生成风格。"
  ],
  "pitfalls": [
    "姓名拼写必须精确。",
    "6 种风格必须有明显差异，不能长得差不多。",
    "练习分解的方向箭头和起止点必须清晰。",
    "提取模式不要加装饰元素。"
  ]
}
```

## Ecommerce

```json
{
  "type": "Chinese e-commerce product poster",
  "product": {
    "name": "[商品名]",
    "category": "[品类]",
    "must_keep": ["[包装形状]", "[主色]", "[核心图案]", "[品牌/标题]"]
  },
  "layout": {
    "format": "[主图海报/详情页长图/卖点图]",
    "hero_area": "complete product box or product shot",
    "selling_points": ["[卖点1]", "[卖点2]", "[卖点3]"],
    "cta": "[行动文案]"
  },
  "style": {
    "palette": "[颜色]",
    "lighting": "[棚拍/柔光/高端商业]",
    "props": ["[辅助元素]"]
  },
  "constraints": "preserve product identity, Chinese readable text, no price unless asked, no QR code",
  "useWhen": "用于商品主图、包装视觉、详情页和销售卖点排版。",
  "guidance": [
    "定义商品、卖点、材质、场景、光线和版块。",
    "区分主商品、卖点标签和辅助道具。",
    "材质和灯光是灵魂——没有它们商品看起来廉价。"
  ],
  "pitfalls": [
    "避免无关道具削弱商品识别。",
    "约束包装文字和卖点表达，促销文案限 1-2 句。",
    "参考产品图必须保留产品识别，不能换成其他产品。"
  ]
}
```

## Infographic

```json
{
  "type": "Infographic",
  "topic": "[主题]",
  "audience": "[读者]",
  "chart_type": "[流程图/对比图/时间线/拆解图/关系图]",
  "structure": {
    "title": "[中文标题]",
    "modules": [
      {"title": "[模块1]", "icon": "[图标]", "text": "[短说明]"},
      {"title": "[模块2]", "icon": "[图标]", "text": "[短说明]"}
    ]
  },
  "style": {
    "aesthetic": "[科普/白皮书/手绘/Apple keynote]",
    "colors": "[低饱和配色]",
    "background": "[浅色/深色/纸感]"
  },
  "constraints": "clear hierarchy, short Chinese text, no clutter, no gibberish",
  "useWhen": "用于解释图、技术图解、时间线和知识卡片。",
  "guidance": [
    "定义 3-5 个模块、信息流、层级和短标签。",
    "用色块、箭头、图标和留白控制复杂度。",
    "模块间需有逻辑连接（箭头、颜色区分或连接线）。"
  ],
  "pitfalls": [
    "避免把长段正文塞进画面。",
    "先限制模块数量（3-6 个），再补视觉细节。",
    "中文短标题 + 一句话说明，不要大段文字。"
  ]
}
```

## 科学比例尺缩放信息图

```json
{
  "type": "Scientific Scale-Zoom Infographic",
  "topic": "[主题]",
  "scale_levels": [
    {"name": "[尺度1名称]", "insight": "[3-5 词洞察]", "unit": "[测量单位/倍率]", "render": "[该尺度的 3D 渲染描述]"},
    {"name": "[尺度2名称]", "insight": "[3-5 词洞察]", "unit": "[测量单位/倍率]", "render": "[该尺度的 3D 渲染描述]"},
    {"name": "[尺度3名称]", "insight": "[3-5 词洞察]", "unit": "[测量单位/倍率]", "render": "[该尺度的 3D 渲染描述]"},
    {"name": "[尺度4名称]", "insight": "[3-5 词洞察]", "unit": "[测量单位/倍率]", "render": "[该尺度的 3D 渲染描述]"},
    {"name": "[尺度5名称]", "insight": "[3-5 词洞察]", "unit": "[测量单位/倍率]", "render": "[该尺度的 3D 渲染描述]"},
    {"name": "[尺度6名称]", "insight": "[3-5 词洞察]", "unit": "[测量单位/倍率]", "render": "[该尺度的 3D 渲染描述]"}
  ],
  "frame_shape": "[六边形/圆形/方形]",
  "connection": "[连接线/缩放箭头/渐变过渡]",
  "format_title": "[如 AT EVERY SCALE / 万物尺度]",
  "constraints": "6-8 scale levels, no generic magnifying glass icon, no equal-sized frames, distinct visual per scale",
  "useWhen": "用于需要从微观到宏观展示尺度变化的科普主题。",
  "guidance": [
    "使用 6-8 个尺度框，每个标签保持短句。",
    "展示单位、倍率和不同尺度的细节。",
    "每个尺度框需有独特的视觉内容，不能雷同。",
    "使用连接线或缩放箭头表达尺度关系。"
  ],
  "pitfalls": [
    "避免所有尺度框长得一样。",
    "避免通用放大镜式布局。",
    "每个尺度的 3D 渲染需有明确差异。",
    "格式标题（如 AT EVERY SCALE）需统一风格。"
  ]
}
```

## Boardgame Card

```json
{
  "type": "Board game card face",
  "card_mode": "front-facing printable face / product mockup / series",
  "name": "[卡名]",
  "subtitle": "[副标题]",
  "hero_symbol": "[中心图标或角色]",
  "stats": [
    {"label": "[属性1]", "value": "[数值]"},
    {"label": "[属性2]", "value": "[数值]"}
  ],
  "rule_text": "[规则栏短句]",
  "visual_system": {
    "frame": "[边框风格]",
    "palette": "[主色/强调色]",
    "material": "[印刷质感/镭射/压纹/纸张]",
    "layout": "[中心主视觉 + 周边属性 + 底部规则栏]"
  },
  "constraints": "Chinese text only, flat orthographic front view, no table, no hand, no mockup unless asked",
  "useWhen": "用于桌游卡牌牌面正面图，包括资源卡、事件卡、角色卡、技能卡等。",
  "guidance": [
    "默认输出可印刷的牌面正面图，不是桌面摆拍。",
    "必须包含：标题、图标、属性值、规则栏、边框。",
    "属性值控制在 4-6 个。",
    "系列卡牌必须锁定统一视觉系统，每张只改名称和图标。"
  ],
  "pitfalls": [
    "卡牌默认是牌面正面图，不是产品效果图。",
    "中文卡牌文字。",
    "不要桌面、手、样机，除非用户要求。",
    "系列卡牌风格不能漂移。"
  ]
}
```

## Brand

```json
{
  "type": "Brand identity visual",
  "brand": "[品牌名]",
  "industry": "[行业]",
  "personality": "[品牌个性]",
  "deliverable": "[logo概念/品牌板/配色板/字体系统/触点系统]",
  "elements": ["logo", "color palette", "typography", "usage examples"],
  "style": "[极简/几何/有机/复古/未来]",
  "constraints": "no copied logos, readable brand name, coherent identity system",
  "useWhen": "用于 Logo 系统、品牌板、VI 套件和应用样机。",
  "guidance": [
    "定义品牌名、定位、配色、字体、Logo 用法和触点。",
    "要求视觉板中的应用统一对齐。",
    "品牌策略先于 Logo 设计——没有受众/竞品/情感目标，Logo 就是随意图形。"
  ],
  "pitfalls": [
    "避免无关 Logo 变体和混乱配色。",
    "保持品牌文字准确。",
    "Logo 必须跨应用触点测试。",
    "品牌手册需包含"不要"规则。"
  ]
}
```

## 品牌触点系统视觉板

```json
{
  "type": "Brand Touchpoint System Visual Board",
  "brand_name": "[品牌名]",
  "industry": "[行业]",
  "core_quality": "[核心气质]",
  "hero_scene": "[主视觉场景]",
  "surface": "[材质表面/空间场景]",
  "lighting": "[光线]",
  "camera": "[镜头]",
  "design_language": "[设计语言]",
  "palette": {
    "primary": "[主色]",
    "secondary": "[辅助色]"
  },
  "touchpoints": ["主视觉", "包装", "手提袋", "杯子", "标签", "贴纸", "菜单卡", "生活场景"],
  "constraints": "unified visual rules across all touchpoints, one palette, one typography logic, agency proposal feel",
  "useWhen": "用于多触点 Campaign 展示和品牌落地预览，如品牌视觉板、VI 应用展示。",
  "guidance": [
    "指定触点清单、统一视觉规则和样机排列。",
    "让所有面板共享配色和字体逻辑。",
    "要求像顶级设计 agency 提案页。",
    "主视觉 + 包装 + 袋 + 杯 + 标签 + 贴纸 + 菜单 + 生活场景。"
  ],
  "pitfalls": [
    "避免混入多个无关 Campaign 风格。",
    "可读性下降时减少触点数量。",
    "所有触点必须共享同一设计语言。",
    "不要在每个触点上都放 Logo，用设计语言统一。"
  ]
}
```

## 品牌信封产品广告

```json
{
  "type": "Brand Envelope Product Ad",
  "product_image": "[产品图描述]",
  "brand_identity": "[品牌身份：色调/字体感/光影风格]",
  "output_format": "[输出格式：海报/社媒图/详情页]",
  "brand_elements": "[品牌元素：Logo 位置/辅助图形/标签风格]",
  "pipeline": {
    "phase_1_anchor": "锚定品牌视觉世界",
    "phase_2_inject": "注入产品",
    "phase_3_format": "格式化输出",
    "phase_4_signature": "品牌签名"
  },
  "constraints": "consistent visual world when swapping products, brand identity subtle not flooding",
  "useWhen": "用于同品牌不同产品的广告图，需要保持视觉世界一致性。",
  "guidance": [
    "四阶段流水线：ANCHOR→INJECT→FORMAT→SIGNATURE。",
    "ANCHOR：先锚定品牌的视觉世界（色调、质感、光影）。",
    "INJECT：将产品注入品牌世界。",
    "FORMAT：格式化为具体输出形态。",
    "SIGNATURE：添加品牌签名元素。",
    "替换不同产品时，视觉世界保持一致。"
  ],
  "pitfalls": [
    "品牌身份要微妙（强调色、字体感、光影），不要 Logo 轰炸。",
    "换产品时视觉世界不能变。",
    "产品是主角，品牌是氛围。",
    "不要在每张图上都放满品牌元素。"
  ]
}
```

## 品牌人设漫画信息图

```json
{
  "type": "Brand Persona Comic Infographic",
  "brand_visual": "[Logo/品牌视觉元素]",
  "brand_quality": "[品牌气质关键词]",
  "panels": {
    "count": "6-8 格",
    "content": [
      "品牌如何说话",
      "品牌如何行动",
      "品牌如何销售",
      "品牌如何应对竞争",
      "品牌如何处理批评"
    ]
  },
  "auxiliary_modules": ["语调", "能量级", "社交行为", "沟通风格", "DO/DON'T"],
  "constraints": "all colors/clothing/posture derived from logo and brand keywords, character consistency",
  "useWhen": "用于品牌人设化展示、品牌性格可视化、品牌策略沟通。",
  "guidance": [
    "将品牌转化为拟人角色。",
    "6-8 格漫画展示品牌说话、行动、销售、应对竞争、处理批评的方式。",
    "辅助模块：语调、能量级、社交行为、沟通风格、DO/DON'T。",
    "所有颜色、服装、姿势必须源自 Logo 和品牌关键词。"
  ],
  "pitfalls": [
    "角色设计必须与品牌视觉一致，不能随意。",
    "每格漫画需有明确的品牌行为。",
    "DO/DON'T 模块必须具体，不能空泛。",
    "避免角色与品牌气质脱节。"
  ]
}
```

## Photo

```json
{
  "type": "Commercial photography",
  "subject": "[主体]",
  "scene": "[场景]",
  "camera": "[镜头/角度/景深]",
  "lighting": "[自然光/棚拍/电影感/轮廓光]",
  "texture": "[皮肤/布料/包装/金属/食物细节]",
  "composition": "[主体占比/留白/前景背景]",
  "constraints": "photorealistic, natural proportions, no plastic skin, no distorted hands",
  "useWhen": "用于人像、商品摄影和电影感写实场景。",
  "guidance": [
    "指定机位、镜头、光源、质感、背景和动作。",
    "加入可信的小瑕疵增强纪实感（皮肤纹理、雀斑、胶片颗粒）。",
    "使用技术参数（f/1.4、50mm）代替模糊描述。"
  ],
  "pitfalls": [
    "商业美妆之外，避免过度磨皮塑料感。",
    "需要时加入手部、文字、结构类负面约束。",
    "指定不完美细节：粗糙砖面、散落冰块、自然阴影、手持感。"
  ]
}
```

## 街拍抓拍摄影

```json
{
  "type": "Street Candid Photography",
  "moment": "[意外事件/日常瞬间]",
  "location": "[街头/室外地点]",
  "subject": "[物品/人物动作]",
  "material_state": "[材质状态描述：湿/脏/旧/破]",
  "environment": {
    "ground": "[地面材质]",
    "wall": "[墙面]",
    "street_scene": "[街景元素]"
  },
  "lighting": "[自然光/逆光/侧光/阴天]",
  "shadow": "[阴影描述]",
  "camera_perspective": "手机视角：手持、略俯或低角度、自然构图",
  "constraints": "raw unedited photo look, natural color, real texture, no illustration, no anime, no CGI, no studio lighting, no floating objects, no brand text, no watermark",
  "useWhen": "用于街头抓拍、意外瞬间、手机纪实、快速动作等场景。",
  "guidance": [
    "手机视角：手持、略俯或低角度、自然构图。",
    "要求 raw unedited photo look，自然色彩、真实质感。",
    "描述具体瞬间、机位高度、运动模糊和街景。",
    "加入避免摆拍和广告棚拍感的限制。"
  ],
  "pitfalls": [
    "禁止：插画、动漫、CGI、棚拍灯光、漂浮物体、品牌文字、水印、海报设计感。",
    "避免画面过于干净，要有街头质感。",
    "让事件看起来可信。",
    "不要做成杂志大片感，要纪实感。"
  ]
}
```

## Publication

```json
{
  "type": "Publication or document design",
  "format": "[杂志/菜单/报纸/笔记/课本/资料卡]",
  "topic": "[主题]",
  "layout": "[网格/栏目/封面/展开页]",
  "copy": ["[标题]", "[短说明]", "[标签]"],
  "style": "[编辑设计/手写/复古印刷/现代排版]",
  "constraints": "readable Chinese text, realistic page layout, no excessive small text",
  "useWhen": "用于白皮书、手册、百科图鉴、报告页面和出版系统。",
  "guidance": [
    "定义页面尺寸、分栏、目录、图表系统和字体层级。",
    "使用可读标题、表格、标签和页面节奏。",
    "结构优先：分栏和边距比风格形容词更重要。"
  ],
  "pitfalls": [
    "避免密集小字。",
    "让图表和说明对齐页面网格。",
    "正文使用模拟文本块，不要期望模型生成无错完整页面。"
  ]
}
```

## Space

```json
{
  "type": "Architecture or interior visualization",
  "space": "[建筑/室内/城市/展厅]",
  "function": "[用途]",
  "style": "[现代/新中式/未来/自然/极简]",
  "materials": ["[材质1]", "[材质2]"],
  "lighting": "[昼光/夜景/展陈灯光]",
  "camera": "[广角/正立面/鸟瞰/剖面]",
  "constraints": "coherent spatial logic, no impossible structure",
  "useWhen": "用于室内、建筑表现、城市地图、空间规划和环境概念图。",
  "guidance": [
    "定义视角、尺度、材质、光线和空间功能。",
    "使用 Eye-level perspective 防止透视畸变。",
    "冷暖对比（外部蓝灰 vs 内部黄橙）是提升质感的捷径。"
  ],
  "pitfalls": [
    "概念图之外要避免不合理透视。",
    "空间逻辑必须连贯，不能有不可能的结构。",
    "地图需锁定标签语言和相对位置。"
  ]
}
```

## Scene

```json
{
  "type": "Narrative scene",
  "story_moment": "[叙事瞬间]",
  "characters": ["[角色]"],
  "environment": "[场景]",
  "composition": "[电影构图/分镜/长卷/特写]",
  "mood": "[情绪]",
  "style": "[写实/插画/水墨/电影感]",
  "constraints": "one clear story moment, no unrelated elements",
  "useWhen": "用于分镜、世界观、直播场景和情绪叙事画面。",
  "guidance": [
    "定义人物、地点、时间、冲突、情绪和机位。",
    "让场景细节服务故事，而非装饰。",
    "使用电影镜头语言：Low angle shot、Dutch angle 增强戏剧张力。"
  ],
  "pitfalls": [
    "避免通用幻想背景。",
    "让故事线索在画面里可见。",
    "必须包含动词/动作，防止明信片式静止（如"正在崩塌""刚点燃火把"）。"
  ]
}
```

## 动作分解参考表

```json
{
  "type": "Action Breakdown Reference Sheet",
  "character": "[角色/人物]",
  "style": "[画风]",
  "action_sequence": "[动作序列描述]",
  "grid": {
    "layout": "4x4",
    "total_panels": 16,
    "per_panel": {
      "action_title": "[动作名称]",
      "pose": "[全身姿势]",
      "description": "3-4 行线性描述",
      "arrows": "[方向/旋转箭头叠加]"
    }
  },
  "consistency": "same face, clothing, proportions, hairstyle across all 16 panels",
  "constraints": "character consistency paramount, locked grid count, numbered panels, no costume drift",
  "useWhen": "用于角色动作分解、姿势参考表、动画参考、游戏动作设计。",
  "guidance": [
    "4×4 网格（16 面板），每格含：动作标题、全身姿势、3-4 行描述、方向箭头。",
    "角色一致性至上：同一张脸、服装、比例、发型贯穿所有面板。",
    "显式锁定网格数量、编号、每格结构。",
    "动作序列需有逻辑递进（如：待机→行走→奔跑→跳跃→攻击→受伤→倒地→起身）。"
  ],
  "pitfalls": [
    "避免不同动作里服装细节变化。",
    "画面拥挤时减少动作数量（可用 3×4 或 3×3）。",
    "角色一致性必须在 prompt 中显式声明。",
    "长序列更容易出现脸部/服装漂移，需加强约束。"
  ]
}
```

## 3D 收藏玩具

```json
{
  "type": "3D Collectible Toy",
  "source": "[参考照片描述或角色名称]",
  "identity_anchors": ["[脸型]", "[发型]", "[服装识别点]"],
  "toy_specs": {
    "head_ratio": "大头设计",
    "features": "略微夸张特征",
    "proportions": "玩具比例但保持高端设计感",
    "finish": "哑光乙烯基/树脂质感",
    "material_reflection": "真实材质反射"
  },
  "packaging": {
    "type": "[盲盒/展示盒/限量版盒]",
    "text": "[包装文字，少量且准确]"
  },
  "base": "[底座描述]",
  "lighting": "[展陈灯光/柔光/暗背景聚光]",
  "render_quality": "8K",
  "constraints": "preserve identity anchors, premium design feel, minimal packaging text, no generic toy body",
  "useWhen": "用于高级收藏玩具、头像公仔、潮玩角色和 3D 展示图。",
  "guidance": [
    "保留参考图中的脸和服装锚点。",
    "指定材质、包装、底座、光线和收藏比例。",
    "大头设计、略微夸张特征、玩具比例但保持高端设计感。",
    "哑光乙烯基/树脂质感，真实材质反射。"
  ],
  "pitfalls": [
    "避免没有身份细节的通用玩具。",
    "包装文字保持少量且准确。",
    "身份锚点（脸型、发型、服装）必须在写比例/材质前锁定。",
    "质感要像真实玩具，不能像 3D 渲染图。"
  ]
}
```

## Creative

```json
{
  "type": "Creative composite",
  "concept": "[创意概念]",
  "collision": ["[元素A]", "[元素B]"],
  "visual_metaphor": "[视觉隐喻]",
  "style": "[趣味/高级/超现实/混搭]",
  "constraints": "concept readable, not cluttered, no random collage",
  "useWhen": "用于创意合成、趣味混搭、跨界概念、超现实组合。",
  "guidance": [
    "先确定创意概念和视觉隐喻。",
    "两个碰撞元素需有概念关联，不能随机拼贴。",
    "一版主方案 + 一版备选方案。"
  ],
  "pitfalls": [
    "避免随机拼贴，概念必须可读。",
    "不要堆砌元素，保持画面干净。",
    "创意合成需要有故事或隐喻，不是单纯的元素叠加。"
  ]
}
```

## Illustration

```json
{
  "type": "Illustration",
  "subject": "[主体]",
  "style": "[日系/国风/水彩/扁平/科幻]",
  "composition": "[半身/全身/场景/封面]",
  "color": "[色彩]",
  "line_and_texture": "[线条/笔触/纸感]",
  "constraints": "consistent style, clear subject, no plastic 3D unless requested",
  "useWhen": "用于动漫、水彩、水墨、装饰画和风格实验。",
  "guidance": [
    "定义构图、主体、配色、笔触材质、情绪和完成度。",
    "参考图任务需要说明保留哪些特征。",
    "锁定笔触风格——没有它，输出默认为 AI 塑料风。"
  ],
  "pitfalls": [
    "避免只写风格，不写构图。",
    "使用参考图时锁定角色识别。",
    "不要直接写大师名字，提取其标志性特征（如"梵高的旋转星空笔触"）。"
  ]
}
```

### 附录：海报风格扩展

> 完整设计师风格词库：参见 `references/poster-artist-styles.md`（20位设计师，含完整 Prompt Modifiers）
> 完整构图模式词库：参见 `references/poster-composition-patterns.md`（8种构图模式，含示例 prompt）
> 使用：当用户描述海报风格时，从下方速查词库或上方参考文件精准匹配并注入 prompt。

#### 具名设计师风格（可直接写入 prompt style anchor）

| 风格锚定词 | 视觉特征 | 适用场景 |
|-----------|---------|---------|
| `Tyler Stout style` | 密集人物拼贴、繁复细节、最大化构图 | 电影、角色、史诗主题 |
| `Olly Moss style` | 极简负空间、1-2 色、图形化剪影 | 概念海报、极简活动 |
| `Martin Ansin style` | Art Deco 线条、优雅版刻、复古哑光调 | 文化、艺术、奢品 |
| `Mondo poster style` | 丝网印刷美学、限色块面、符号化叙事 | 限量版、独立活动、复古宣传 |
| `alternative movie poster` | 非字面场景、概念化视觉提炼 | 文艺片、节日、品牌再创 |

#### 丝网印刷质感词（Screen Print Texture）

将以下词组按需组合追加至 `constraints` 或 `style.texture`：

```
halftone dot texture
risograph printing effect
paper texture grain
slight misalignment between color layers
vintage print imperfections
screen print aesthetic
limited edition poster art
```

#### 限色策略（Limited Color Palette）

```
3-color screen print: [color 1], [color 2], [color 3]
duotone: [warm color] and [cool color]
70s palette: burnt orange, mustard yellow, brown
high contrast: bold [foreground color] on [background color]
```

#### 构图技法（Composition Technique，选 1-2 个注入 layout 槽）

```
centered symmetrical composition          → 正式、庄重
silhouette against [color] background     → 极简、符号感强
negative space storytelling               → Olly Moss 风
geometric framing (circles / triangles / arches) → 设计感强
layered depth: foreground / midground / background → 层次感强
```

#### 使用环境 × 设计要求对应表

| 使用环境 | 推荐对比度 | 文字密度 | 视距 |
|---------|-----------|---------|-----|
| 室内展览 / 画廊 | 中低对比 | 可稍密 | 1-3m |
| 室外广告 / 橱窗 | 高对比、粗字 | 极简 | 3-10m |
| 交通媒介（地铁/公交） | 高对比 | 1 句话 + 1 个视觉 | 快速浏览 |
| 社交媒体（手机屏） | 中高对比 | 短标题 + 短副标 | 拇指滚动 |
| 印刷单张传单 | 中等 | 适中 | 手持近距 |

#### 海报标准尺寸快查（生成前选定比例）

| 名称 | 尺寸 | 比例 | 常见用途 |
|-----|------|-----|---------|
| A4 传单 | 210×297mm | 1:1.41 | 线下传单、社媒竖图 |
| A3 小海报 | 297×420mm | 1:1.41 | 室内展示 |
| A2 标准海报 | 420×594mm | 1:1.41 | 活动展板 |
| A1 大海报 | 594×841mm | 1:1.41 | 户外、展览 |
| 社媒竖图 | - | 4:5 | Instagram / 小红书 |
| 社媒方图 | - | 1:1 | 通用方图 |
| 公众号封面 | - | 2.35:1 | 微信封面首图 |

## 个性化美妆报告

```json
{
  "type": "Personalized Beauty Report",
  "report_style": "[诊断报告/推荐卡片/导购助手]",
  "product": {
    "name": "[产品名]",
    "category": "[护肤/彩妆/香水/生活方式]",
    "key_ingredients": ["[成分1]", "[成分2]"],
    "skin_type": "[适用肤质]"
  },
  "layout": {
    "format": "[单卡/多卡对比/报告长图]",
    "hero_area": "产品图或成分可视化",
    "data_zones": ["肤质诊断", "产品推荐", "评分", "使用建议"],
    "rating_display": "[星级/百分制/雷达图]"
  },
  "style": {
    "palette": "[玫瑰金/裸色/粉调/冷白]",
    "typography": "elegant serif + clean sans",
    "imagery": "clean product shot with soft lighting"
  },
  "constraints": "readable labels, clear recommendation logic, no medical claims, no cluttered small text",
  "useWhen": "用于美妆推荐、肤质报告、导购助手和生活方式商品卡片。",
  "guidance": [
    "使用诊断、推荐和商品卡片的报告层级。",
    "对齐商品图、标签和评分。",
    "推荐逻辑清楚：肤质→问题→推荐产品→使用建议。",
    "评分和标签需对齐，不要东一块西一块。"
  ],
  "pitfalls": [
    "避免医疗化结论和难读小字。",
    "推荐逻辑必须清楚，不能只堆产品图。",
    "不要声称诊断或治疗效果。",
    "评分区域需统一格式。"
  ]
}
```

## 概念产品研发拆解

```json
{
  "type": "Concept Product Breakdown",
  "product": "[产品/概念]",
  "breakdown_format": "[爆炸拆解图/研发板/组件展示/混合任务]",
  "components": [
    {"name": "[组件1]", "material": "[材质]", "function": "[功能]"},
    {"name": "[组件2]", "material": "[材质]", "function": "[功能]"},
    {"name": "[组件3]", "material": "[材质]", "function": "[功能]"}
  ],
  "visual_system": {
    "background": "[纯白/浅灰/深色]",
    "labels": "[标注线/编号/短标签]",
    "arrangement": "[爆炸图/平铺/网格/层级]",
    "style": "[技术插画/产品渲染/混合媒介]"
  },
  "constraints": "clear component relationships, short labels, controlled technical style, no vague task boundaries",
  "useWhen": "用于实验型任务、研发视觉板、拆解图和特殊视觉系统。",
  "guidance": [
    "定义产物类型、组件、标签、材质逻辑和展示格式。",
    "使用清晰标注和受控技术风格。",
    "组件关系要清楚：哪个在前、哪个在内、哪个是核心。",
    "标签要短，用编号系统而非长段文字。"
  ],
  "pitfalls": [
    "避免任务边界过泛，需明确拆解什么。",
    "标签要短，组件关系要清楚。",
    "不要堆砌无关组件。",
    "技术风格要统一，不能混搭过多视觉语言。"
  ]
}
```

## 历史与古风题材

```json
{
  "type": "History & Classical Themes",
  "era": "[朝代/时期：唐代/宋代/明清/民国/西方古典]",
  "subject": "[人物/场景/器物/事件]",
  "visual_style": "[国潮/水墨/工笔/油画/版画/新中式]",
  "elements": {
    "architecture": "[建筑风格]",
    "costume": "[服饰]",
    "props": "[器物/道具]",
    "texture": "[质感：宣纸/绢帛/壁画/石刻]"
  },
  "composition": "[全景/半身/群像/场景叙事]",
  "palette": "[朱砂红/石青/赭石/金色/水墨黑白]",
  "constraints": "historical accuracy in costume and props, no anachronistic elements, coherent period aesthetic",
  "useWhen": "用于历史题材海报、古风人物设定、国潮视觉、朝代文化展示。",
  "guidance": [
    "锁定朝代/时期，明确服饰、建筑、器物的时代特征。",
    "选择视觉风格：国潮（现代+传统混搭）、水墨（留白写意）、工笔（精致细腻）。",
    "色彩参考对应时代的传统色谱。",
    "避免穿越感：不要在同一画面混搭不同时代的服饰和建筑。"
  ],
  "pitfalls": [
    "服饰和建筑必须对应正确朝代，不能穿越。",
    "不要把所有'古风'画成同一种风格。",
    "国潮≠堆砌传统纹样，需要有现代设计逻辑。",
    "水墨风格要留白，不能填满画面。"
  ]
}
```
