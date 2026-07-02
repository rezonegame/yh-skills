# 来源与持续进化记录

本技能的底层协作精神来自以下已吸收的方法来源记录。它们不是使用时入口；除明确声明的独立 FigEdit 技能联动外，执行 `yh-slides` 时不得依赖外部仓库、外部索引资产或远程 slide runtime。

- `huashu-slides`
- `baoyu-slide-deck`
- `Kami`
- `huashu-design`
- `open-design`
- Open-Slide-style fixed-canvas authoring

## 已吸收原则

从 `huashu-slides` 吸收：

- 先确认协作模式，再进入制作；不要默认直接生成。
- 默认采用引导式协作，让用户在关键节点保持导演位。
- 在大纲、设计方向、成稿前预览等位置设置 checkpoint。
- 视觉风格不是单一默认值，而应从风格库中推荐、比较、确认。
- AI 是有审美判断和提案能力的共创伙伴，而不是问卷机器或纯执行脚本。

从其他参考源吸收：

- `baoyu-slide-deck`：端到端 slide deck 制作、图片型/可编辑型产物思路、批量生成与交付意识。
- `Kami`：文档与演示稿的排版质感、留白、层级、可读性，以及“成品要像认真设计过”的审美标准。
- `huashu-design`：设计哲学、风格家族、方向包与视觉语言拆解方法。
- `open-design`：开放式设计评审、5 维设计自评、反默认审美和质量门意识。

## 本地扩展

- 从原始 PPT / 图片路径扩展为 `Path A/B/C/D/E` 五类产物路径。
- 增加 `2A-S / Path S`：SVG → DrawingML 的高保真原生可编辑 PPTX 路径。
- 增加 `2A-T / Template Fill`：复用已有 PPTX 模板的原生填充路径。
- 将 `2B-R` 升级为独立 FigEdit 联动的正式位图可编辑重建路径；`yh-slides` 只维护发现、批处理、质量门与整套导出，不复制 OCR/CV/重建内核。
- 增加 `2D-P / Presenter Mode`：带逐字稿、当前/下一页预览和计时器的 HTML 演讲者模式。
- 增加 `Path E` 本地 React Deck 方法，但不默认依赖 Open-Slide 或其他外部 slide runtime。
- 增加品牌系统、事实缺口、图片策略、TTS、HTML magazine、动效等复杂场景支持。
- 增加 P0-P3 分级质量检查和 5 维设计自评。
- 增加风格地图：先展示风格家族，再推荐 3 个方向，并保留样张和自定义入口。
- 增加质量基线判断、页型覆盖检查、模板矿化、视觉截图 QA 和评论迭代循环。
- 增加完整本地吸收资产库：`ppt-master`、`guizang-ppt-skill`、`html-ppt-skill` 的可用模板、主题、脚本和运行时已吸收到 `templates/`、`assets/`、`scripts/`、`references/provenance/`，统一通过 `references/meta/asset-registry.json` 调用。
- 增加离线稳定门：`check_offline_ready.py`、`check_yh_slides_integrity.py`、`build_asset_registry.py`、`check_upstream_locks.py`。
- 从 `Ian Handdrawn PPT` 吸收中文手绘技术解释方法：固定视觉外壳、物件语义图、短文字约束、页型原型和联系表 QA；接入现有 2B/2C，不新增路径，不设为全局默认。

## 维护原则

- 后续迭代不能牺牲 `huashu-slides` 的启发式共创入口。
- 除独立 FigEdit 联动外，运行时仍不得依赖未声明的外部仓库或远程 slide runtime。
- 新增能力必须服务用户选择，而不是隐藏选择权。
- 任何重要分支都应保留“推荐项 / 备选项 / 自定义入口 / 风险提示”。
- 本地模板库不得替代 Step 0 意图启动、Step 3 大纲确认、Step 4 风格确认、样稿 checkpoint 和 P0-P3 QA。
- AGPL 来源资产必须保留清晰 provenance；更新上游 lock 或重新吸收资产后必须重跑离线自检。
