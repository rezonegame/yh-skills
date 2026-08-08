# Evidence-Driven PPT Methodology

> 吸收自 Tosea.ai 全量研究（2026-08-05）：官网+Showcase+Blog+58模板+24个社区GitHub项目
> 来源：Tosea.ai / McKinsey-style 8 rules / 14 Layout Patterns / 6 反AI-slop 层级 / 6 Tier-S slide skills

---

## 1. Source-Grounded 五阶段工作流

当输入是**已有文档**（PDF/Word/论文/报告）时，不走 prompt-first 路径，走 document-to-slide pipeline：

```
① 上传解析 → 提取文本/图表/公式/图片/表格
② AI 问 3 个决策问题 → 用户确认 → 生成 slide-by-slide 大纲
③ 用户审查 storyline + evidence placement + visual opportunities
④ 渲染幻灯片（每页含 Speaker Notes）
⑤ 双模式精修 → 可编辑 PPTX 导出
```

### 阶段① 脚本调用（PDF 输入时强制执行）

当源文件是 PDF 时，**先运行 `pdf_evidence_pipeline.py` 提取结构化证据，再进入阶段②**。不要跳过直接靠 LLM 读 PDF——脚本提取的标题层级、图片、表格和公式检测比 LLM 逐页阅读更精确，且自动生成 Slide-to-Source Register 草稿。

```bash
# 基础用法
python scripts/pdf_evidence_pipeline.py input.pdf --output-dir ./output --max-pages 50

# 输出文件用途
#   evidence.json   → 阶段②生成大纲的输入（标题层级、正文块、图片清单、表格、公式）
#   outline.json    → slide-by-slide 大纲草案，供阶段②③参考和修改
#   register.csv    → Slide-to-Source 追溯表草稿，阶段③审查时逐行验证
#   images/         → 提取的图片，阶段④渲染时直接引用
#   tables/         → 提取的表格（CSV），阶段④渲染数据页时引用
```

**非 PDF 输入**（Word/网页/纯文本）：没有等价脚本，直接由 LLM 解析内容并手工构建 evidence 结构（headings/body/images/tables），在生成大纲前完成 Source Inventory（第 7 节）。

### 3 个决策问题（阶段②必问）

1. **Emphasis（重点）**：哪部分是核心？宏观框架？具体案例？方法论？
2. **Audience（受众）**：决策级（委员会/董事会）？教学级（学生/参会者）？销售级？
3. **Depth（深度）**：高信念摘要？完整分析？

### 双模式精修（阶段⑤）

- **Layout Only**：只换版式，不动内容
- **Refine Everything**：内容+版式都可以改

---

## 2. McKinsey 咨询级 8 条规则

### Rule 1: Storyline 先行
- 先写答案的一句话总结
- 列支撑论点 → 每个论点下放最强证据
- 形成 argument tree：结论 → 论点 → 证据 → 行动
- **测试**：仅读标题就能复现完整论证

### Rule 2: 每个标题都是结论
- Topic title（主题标题）→ Action title（行动标题）
- ❌ 弱：`Market growth`
- ✅ 强：`Premium demand will account for most category growth through 2029`

### Rule 3: 每页一个主要任务
- 完成这句话："The audience should leave this page understanding that..."
- 答案有多个无关从句 → 拆页

### Rule 4: 视觉形式匹配信息关系

| 信息关系 | 推荐视觉 |
|---------|---------|
| 时间变化 | 折线图 / 时间线 |
| 类别比较 | 排序柱状图 |
| 贡献拆解 | 瀑布图 / 堆叠柱状图 |
| 二变量分类 | 2×2 矩阵 |
| 有序动作 | 流程图 |
| 循环活动 | 循环图 |
| 问题成因 | 鱼骨图 |
| 工作流+日期 | 甘特图 |
| 组织层级 | 层级图 |
| 现状 vs 未来 | 双列对比 |

### Rule 5: 图表是证据不是装饰
- 移除不帮助读者的 series/labels/gridlines
- 一个 accent color 给主证据，neutral 给上下文
- 每个重要数字配 source note

### Rule 6: 间距建层级
- 弱 slide 用边框/图标/阴影补偿层次不清
- 咨询风格：顶部窄标题区 → 稳定内容网格 → 一致边距 → 对齐的图表文字边缘 → 证据与推论分离
- W3C 对比度：正常文字 4.5:1，大文字 3:1

### Rule 7: 功能性页面模板复用
封面/章节页 → 执行摘要 → 论点+证据页 → 对比页 → 数据图表页 → 流程/时间线页 → 建议+下一步页 → 附录

