# Open Design Metadata

> 这份文件保留原先放在 `SKILL.md` frontmatter 中的 Open Design 兼容信息。不要把这些字段放回 YAML frontmatter；官方 skill 校验只接受受支持的顶层字段。

```yaml
od:
  mode: deck
  preview:
    type: html
    entry: output/presentation.html
  design_system:
    requires: false
    sections: [color, typography, layout, components]
  outputs:
    primary: output/presentation.html
    secondary: [output/*.pptx, tasks.json]
```

使用 Open Design 风格工作流时，将这些值视为约定：

- 默认产物是 deck / presentation。
- 默认 HTML 预览入口是 `output/presentation.html`。
- 设计系统可以按项目需要生成 `DESIGN.md`，但不是所有项目强制要求。
- 常见辅助产物包括 `.pptx`、`tasks.json` 和图片资产。

