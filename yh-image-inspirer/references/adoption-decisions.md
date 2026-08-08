# Adoption Decisions

## D. Asset Intent Handoff
- Source: OpenAI Codex imagegen SKILL.md
- Source URL: https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/imagegen/SKILL.md
- License: MIT (Apache 2.0 for codex repo, SKILL.md is method-only)
- Material adopted: generate/edit mode split, edit constraints, non-destructive filename
- Material excluded: new API backend, silent model downgrade
- Test: scripts/validate_asset_intent.py + 6 fixtures (2 positive, 4 negative)
- Rollback: delete references/contracts/asset-intent.md, scripts/validate_asset_intent.py, fixtures/asset-intent/
- Date: 2026-07-28

## E. Prompt Compiler + Variation Engine + Color Engine
- Source: gc-minimal-zine-poster
- Source URL: https://github.com/LiamGvchi/gc-minimal-zine-poster
- License: MIT
- Material adopted: 5-axis variation engine, numerical color engine, 9-field prompt compiler, style-specific anti-patterns, quantitative quality gates
- Material excluded: fixed zine-only recipes (generalized into multi-style-family axes)
- Scope: 5 new reference files, 3 patches to SKILL.md workflow
- Rollback: delete references/variation-engine.md, color-engine.md, prompt-compiler.md, style-avoids.md; revert output-checklists.md; revert SKILL.md director-stage patches
- Date: 2026-07-28
