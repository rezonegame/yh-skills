# Type Composition Guidelines

## Type Gallery

| Type | Description | Best For |
|------|-------------|----------|
| `hero` | Large visual impact, title overlay | Product launch, brand promotion, major announcements |
| `conceptual` | Concept visualization, abstract core ideas | Technical articles, methodology, architecture design |
| `typography` | Text-focused layout, prominent title | Opinion pieces, quotes, insights |
| `metaphor` | Visual metaphor, concrete expressing abstract | Philosophy, growth, personal development |
| `scene` | Atmospheric scene, narrative feel | Stories, travel, lifestyle |
| `minimal` | Minimalist composition, generous whitespace | Zen, focus, core concepts |

## Cover Safe Zone

When targeting platforms with wide cover formats (e.g., WeChat 2.35:1), the cover image has a center crop safe zone:

```
┌─────────────────────────────────────┐
│         │ Safe Zone │               │
│  Decor  │ (Core)    │  Decor        │ Full width × height
│         │           │               │
└─────────────────────────────────────┘
           ↑ Social feed crops here ↑
```

Rules:
- **Safe zone**: central square region — all titles, key visuals, and critical information must fit here
- **Decor zones**: sides can contain gradients, textures, supporting graphics — never key text
- WeChat: safe zone = center 766×766 of 1800×766 image (朋友圈裁切为正方形)
- Title ≤ 10 characters within safe zone
- For platform-specific dimensions, see `references/platform-presets.md`

## Type-Specific Composition

| Type | Composition Guidelines |
|------|------------------------|
| `hero` | Large focal visual (60-70% area), title overlay on visual, dramatic composition. Safe zone: focal visual centered. |
| `conceptual` | Abstract shapes representing core concepts, information hierarchy, clean zones. Safe zone: key concept centered. |
| `typography` | Title as primary element (40%+ area), minimal supporting visuals, strong hierarchy. Safe zone: title centered. |
| `metaphor` | Concrete object/scene representing abstract idea, symbolic elements, emotional resonance. Safe zone: metaphor object centered. |
| `scene` | Atmospheric environment, narrative elements, mood-setting lighting and colors. Safe zone: main subject centered. |
| `minimal` | Single focal element, generous whitespace (60%+), essential shapes only. Safe zone: focal element centered. |
