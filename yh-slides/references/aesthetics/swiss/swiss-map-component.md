# Swiss Map Component

Use this for geography, routes, store/campus distribution, historical locations, city relationships, or spatial evidence pages in Swiss mode.

## Role

This is not a new Swiss layout. Treat it as an `S08 Duo Compare` right-slot extension.

## Hard Rules

- Keep `data-layout="S08"`.
- Page structure: top title, left explanation cards, right map card.
- HTML renders pin dots, relation lines, labels, and cards.
- SVG may provide fallback lines only; do not put text inside SVG.
- Map interaction must not hijack slide navigation.
- If map tiles or online maps are unavailable, static fallback pins and relations must remain visible.

## Data Contract

Define points before writing the page:

```js
const MAP_POINTS = [
  { id: 'a', name: 'Point A', meta: 'Context', x: 35, y: 48, accent: true },
  { id: 'b', name: 'Point B', meta: 'Context', x: 62, y: 56 }
];
const MAP_RELATIONS = [['a', 'b']];
```

`x` and `y` are fallback percentage positions. Optional `coord` may be stored for future MapLibre integration, but offline fallback must not depend on it.

## QA

- `data-layout="S08"` is present.
- No new fake `P23/P24` layout is introduced.
- Pins and labels stay above bottom navigation safe area.
- One accent color only.
- Static fallback is meaningful without network.
