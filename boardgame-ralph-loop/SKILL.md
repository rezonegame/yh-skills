---
name: boardgame-ralph-loop
description: Ralph Loop自主迭代技能。当用户要求"Ralph Loop"、"游戏自主迭代"、"GRD迭代设计"、"游戏自动测试循环"时使用此技能。提供完全自主的bash循环和交互模式，通过GRD（游戏需求文档）持续迭代游戏设计，直到达到适应度目标。
version: 1.0.0
tags: [boardgame, design, automation, iteration, ralph-loop]
triggers:
  - "Ralph Loop"
  - "游戏自主迭代"
  - "GRD迭代设计"
  - "游戏自动测试循环"
---

# Board Game Ralph Loop

基于 Ralph Loop 方法论的桌面游戏自主迭代设计系统。

## 🤖 执行流程

### 模式A：完全自主循环

启动后自动循环，直到达到目标：

```bash
cd ~/game-project
while ! cat fitness-goals.txt | grep -q "ALL_MET"; do
  # 读取GRD
  # 生成设计任务
  # 进行测试
  # 分析改进
done
```

### 模式B：交互模式

手动触发每个迭代阶段：

```
1. 读取 GRD
2. 生成设计任务
3. 进行测试
4. 分析改进
```

## 📝 GRD 结构

**游戏需求文档**包含：
- 游戏目标
- 机制要求
- 约束条件
- 适应度目标

---

**Version**: 1.0.0
