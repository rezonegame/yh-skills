---
name: boardgame-cards
description: 桌游卡牌设计技能。当用户要求"设计桌游卡牌"、"卡牌布局"、"卡牌背面对齐"、"卡牌整版排版"、"游戏卡牌制作"时使用此技能。提供卡牌布局层级、图标系统、背面对齐和整版排版指导，涵盖扑克/迷你/方形尺寸和可读性标准。
version: 1.0.0
parent: print-design
tags: [boardgame, cards, print-design, game-components, layout]
triggers:
  - "设计桌游卡牌"
  - "卡牌布局"
  - "卡牌背面对齐"
  - "卡牌整版排版"
  - "游戏卡牌制作"
---

# Board Game Card Design

桌游卡牌的完整设计指南，涵盖布局层级、图标系统、背面对齐和印刷生产。

## 🤖 执行流程

### 第1步：选择卡牌尺寸

**标准尺寸**：
- Poker (63×88mm) - 最常见，标准卡套
- Bridge (57×89mm) - 传统卡牌，塔罗牌
- Mini European (44×67mm) - 小型游戏，100+张卡
- Square (70×70mm) - 方形卡牌，独特视觉
- Hexagonal (60×70mm) - 六边形卡牌
- Large (80×120mm) - 参考卡，超大型

### 第2步：设计卡牌正面布局

**标准布局结构**：
1. **Header**（12-18%）- 图标 + 标题 + 徽章
2. **Visual**（30-45%）- 主艺术区域
3. **Body**（40-55%）- 能力/效果文字

**可读性标准**：
- 最小文字：8pt（30cm观看）
- 标题文字：14-18pt
- 正文文字：10-12pt
- 图标：8-12mm

### 第3步：设计卡牌背面

**背面对齐类型**：
- Radial（径向）- 适用于圆形图案
- Linear（线性）- 适用于边框图案
- Random（随机）- 适用于纹理图案

**对齐精度**：±0.5mm 标准印刷容差

### 第4步：整版排版

**A4整版容量**：
- Poker: 14-16张
- Bridge: 16-18张
- Mini European: 20-24张
- Square: 12-14张

**出血和安全区**：
- 出血：3mm 四周
- 安全区：5mm from trim

### 第5步：验证制作规格

**分辨率**：300 DPI @ 最终尺寸
**颜色**：CMYK
**文件格式**：PDF/X-4

---

## 📚 相关技能

- **`boardgame-boards`** - 游戏板设计
- **`boardgame-tiles`** - 方块设计
- **`print-design`** - 父技能

---

**Version**: 1.0.0
