# Diagram Selection Contract

Use a diagram only when it explains a relationship more clearly than a concise paragraph. Keep the caption as the conclusion, not a restatement of labels.

## Selection

| Relationship | Preferred primitive |
|---|---|
| Time, milestones, or ordered change | `assets/diagrams/timeline.html` or `timeline.svg` |
| Branching decisions | `assets/diagrams/flowchart.html` |
| A short linear process | `assets/diagrams/process.svg` |
| Two evidence-backed alternatives | `assets/diagrams/comparison.html` or `comparison.svg` |
| Other structured relationships or quantitative data | Use the matching HTML primitive listed in `references/diagrams.md` |
| Two or three plain points without a relationship | Use prose; do not draw a diagram |

Use SVG primitives for lightweight inline figures and HTML primitives when the diagram needs the richer local template system. Do not load remote images, fonts, scripts, or styles into printable diagrams.

## Accessibility and print checks

- Give every SVG a `<title>` and `<desc>` or an equivalent accessible label.
- Provide a nearby textual explanation or `<figcaption>`.
- Use the local color tokens and verify readable contrast in print.
- Preserve a `viewBox`; do not embed scripts or `foreignObject` content.
- Run `python scripts/check_diagram_contract.py` to validate the bundled set, or pass one or more explicit HTML/SVG paths.
