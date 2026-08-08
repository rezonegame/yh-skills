---
name: yh-social-visual
description: This skill should be used when the user asks to turn an article, post, topic, or existing content into platform-ready social visuals, including 小红书图文/九宫格/轮播图, 公众号封面/正文配图, 微博或知乎配图, 抖音/视频号封面, article covers and inline illustrations, or cross-platform visual adaptation. It plans content-first image packages and routes each asset to native image generation, deterministic HTML rendering, or a resumable hybrid workflow. Do not use it for standalone posters, general image inspiration, product imagery, board-game art, or visual style exploration without a content-distribution goal; use `yh-image-inspirer` for those visual-first tasks.
---

# YH Social Visual

Turn content into platform-ready visual packages. Treat content structure, communication goal, and destination platform as the primary constraints; an image succeeds when it helps the content travel.

## Boundary

Use this skill when content or platform intent comes first:

- Convert an article into a cover and inline illustrations.
- Split a topic into a Xiaohongshu carousel.
- Create WeChat cover pairs or article graphics.
- Adapt an existing package for Weibo, Zhihu, Douyin, or WeChat Channels.

Do not use this skill for visual-first independent posters, product photography, board-game cards, style discovery, or reference hunting. Route those to `yh-image-inspirer`; do not call it from this workflow.

## Runtime Requirements

Use Node.js 20+ for bundled scripts. Resolve Playwright from a local installation or Codex workspace dependencies. Use the runtime `imagegen` capability for native raster generation.

## Modes

| Mode | Use when | Typical deliverables |
| --- | --- | --- |
| `package` | A complete platform package is requested | Cover, content cards, summary card, manifest |
| `carousel` | Content should become a multi-page sequence | Cover plus ordered 3:4 or 1:1 cards |
| `cover` | One platform cover is needed | One cover or a WeChat 21:9 + 1:1 pair |
| `article` | A long-form article needs visual support | Cover, summary graphic, inline illustrations |
| `adapt` | Existing content or visuals must fit another platform | Reframed copy, crops, ratios, and platform variants |

Default to `package` when a platform is named but a mode is not.

## Preset Contract

Every rendered asset must use a registered style preset and platform geometry preset. Read `references/contracts/social-preset.md` and run `node scripts/validate_social_preset.mjs <manifest-or-fixture.json>` before rendering. Keep `scripts/lib/browser-safety.mjs` enabled so local HTML cannot fetch remote resources.

Three MIT-licensed structural preset families from PPT Master commit `bbb323f0ebd6a6a230dd6063209326b53bfd2e1d` are available under `assets/upstream/ppt-master/layouts/`: `xiaohongshu_post` (10, 3:4), `story_vertical` (9, 9:16), and `moments_square` (8, 1:1). Their local routing and geometry adapter is `presets/ppt-master-social.json`. They remain neutral structure presets owned by this skill; never route a social task to `yh-slides`, fetch a remote asset at render time, or let upstream preview paint override project direction.

## Rendering Strategies

| Strategy | Choose when |
| --- | --- |
| `auto` | Select the best strategy per asset; this is the default. |
| `native` | The asset is image-led: photography, illustration, scene, character, or expressive cover art. |
| `html` | Exact text, comparisons, data, lists, labels, or a repeatable card system matters. |
| `hybrid` | A generated hero visual must be combined with precise HTML typography or information layout. |

In `auto`, prefer HTML when text accuracy and consistency determine success. Prefer native when atmosphere and originality determine success. Hybrid is a resumable two-stage workflow, not a single uninterrupted call.

## Workflow

### 1. Read preferences

Read `{skills-dir}/.yh-skills/yh-social-visual/EXTEND.md` when present. Apply `render_strategy`, `output_root`, and platform defaults without asking again.

### 2. Establish the brief

Identify source content, central claim, target platform, audience, publishing goal, required deliverables, supplied assets, exact text, preservation constraints, mode, and strategy.

Ask only for missing information that materially changes usability. Before creating state or rendering, give a concise non-blocking preflight whenever platform, mode, strategy, or scope was inferred. Read `references/intake-guidance.md`.

For an existing long article needing cover and inline illustrations without adaptation, use `article` and a general long-form, WeChat-compatible default. State that the publishing destination is inferred, then continue. Do not add Xiaohongshu, Weibo, Zhihu, Douyin, or other variants unless requested.

