# Metrics Schema

本文档说明 boardgame-ralph-loop 中使用的数据结构和指标追踪系统。

## grd.json 结构

`grd.json` (Game Requirements Document) 是 Ralph Loop 的核心状态文件，追踪所有设计任务和适应度分数。

### 完整结构

```json
{
  "gameName": "游戏名称",
  "version": "当前版本号",
  "branchName": "Git 分支名",
  "lastUpdated": "最后更新时间",

  "gameOverview": {
    "theme": "游戏主题",
    "playerCount": {"min": 2, "max": 4, "recommended": 3},
    "duration": {"target": 45, "unit": "minutes"},
    "age": {"min": 12},
    "mechanics": ["机制1", "机制2"]
  },

  "fitnessGoals": {
    "clarity": {"current": 7.5, "target": 8.0, "description": "规则清晰度"},
    "strategy": {"current": 7.0, "target": 7.5, "description": "策略深度"},
    "interaction": {"current": 6.5, "target": 7.0, "description": "玩家互动"},
    "balance": {"current": 7.0, "target": 7.5, "description": "游戏平衡"},
    "fit": {"current": 7.5, "target": 8.0, "description": "主题适配度"}
  },

  "design_tasks": [
    {
      "id": "DT-001",
      "title": "任务标题",
      "description": "详细描述",
      "acceptanceCriteria": ["标准1", "标准2"],
      "priority": 1,
      "passes": false,
      "notes": "",
      "category": "core|component|documentation"
    }
  ],

  "playtest_tasks": [
    {
      "id": "PT-001",
      "title": "测试标题",
      "description": "详细描述",
      "acceptanceCriteria": ["标准1", "标准2"],
      "priority": 1,
      "passes": false,
      "notes": "",
      "category": "validation|session|ux"
    }
  ],

  "balance_tasks": [
    {
      "id": "BT-001",
      "title": "平衡任务标题",
      "description": "详细描述",
      "acceptanceCriteria": ["标准1", "标准2"],
      "priority": 1,
      "passes": false,
      "notes": "",
      "category": "component|mechanics|flow"
    }
  ],

  "metadata": {
    "totalTasks": 11,
    "completedTasks": 0,
    "totalPlaytests": 0,
    "currentIteration": 0,
    "designStarted": "2025-01-24",
    "lastPlaytest": null,
    "targetCompletion": null
  }
}
```

## 任务类型详解

### Design Tasks (design_tasks)

设计类任务，创建或修改游戏组件。

**Category 类型**:
- `core`: 核心机制设计
- `component`: 组件设计（卡牌、棋盘、板块等）
- `documentation`: 文档编写

**示例**:
```json
{
  "id": "DT-001",
  "title": "设计核心回合结构",
  "description": "定义游戏的回合流程和阶段",
  "acceptanceCriteria": [
    "清晰描述所有回合阶段",
    "定义阶段转换条件",
    "文档完整且逻辑一致"
  ],
  "priority": 1,
  "passes": false,
  "notes": "",
  "category": "core"
}
```

### Playtest Tasks (playtest_tasks)

测试类任务，进行 playtest 会话并记录数据。

**Category 类型**:
- `validation`: 验证机制可行性的测试
- `session`: 正式游戏测试会话
- `ux`: 用户体验测试

**示例**:
```json
{
  "id": "PT-001",
  "title": "2人游戏测试",
  "description": "进行2人配置的完整游戏测试",
  "acceptanceCriteria": [
    "完成至少2局游戏",
    "记录玩家策略和选择",
    "测量实际游戏时长",
    "记录所有问题",
    "计算适应度分数",
    "创建测试记录文档"
  ],
  "priority": 1,
  "passes": false,
  "notes": "",
  "category": "session"
}
```

### Balance Tasks (balance_tasks)

平衡类任务，分析数据并调整游戏平衡。

**Category 类型**:
- `component`: 特定组件的平衡分析
- `mechanics`: 机制的平衡调整
- `flow`: 游戏流程和节奏的平衡

**示例**:
```json
{
  "id": "BT-001",
  "title": "分析卡牌平衡性",
  "description": "基于测试数据分析所有卡牌的强度",
  "acceptanceCriteria": [
    "统计每张卡牌使用率",
    "识别主导/弱势卡牌",
    "计算卡牌对胜率的贡献",
    "提出具体的平衡调整方案",
    "更新卡牌设计文档"
  ],
  "priority": 2,
  "passes": false,
  "notes": "",
  "category": "component"
}
```