### Rule 8: 三遍审查
- **第一遍**：仅读标题，检查论证是否得出清晰建议
- **第二遍**：验证每个数字、单位、日期、计算、来源
- **第三遍**：检查对齐、间距、排版、颜色、导出质量

### 6 种常见失败模式

| 失败模式 | 症状 | 修复 |
|---------|------|------|
| The data dump | 一页四图表+十二条 bullet | 一页一 claim |
| Topic titles | "Q3 results" | 重写为 takeaway |
| The decorated slide | 图标/阴影代替层次 | 去装饰，用网格重建 |
| Geometry mismatch | 线性流程用循环图 | 重新匹配视觉形式 |
| Orphaned numbers | 数字无来源 | 每页 source note |
| Storyline drift | 标题串起来不构成论证 | 标题-only 审查先做 |

---

## 3. 14 Layout 选择系统

### 选择前回答 5 问

1. 顺序重要吗？
2. 项目是并列、层级、还是因果关系？
3. 受众在比较替代方案吗？
4. 是否一个结论应该占据大部分页面？
5. 受众需要查看精确数据吗？

### 速查表

| 模式 | 适用 | 关键规则 |
|------|------|---------|
| Hero page | 一个结论/大数字 | 发现占据大部分页面 |
| Two-column | 对比/before-after | 保持类别平行 |
| Card grid | 3-6 并列想法 | 超过6个拆页 |
| Process arrows | 有序步骤 | 轴表示序列 |
| Timeline | 日历事件 | 水平轴间距与时间成比例 |
| Cycle | 循环/反馈 | 最后一步回到第一步 |
| Gantt | 并行工作流 | 重叠时使用 |
| Hierarchy/Pyramid | 组织层级 | staircase=累积，pyramid=比例 |
| Matrix/Quadrant | 两轴分类 | 两轴命名、连续、独立 |
| Funnel | 数量递减 | 宽度与数量成比例 |
| Fishbone | 一问题多成因 | 问题陈述单一可测量 |
| Strategy map | 因果目标 | 每连接器能口头解释 |
| Target/Bullseye | 距核心远近 | 环位置=优先级 |
| Chart/Table | 定量证据 | chart看趋势，table看精确值 |

### 按 deck 类型的 layout 分布

| Deck 类型 | 主要 layout | 特点 |
|-----------|------------|------|
| 咨询/策略 | Hero + Matrix | 每页 action title |
| 董事会/投资者 | 大数字页 + 时间线 + 干净对比表 | 图解比预期少 |
| 季度业务回顾 | 前部时间线，后部 card grid | 先发生了什么，再做什么 |
| 财报/财务更新 | 表格 + 图表 | 受众会引用数字 |
| 学术演讲 | 流程图(方法) + 图表(结果) + Hero(贡献) | 压缩取决于时长 |

---

## 4. 6 层反 AI-Slop 体系

| 层级 | 策略 | 技术实现 |
|------|------|---------|
| **L0 源头预防** | Source-grounded generation | 所有内容来自源文件，AI 只做转录和重组 |
| **L1 结构控制** | Outline-first + storyline 审查 | 渲染前先审查结构问题 |
| **L2 视觉匹配** | Layout 形式匹配信息关系 | 防止 geometry mismatch |
| **L3 质量门控** | 多 checkpoint 审查 / 3-pass review | 故事→数据→像素分别检查 |
| **L4 输出保真** | Editable PPTX + preview-export 一致性 | 避免 flat image 陷阱 |
| **L5 组合多样性** | Token-based anti-slop / 50K+ designs | 防止模板化重复 |

### 反 AI-Slop 检查清单

**内容真实性**
- [ ] 每个关键数字能追溯到源文件具体页码
- [ ] 没有不在源文件中的 claim
- [ ] 图表数据与源文件一致
- [ ] 引用/来源信息完整

**结构逻辑**
- [ ] 仅读标题能复现完整论证
- [ ] 每页只有一个主要任务
- [ ] 标题是 action title 不是 topic title
- [ ] storyline 没有漂移

**视觉设计**
- [ ] layout 形式匹配信息关系
- [ ] 没有过度装饰代替层次
- [ ] 网格/间距/对齐一致
- [ ] 对比度满足 4.5:1
- [ ] 不通过缩小字体解决拥挤

**技术质量**
- [ ] 导出的 PPTX 文本可编辑
- [ ] preview 与 export 高度一致
- [ ] 图层没有重叠

---

## 5. Slide-to-Source Register

对 evidence-driven deck（从文档生成的 PPT），维护追溯表：

