# Second-Pass Upstream Audit

Date: 2026-06-03

This audit checks the offline `yh-slides` upgrade against the three absorbed upstreams after implementation. The goal is feature/design coverage while preserving the original guided `yh-slides` workflow.

## Scope

| Upstream | Pinned commit | Local path | Audit focus |
|---|---|---|---|
| `hugohe3/ppt-master` | `328388d4e76778535676056f49be8f28a08e79b2` | `scripts/template_fill_pptx*`, `templates/charts`, `templates/icons`, `templates/layouts` | Native editable PPTX, Path S, template fill, scripts, charts/icons/templates |
| `op7418/guizang-ppt-skill` | `82fe5ae129e8c2a12e1155fcabed6703342749d6` | `templates/html-decks/guizang`, `assets/screenshot-backgrounds/guizang` | Magazine/Swiss aesthetics, screenshot framing, Swiss map, validator, local runtime |
| `lewislulu/html-ppt-skill` | `f3a8435d3901697d5ac5e64d356c933637e43107` | `templates/html-decks/html-ppt` | Themes, layouts, full decks, animations, presenter mode, runtime |

## Coverage Matrix

| Capability | Upstream source | Local coverage | Evidence |
|---|---|---|---|
| Strong guided entry remains primary | `yh-slides` original | Covered | `SKILL.md` Step 0 preserved; vendor assets introduced only after Step 0-3 and Step 4 recommendation layer |
| Native editable SVG -> PPTX | `ppt-master` | Covered | `references/integrations/path-s-svg-native-pptx.md`; local `scripts/svg_to_pptx.py`; smoke `--help` passed |
| Template Fill PPTX reuse | `ppt-master` | Covered | `references/integrations/template-fill-pptx.md`; local upstream `template_fill_pptx.py`; smoke `--help` passed |
| Charts/icons/layout assets | `ppt-master` | Covered | `templates/charts`, `templates/icons`, `templates/layouts`; indexed in `asset-registry.json` |
| Page transitions/object animation reference | `ppt-master` | Covered | `SKILL.md` and Path S docs reference animation sidecar and `svg_to_pptx.py` flags |
| Magazine HTML deck | `guizang-ppt-skill` | Covered | Local seed plus absorbed `templates/html-decks/guizang/template.html`, layouts/themes/checklist |
| Swiss HTML deck | `guizang-ppt-skill` | Covered | `path-c-swiss-seed.html`, absorbed `templates/html-decks/guizang/template-swiss.html`, `swiss-layout-lock.md`, `validate-swiss-deck.mjs`; validator smoke passed |
| Screenshot framing/background assets | `guizang-ppt-skill` | Covered | Vendored `assets/screenshot-backgrounds`; local `references/aesthetics/screenshot-framing.md` |
| Swiss map component | `guizang-ppt-skill` | Covered | Vendored upstream reference; local `references/aesthetics/swiss/swiss-map-component.md` with offline fallback contract |
| Low-power Swiss runtime | `guizang-ppt-skill` | Covered | `path-c-swiss-seed.html` and absorbed template retain `B` low-power behavior |
| HTML themes/layouts/full decks | `html-ppt-skill` | Covered | Vendored `assets/themes`, `templates/single-page`, `templates/full-decks`; indexed |
| Presenter mode | `html-ppt-skill` | Covered | `references/integrations/presenter-mode.md`; absorbed presenter template/runtime exists |
| CSS/canvas animations | `html-ppt-skill` | Covered | Vendored animation CSS/fx/runtime; local Chart/highlight dependencies patched |
| Offline runtime | All | Covered | `check_offline_ready.py` passed; Google Fonts/unpkg/jsDelivr runtime dependencies patched to local files |
| Provenance/license | All | Covered | `references/meta/upstreams.md`; license files for MIT/AGPL/Chart.js/highlight.js |
| Skill reliability self-audit | skill-creator | Covered | `scripts/skill_creator_self_audit.py` passed |

## Design and Aesthetic Coverage

- Magazine and Swiss aesthetics are preserved as first-class Path C recommendations, not hidden references.
- Swiss-specific discipline is retained: locked layouts, single accent, low-power mode, local validator, and S08 map extension.
- html-ppt's broader theme/layout/animation library is available for HTML deck variety, but only through the asset registry and recommendation layer to avoid overwhelming the user.
- Path S gives high-fidelity native PPTX an aesthetic route beyond Path A's constrained HTML, especially for charts, diagrams, and consulting-style layouts.

## Reliability and Stability Coverage

- Backup exists under `backups/pre-offline-upgrade-*`.
- Upstream commits are pinned in `provenance/upstream-locks/` and auditable with `scripts/check_upstream_locks.py`.
- Local asset discovery is generated, not handwritten: `scripts/build_asset_registry.py`.
- Offline runtime is enforced: `scripts/check_offline_ready.py`.
- Structural integrity is enforced: `scripts/check_yh_slides_integrity.py`.
- Skill-creator principles are enforced: `scripts/skill_creator_self_audit.py`.

## Known Boundaries

- Cloud image generation, web fact checking, and cloud TTS remain optional online enhancements. Offline mode preserves structure, notes, placeholders, and local user assets.
- AGPL assets from `guizang-ppt-skill` are absorbed with explicit provenance. Do not blend AGPL code into unmarked local files.
- Full visual smoke tests requiring PowerPoint GUI or browser dual-window interaction are documented QA steps; command-line checks verify local availability and runtime dependency safety.

## Verdict

The current upgrade covers the three upstreams at the feature, asset, workflow, provenance, and offline-runtime levels while preserving `yh-slides` strong guided behavior. No further structural upgrade is required before use. Future improvements should be incremental: add real project eval cases, improve template ranking in `asset-registry.json`, and add optional browser-based presenter smoke automation.