## 适应度分数追踪

### Fitness Goals 结构

```json
"fitnessGoals": {
  "clarity": {
    "current": 7.5,      // 当前分数
    "target": 8.0,       // 目标分数
    "description": "规则清晰度"
  }
}
```

### 评分更新时机

适应度分数应该在以下情况更新：

1. **每次 Playtest 任务完成后**
   - 基于 test session 的实际观察评分
   - 更新所有五个维度

2. **每次 Balance 任务完成后**
   - 主要更新 Balance 和 Strategy 分数
   - 其他维度可能也受影响

3. **设计重大变更后**
   - 评估变更对各维度的影响
   - 更新相关维度分数

## Metadata 追踪

`metadata` 部分提供整体项目状态的快照：

```json
"metadata": {
  "totalTasks": 11,           // 所有任务总数
  "completedTasks": 3,        // 已完成任务数
  "totalPlaytests": 2,        // 累计测试次数
  "currentIteration": 5,      // 当前迭代次数
  "designStarted": "2025-01-24",
  "lastPlaytest": "2025-01-26",
  "targetCompletion": null    // 预计完成日期（可选）
}
```

## 平衡性数据文件

### strategy_matrix.json

追踪不同策略的表现：

```json
{
  "version": "v0.1.0",
  "lastUpdated": "2025-01-24",
  "strategies": [
    {
      "name": "快攻策略",
      "playCount": 5,
      "winCount": 3,
      "winRate": 0.6,
      "avgScore": 85,
      "games": [
        {"date": "2025-01-24", "players": 2, "winner": true},
        {"date": "2025-01-24", "players": 3, "winner": false}
      ]
    },
    {
      "name": "资源积累策略",
      "playCount": 5,
      "winCount": 2,
      "winRate": 0.4,
      "avgScore": 78,
      "games": []
    }
  ]
}
```

### economy_tracker.json

追踪经济系统的平衡：

```json
{
  "version": "v0.1.0",
  "resources": {
    "gold": {
      "avgStart": 0,
      "avgEnd": 15,
      "avgPerTurn": 2.5,
      "games": []
    },
    "wood": {
      "avgStart": 0,
      "avgEnd": 12,
      "avgPerTurn": 2.0,
      "games": []
    }
  }
}
```

### player_count_matrix.json

追踪不同玩家人数下的游戏表现：

```json
{
  "version": "v0.1.0",
  "playerCounts": [
    {
      "count": 2,
      "games": 3,
      "avgDuration": 42,
      "avgScores": [85, 82],
      "balance": 8.5
    },
    {
      "count": 3,
      "games": 2,
      "avgDuration": 58,
      "avgScores": [78, 82, 75],
      "balance": 7.0
    },
    {
      "count": 4,
      "games": 1,
      "avgDuration": 65,
      "avgScores": [70, 75, 72, 73],
      "balance": 6.5
    }
  ]
}
```

## 使用 jq 查询数据

```bash
# 查看所有任务状态
cat grd.json | jq '.design_tasks[] | {id, title, passes}'

# 查看适应度分数
cat grd.json | jq '.fitnessGoals'

# 统计完成任务数
cat grd.json | jq '[.design_tasks[], .playtest_tasks[], .balance_tasks[] | select(.passes == true)] | length'

# 查找下一个任务（优先级最高且未完成）
cat grd.json | jq '[.design_tasks[], .playtest_tasks[], .balance_tasks[]] | sort_by(.priority) | .[0]'

# 检查是否所有任务完成
cat grd.json | jq '[.design_tasks[], .playtest_tasks[], .balance_tasks[] | .passes] | all'
```

## 测试记录文件

每次 playtest 应创建独立的记录文件：`playtests/YYYY-MM-DD_sessionN.md`

使用模板：[assets/templates/playtest_template.md](../assets/templates/playtest_template.md)

关键数据点：
- 玩家信息和策略
- 游戏结果（时长、获胜者、分数）
- 问题记录（严重/中等/轻微）
- 适应度评分
- 观察（流程/策略/互动/平衡性）
- 数据统计（资源使用、行动选择）
