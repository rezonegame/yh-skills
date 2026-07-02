# Platform Defaults

Use these as production defaults when the user does not provide exact dimensions. Treat platform requirements as revisable presets rather than permanent facts.

## Unspecified Long-form Destination

When the user supplies an existing long article and asks only for a cover plus inline illustrations:

- Use `article` mode; do not reinterpret the request as a carousel or content rewrite.
- Use a general long-form, WeChat-compatible working specification: 21:9 cover plus 16:9 or 4:3 inline images when no dimensions are given.
- Describe WeChat compatibility as an inferred production default, not as the confirmed destination.
- Mention that Xiaohongshu or Zhihu would require different composition only when that alternative is plausibly useful.
- Do not generate additional platform variants without an explicit request.

| Platform | Primary format | Default output | Notes |
| --- | --- | --- | --- |
| Xiaohongshu | Carousel | 1080×1440, 3:4 | Keep key text inside 72–96px side margins and away from the bottom interaction area. Use one idea per page. |
| WeChat Official Account | Cover pair | 2100×900, 21:9 and 1080×1080, 1:1 | Build the pair together. Keep the wide-cover title in a clear central band; shorten the square title to roughly 4–10 Chinese characters. |
| WeChat article | Inline image | 1920×1080, 16:9 or 1440×1080, 4:3 | Prefer medium-tone backgrounds that remain readable in light and dark reading environments. |
| Weibo | Feed image set | 1080×1080, 1:1 by default | Use 16:9 for link-preview or landscape editorial assets when requested. Keep the first image independently understandable. |
| Zhihu | Article cover and inline | 1920×1080, 16:9 | Use 4:3 for dense explanatory graphics when it improves readability. |
| Douyin | Static cover | 1080×1920, 9:16 | Keep important text and faces inside the central region; avoid edge-mounted copy that UI chrome may cover. |
| WeChat Channels | Static cover | 1080×1920, 9:16 | Use the same central-safe composition principle as short-video covers. |

## Package Defaults

### Xiaohongshu

- Produce one cover and 4–8 content pages.
- Add one summary or checklist page only when it improves closure.
- Use short page titles and 2–4 concise supporting fragments.
- Name files `xiaohongshu-01-cover.png`, `xiaohongshu-02-<topic>.png`, and so on.

### WeChat Cover Pair

- Produce `wechat-21x9-cover.png` and `wechat-1x1-cover.png`.
- Produce `wechat-cover-pair-preview.png` for visual checking when using HTML rendering.
- Keep the square cover typographic by default; add an image only when the brief calls for it.

### Cross-platform Adaptation

- Preserve the message hierarchy, brand anchors, and source-image identity.
- Rewrite title length and card count for the destination platform instead of merely cropping.
- Record every destination variant as a separate manifest asset.
