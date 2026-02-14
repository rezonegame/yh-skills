# 迭代包模板 (ITERATION PACKAGE TEMPLATE)

**方案C：单一Skill + 增强迭代包**

每个迭代包包含：
- 📄 **人类可读部分**：Markdown格式的完整文档
- 📊 **机器可读部分**：JSON格式的结构化数据

---

## 命名规范

### 游戏项目文件夹
```
[GameName_English]_Design/
```

**规则：**
- 使用英文或拼音
- 无空格，单词间用下划线连接
- 首字母大写
- 以 `_Design` 结尾表示这是设计文件夹

**示例：**
```
Dragon_Valley_Design/
Star_Traders_Design/
Mystery_Mansion_Design/
```

### 迭代包文件
```
iteration_v[X.X.X]_[YYYY-MM-DD]_[type].md
```

**类型标识：**
- `record` - 记录模式（原始playtest记录）
- `analysis` - 分析模式（已分析的迭代包）
- `plan` - 计划模式（下一版本的迭代计划）

**示例：**
```
iteration_v0.1.0_2024-01-15_record.md
iteration_v0.1.0_2024-01-15_analysis.md
iteration_v0.1.1_2024-01-16_plan.md
```

### 项目文件夹结构
```
[GameName]_Design/
├── 00_GAME_BRIEF.md           # 游戏概要
├── iterations/                 # 所有迭代包
│   ├── iteration_v0.1.0_2024-01-15_record.md
│   ├── iteration_v0.1.0_2024-01-15_analysis.md
│   ├── iteration_v0.1.1_2024-01-16_plan.md
│   └── ...
├── components/                 # 组件文件
│   ├── cards/
│   ├── board/
│   └── tokens/
├── rulebook/
│   ├── RULEBOOK_DRAFT.md
│   └── RULEBOOK_vX.X.X.md
└── CHANGELOG.md               # 版本变更历史
```

---

## 迭代包完整模板

