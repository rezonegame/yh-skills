# Mermaid Diagrams

Use Mermaid only when the diagram's structure is easier to express as graph text than by editing a supplied static SVG. This is the preferred extension for class diagrams, ER diagrams, and sequence diagrams. Keep the existing static diagram library for architecture, charts, timelines, flowcharts, and other listed types.

## PDF-safe workflow

1. Draft a compact Mermaid graph. Keep nodes at or below nine and write labels that still make sense without decorative styling.
2. Render it to SVG using a Mermaid renderer that the user has approved or supplied. Do not use an untrusted diagram's embedded scripts or fonts.
3. Normalize the SVG before embedding it in a document:

```bash
python scripts/mermaid_normalize.py raw.svg -o clean.svg
```

4. Open `clean.svg`, visually inspect Chinese labels, arrow direction, contrast, and clipping, then embed only the `<svg>...</svg>` into a document `<figure>`.

`mermaid_normalize.py` is offline and uses only the Python standard library. It removes remote font imports, resolves supported CSS variables and `color-mix()` values to static colours, and applies the local Kami-compatible palette from `mermaid-theme.json`.

## Boundaries

- Use graph types: flowchart, state, sequence, class, and ER.
- Do not use `xychart-beta` for PDF output; its style selectors are not reliable in WeasyPrint. Use the supplied bar, line, donut, candlestick, or waterfall diagrams instead.
- Never add browser JavaScript, remote fonts, or remote CSS to a document artifact.
- If rendering cannot be verified, fall back to the local inline-SVG templates or a table.

## Provenance

This normalizer and palette strategy are selectively imported from `tw93/kami` at commit `b3d856266d3e75278770f58e55d19d69583e35b0` (MIT). The renderer itself is not bundled and is never a runtime dependency of this skill.
