# Edit Workflows

统一所有“参考图改造”任务的结构。涉及上传图、参考图、现有包装、现有角色、现有牌面、现有海报改造时，优先读取本文件。

## 目录

- 通用 edit 模板与规则
- 局部、背景、风格、产品和穿搭替换
- 文案、包装、海报和卡牌重构
- Prompt Snapshot 写法

## 通用 edit 模板

```markdown
useWhen:
requiredInputs:
identityAnchors:
Change:
Preserve:
Constraints:
PromptSnapshot:
FailureRisks:
```

## 0. 通用规则

- 先列出 `identityAnchors`，再写 `Change`。
- `identityAnchors` 默认 3-5 条。
- `Preserve` 用完整句子写，不要只写关键词。
- 如果任务本质是“保主体换场景/换排版/换文案”，就不要当成重新生成。

## 1. 局部替换

- `useWhen`: 只改一个局部元素，如背景物件、按钮区、文案条、边角装饰、角色手持物。
- `requiredInputs`: 原图、要替换的局部说明、替换后的新元素。
- `identityAnchors`: 主体位置、主体轮廓或包装结构、核心品牌/角色识别。
- `Change`: 只替换指定局部，不改变主体、构图主框架和光线逻辑。
- `Preserve`: 保留原图中的主体识别、整体比例、现有排版层级和其余区域。
- `Constraints`: 新局部必须融入原图材质、光影和透视。
- `FailureRisks`: 模型误改主体、局部融合不自然、不相关区域被一并重绘。

## 2. 背景替换

- `useWhen`: 主体必须保留，只换环境、氛围、舞台、货架、城市或空间背景。
- `requiredInputs`: 原图、新背景类型、是否保留原光线方向。
- `identityAnchors`: 主体本身、包装/角色/产品造型、主体主色与标识。
- `Change`: 将原背景替换为指定新场景，并让新背景服务主体展示。
- `Preserve`: 主体完整性、主体朝向、主体比例、主体清晰度。
- `Constraints`: 禁止把主体变成别的产品或别的角色。

## 3. 保主体换风格

- `useWhen`: 保留同一主体识别，只改变风格、材质感、画法、摄影气质或 campaign 调性。
- `requiredInputs`: 原图、目标风格、必须保留的识别锚点。
- `identityAnchors`: 形状、配色、品牌/角色识别特征、关键图案或服装。
- `Change`: 切换整体视觉表达方式，但不换主体身份。
- `Preserve`: 主体的可辨认性、品牌归属、核心轮廓和关键元素。
- `Constraints`: 风格变化不能压倒识别。

## 4. 产品抠出重组

- `useWhen`: 现有产品或包装必须保留，但要重做为海报、详情页、发布图或卖点图。
- `requiredInputs`: 原产品图、新输出形态、卖点结构。
- `identityAnchors`: 包装形状、主色、品名或品牌名、核心图案。
- `Change`: 将原产品作为主视觉重新编排到新的商业版式中。
- `Preserve`: 产品本身不变，不换品类、不换包装、不改品牌归属。
- `Constraints`: 版式重组可以变化，但产品识别必须绝对稳定。

## 5. 人物穿搭替换

- `useWhen`: 保留人物身份，改服装、材质、配饰或造型方向。
- `requiredInputs`: 人物原图、新穿搭方向、是否保脸、发型、姿态。
- `identityAnchors`: 脸部结构、发型、姿态或构图、角色身份特征。
- `Change`: 替换服装与配饰，必要时联动场景小改。
- `Preserve`: 人物身份与核心表情，不改变成另一个人。

## 6. 文案区重做

- `useWhen`: 海报、详情页、卡牌、规则页需要在保主体前提下重做标题区、卖点区、标签区。
- `requiredInputs`: 原图、新文案、新信息层级。
- `identityAnchors`: 主视觉主体、原本有效的信息层级、主配色体系。
- `Change`: 重做文案区与标签区，使文字更清晰可读。
- `Preserve`: 主体、构图大框架和品牌/产品归属。
- `Constraints`: 文字区升级不能让画面变成信息拥堵的广告板。

## 7. 包装不变、海报重构

- `useWhen`: 原包装必须保留，但要升级成新的活动海报、电商首图、发布图或 campaign 主视觉。
- `requiredInputs`: 包装参考图、海报用途、新标题和卖点。
- `identityAnchors`: 包装正面、品名、主图案、品牌标识。
- `Change`: 在不改变包装的前提下重建周边背景、辅助元素、标题与气氛。
- `Preserve`: 包装完整性和识别度。

## 8. 卡牌正面保结构改主题

- `useWhen`: 已有牌面结构有效，但要换题材、角色、阵营、规则名称或图标系统。
- `requiredInputs`: 原卡牌图、新主题、必保留结构区块。
- `identityAnchors`: 边框结构、标题区、属性区、规则栏、整体比例。
- `Change`: 更换主题主视觉、文案和局部图标，但保留牌面结构骨架。
- `Preserve`: 平面正交正面、可印刷结构、区块布局和视觉系统。
- `Constraints`: 禁止把牌面改成效果图、桌面摆拍或海报。

## 通用 Prompt Snapshot 写法

```markdown
Use the uploaded image as a strict reference.

Identity anchors:
1. ...
2. ...
3. ...

Change:
- ...

Preserve:
- ...

Constraints:
- keep the subject identity intact
- do not redesign unrelated areas
- readable simplified Chinese text only when explicitly required
```