```markdown
# ITERATION PACKAGE
**游戏名称：** [GameName]
**迭代版本：** v[X.X.X] → v[X.X.X]
**日期：** YYYY-MM-DD
**类型：** record / analysis / plan

---

## 📋 METADATA

| 字段 | 值 |
|------|-----|
| Game_Name | [游戏英文名] |
| Version_From | vX.X.X |
| Version_To | vX.X.X |
| Date | YYYY-MM-DD |
| Type | record/analysis/plan |
| Player_Count | X |
| Test_Location | [地点/线上] |
| Tester_Experience | [新手/普通/专家] |

---

## 🎯 TESTING FOCUS

本次测试的重点：
- [ ]
- [ ]
- [ ]

---

## 📊 PLAYTEST SUMMARY

### What Happened
[简要描述游戏过程]

### Session Metrics
| 指标 | 实际 | 目标 | 状态 |
|------|------|------|------|
| 游戏时长 | __分钟 | __分钟 | ✅/❌ |
| 规则问题数 | __ | <3 | ✅/❌ |
| 分析停顿时长 | __秒 | <30秒 | ✅/❌ |
| 获胜起始位置 | __ | - | 记录 |

### Observations
| 时间 | 事件 | 观察 |
|------|------|------|
| | | |

### Body Language Notes
- **参与度：** 高/中/低
- **困惑时刻：**
- **兴奋时刻：**
- **挫折点：**

---

## 💬 FEEDBACK SUMMARY

### The Magic Question
*"如果让你再次游玩，只改变一样东西就能让游戏提升5%，那会是什么？"*

**回答：**

### Most Fun Part
**最有趣的部分：**

### Least Fun Part
**最不有趣的部分：**

### Agency & Choices
**是否有意义的决策？** 是/否
**说明：**

### Would Play Again
**是否愿意再玩？** 是/否/也许
**原因：**

### Additional Feedback
[其他反馈]

---

## 🔍 5-COMPONENT ANALYSIS

| 组件 | 评分 (1-5) | 关键问题 | 优先级 |
|------|-----------|----------|--------|
| **Clarity** | ? | | |
| **Strategy** | ? | | |
| **Interaction** | ? | | |
| **Satisfaction** | ? | | |
| **Fit** | ? | | |

**评分说明：**
- 1 = 严重问题，必须修复
- 2 = 有明显问题
- 3 = 基本满足
- 4 = 很好
- 5 = 优秀

---

## 🧅 ROOT CAUSE ANALYSIS (5 Whys)

**问题：** [描述主要问题]

1. 为什么？
2. 为什么？
3. 为什么？
4. 为什么？
5. **根本原因：**

---

## 📝 IDENTIFIED ISSUES

| 优先级 | 问题描述 | 类别 | 影响组件 | 状态 |
|--------|----------|------|----------|------|
| 高 | | | | 待处理 |
| 中 | | | | 待处理 |
| 低 | | | | 待处理 |

**类别：** Clarity / Strategy / Interaction / Satisfaction / Fit

---

## ✅ CHANGES PROPOSED

### Change 1
- **What（改什么）：**
- **Why（为什么）：**
- **Expected Impact（预期影响）：**
- **Revert Difficulty（回滚难度）：** 易/中/难
- **Risk Assessment（风险评估）：** 低/中/高

### Change 2
- **What:**
- **Why:**
- **Expected Impact:**
- **Revert Difficulty:**
- **Risk Assessment:**

---

## ❌ WHAT WE'RE NOT CHANGING

| 决定不改动的内容 | 原因 |
|-----------------|------|
| | |
| | |

---

## 🎯 NEXT VERSION PLAN

### Version Number
**从：** vX.X.X
**到：** v[X.X.X]
**原因：** [PATCH/MINOR/MAJOR 变更]

### Testing Focus for Next Version
1. [ ]
2. [ ]
3. [ ]

### Success Criteria
- [ ] [具体可验证的标准]
- [ ] [具体可验证的标准]
- [ ] [具体可验证的标准]

---

## 📚 REFERENCE FRAMEWORDS APPLIED

本次迭代中参考的设计框架：
- [ ] 5-Component Filter
- [ ] MDA Framework
- [ ] Player Experience First
- [ ] Building Blocks Framework
- [ ] Psychology of Choice
- [ ] Single-Change Rule
- [ ] 5-Whys Technique

---

## 📎 ATTACHMENTS

- [ ] 反馈表单
- [ ] 照片/视频
- [ ] 规则书版本
- [ ] 组件版本

---

## 💡 NOTES

[任何额外的备注、想法、待办事项]

---

```json
{
  "package_version": "1.0",
  "game_info": {
    "name": "",
    "version_from": "0.0.0",
    "version_to": "0.0.0",
    "date": "YYYY-MM-DD",
    "type": "record"
  },
  "session": {
    "player_count": 0,
    "player_names": [],
    "experience_level": "beginner/intermediate/expert",
    "location": "",
    "duration_minutes": 0
  },
  "metrics": {
    "game_length": {
      "actual": 0,
      "target": 0,
      "status": "pass/fail"
    },
    "rules_questions": {
      "count": 0,
      "target": 3,
      "status": "pass/fail"
    },
    "analysis_paralysis": {
      "max_seconds": 0,
      "target": 30,
      "status": "pass/fail"
    },
    "winner_starting_position": 0
  },
  "component_ratings": {
    "clarity": {
      "score": 3,
      "issues": [],
      "priority": "high/medium/low"
    },
    "strategy": {
      "score": 3,
      "issues": [],
      "priority": "high/medium/low"
    },
    "interaction": {
      "score": 3,
      "issues": [],
      "priority": "high/medium/low"
    },
    "satisfaction": {
      "score": 3,
      "issues": [],
      "priority": "high/medium/low"
    },
    "fit": {
      "score": 3,
      "issues": [],
      "priority": "high/medium/low"
    }
  },
  "issues": [
    {
      "priority": "high",
      "description": "",
      "category": "clarity/strategy/interaction/satisfaction/fit",
      "affected_component": "",
      "status": "pending/in_progress/resolved"
    }
  ],
  "changes": [
    {
      "id": 1,
      "what": "",
      "why": "",
      "expected_impact": "",
      "revert_difficulty": "easy/medium/hard",
      "risk": "low/medium/high"
    }
  ],
  "root_cause": {
    "problem": "",
    "whys": ["", "", "", "", ""],
    "root_cause": ""
  },
  "feedback": {
    "magic_question": "",
    "most_fun": "",
    "least_fun": "",
    "agency": true,
    "would_play_again": true
  },
  "next_version": {
    "version": "0.0.0",
    "change_type": "patch/minor/major",
    "testing_focus": [],
    "success_criteria": []
  },
  "frameworks_used": [],
  "notes": ""
}
```
<!-- END_JSON -->
```

