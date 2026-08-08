# Adoption Decisions

## E. Locked Presets and Device QA
- Source: op7418/guizang-social-card-skill
- Source URL: https://github.com/op7418/guizang-social-card-skill
- License: AGPL-3.0 (method concept only, all implementation self-written)
- Material adopted: preset locking philosophy (concept only)
- Material excluded: all code, templates, assets from upstream
- Test: scripts/validate_social_preset.mjs + 9 fixtures (3 positive, 6 negative)
- Rollback: delete references/contracts/social-preset.md, scripts/validate_social_preset.mjs, fixtures/social-preset/
- Date: 2026-07-28
