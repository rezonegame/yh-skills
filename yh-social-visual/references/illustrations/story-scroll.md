# Story-scroll Production

Use `story-scroll` only when the user explicitly requests a long scroll, complete growth path, project story overview, or product evolution graphic. A retrospective alone is not enough; suggest this asset when useful, but do not create it automatically.

## Asset Contract

- Manifest role: `story-scroll`
- Mode: keep the enclosing task in `article`
- Strategy: `hybrid`
- Default size: `2400×900`
- Allowed ratio: `2.6:1–3:1`
- Default nodes: 5–8 fact-anchored nodes
- Default output: `output/article-story-scroll.png`
- HTML seed: `assets/social-card/template-story-scroll.html`

Use the existing schema and state sequence:

```text
planned
→ awaiting-generation
→ generated
→ awaiting-composition
→ rendered
→ validated
```

## Node Plan

Extract a left-side starting state, 5–8 meaningful nodes, a middle turn, and a right-side resolution. For each node record:

- Exact label and concise annotation.
- Fact source and unresolved facts.
- Object, physical action, and relative importance.
- Intended visual region and text-safe region.

Use an irregular continuous path with visible breathing room. Avoid numbered dots, equally spaced cards, mechanical timelines, and decorative milestones that are not grounded in the source.

## Two-stage Hybrid Flow

1. Plan the main line, nodes, object-action relationships, irregular route, and empty text regions.
2. Write a native prompt for a text-free continuous-scene base. Use a neutral near-white background only as a default; brand and user visual preferences take precedence.
3. Generate the base and copy it into `sources/`.
4. View the actual base. Confirm node count, route, object placement, balance, and usable empty regions. The first base remains a candidate.
5. If the node count or spatial logic is wrong, regenerate the base. Do not move labels to disguise a structural failure.
6. Record each observed node position as normalized `x` and `y` coordinates from `0` to `1`.
7. Copy the story-scroll seed into `html/index.html`, replace the base layer, and place exact HTML labels at the recorded coordinates.
8. Set `data-story-base-reviewed="true"` only after the visual review, render with Playwright, and run the validator.

## Required HTML Contract

```html
<section class="poster story-scroll" data-story-base-reviewed="true">
  <div
    data-story-node
    data-anchor="node-id"
    data-source="brief:node-id"
    data-x="0.18"
    data-y="0.62"
  >...</div>
</section>
```

- Keep the root as `section.poster.story-scroll` so the standard renderer can capture it.
- Give every node `data-story-node`, a non-empty `data-source`, and normalized `data-x`/`data-y` values.
- Mark each observed base object with `data-story-anchor="node-id"` and bind its label with the matching `data-anchor="node-id"`. These markers may be transparent overlays when the base is one raster image.
- Include one `.story-route` spanning the visual sequence.
- Put text directly in safe empty regions; do not turn nodes into equal cards or a numbered timeline.

## Long-scroll QA

- Ratio remains between `2.6:1` and `3:1`.
- Five to eight HTML nodes correspond to visible base objects.
- The left start, middle turn, and right resolution are present.
- The route is continuous, visibly irregular, and not evenly spaced.
- Labels do not cover objects, collide, leave the canvas, or fall below 26px.
- Names, project labels, numbers, and dates exactly match `brief.md`.
- Large objects and visual weight are balanced across the width.
- Failed base review, coordinates, source metadata, text safety, or geometry prevent `validated`.