---

## 迭代模式使用说明

### 模式1：记录模式 (Record Mode)
**触发方式：** 说"记录playtest"或"开始记录"

**用途：** 纯粹记录playtest结果，不做分析

**输出：** `iteration_vX.X.X_YYYY-MM-DD_record.md`

---

### 模式2：分析模式 (Analysis Mode)
**触发方式：** 说"分析迭代"或"分析playtest结果"

**用途：** 读取记录模式的迭代包，进行分析并生成建议

**输入：** 读取最新的 `*_record.md`
**输出：** `iteration_vX.X.X_YYYY-MM-DD_analysis.md`

---

### 模式3：计划模式 (Plan Mode)
**触发方式：** 说"生成下一版本计划"或"准备下一次迭代"

**用途：** 基于分析结果，生成下一版本的具体计划

**输入：** 读取最新的 `*_analysis.md`
**输出：** `iteration_vX.X.X_YYYY-MM-DD_plan.md`

---

## 工作流程

```
┌─────────────────────────────────────────────────────────┐
│                    Playtest 完成                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   模式1: 记录模式        │
        │   "记录playtest"        │
        └────────────────────┬───┘
                             │
                             ▼
                    生成 *_record.md
                             │
                             ▼
        ┌────────────────────────┐
        │   模式2: 分析模式        │
        │   "分析迭代"            │
        └────────────────────┬───┘
                             │
                             ▼
                   读取 record → 分析
                             │
                             ▼
                   生成 *_analysis.md
                             │
                             ▼
        ┌────────────────────────┐
        │   模式3: 计划模式        │
        │   "生成下一版本计划"     │
        └────────────────────┬───┘
                             │
                             ▼
                   读取 analysis → 规划
                             │
                             ▼
                   生成 *_plan.md
                             │
                             ▼
                   实施改动 → 下次Playtest
                             │
                             └──→ 循环
```

---

## Claude 读取迭代包时的提示

当 skill 读取迭代包时，它会：

1. **解析 JSON 部分**获取结构化数据
2. **阅读 Markdown 部分**获取上下文和细节
3. **结合两者**生成分析和建议

**关键数据点：**
- `component_ratings`：各组件评分
- `issues`：问题列表
- `changes`：已做的改动
- `next_version`：下一版本信息
- `feedback`：玩家反馈

---

## 快速命令参考

| 命令 | 模式 | 说明 |
|------|------|------|
| "记录playtest" | Record | 开始记录新的测试结果 |
| "分析迭代" | Analysis | 分析最新的测试记录 |
| "生成下一版本计划" | Plan | 基于分析生成迭代计划 |
| "查看迭代历史" | - | 显示所有迭代包列表 |
| "比较版本 vX.X.X 和 vY.Y.Y" | - | 对比两个版本 |

---

## 自动化功能

Skill 会自动：

1. **检测当前文件夹**，查找游戏设计项目
2. **定位最新的迭代包**
3. **解析 JSON 和 Markdown**
4. **追踪版本变化**
5. **建议版本号**（遵循语义化版本）
6. **检查完成标准**（Definition of Done）

---

## 示例：完整迭代流程

```bash
# 第一次迭代
用户: 记录playtest
Skill: [引导填写信息] → 生成 iteration_v0.1.0_2024-01-15_record.md

用户: 分析迭代
Skill: [读取 record] → 分析 → 生成 iteration_v0.1.0_2024-01-15_analysis.md

用户: 生成下一版本计划
Skill: [读取 analysis] → 规划 → 生成 iteration_v0.1.1_2024-01-16_plan.md

# 第二次迭代（用户实施改动后）
用户: 记录playtest
Skill: [自动读取最新 plan 作为上下文] → 生成 iteration_v0.1.1_2024-01-16_record.md

...以此类推
```
