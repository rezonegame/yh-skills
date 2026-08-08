# Design Brief Contract

`design-brief.json` captures the human-facing visual and narrative decisions
before a multi-page deck is built. It is deliberately route-neutral and is
written by the local workflow; it does not require an upstream runtime.

Use it when the deck has a meaningful visual system, multiple audiences, data
visualization, or an explicit review-before-build checkpoint:

```powershell
python scripts/validate_design_brief.py <project-dir>/design-brief.json `
  --deck-plan <project-dir>/deck-plan.json
```

Required fields:

- `title`, `objective`, `audience`, `canvas`, and `visual_system`
- non-empty `layout_principles`
- `pages`: each page has a unique `id`, a `purpose`, and an `audience_move`
- `speaker_notes_strategy`

`visual_system` must state a mood, typography direction, and named colour
roles. If `pages` declares `has_ai_images: true`, it must also state an
`ai_image_strategy`. The optional `--deck-plan` check ensures both artifacts
use the same ordered page IDs, so a reviewed brief cannot silently drift from
the build plan.

The brief is a review checkpoint, not a substitute for route-specific render
or visual QA. Do not author production files until the user has approved a
brief when they explicitly request review-first work.
