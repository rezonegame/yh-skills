# 色彩引擎（Color Engine）

> 来源：gc-minimal-zine-poster 的 Standard Color Engine，扩展为通用色彩控制系统。
> 核心理念：色彩不是装饰，是**视觉锚点**。一个画面只需要一个明确的高纯度锚色。

## 色彩锚点理论

### 什么是色彩锚点（Color Anchor）
画面中唯一具有高纯度（chroma）的色彩元素。它不是点缀色，而是**承载视觉焦点的结构性角色**——可以是主体本身、主体的一部分、或一个独立的色块/形状。

### 锚色三要素
1. **Material Form（物质形态）**：锚色必须有可渲染的物质形态——色块、剪影、物体、文字、几何形状，不能只是「画面整体偏蓝」
2. **Chroma Target（纯度目标）**：必须达到「在缩略图尺寸下清晰可见」的纯度
3. **Area Target（面积目标）**：必须占据足够的面积，不被其他元素吞没

## 风格族色彩标准

### 极简/Zine 风格
- **底层**：纸张色调（米白/灰白/泛黄）+ 灰度/黑色辅助元素
- **锚色占比**：画布面积 0.8%-2.5%，或视觉集群面积的 15%-35%
- **锚色纯度**：fully saturated。用词如 `fully saturated cobalt-blue risograph ink`、`opaque ultramarine cutout`
- **锚色形态**：纯色块、剪影、旧印刷插图、色窗、粗体文字
- **首选色序**：钴蓝 > 群青 > 青色 > 紫色 > 品红粉 > 柠檬黄 > 梨绿 > 橙色 > 番茄红
- **禁止弱化词**：`near-monochrome`、`no strong accent`、`pale accent`、`muted accent`、`faded accent`、`pastel accent`
- **特殊规则**：低对比度和灰度处理只应用于纸张、照片和辅助墨迹，不应用于锚色

### Mondo/丝网印刷海报
- **底层**：深色背景（黑/深蓝/深棕）或大胆的纯色背景
- **锚色占比**：主体面积的 30%-60%
- **锚色纯度**：高纯度丝网印刷墨色感。用词如 `bold screen-print red`、`electric blue ink on black`
- **锚色形态**：层叠的人物/场景剪影、大面积色域分割、标题文字
- **色彩数量**：2-4 个丝网印刷色（含黑/白），模拟分版套印
- **首选色序**：红+黑 > 蓝+黄 > 绿+橙 > 紫+金

### 电商/商品海报
- **底层**：干净纯色或渐变背景，不抢主体
- **锚色占比**：商品本身的色彩即为锚色；背景色占 40%-70%
- **锚色纯度**：中高纯度，不刺眼但有存在感
- **色彩策略**：60-30-10 规则——60% 底色 + 30% 辅助色 + 10% 强调色
- **禁止**：背景色与商品色冲突；过多装饰色分散注意力

### 信息图/图解
- **底层**：白色或极浅灰背景
- **锚色占比**：数据高亮区域 5%-15%
- **锚色纯度**：高纯度用于数据重点，中纯度用于分区
- **色彩策略**：语义化配色（红=警告、绿=正常、蓝=信息、橙=注意）
- **色彩数量**：≤5 个语义色 + 黑白灰

## 色彩可见性检查

生成 prompt 前，验证以下标准：

1. **缩略图可见性**：锚色在 100×60px 缩略图下是否仍可辨认？如果不可见，加大面积或提高纯度
2. **语义正确性**：锚色是否与主体语义一致？（蓝色海洋、红色警告、绿色自然）
3. **对比度充足**：锚色与背景/纸张的对比度是否足够？（WCAG AA 标准至少 3:1）
4. **单锚原则**：画面中是否只有一个主锚色？允许一个微小的辅助色支持主体，但不能让画面变成「商业彩色」
5. **非弱化检查**：prompt 中是否出现了弱化锚色的词汇？（pale/muted/faded/pastel/low saturation/near-monochrome）

## Anti-Muting 规则（反弱化）

以下是必须从 prompt 中排除的弱化表述，除非用户明确要求：

| 禁止词 | 替代方案 |
|---|---|
| `pale accent` | `vivid [color] anchor` |
| `muted accent` | `saturated [color] block` |
| `faded accent` | `clean [color] cutout` |
| `pastel accent` | `fully saturated [color] ink` |
| `low saturation` | `high-chroma [color] subject` |
| `near-monochrome` | `one clear [color] accent on neutral ground` |
| `subtle color` | `bold [color] anchor visible at thumbnail` |
| `hint of color` | `substantial [color] area occupying X%` |

## Prompt 中的色彩描述模板

### 极简/Zine 风格
```
Paper tones plus gray/black support one unmistakably [color] anchor.
The [color] takes the form of a [material form], occupying approximately
[X]% of the canvas. It remains clearly visible at thumbnail scale.
```

### Mondo 风格
```
[X]-color screen-print palette: [color1] dominates [area], [color2] fills
[layer], black defines [outlines/shadows]. Colors simulate layered
ink registration with slight misregistration at edges.
```

### 电商风格
```
Clean [background color] background supports the [product color] product
as the primary visual anchor. Accent color [color] appears in [element]
for call-to-action emphasis, occupying approximately [X]% of the frame.
```
