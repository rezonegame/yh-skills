# 检索与图谱增强（Retrieval & Graph Enhancement）

本文件定义 yh-local-knowledge 的结构化检索和轻量图谱能力，吸收自 knowhere（Ontos-AI/knowhere）的方法论。knowhere 是重型后端应用，但它的检索刻意不用向量——纯词法+结构+图谱——这套方法论可以用纯 JSON+纯算术移植到 prompt skill 形态。

核心理念（吸收自 knowhere）：**文档天然有结构，保留并利用结构比拍平后做相似度更可靠。** yh 不引入向量库，靠层次路径 + 关键词融合 + 轻量图谱实现精确检索。

## 一、章节树路径导航 + 动态大纲/水合（吸收点①）

### 为什么需要

yh 当前的检索偏关键词。取"某一节的完整内容"时，关键词命中可能只取到片段，丢失章节上下文。knowhere 的解法：让检索像"翻书"——先看目录大纲，再按章节下钻。

### path 字段（层次路径）

给可信资产和归一化后的内容都带一个层次 `path`：

```
path: [workspace]/[file]/[section1]/[section2]/...
例: 桌游设计/notes.md/核心概念/Agent定义
```

- 归一化阶段：从 markdown 标题层级提取 section 路径。
- 资产阶段：资产可显式声明它源自哪个 section（继承自来源的 path）。

path 是后续"路径通道检索"和"导航树构建"的基础。

### 导航树（doc_nav 式）

在 `.knowledge/indexes/nav.json` 维护一棵导航树（每个源文件一棵）：

```json
{
  "workspace": "桌游设计",
  "trees": {
    "notes.md": {
      "title": "notes.md",
      "path": "桌游设计/notes.md",
      "summary": "关于 AI Agent 的学习笔记",
      "children": [
        {
          "title": "核心概念",
          "path": "桌游设计/notes.md/核心概念",
          "summary": "Agent定义、工具调用、记忆",
          "children": [...]
        }
      ]
    }
  }
}
```

### 动态大纲/水合二态

检索/组装导出包时，对导航树采用二态处理（吸收 knowhere 的 hydration）：

- **大纲态**：未下钻的章节只渲染 `title + summary`，给 LLM/用户当导航线索。这样一棵大树的"骨架"占用很少 token。
- **水合态**：被明确选定的章节，其完整内容（text/image/table）才展开。

好处：处理大资料时，先给概览让用户/Agent 决定深挖哪一节，而不是一次性把全部灌进上下文。这和 yh 的"渐进式检索纪律"一致，但更结构化。

### 怎么用

- 用户问"这批资料里关于 Agent 记忆的部分"：先返回 nav.json 里含"记忆"的章节大纲 → 用户确认 → 水合该章节全内容。
- 组装"学习路径包"：沿导航树 BFS 选相关章节，只水合选中的，避免无关章节浪费 token。
- `scripts/build_index.py` 从 `.knowledge/normalized/` 自动构建 nav.json。

## 二、三通道 BM25 + RRF 融合（吸收点②）

### 为什么需要

单通道关键词容易漏召（关键词没命中就全丢）。knowhere 用三通道 + RRF 融合，多个弱信号叠加 > 单强信号。关键是路径通道——直接命中"知识在哪一节"，比纯内容匹配更精准。

### 三通道

对每条内容预切分三份索引文本（在 `.knowledge/indexes/search.json`）：

```json
{
  "items": [
    {
      "ref": "asset_001 或 normalized path",
      "path_text": "桌游设计 notes.md 核心概念 Agent定义",
      "content_text": "Agent 是自主规划并调用工具完成任务的系统...",
      "term_text": "Agent 自主 规划 工具调用 任务 系统",
      "path": "桌游设计/notes.md/核心概念/Agent定义"
    }
  ]
}
```

- **path 通道**：对 `path_text` 做关键词匹配，命中"知识在哪个章节"。
- **content 通道**：对 `content_text` 做关键词匹配，命中"说什么"。权重最高（默认 2.0）。
- **term 通道**：对 `term_text`（LLM 抽取的关键词/术语）做子串匹配，精确命中术语。权重默认 1.5。

### RRF 融合

Reciprocal Rank Fusion，纯算术，不需要分数归一化：

```
score = Σ_channel ( weight_channel / (k + rank_channel + 1) )
k = 60（经验值，防止 top-1 过度主导）
默认权重：path=1.0, content=2.0, term=1.5
```

