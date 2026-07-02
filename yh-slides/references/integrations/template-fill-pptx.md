# 2A-T Template Fill

Use `2A-T` when the user provides an existing `.pptx` and wants to reuse its native PowerPoint design with new content. This path is independent of HTML conversion and SVG generation.

## Trigger

Recommend `2A-T` only when the user says things like:

- "复用这个 PPT 模板"
- "把新内容填进这份 PPT"
- "保留原设计，只换文案/数据"
- "从这个模板里挑合适页面"

If the user only asks for a normal editable PPTX, keep recommending `2A / Path A` or `2A-S` depending on complexity.

## Local Assets

Absorbed local implementation: `scripts/template_fill_pptx.py` and `scripts/template_fill_pptx/`.

Expected workflow/script assets are indexed in `references/meta/asset-registry.json` with route hint `2A-T Template Fill`.

## Project Structure

```text
C:\PPTX\{project}\
├── sources\        # source PPTX and input material
├── analysis\       # slide_library.json, fill_plan.json, check_report.json
├── exports\        # final PPTX only
└── validation\     # read-back text and validation notes
```

## Execution Contract

1. Analyze template deck into `analysis/slide_library.json`.
2. Select pages by rhetorical fit, not source order.
3. Create `analysis/fill_plan.json`.
4. Run capacity check before apply.
5. Apply the plan to produce `exports/*.pptx`.
6. Read back output and verify slide count, key text, tables/charts, and notes.

## Fit Rules

- Reuse a source page only when its visible structure fits the target message.
- A source page may be repeated for multiple output slides.
- Do not shrink fonts as the default fix; rewrite, split, or choose a better source page.
- Preserve native PowerPoint tables/charts where supported.

## QA

Add these to P0:

- `slide_library.json` exists and contains replaceable slots.
- `fill_plan.json` selects, reorders, or repeats pages intentionally.
- Capacity warnings are resolved or explicitly accepted.
- Output `.pptx` opens and remains editable.
- Read-back validation finds expected titles and notes.