```
| Slide # | Claim/数据 | 源文件 | 源页码 | 备注 |
|---------|-----------|--------|--------|------|
| 3 | UBER BB+ 评级 | barclays.pdf | p.12 | 表2 |
| 5 | BBB 利差 125bps | barclays.pdf | p.8 | 图3 |
```

生成时自动填充，审查时逐行验证。

---

## 6. Evidence-Driven 设计 DNA

### 色彩：二值承诺
- 纯亮（>235 brightness）或 纯暗（<25）
- **禁止**中等灰背景——要么"纸张"，要么"影院"
- 品牌色作为 data 页的全幅背景

### 字体：Serif = 权威，Sans = 清晰
- 40% Serif display + Sans body（学术/古典）
- 35% Sans display + Sans body（现代/数据）
- 15% 单一字族 weight 对比（极简）

### 层级比：标题:正文 = 4:1 ~ 5:1
- 远高于 AI PPT 的 ~2:1
- 创建强有力的视觉锚点

### 节奏：亮度震荡
- 暗封面 → 亮内容 → 暗数据表 → 亮结尾
- 创建电影般的步调，不是平面统一

### 内容结构：论点→证据→含义
- 不是 bullet list
- 三点证据结构（thesis → 3 evidence points → implication）

### 左轨导航（内容页）
- "book chapter" 比喻
- 封面无导航，内页有持续导航

---

## 7. Source Inventory 映射

从文档生成 deck 时，**枚举源文档全部内容项**，确保 100% 映射到 slide：

1. 读完源文档，列举每个 section/subsection/card/table row/decision/footnote
2. 为每个项目分配 slide 位置
3. 规则：
   - 6 个决策 → 全部出现，不是只放能塞下的 2 个
   - 7 行表格 → 7 行全部出现
   - 折叠/附录内容 → 成为独立 slide
   - 子节有多卡片 → 可能需要 2-3 slide 覆盖

---

## 8. 场景化工作流矩阵

| 场景 | Storyline 重点 | Layout 偏好 | 页数 | 核心挑战 |
|------|---------------|-------------|------|---------|
| 商业/咨询 | 结论先行，金字塔原理 | Hero + Matrix + Waterfall | 10-20 | 信息密度控制 |
| 金融/投资 | 数据驱动 | Table + Chart + Comparison | 12-15 | 数字精确性 |
| 学术/研究 | 问题→方法→结果→贡献 | Process + Chart + Hero | 6-15 | 严谨性保持 |
| 教学/培训 | 认知科学，知识留存 | Card grid + Process + Cycle | 15-30 | 分层递进 |
| 技术/产品 | 功能→价值→实现 | Architecture + Timeline + Comparison | 10-20 | 抽象层次管理 |
| 董事会 | 决策/行动导向 | 大数字 + Timeline + 对比表 | 8-12 | 简洁有力 |

---

## 9. Swiss Locked Mode 字重阶梯

当使用瑞士国际主义风格时：

- ≥ 8vw → weight **200** (ExtraLight)
- 4-7.9vw → weight **300** (Light)
- 2-3.9vw → weight **400** (Regular)
- 1-1.9vw → weight **500** (Medium)
- <1vw / caption → weight **700** (Bold)

原则：**越大越细，越小越粗**

字号下限：
- 正文段落 ≥ 18px
- 卡片描述/caption ≥ 16px
- meta/kicker/label ≥ 14px
- 超出不缩字，而是删减文案/拆页/换版式

---

## 10. 可复用提示词模板

### 咨询级 Deck
```
Create an executive presentation from the attached source material.
Audience: senior decision-makers
Structure: conclusion-first storyline with one main message per slide
Titles: write action titles that state the takeaway
Evidence: preserve important numbers, tables, charts, figures, and source context
Visual style: restrained consulting presentation with clear hierarchy, consistent grid, generous white space
Layouts: choose comparison, process, timeline, matrix, hierarchy, or chart layouts according to the information relationship
Output: editable 16:9 PowerPoint deck with source notes
Before rendering, show the slide-by-slide outline and proposed layout for approval.
```

### 研究论文演讲
```
Turn this research paper into a conference-style presentation. Preserve the research
question, method, experimental setup, key figures, results, limitations, and conclusion.
Keep the explanation accurate but presentation-friendly. Use editable slide text and
keep figures connected to the source.
```

### 财务报告
```
Convert this financial report into an editable PowerPoint deck for an analyst review.
Preserve key tables, charts, ratios, risk factors, and management commentary. Do not
invent numbers. Use a clear investment committee style with concise headlines and
source-grounded evidence.
```
