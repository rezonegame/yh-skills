# Content-to-Layout Candidate Discipline

Use this method when a page could fit several local templates or composition
families. It strengthens `yh-slides` Step 3-C and Step 4 without adding a new
runtime, theme pack or product path.

## Freeze content first

For each logical page, create one canonical content package:

- action title and optional short title;
- summary and takeaway;
- required facts and key numbers with units;
- items with stable IDs and priority;
- chart insight and citations;
- media intent and available assets.

All candidate layouts consume this same package. They may use a short copy
variant, reorder items or change emphasis, but cannot add facts or silently
drop required facts. This prevents a theme change from rewriting the argument.

## Query by capacity, not appearance alone

Before selecting a layout, compare the real content against:

- title and body character capacity;
- item count and nested depth;
- numeric versus textual values;
- chart, comparison, process or timeline needs;
- media-slot count and aspect ratio;
- emphasis hierarchy and audience move.

Reject a candidate if a required item has no legal slot, a visible template
slot cannot be hidden or filled honestly, or the page would depend on shrinking
text below the route's legibility floor.

## Keep candidate families meaningfully different

For important pages, consider two or three candidates from different structural
families, such as `hero`, `split`, `metric-spotlight`, `chart-led`, `timeline`,
`matrix`, `editorial`, `comparison` and `process`. Candidates are alternatives
for review, not multiple stories.

Across the deck:

- avoid repeating the same selected layout unless the repetition is meaningful;
- do not use one composition family on more than two consecutive substantive
  pages;
- keep card grids below roughly one third of substantive pages;
- chart-led pages make the data graphic the visual focus;
- process/timeline pages show direction and relationships;
- split/editorial pages use asymmetry rather than disguised card walls.

## Template-fill safety

- Replace every visible default string; never deliver demo copy.
- Treat decorative fields as decoration, not content slots.
- Keep text-only overrides text-only; do not alter component structure merely
  to force unsuitable content into a template.
- If the data changes, recompute the title, annotation and insight.
- Stage media into the project and reference safe relative paths.

## Review gate

Before build, record the selected layout ID or composition family in
`deck-plan.json`. For a high-value page, also record the rejected candidates and
one-line reasons. The normal `yh-slides` sample checkpoint remains the user-facing
decision point; this candidate discipline is an internal preparation layer.
