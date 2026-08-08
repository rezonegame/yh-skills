# Deck Plan Contract

`deck-plan.json` is an optional, path-neutral planning artifact for a slide project. Create it after intent and route confirmation, before build.

Run before assembly:

```powershell
python scripts/validate_deck_plan.py <project-dir>/deck-plan.json --project-root <project-dir>
```

It rejects known template/demo copy, duplicate layout IDs, text that exceeds its declared budget, unsafe or missing media, repeated media unless allowed, and chart data with no page insight. It does not replace path-specific build, render, or visual QA.

For an important page with several viable templates, optionally add
`layout_candidates` (2–4 candidates with unique `id` and different
`family` values), keep the selected candidate in `layout_id`, and add a
`content_package.required_facts` string list. This makes layout alternatives
share one canonical fact set. Supported families are `hero`, `split`,
`metric-spotlight`, `chart-led`, `timeline`, `matrix`, `editorial`,
`comparison`, `process` and `custom`. Do not repeat one selected family for
more than two consecutive pages unless `allow_family_run` is explicitly true.

Detailed selection guidance:
`references/aesthetics/content-layout-candidates.md`.
