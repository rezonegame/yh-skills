# Editable text contract

Native SVG-to-PPTX text supports BCP-47 `lang`/`xml:lang`, `dir="rtl"`, and explicit `data-pptx-font-latin`, `data-pptx-font-ea`, and `data-pptx-font-cs` slots. Invalid language or direction values fail conversion.

`data-pptx-text-flow` has three modes:

- `preserve` (default): keep authored positional line breaks and do not allow PowerPoint to rewrap them.
- `reflow`: keep one editable text box and allow PowerPoint wrapping.
- `split`: preserve the converter's positional-tspan split into independent editable text boxes; authors must provide `x`, `y`, or non-zero `dy` for each intended line.

Text boxes sharing `data-pptx-flow-group` must agree on language, direction, flow mode, and all declared font slots. Validate with `python scripts/validate_svg_text_contract.py <svg-or-directory>`.
