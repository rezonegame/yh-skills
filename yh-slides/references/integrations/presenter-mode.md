# 2D-P Presenter Mode

Use `2D-P` when the deck is for a live talk, training, technical sharing, roadshow, or any situation where the presenter needs notes, a next-slide preview, and a timer.

## Trigger

Recommend this mode when the user mentions:

- 演讲 / 分享 / 讲稿 / 逐字稿
- speaker notes / presenter view / 演讲者模式 / 提词器
- "怕忘词" / "讲不流畅"
- 30/45/60 minute talk planning

If the user wants a static visual deck or editable PPTX, do not force presenter mode.

## Local Assets

Absorbed local implementation: `templates/html-decks/html-ppt/`.

Relevant assets include:

- `templates/html-decks/html-ppt/runtime.js`
- `templates/html-decks/html-ppt/full-decks/presenter-mode-reveal/`
- `references/provenance/html-ppt-skill-references/presenter-mode.md`

These are indexed in `asset-registry.json` with route hint `2D-P Presenter Mode`.

## Authoring Contract

Each slide must contain audience-facing content plus hidden notes:

```html
<section class="slide">
  <h1>Audience title</h1>
  <p>Audience-facing content only.</p>
  <aside class="notes">
    <p>Presenter script with <strong>keywords</strong> and natural transitions.</p>
  </aside>
</section>
```

Rules:

- Presenter notes must not appear as visible slide text.
- Write notes like spoken prompts, not formal prose.
- Use 150-300 Chinese characters/words per slide only when the user needs detailed delivery support; otherwise 2-5 natural sentences is enough.
- End each note with a natural transition into the next slide when useful.

## Runtime Expectations

- `S` opens the presenter window.
- Presenter window contains current slide, next slide, script, and timer.
- Audience and presenter windows sync through `BroadcastChannel`.
- `?preview=N` renders a single slide preview without chrome.
- Offline mode must use local runtime JS and local CSS/fonts.

## QA

P0 checks:

- Every slide has notes when presenter mode is requested.
- Notes are hidden from the audience view.
- `S` opens the presenter window.
- Current/next previews render.
- Timer works.
- Keyboard navigation syncs both windows.
