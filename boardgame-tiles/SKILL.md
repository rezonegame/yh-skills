---
name: boardgame-tiles
description: 方块 (Tiles) 设计技能。专注于六边形、方形等方块的边缘连接系统、旋转兼容性和模切考虑。
---

# Board Game Tile Design

桌游方块的完整设计指南，涵盖六边形、方形和圆形方块。

## 🤖 执行流程

### 第1步：选择方块类型

**六边形方块（最常见）**：
- Small: 30mm flat-to-flat
- Medium: 40mm flat-to-flat（标准）
- Large: 50mm flat-to-flat
- Extra Large: 60mm flat-to-flat

**方形方块**：
- Standard: 50×50mm
- Large: 60×60mm

### 第2步：设计边缘连接

**边缘类型**：
- 平边 - 简单拼接
- 凹槽 - 机械锁定
- 磁性 - 高级连接

### 第3步：处理旋转兼容

**旋转规则**：
- 六边形：6个方向均等
- 方形：4个方向均等
- 确保旋转后图案连贯

### 第4步：规格验证

**制作规格**：
- 厚度：1.5-2mm
- 模切：±0.2mm
- 尺寸：±0.3mm

---

## 📚 相关技能

- **`boardgame-boards`** - 游戏板设计
- **`boardgame-cards`** - 卡牌设计
- **`print-design`** - 父技能

---

**Version**: 1.0.0
