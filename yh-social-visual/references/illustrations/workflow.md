# Article Illustration Workflow

Use this workflow when images serve a long-form article or post. Preserve the article's argument and reading rhythm; do not add decorative images that merely repeat nearby text.

## 1. Analyze the Article

Extract the central claim, audience, section structure, important transitions, difficult concepts, high-value lived situations, existing evidence, and supplied visual references.

## 2. Route Each Candidate

Read `visual-conception.md`, then assign one internal `visual_form`:

- `concept-metaphor` for judgments, relationships, methods, and abstract structures.
- `object-scene` for pressure, conflict, emotion, and recognizable situations.
- `story-scroll` only for an explicitly requested long-scroll overview.
- `literal` for recognizable people, products, places, screenshots, or factual scenes.
- `structured` for exact processes, comparisons, data, labels, and information cards.
- `skip` when the visual adds no distinct value.

Treat one meaningful visual per 600–1000 Chinese characters as a quantity ceiling, not a distribution target. Choose cognitive anchors first. If the user requests more images than the article supports, distinguish core concepts from optional weak candidates rather than inventing filler.

## 3. Write the Conception Contract

For every candidate, complete the `Illustration Concepts` fields in `brief.md`: placement, cognitive anchor, conflict sentence, action, object, semantic subject, composition archetype, three-second read, facts and sources, text policy, originality risk, and failure signals.

Reject candidates that cannot pass the visual-worthiness gate or semantic-subject test. Within one package, do not repeat the same primary object-plus-action metaphor.

## 4. Choose Rendering Per Image

- Use `native` for scenes, illustration, metaphor, editorial art, and photographic concepts.
- Use `html` for exact labels, tables, steps, quotes, comparisons, and dense information.
- Use `hybrid` when a generated visual must support exact typography, names, numbers, logos, or multiple fact nodes.

Native defaults to no text. Short labels are optional, must improve comprehension, and follow the source-content language. Do not choose one rendering strategy for an entire article when assets have different jobs.

## 5. Maintain a Visual System

Keep no more than two related style families across one article package. Lock palette, contrast, line or photographic treatment, shape language, typography, identity, and brand invariants. Vary composition, object-action relationships, and viewpoint while preserving the system.

## 6. Build and Generate

Read `prompt-construction.md` and the selected style reference. For native assets, state the editorial role, visible action, composition contract, style, palette, factual constraints, reference roles, ratio, and text policy.

Treat local reference images as runtime inputs to native generation rather than provider-specific flags. The first generated image is a candidate. View it, run Critical QA from `visual-conception.md`, and revise or regenerate before marking it `validated`.

For an explicit `story-scroll`, read `story-scroll.md`; inspect the native base before recording normalized coordinates or composing exact HTML labels.

## 7. Record Placement and State

Record each asset's target section, purpose, `visual_form`, caption or alt-text idea, strategy, prompt path, factual source, and output path in `brief.md` and `manifest.json`. Keep incomplete or failed work resumable.
