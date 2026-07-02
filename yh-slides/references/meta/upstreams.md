# Upstream Sources

`yh-slides` has absorbed selected upstream slide-skill assets for offline use. These sources are now local `yh-slides` assets; they do not replace Step 0 intent discovery, route recommendation, checkpoints, or QA gates.

| Source | Pinned commit | License | Local path | Primary use |
|---|---|---|---|---|
| `hugohe3/ppt-master` | `328388d4e76778535676056f49be8f28a08e79b2` | MIT | `scripts/template_fill_pptx*`, `templates/charts`, `templates/icons`, `templates/layouts`, `references/provenance/` | Path S native editable PPTX, SVG/PPTX tools, charts/icons/templates, template-fill workflow |
| `op7418/guizang-ppt-skill` | `82fe5ae129e8c2a12e1155fcabed6703342749d6` | AGPL-3.0 | `templates/html-decks/guizang`, `assets/screenshot-backgrounds/guizang`, `references/provenance/` | Magazine and Swiss HTML deck seeds, layouts, themes, screenshot framing, Swiss validator |
| `lewislulu/html-ppt-skill` | `f3a8435d3901697d5ac5e64d356c933637e43107` | MIT | `templates/html-decks/html-ppt`, `references/provenance/` | Static HTML themes, layouts, full-deck templates, runtime, animations, presenter mode |
| `helloianneo/ian-handdrawn-ppt` | `b2cc5f303337e5470fd6ac2870d261a43b218439` | MIT | `assets/style-samples/ian-handdrawn-technical-anchor.png`, `references/aesthetics/ian-handdrawn-technical.md` | Ian 中文手绘技术解释的视觉锚点、语义页型、2B/2C prompt 与 QA 方法 |

## Provenance Rules

- Keep each upstream lock pinned in `provenance/upstream-locks/`. Do not silently replace absorbed files from a new commit.
- After changing a pinned commit or re-absorbing assets, rerun:
  - `python scripts/check_upstream_locks.py`
  - `python scripts/build_asset_registry.py`
  - `python scripts/check_yh_slides_integrity.py`
  - `python scripts/check_offline_ready.py`
- Keep license files in `assets/external-licenses/`.
- Keep Ian's MIT license and NOTICE attribution with the renamed style anchor; the image is a visual calibration asset, not local original artwork or deck content.
- AGPL assets from `guizang-ppt-skill` must remain clearly attributed. Do not paste AGPL code into unmarked local files.

## Local Runtime Notes

- Absorbed templates that originally used Google Fonts, unpkg, or jsDelivr must be patched to local fonts and local JS before being treated as offline-ready.
- The generated `asset-registry.json` is the discovery layer. Main workflow guidance should read that registry first, then open specific assets only when needed.