每个通道各自排名（rank 从 0 开始），跨通道求和得最终分。命中多通道的条目自然上升。

### 为什么符合约束

这是纯词法方案，不需要 embedding 模型，不需要向量库。关键词匹配可以用 grep/正则实现，RRF 是几个除法加法。整个检索靠 `search.json` + 一段脚本/prompt 完成。

`scripts/build_index.py` 负责生成 search.json（含三份预切分文本 + path）。

## 三、轻量图谱 + 使用频次复利（吸收点③）

### 为什么需要

yh 已有"图谱/wiki"导出包和"复利闭环"，但缺一套具体的建边策略和使用频次信号。knowhere 的方案极简且可落地：关键词重叠建边 + 被检索次数喂 importance。

### 关键词节点 + 重叠建边

对每个可信资产，LLM 抽取 top_keywords（5-10 个）。在 `.knowledge/indexes/graph.json` 维护：

```json
{
  "nodes": [
    {
      "id": "asset_001",
      "title": "AI Agent",
      "keywords": ["Agent", "自主", "规划", "工具调用", "任务"],
      "importance": 0.8,
      "hit_count": 12,
      "last_hit_at": "2026-06-21T..."
    }
  ],
  "edges": [
    {
      "from": "asset_001",
      "to": "asset_002",
      "weight": 0.85,
      "shared_keywords": ["Agent", "规划", "工具调用"]
    }
  ]
}
```

建边规则（吸收 knowhere 的阈值思路，已放宽以捕捉对立观点关联）：
- 两资产关键词的 Jaccard 重叠度 ≥ 0.15 → 建边；或共享关键词 ≥ 2 → 建边。
- 特例：共享 1 个核心词且 Jaccard ≥ 0.1 也建边——这是为了让"对立但同主题"的观点关联起来（如归纳法 vs 演绎法共享"方法论"）。矛盾专题包依赖这种关联发现。
- 边的 weight = 重叠度（Jaccard）。完全无共享的不建边。
- 这是纯算术，不需要图数据库。

### importance 复利信号

吸收 knowhere 的 `retrieval_hit_stats`：
- 每次某资产被检索/引用/用于导出包，`hit_count += 1`，`last_hit_at` 更新。
- `importance = normalize(hit_count)` 归一化到 0-1，喂给排序和复利闭环。
- 被频繁使用的资产权重上升——这正是"复利"的量化体现：用得越多越重要。

### 与现有治理的融合

- 这个 graph.json 直接驱动"图谱/wiki 导出包"（之前只有 mermaid 示意，现在有真实边数据）。
- importance 信号喂给复利闭环：高 importance 资产在"推荐方向"简报里优先展示。
- lint 可检查 graph.json 一致性（孤立的 asset_001 在图里也应是孤立节点，对应 lint 的孤儿检测）。
- 这不绕过信任闸门——hit_count 只是统计信号，不改资产内容。

## 四、脚本支持

`scripts/build_index.py`（纯标准库）负责：
- 扫描 `.knowledge/normalized/` 和 `可信资产/`，构建 `nav.json`（导航树）。
- 生成 `search.json`（三通道预切分文本）。
- 生成/更新 `graph.json`（关键词节点 + 重叠边 + importance）。
- 增量：只重算变化的文件（基于 mtime），不每次全量重建。

关键词提取依赖 LLM（在提取阶段做，不是脚本做）；脚本只做重叠计算、RRF 索引生成、importance 统计。

## 五、不要做的事

- 不要引入向量库/embedding（knowhere 的方案本身就是词法的，无需向量）。
- 不要让图谱变成重型 KG（保持关键词重叠的极简策略，Jaccard 纯算术）。
- 不要让 hit_count 绕过信任闸门（使用频次只影响排序/推荐，不改资产内容或可信度）。
- 不要强制每个资产都进图谱（资产数少时图谱意义不大，可设阈值跳过）。
- 不要在水合时把整棵大树灌进上下文（默认大纲态，按需水合）。

## 六、与现有设计的兼容

- path 字段是新增（向前兼容，旧资产无 path 不影响）。
- nav.json/search.json/graph.json 都在 `.knowledge/indexes/`，是新增目录。
- 三通道检索是 extract/导出阶段的增强，不替代现有的"grep + offset/limit"渐进检索，而是叠加结构化导航。
- importance 信号是复利闭环的量化补充，不改变候选→确认闸门。
- 所有新增都符合"坚守 prompt skill 形态"——纯 JSON + 纯算术 + LLM 抽关键词。
