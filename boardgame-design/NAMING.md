# 项目命名规范 (Project Naming Convention)

统一的命名规范让项目文件更易管理和阅读。

---

## 游戏项目文件夹命名

### 格式
```
[GameName_English]_Design/
```

### 规则
| 规则 | 说明 | 示例 |
|------|------|------|
| 使用英文名或拼音 | 便于文件系统兼容 | `Dragon_Valley_Design/` |
| 无空格 | 用下划线连接单词 | `Star_Traders_Design/` |
| 首字母大写 | 每个单词首字母大写 | `Mystery_Mansion_Design/` |
| 以 `_Design` 结尾 | 标识这是设计文件夹 | `Kingdom_Builder_Design/` |

### 命名示例

| 中文游戏名 | 英文翻译 | 项目文件夹名 |
|-----------|---------|-------------|
| 龙之谷 | Dragon Valley | `Dragon_Valley_Design/` |
| 星际商人 | Star Traders | `Star_Traders_Design/` |
| 神秘庄园 | Mystery Mansion | `Mystery_Mansion_Design/` |
| 长安城 | Chang'an City | `Changan_City_Design/` |
| 三国演义 | Three Kingdoms | `Three_Kingdoms_Design/` |

---

## 迭代包文件命名

### 格式
```
iteration_v[X.X.X]_[YYYY-MM-DD]_[type].md
```

### 版本号规则 (语义化版本)

| 版本类型 | 格式 | 触发条件 | 示例 |
|---------|------|---------|------|
| MAJOR | X.0.0 | 完全重构，几乎变成另一个游戏 | v0.1.0 → v1.0.0 |
| MINOR | 0.X.0 | 新机制、重大规则变更 | v0.1.0 → v0.2.0 |
| PATCH | 0.0.X | 数值调整、文字修改 | v0.1.0 → v0.1.1 |

### 类型标识

| 类型 | 说明 | 使用时机 |
|------|------|---------|
| `record` | 记录模式 | 纯记录playtest结果 |
| `analysis` | 分析模式 | 已分析的迭代包 |
| `plan` | 计划模式 | 下一版本计划 |

### 文件名示例

```
iteration_v0.1.0_2024-01-15_record.md
iteration_v0.1.0_2024-01-15_analysis.md
iteration_v0.1.1_2024-01-16_plan.md
iteration_v0.1.1_2024-01-16_record.md
iteration_v0.1.1_2024-01-16_analysis.md
iteration_v0.2.0_2024-01-20_plan.md
```

---

## 项目文件夹结构

```
[GameName]_Design/
│
├── 00_GAME_BRIEF.md           # 游戏概要（必选）
├── NAMING.md                  # 本命名规范（必选）
│
├── iterations/                 # 所有迭代包
│   ├── iteration_v0.1.0_2024-01-15_record.md
│   ├── iteration_v0.1.0_2024-01-15_analysis.md
│   ├── iteration_v0.1.1_2024-01-16_plan.md
│   └── ...
│
├── components/                 # 组件文件
│   ├── cards/
│   │   └── cards_vX.X.X.pdf
│   ├── board/
│   │   └── board_vX.X.X.pdf
│   └── tokens/
│       └── tokens_vX.X.X.pdf
│
├── rulebook/
│   ├── RULEBOOK_DRAFT.md      # 规则书草稿
│   └── RULEBOOK_vX.X.X.md     # 发布版本
│
├── CHANGELOG.md               # 版本变更历史
│
└── assets/                    # 图片、参考图等
    ├── concept_art/
    ├── reference/
    └── playtest_photos/
```

---

## 其他文件命名

### 规则书
```
RULEBOOK_vX.X.X.md
RULEBOOK_DRAFT.md
```

### 组件文件
```
cards_vX.X.X.pdf
board_vX.X_X.pdf
tokens_vX.X.X.pdf
```

### 变更日志
```
CHANGELOG.md
```

---

## 快速参考

### 创建新项目
```bash
mkdir [GameName_English]_Design
cd [GameName_English]_Design
mkdir iterations components rulebook assets
```

### 命名检查清单

创建文件时，确认：
- [ ] 文件夹名以 `_Design` 结尾
- [ ] 无空格，使用下划线
- [ ] 版本号格式正确（vX.X.X）
- [ ] 日期格式正确（YYYY-MM-DD）
- [ ] 类型标识正确（record/analysis/plan）

---

## 常见错误

| 错误 | 正确 | 原因 |
|------|------|------|
| `Dragon Valley Design/` | `Dragon_Valley_Design/` | 有空格 |
| `dragon_valley_design/` | `Dragon_Valley_Design/` | 全小写 |
| `DragonValley_Design/` | `Dragon_Valley_Design/` | 单词间无下划线 |
| `iteration_v0.1.0.md` | `iteration_v0.1.0_2024-01-15_record.md` | 缺少日期和类型 |
| `iteration_0.1.0_2024-01-15.md` | `iteration_v0.1.0_2024-01-15.md` | 缺少 v 前缀 |

---

## 为什么这样命名？

### 一致性
- 所有项目遵循相同结构
- 易于在不同项目间切换

### 可读性
- 文件名即内容
- 无需打开即可了解

### 可排序
- 版本号自动排序
- 日期自动排序
- 类型自动分组

### 可维护
- 版本控制友好
- 自动化脚本友好
- 团队协作友好

---

## 示例：完整的项目

```
Dragon_Valley_Design/
│
├── 00_GAME_BRIEF.md
├── NAMING.md
├── CHANGELOG.md
│
├── iterations/
│   ├── iteration_v0.1.0_2024-01-15_record.md
│   ├── iteration_v0.1.0_2024-01-15_analysis.md
│   ├── iteration_v0.1.1_2024-01-16_plan.md
│   ├── iteration_v0.1.1_2024-01-16_record.md
│   ├── iteration_v0.1.1_2024-01-16_analysis.md
│   ├── iteration_v0.2.0_2024-01-20_plan.md
│   └── iteration_v0.2.0_2024-01-20_record.md
│
├── components/
│   ├── cards/
│   │   ├── cards_v0.1.0.pdf
│   │   └── cards_v0.2.0.pdf
│   ├── board/
│   │   ├── board_v0.1.0.pdf
│   │   └── board_v0.2.0.pdf
│   └── tokens/
│       └── tokens_v0.2.0.pdf
│
├── rulebook/
│   ├── RULEBOOK_DRAFT.md
│   └── RULEBOOK_v0.2.0.md
│
└── assets/
    ├── concept_art/
    ├── reference/
    └── playtest_photos/
```
