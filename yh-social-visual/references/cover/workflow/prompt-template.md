# Cover Prompt Template

Use this template for native or hybrid cover assets after selecting the platform, cover type, and visual direction.

## Core Template

```text
Create a [platform] cover for [content title or topic].

Communication goal: [what the viewer should understand or feel immediately].
Audience: [specific audience].
Hero subject: [concrete subject, action, and setting].
Composition: [cover type, framing, focal hierarchy, viewpoint, negative space, text-safe zone].
Visual direction: [rendering style], [palette], [lighting], [texture].
Brand or continuity constraints: [elements that must remain consistent].
Reference roles: [identity / style / composition / continuity and what to preserve].
Output: [dimensions and aspect ratio].
Text policy: [no text / exact short text / leave a clean title zone for HTML composition].
Avoid: [clutter, illegible text, generic symbols, malformed details, unsafe crop zones].
```

## Native Covers

Use native rendering when the cover succeeds mainly through scene, illustration, photography, character, or atmosphere. Keep generated text absent unless the wording is extremely short and the user accepts possible variation.

## Hybrid Covers

For exact titles, logos, dates, or dense information:

1. Generate a clean hero visual with an explicit empty title zone.
2. Store the generated image under `sources/`.
3. Compose exact typography and brand elements in HTML.
4. Render and validate the final cover.

## Platform Variants

Do not describe one universal crop when multiple ratios are required. Write a shared visual lock, then specify composition changes for each target ratio. A 21:9 WeChat cover and a 1:1 share image should preserve the idea and identity while using different hierarchy and crop logic.

## Reference Images

Read `reference-images.md` before using supplied images. Describe what each reference controls; do not encode runtime- or provider-specific flags in the prompt.

## Check Before Generation

- The cover communicates one clear promise.
- The platform ratio and safe zone are explicit.
- Generated and deterministic responsibilities are separated.
- Exact preservation constraints are named.
- The prompt contains concrete visual decisions rather than style-word accumulation.
