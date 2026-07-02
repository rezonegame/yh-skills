# Rendering Routes

## Native Route

Use runtime-native image generation for photography, illustration, scenes, people, expressive hero images, and visual concepts. Store the final prompt before generation. Native output is project-bound only after it has been copied from the runtime generation directory into the task directory.

Do not call provider APIs automatically. Do not fall back to the removed `yh-image` skill. If the runtime built-in path is unavailable, retain the prompt and mark the asset failed.

## HTML Route

Use HTML when exact Chinese copy, data, labels, ordered steps, reusable cards, or a stable series system determines quality.

Choose a seed:

- `assets/social-card/template-editorial-card.html`
- `assets/social-card/template-swiss-card.html`

Read the relevant files under `references/social-card/` before adapting the seed. Render `.poster`, `.cover`, and `.wechat-pair-preview` elements with `scripts/render-social-deck.mjs`. Validate card density and typography with `scripts/validate-social-deck.mjs`.

## Playwright Resolution

The renderer resolves Playwright in this order:

1. A normal package visible from the skill scripts.
2. A package under `CODEX_NODE_MODULES`.
3. A package under `NODE_PATH`.

In Codex Desktop, call the workspace dependency loader and set `CODEX_NODE_MODULES` to its Node packages path before running the scripts. The renderer prefers an installed system Chrome or Edge executable, then uses Playwright's own browser when available. Set `PLAYWRIGHT_CHROME_EXECUTABLE` only when an explicit browser path is needed. Do not silently install packages or browsers from the network.

## Hybrid Route

Use hybrid only when a generated visual and deterministic typography are both essential.

Stage 1 prepares all non-image work and leaves explicit placeholders. Stage 2 begins after generated files have been copied into `sources/`. Record the transition in the manifest so another turn can resume without repeating planning or generation.
