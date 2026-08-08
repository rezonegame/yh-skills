# Bento Deck Contract

`bento-deck.json` is the route-specific source plan for `2D-B / Bento Deck`.
It becomes a self-contained, editable `.bento.html`; it is not a PPTX
intermediate file and it does not replace `deck-plan.json`.

## When to use it

Use this adapter when the requested deliverable is a browser-editable single
file, the recipients should not install an editor, or the deck benefits from
native object states, morph transitions, review comments, or optional private
collaboration. Keep using Path A/S/T when the promised deliverable is PPTX;
use Path C/D/E for bespoke web presentation, animation/TTS, or a maintained
React application.

## Minimal schema

```json
{
  "schema": "yh_slides_bento_deck.v1",
  "title": "项目标题",
  "size": {"width": 1280, "height": 720},
  "theme": {"background": "#F7F3EB", "color": "#17212B", "accent": "#C75B39"},
  "assets": {"hero": "data:image/png;base64,..."},
  "slides": [
    {
      "id": "cover",
      "name": "封面",
      "background": "#F7F3EB",
      "transition": "none",
      "notes": "开场：说明听众将得到什么。",
      "elements": [{"id": "title", "type": "text", "x": 96, "y": 120, "w": 920, "h": 160, "html": "<b>行动标题</b>"}]
    }
  ]
}
```

Required slide fields are `id`, `name`, `notes`, and non-empty `elements`.
Every element has a stable `id`, `type`, `x`, `y`, `w`, `h`. Supported types:
`text`, `shape`, `image`, `svg`, `chart`, `table`, `media`. A `morph`
transition must share at least one element ID with the preceding slide.
State slides may add `state_of` pointing at their parent slide ID.

Sources must be `data:` or `asset:<asset-id>` by default. Remote media is
disallowed except `media` with explicit `allow_external_media: true`; use that
exception only after the user accepts that the deck is no longer fully offline.

## Build and review loop

```powershell
python scripts/validate_bento_deck.py bento-deck.json --deck-plan deck-plan.json
python scripts/create_bento_deck.py bento-deck.json output/项目.bento.html --deck-plan deck-plan.json
python scripts/extract_bento_comments.py output/项目.bento.html --output review-comments.json
```

The generator injects only the JSON inside `#bento-doc` into the pinned local
shell. It refuses a shell containing remote `src`/`href` runtime dependencies,
escapes `<` in JSON, and never silently enables collaboration or uploads.

## Review and collaboration boundary

Open the `.bento.html` locally, edit only as necessary, and return exported
comments to the author through `extract_bento_comments.py`. Treat comments as
revision input, not approval by themselves. Bento can support encrypted
collaboration, but this adapter never creates a room, key, or network session.
If a user explicitly enables collaboration, tell them that possession of the
collaboration link/key grants access and keep that key out of public releases.

## QA

Run the validator, open the output locally, test navigation/editability and
notes, then do the normal visual screenshot QA. For every `morph` or state
slide, manually test the transition. Do not add remote fonts, analytics,
tracking, CDN scripts, or external media to a default delivery.
