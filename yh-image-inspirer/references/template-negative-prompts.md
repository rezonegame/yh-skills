# 模板级负面约束与 JSON Schema 双格式

> 来源：awesome-gpt-image-2 补充吸收 (2026-08-04)
> 上一级：references/structured-templates.md

## 1. Per-Template Negative Prompts

上游每个模板自带 10+ 条"不要..."负面约束。这些约束比全局 style-avoids.md 更精确——它们针对特定输出类型的常见翻车点。

### 使用方式

在选择模板后，除了读取 `style-library.json#<template>.guidance` 和 `style-library.json#<template>.pitfalls`，同时读取以下对应类型的负面约束，写入 prompt 的禁止项部分。

### 按类型分类的负面约束

**海报与排版类：**
- 不要使用样机/mockup/PSD 模板外观
- 不要生成二维码、条形码、价格标签
- 不要使用超过 2 种字体风格
- 不要在安全区域外放置关键文字
- 不要使用低对比度文字（浅色文字+浅色背景）
- 不要生成 AI 拼贴感的随机素材堆砌
- 不要使用彩虹色/全光谱配色
- 不要在海报内嵌入产品包装盒照片

**商品与电商类：**
- 不要生成台面摆拍/桌面场景（除非明确要求）
- 不要使用"促销""限时""爆款"等营销文字
- 不要在产品图上加水印或 logo（除非是品牌方要求）
- 不要生成模糊的产品边缘
- 不要使用与产品无关的装饰物遮挡产品主体
- 不要改变产品原有颜色/材质/形态

**UI 与界面类：**
- 不要生成真实 App 的精确界面（版权风险）
- 不要使用 Lorem Ipsum 或无意义填充文字
- 不要在 UI 中放置真实的第三方品牌 logo
- 不要生成不可读的小字号文字
- 不要使用与目标平台不符的 UI 范式（如 iOS 风格用在 Android 场景）

**信息图与图表类：**
- 不要使用虚假数据或随机数字
- 不要生成 3D 饼图（可读性差）
- 不要在信息图中使用过多装饰性插图
- 不要使用超过 5 种颜色编码数据
- 不要省略图例/单位/数据来源

**插画与艺术类：**
- 不要混用多种画风（水彩+数码+油画混搭）
- 不要在插画中加入照片级写实元素
- 不要使用 AI 特征明显的"塑料质感"
- 不要生成没有视觉焦点的均匀细节分布

**人物与角色类：**
- 不要生成多于 5 根手指/多余肢体
- 不要改变角色已有的识别特征（发色/瞳色/服装）
- 不要使用真实名人面孔
- 不要生成不合理的身体比例

**建筑与空间类：**
- 不要生成违反物理规律的悬浮结构
- 不要使用与地理环境不符的植被
- 不要在建筑图中放置比例错误的人物

## 2. JSON Schema 双格式模板

上游每个模板同时提供两种格式：

### Text 格式（人类可读，带占位符）

```
[角色定义] 你是一个高端[类型]生成系统
[整体方向] 视觉风格关键词 + 比例
[核心设计原则] 5-7 条编号规则
[画面结构] 顶部/中部/底部 分区描述
[具体内容] 每个区域的变量占位符
[色彩规范] 明确的调色板
[图像质量约束] 分辨率、纹理要求
[禁止项] 10+ 条负面清单
[最终输出] 确认输出格式
```

### JSON Schema 格式（程序可解析，用于批量生成）

```json
{
  "template_id": "natural-science-poster",
  "category": "posters",
  "fields": {
    "subject": { "type": "string", "required": true, "description": "主体名称" },
    "scientific_name": { "type": "string", "required": false, "description": "学名" },
    "habitat": { "type": "string", "required": false },
    "key_facts": { "type": "array", "items": "string", "max": 5 },
    "color_palette": { "type": "string", "default": "natural earth tones" },
    "poster_style": { "type": "enum", "values": ["apple_keynote", "vintage_field_guide", "modern_minimal"] }
  },
  "constraints": {
    "aspect_ratio": "2:3",
    "text_language": "zh-CN",
    "max_text_regions": 4
  }
}
```

### 何时用哪种

| 场景 | 格式 |
|---|---|
| 单张出图、用户交互式 brief | Text 格式（人类可读） |
| 批量系列生成、程序化管道 | JSON Schema（程序可解析） |
| 模板开发/维护 | JSON Schema（结构化校验） |
| 案例存档 | Text 格式（便于参考） |

## 3. 与现有系统的集成

- 负面约束在出图流程步骤 5「导演阶段分离 → 阶段一 → ⑧ 避免项」中，除了读取全局 `style-avoids.md`，额外读取本文件中对应类型的负面约束
- JSON Schema 格式主要用于 `recipes/series-generation.md` 的批量场景，每个变体通过填充 JSON fields 而非重写完整 prompt
