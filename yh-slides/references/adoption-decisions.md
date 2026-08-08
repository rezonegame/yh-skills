# Adoption Decisions

记录 yh-slides 从外部来源吸收方法论的决策和回滚路径。

## B. Academic Deck Contract
- Source: Gabberflast/academic-pptx-skill
- Source URL: https://github.com/Gabberflast/academic-pptx-skill
- Source commit: 90ba1af (2026-02-28)
- License: MIT
- Material adopted: action title rule, results page contract, citation requirement
- Material excluded: academic-only slide replacement, code, templates
- Test: scripts/validate_academic_deck.py + 4 fixtures (1 positive, 3 negative)
- Rollback: delete references/contracts/academic-deck.md, scripts/validate_academic_deck.py, fixtures/academic-deck/, and the academic mode pointer in SKILL.md Step 0
- Date: 2026-07-28

## Tosea Preview Library and Evidence Method
- Source: Tosea.ai showcase, blog, and template catalog
- Source URL: https://tosea.ai/
- Material adopted: local template previews, category metadata, evidence-driven document-to-deck method
- Material excluded: remote runtime dependency and unreviewed third-party code
- Test: asset registry build plus metadata count and path validation
- Rollback: delete `templates/tosea/`, `references/evidence-driven-methodology.md`, and related registry entries
- Date: 2026-08-07

## Wanghong Handwritten HTML Style
- Source: tjxj/z-skills (`z-wanghong-handwritten-ppt`)
- Source URL: https://github.com/tjxj/z-skills
- Reviewed/pinned commit: `f5832fba31911cc423e86fcab88bf04361b5cf36`
- License: MIT for the absorbed runtime/assets; bundled notices retained
- Material adopted: local CSS/runtime, timeline builder, render preparation, and style guide
- Material excluded: paid-font dependency; local fallback uses LXGW WenKai. Local CSS differences are intentional patches recorded in `meta/z-skills-local-patches.json`, not evidence that the upstream lock is stale.
- Test: compile Python helpers, build a local timeline deck, and verify no remote resources
- Rollback: delete `assets/wanghong/`, the helper scripts, and the style reference
- Date: 2026-08-08
