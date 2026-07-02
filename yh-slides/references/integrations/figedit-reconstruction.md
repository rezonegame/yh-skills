# 2B-R: FigEdit Editable Reconstruction

`2B-R` is the formal path for rebuilding existing raster slides, screenshots,
paper figures, diagrams, and infographics as editable SVG and native PPTX.
It delegates reconstruction to the independent `figedit` skill. It does not
erase the source background or overlay guessed text boxes.

## Boundary

- Use `2A`, `2A-S`, or `2C` when editable output is known before authoring.
- Use `2B-R` when the source already exists only as raster imagery.
- Do not redesign the content outline or visual direction unless the user asks.
- Preserve photos, logos, screenshots, maps, dense charts, and distinctive
  pictorial objects as replaceable cropped assets.

## Preflight

```powershell
python scripts\figedit_batch.py preflight
```

The default skill location is
`C:\Users\wudao\OneDrive\skills\figedit`. Override it with
`FIGEDIT_SKILL_DIR` or `--figedit-root`. Missing heavy dependencies stop the
run and print an installation command; never install them silently.

## Batch Workflow

```powershell
python scripts\figedit_batch.py init `
  --project-dir "C:\PPTX\demo" `
  --slides "C:\input\01.png" "C:\input\02.png"

python scripts\figedit_batch.py measure `
  --project-dir "C:\PPTX\demo" `
  --ocr-profile v6_medium
```

For each `reconstruction/page-NN/`:

1. Inspect the source and measurement diagnostics.
2. Read the independent FigEdit `SKILL.md` and route-specific references.
3. Author `manifest.json`; do not promote detector candidates automatically.
4. Rebuild ordinary text as text, stable geometry as shapes, formulas as
   `math`, and source-specific visuals as cropped assets.
5. Add a semantic delivery review after visual inspection:

```json
{
  "delivery_review": {
    "status": "approved",
    "major_structure": true,
    "text_complete": true,
    "connectors_correct": true,
    "distinctive_assets_preserved": true,
    "reviewer_notes": "Compared source, preview, and editable PPTX."
  }
}
```

Compose and check:

```powershell
python scripts\figedit_batch.py compose --project-dir "C:\PPTX\demo"
python scripts\figedit_batch.py status --project-dir "C:\PPTX\demo"
```

Only after every page passes:

```powershell
python scripts\figedit_batch.py assemble `
  --project-dir "C:\PPTX\demo" `
  --output "C:\PPTX\demo\output\demo-editable.pptx"
```

## Hard Delivery Gate

The combined PPTX is blocked when any page:

- lacks the required FigEdit package outputs;
- has invalid SVG or failed native PPTX export;
- contains formula-like text leakage;
- fails editable Office Math export for an important formula;
- has an editability audit marked `review` or `failed`;
- lacks explicit semantic approval for structure, text, connectors, or
  distinctive visual assets.

Failed runs retain `summary_report.md`, `failed_pages.json`, measurements,
manifests, previews, assets, and quality reports. Do not fall back to a
picture-only PPTX or to source-image-plus-text overlays.

