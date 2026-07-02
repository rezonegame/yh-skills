# Article Visual Conception

Use this method before selecting a style or writing a native prompt. It decides whether an illustration is useful, what cognitive work it performs, and which visible relationship carries the meaning.

## Visual-form Routing

`visual_form` is an internal planning field, not a required user parameter.

| Visual form | Use when | Default strategy |
| --- | --- | --- |
| `concept-metaphor` | A judgment, process, relationship, method, or abstract structure needs a concrete explanation | `native` |
| `object-scene` | A situation, pressure, conflict, emotion, or lived experience needs recognition and empathy | `native` |
| `story-scroll` | The user explicitly asks for a project retrospective, growth path, product evolution, or long-scroll overview | `hybrid` |
| `literal` | A screenshot, product, person, place, or factual scene must remain recognizable | `native` or `hybrid` |
| `structured` | Exact process, comparison, numbers, labels, or information cards carry the meaning | `html` or `hybrid` |
| `skip` | An image would only repeat nearby prose, add decoration, or require a long explanation to make sense | no asset |

Treat one visual per 600–1000 Chinese characters only as an upper-bound planning reference. Select cognitive anchors and high-value situations first; never distribute illustrations evenly just to fill a quota.

When the user requests an exact count, satisfy it when strong anchors exist. If they do not, identify core concepts and optional weak candidates in the preflight and `brief.md`; do not silently invent decorative fillers.

## Concept Record

Record these fields under `Illustration Concepts` in `brief.md` for every proposed article image:

- Placement and cognitive anchor.
- Visual task and target reader or use situation.
- Conflict sentence: “Who is pushed by what, through which force, toward what result?”
- Physical action, core object, and spatial relationship.
- Semantic subject and the action that makes it necessary.
- Visual form, composition archetype, and three-second read.
- Known facts, fact sources, and unresolved items.
- Text policy, originality risk, and failure signals.

## Concept-metaphor Method

Translate the idea through this chain:

**abstract concept → physical verb → familiar low-tech object or space → semantic subject action**

Useful composition archetypes include process, system detail, before/after contrast, state sequence, concept metaphor, method layers, route, and short storyboard. Keep one visual thesis and one dominant relationship.

## Object-scene Method

Translate the reader’s situation through this chain:

**reader situation → core conflict → familiar object → clear force relationship → recognition moment**

Useful physical relationships include pulling, spilling, tangling, inspecting, renaming, filtering, compressing, and overloading. The object must be familiar, physically interactive, and understandable without a UI screenshot. Keep one core action, one primary object or tight object group, and few supporting elements.

## Composition Archetype Contract

Write this contract before generation. It replaces reference-master copying and does not require upstream examples.

```text
Composition archetype:
Invariants that must remain:
Content-specific relationship:
Three-second read:
Difference from other images in this package:
Failure signals:
```

Do not repeat the same primary object-plus-action combination within one package.

## Fact, Subject, and Text Gates

- Names, companies, projects, dates, quantities, achievements, and experience nodes must come from user input or supplied sources.
- Delete, abstract, or mark unconfirmed facts in the brief; never complete a plausible story from memory.
- Apply the semantic-subject test: if removing the subject leaves the meaning fully intact, the subject is decoration and the concept must be rebuilt.
- Native images default to no text. Add a short label only when it materially improves comprehension, and match the source-content language.
- Route exact text, names, numbers, logos, or multiple factual nodes to `hybrid` or `html`.

## Critical QA

A native candidate cannot become `validated` until it has been viewed and passes all checks:

- The core conflict is readable within three seconds.
- The subject performs a real semantic action.
- The image is not an element inventory, collage, or presentation slide.
- No facts or private details were invented.
- The package does not repeat its main metaphors.
- The selected style remains intact; no global white-background, hand-drawn, photographic, or topic bias is imposed.

The first generated image is a candidate, not an automatic final. Rewrite the prompt, edit, or regenerate after a critical failure.
