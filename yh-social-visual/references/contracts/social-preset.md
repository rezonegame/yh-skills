# Social Preset Contract

Every output asset uses two independent controls:

- A style preset (`ink`, `paper`, `editorial`, `warm`, `cool`, `mono`, `forest`, `sunset`, `night`, or `signal`) controls the design system.
- A platform preset controls ratio, crop-safe area, and text bounds. Registered platform presets are `xhs-carousel`, `xhs-cover`, `wechat-cover-21-9`, `wechat-cover-1-1`, `weibo-card`, `zhihu-card`, `douyin-cover`, `article-cover`, `article-inline`, `portrait-generic`, `square-generic`, and `landscape-generic`.

New manifests should declare `style_preset`, `platform_preset`, `aspect_ratio`, and `safe_text_bounds`. The validator continues to accept the legacy `preset` style field. A standalone geometry fixture may use `preset` as the platform preset with `target_ratio`, `colors`, `text_blocks`, and `media_refs`.

Validation must reject unknown presets, wrong ratios, invalid bounds, text in crop zones, text below WCAG AA contrast, missing local media, and arbitrary `color_override`. More than three non-achromatic colors is a warning. Rendering remains local-only and must keep the browser isolation guard enabled.

Run:

```bash
node scripts/validate_social_preset.mjs <manifest-or-fixture.json>
```
