# Adoption Decisions

## A. Structure Split
- Source: N/A (internal maintenance)
- Material: moved low-frequency sections to references/
- Test: SKILL.md line count < 350
- Rollback: inline the references/ content back into SKILL.md
- Date: 2026-07-28

## G. Validated Diagram Primitives
- Source: tw93/kami (MIT, existing dependency)
- Source URL: https://github.com/tw93/kami
- License: MIT
- Material adopted: diagram selection discipline, accessible SVG requirements
- Material excluded: wholesale template refresh
- Test: scripts/check_diagram_contract.py + 3 SVG primitives
- Rollback: delete assets/diagrams/timeline.svg, comparison.svg, process.svg, scripts/check_diagram_contract.py, references/diagram-selection.md
- Date: 2026-07-28
