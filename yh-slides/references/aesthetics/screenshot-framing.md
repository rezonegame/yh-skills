# Screenshot Framing

Use this when user assets include product screenshots, webpages, code screenshots, dashboards, design files, or old PPT screenshots.

## Principle

Preserve screenshots by default. Do not redraw UI screenshots with image generation unless the source is unusable or the user wants a conceptual redesign.

## Decision Order

1. Pick the slide layout and image slot first.
2. Choose target ratio from the slot: `21:9`, `16:10`, `16:9`, `4:3`, or `1:1`.
3. Decide treatment:
   - faithful: fit screenshot into a local background canvas;
   - polish: fit screenshot with theme background, inset, and optional shadow;
   - redesign: generate a new UI scene only when fidelity is not required.
4. Export a local asset into the project `images/` folder.

## Semantic Parameters

| Parameter | Options |
|---|---|
| `ratio` | `21:9`, `16:10`, `16:9`, `4:3`, `1:1` |
| `background` | `plain`, `gradient`, `wallpaper`, `blurred`, `grid`, `paper` |
| `padding` | `compact`, `standard`, `spacious` |
| `inset` | `none`, `subtle`, `balanced` |
| `shadow` | `none`, `soft`, `editorial` |
| `corners` | `square`, `small`, `medium` |
| `alignment` | `center`, `top-left`, `top-right`, `bottom-left`, `bottom-right` |

## Style Defaults

- Magazine: paper/blurred background, small corners, soft/editorial shadow.
- Swiss: plain/grid background, square corners, no shadow, one accent color only.

## Offline Fallback

If no background asset is available, use a plain local canvas with the current deck background color and a subtle hairline. Never block deck generation only because screenshot polish is unavailable.
