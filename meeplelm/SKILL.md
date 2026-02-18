---
name: meeplelm
description: MeepleLM 虚拟玩家测试技能。当用户要求"虚拟playtest"、"模拟玩家评测"、"MeepleLM"、"桌游AI评测"、"玩家人设模拟"、"MDA推理"、"生成桌游评测"、"virtual playtester"、"simulate player review"、"board game critique"、"persona simulation"时使用此技能。基于 MeepleLM 框架（arXiv:2601.07251），使用5种玩家人设（Persona）和 MDA（Mechanics-Dynamics-Aesthetics）推理链，由 Claude 直接模拟多样化桌游玩家的主观体验评测。
---

# MeepleLM: Virtual Playtester

基于 [MeepleLM](https://arxiv.org/abs/2601.07251) 框架（1,727 本结构化规则书 + 150K 条筛选评测），通过 Persona + MDA 推理链模拟桌游玩家主观体验。

核心原理：`Mechanics（规则）→ Dynamics（桌面交互）→ Aesthetics（情感体验）`

**关键语调：** 生成的评测是**游戏夜后的随手评论（comment）**，不是正式评测文章（formal review article）。语气应像在 BGG 上发帖分享感受，而非撰写学术分析。

## SOP: Execution Workflow

收到桌游规则书、规则描述或游戏名称时，严格按以下4步执行。

### Step 1: Parse Game Rules

提取关键信息：
- 回合结构与行动经济
- 资源系统与转化路径
- 胜利条件与计分
- 玩家互动方式（直接冲突/间接竞争/合作/谈判）
- 随机性来源与控制程度
- 核心决策点与张力来源

如输入为游戏名称而非规则书，基于已知知识构建规则摘要。可参考 `references/game-metadata.md` 中的 BGG Top 50 和测试集信息。

规则书标准格式见 `references/rulebook-format.md`，5个真实样例见 `references/sample-rulebooks/` 目录。

### Step 2: MDA Chain-of-Thought Reasoning

对每个 Persona 分别在 `<think>` 标签内执行三步因果推理（**不跳步**）：

```
<think>
1. Key Game Elements: {从规则中提取客观机制组件}
2. Gameplay Dynamics: {推理桌面上的运行时交互和涌现行为}
3. Persona Experience: {由 Persona 偏好调制的情感结果，解释评分动因}
</think>
```

| Step | MDA 层 | 内容 |
|------|--------|------|
| 1. Key Game Elements | Mechanics | 从规则中识别客观机制，确保评测有据可依 |
| 2. Gameplay Dynamics | Dynamics | 推理这些机制产生的交互模式 |
| 3. Persona Experience | Aesthetics | 综合 Persona 偏好，解释情感反应 |

完整模板、真实样例和 Alpaca 微调数据格式见 `references/prompt-templates.md`。

### Step 3: Generate Persona Reviews

对5种 Persona 分别生成评测。在生成前，先为该 Persona **确定立场（Determine Stance）**：

| 立场 | 含义 | 示例 |
|------|------|------|
| **Guilty Pleasure** | 与 Persona 偏好相反，但意外喜欢 | "我通常讨厌派对游戏，但这个机制让我笑了" |
| **Respectful Pass** | 承认设计好，但不适合自己 | "出色的设计，但不是我的菜" |
| **Perfect Match** | 完美契合 Persona 偏好 | "正是我想要的深度策略体验" |
| **Design Failure** | 即使类型匹配，设计也令人失望 | "本该是我喜欢的类型，但执行太差" |

每个 Persona 输出纯文本格式：

```
### [Persona 名称]

**评分：N / 10**

**评测理由：**
基于 MDA 推理的关键依据，说明该 Persona 为什么给出此评分（机制如何产生动态，动态如何触发该 Persona 的情感反应）。2-4 句话。

**评测：**
以该 Persona 第一人称视角撰写的主观评测。像在 BGG 论坛发帖，不是写学术论文。150-200 词目标，20-400 词变化范围。
```

**5种 Persona（详细定义见 `references/personas.md`）：**

| Persona | Core Motivation | Key Bias |
|---------|----------------|----------|
| **The System Purist** | 智力控制 | 厌恶运气，追求优化 |
| **The Efficiency Essentialist** | 乐趣/时间最大化 | 厌恶繁琐，追求心流 |
| **The Narrative Architect** | 沉浸与史诗感 | 机制服务主题 |
| **The Social Lubricator** | 人际连接 | 低门槛，社交优先 |
| **The Thrill Seeker** | 多巴胺刺激 | 拥抱风险与逆转 |

### Step 4: Synthesis Report

汇总分析：
- 各 Persona 评分分布表（含每个 Persona 的立场标签）
- 平均分与标准差
- 评分离散度分析（如果所有 Persona 评分过于接近，需重新校准）
- 核心受众识别（哪些 Persona 最喜欢/最不喜欢，及其原因）
- 设计薄弱环节分析
- 针对性改进建议

---

## Critical Simulation Guidelines

1. **Persona is a Bias, Not a Straitjacket** — 允许"Guilty Pleasures"和"Unexpected Disappointments"。不要做脸谱化模拟。
2. **Embrace Diversity** — 同一 Persona 内部有从纯粹主义者到杂食者的光谱。
3. **Ground in Dynamics** — 描述桌面交互（"投票机制引发搞笑争吵"），不要仅列出机制。将动态与情感反应关联。
4. **Review Length** — 目标 150-200 词，但必须有 20-400 词的显著变化以反映真实人类多样性。
5. **Rating Calibration** — 1-10 整数。不要所有 Persona 都给相似分数。匹配的 Persona 也可能给低分（设计失败），不匹配的也可能给高分（罪恶快感）。

---

## 参考文件

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| `references/prompt-templates.md` | System/User prompt 模板、MDA CoT `<think>` 格式规范、Alpaca 微调数据格式、3个真实 CoT 样例 | 执行 Step 2-3 时 |
| `references/personas.md` | 5种 Persona 完整定义（动机、画像、互动偏好、关键词） | 执行 Step 3 时 |
| `references/game-metadata.md` | BGG 167K 游戏排名结构、10K 详细信息格式、207 测试集 ID、Top 50 快速参考 | Step 1 需要查询游戏信息时 |
| `references/rulebook-format.md` | 标准化规则书 7 章节 Markdown 格式规范 | Step 1 解析规则时 |
| `references/sample-rulebooks/` | 5本真实规则书样例（Caverna, RA, Modern Art 等） | 需要参考规则书写作风格时 |
