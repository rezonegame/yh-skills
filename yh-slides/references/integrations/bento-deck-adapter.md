# 2D-B / Bento Deck Adapter

This is a deliberately narrow adapter around a pinned, local Bento Slides
shell. `yh-slides` still owns Step 0 intent discovery, narrative, design
direction, asset provenance, sample-page review, and P0/P1 QA. Bento supplies
the editable browser artifact, object model, states/morph, notes, comments and
optional collaboration capability.

## Routing

Recommend `2D-B` only for: a self-contained editable `.bento.html`, browser
editing without installing a desktop editor, reviewer comments, or interactive
state/morph slides. Do not use it by default just because the output is HTML.

| Need | Route |
|---|---|
| Native editable PowerPoint | `2A`, `2A-S`, or `2A-T` |
| Bespoke single-page/web magazine | `2D / Path C` |
| Narrated or animation-led HTML | `2D / Path D` |
| Long-lived React interaction | `2D / Path E` |
| One local editable file / review states | `2D-B / Bento Deck` |

## Authoring procedure

1. Complete Steps 0–4 and create `deck-plan.json` for multi-page work.
2. Draft `bento-deck.json` using [the contract](../contracts/bento-deck.md).
3. Validate it and build from `templates/html-decks/bento/Bento_Slides.bento.html`.
4. Open the result locally; verify editing, notes, transitions and state links.
5. Capture screenshots/contact sheet using normal 2D visual QA.
6. If review comments exist, extract them to JSON, resolve them in the source
   plan, regenerate, then retain a final review record.

## Non-negotiable boundaries

- Do not replace the pinned shell with a browser-downloaded update. Refreshes
  require source/license/security review and a new provenance lock.
- The vendored shell has its Cloudflare analytics beacon removed. Keep it that
  way; `check_offline_ready.py` must pass.
- Do not auto-enable remote media, collaboration, tracking, or CDN assets.
- Keep one authorial voice: use Bento interaction only when it advances the
  narrative; do not turn every page into a different animated demo.
- Preserve the shell's third-party notices and the Bento MIT record.
