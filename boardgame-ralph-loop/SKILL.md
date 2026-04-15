---
name: boardgame-ralph-loop
description: 基于 Ralph Loop 方法论的自主迭代设计技能。提供自动化的测试和设计改进循环。
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
