# Article Illustration Prompt Construction

Build prompts from the article's communication job and completed composition contract, not from decorative style words alone.

## Prompt Order

1. **Editorial purpose and visual form**: state what the image clarifies and whether it is a concept metaphor, object scene, literal scene, or another routed form.
2. **Conflict and physical action**: identify who is affected, the visible force, the core object, and the result.
3. **Semantic subject**: make the subject perform the action that carries the meaning.
4. **Composition contract**: state the archetype, invariants, content-specific relation, three-second read, package difference, and failure signals.
5. **Visual language**: select one style and palette from the illustration references without overriding the user's brand or supplied direction.
6. **Facts and references**: name only verified details and assign each supplied image an identity, style, composition, or continuity role.
7. **Output constraints**: state ratio, text policy, safe area, and forbidden artifacts.

## Template

```text
Create an editorial illustration for [article section / communication purpose].
Visual form: [concept-metaphor / object-scene / literal].

The conflict is: [who] is pushed by [force], through [physical mechanism], toward [result].
Show [semantic subject] [concrete action] with [one core object or tight object group] in [spatial relationship].
Composition archetype: [type]. Preserve [invariants]. The three-second read is: [single visible thesis].
Make this image distinct from the package by [unique object-action/composition].

Use [style] with [palette], [lighting], and [surface treatment].
Verified facts only: [facts and sources, or none]. Preserve [reference roles and exact properties].
Output at [aspect ratio]. [No text / use only this short non-critical label in the source language: "..."].
Avoid [failure signals, repeated package metaphors, clutter, slide-like layout, invented facts, malformed artifacts].
```

## Reference Images

Describe each image's role before native generation:

- **Identity**: preserve a person, product, place, or object.
- **Style**: borrow color, texture, rendering, or photographic treatment.
- **Composition**: borrow spatial organization without copying content.
- **Continuity**: keep a series coherent.

Do not rely on “first image” alone. Name the role and property to preserve. Factual identity and communication clarity override surface style.

## Text and Fact Rule

Native defaults to no text. A short label is permitted only when it materially improves comprehension and follows the content language. Route exact wording, names, numbers, logos, and multiple factual nodes to HTML or hybrid. Never invent a plausible name, date, achievement, quantity, or experience node.

## Final Check

- The core relationship is understandable within three seconds without reading the prompt.
- The subject is semantically necessary rather than decorative.
- The prompt contains one core action and one primary object relationship.
- The composition contract and verified facts are explicit.
- The object-plus-action combination does not repeat another package image.
- Ratio, text policy, and placement match the manifest.
