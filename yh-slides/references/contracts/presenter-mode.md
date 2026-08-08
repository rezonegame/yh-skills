# Presenter mode contract

This contract independently implements the behavior reviewed in Guizang PPT at commit `c91369c449d34755d320a8b81d0734000d99d1ab`. No AGPL runtime code is copied.

- Every page has one stable semantic lowercase kebab-case `data-slide-id`.
- Embed one `<script id="speaker-notes" type="application/json">` object. Its `notes` array matches the rendered slide order exactly.
- Every note declares `id`, `title`, `purpose`, non-empty `talking_points`, `transition`, positive `talk_seconds`, `interaction`, `fallback`, and `pronunciation`. `auto_advance_seconds` is optional and distinct; the ambiguous key `duration` is forbidden.
- The top-level object declares `talk_budget_seconds`, all five `runtime_features`, and recovery heartbeat/timeout/resume-token behavior.
- `audience-connection`, `heartbeat-timeout`, `recovery`, `end-mask`, and `notes-persistence` are required audience-window behaviors. The implementation may use BroadcastChannel, storage events, or another local transport, but reconnect must not silently reset the current slide or notes.
- Run `python scripts/validate_presenter_mode.py <deck.html>` before delivery.