### 3. Create task state

Run:

```powershell
node scripts/init-task.mjs --dir <task-dir> --mode <mode> --platforms <comma-list> --strategy <strategy> --title "<title>"
```

This creates `brief.md`, `manifest.json`, `prompts/`, `html/`, `sources/`, and `output/`. Do not overwrite an existing task unless replacement is explicit. Read `references/workflow-state.md` before changing states or resuming hybrid work.

### 4. Plan the package

Read `references/platforms.md` for ratios, safe areas, and naming. For article mode, start with `references/illustrations/index.md`; complete the visual-worthiness gate, internal `visual_form`, conception contract, facts, and source records before prompt writing. For cover direction, read `references/cover/index.md`. For text-card decks, read `references/social-card/index.md`.

Write the content breakdown and asset list to `brief.md`. Add requested deliverables to `manifest.json` before rendering. Keep one communication job per card.

A `story-scroll` is an asset role inside article mode, not a mode. Create it only after an explicit request for a long-scroll story, growth path, project overview, or product evolution. Read `references/illustrations/story-scroll.md`.

### 5. Render

#### Native

Write one complete prompt per asset under `prompts/` before calling runtime `imagegen`. Do not call provider APIs or the removed `yh-image` skill.

After generation, copy project outputs into task `output/` or `sources/`, then record path and state. View every generated image. The first generation is a candidate; it cannot become `validated` until it passes the Critical QA in `references/illustrations/visual-conception.md`. If native generation is unavailable, preserve the prompt and mark `failed`; do not silently fall back to CLI or API generation.

#### HTML

Copy a seed from `assets/social-card/` into task `html/`, adapt it, then render and validate:

```powershell
$env:CODEX_NODE_MODULES = "<workspace dependency node_modules path>" # when Playwright is not local
node scripts/render-social-deck.mjs <task-dir>
node scripts/validate-social-deck.mjs <task-dir>
```

Load Codex workspace dependencies first in Codex Desktop. The scripts also accept normal local Playwright.

#### Hybrid

Stage 1 creates the brief, manifest, prompts, HTML skeleton, and explicit placeholders; set generated-image assets to `awaiting-generation`.

Stage 2 copies native images into `sources/`, updates states to `generated` or `awaiting-composition`, completes composition, renders, and validates. Never report completion while placeholders remain.

For `story-scroll`, inspect the text-free base before recording normalized node coordinates or placing labels. A mismatched node count, route, or spatial relationship requires base regeneration, not label repositioning.

### 6. Validate and deliver

Validate dimensions, text accuracy, overflow, safe areas, ordering, naming, factual integrity, visual-form Critical QA, and manifest completeness. Show important final images with absolute local paths in Codex Desktop. Report failed or pending assets without hiding partial completion.

For high-stakes campaigns, carousels, covers, or multi-asset packages, use `autoreason-review` only as a concept/communication gate before final rendering or after the brief is stable. Review platform fit, content-image alignment, sequence logic, hook clarity, and restraint. Do not use it instead of dimension checks, safe-area checks, text rendering, factual integrity, or visual QA.

## Output Contract

```text
<task-dir>/
├── brief.md
├── manifest.json
├── prompts/
├── html/
├── sources/
└── output/
```

Use descriptive names such as `xiaohongshu-01-cover.png`, `wechat-21x9-cover.png`, `zhihu-article-02.png`, `douyin-cover.png`, or `article-story-scroll.png`.

## References

- `references/platforms.md` — platform defaults, safe areas, and naming.
- `references/intake-guidance.md` — non-blocking preflight, inference, and alternatives.
- `references/workflow-state.md` — manifest schema, states, and resume rules.
- `references/rendering.md` — native, HTML, hybrid, and Playwright routing.
- `references/cover/index.md` — cover composition, palettes, styles, and prompts.
- `references/illustrations/index.md` — article visual routing and progressive references.
- `references/illustrations/visual-conception.md` — cognitive anchors, visual forms, conception contracts, facts, and Critical QA.
- `references/illustrations/story-scroll.md` — explicit long-scroll hybrid planning and validation.
- `references/social-card/index.md` — card layouts, themes, components, production, and QA.
- `references/source-attribution.md` — retained sources and licenses.
