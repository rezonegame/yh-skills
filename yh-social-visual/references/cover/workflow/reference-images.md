# Cover Reference Images

Use supplied images only when they improve identity, continuity, composition, or art direction. Treat them as inputs to the runtime-native image generation workflow, not as provider-specific parameters.

## Assign Roles

Give every reference one primary role:

| Role | Preserve | May change |
| --- | --- | --- |
| Identity | person, product, object, place | background, crop, lighting |
| Style | palette, medium, texture, lighting | subject and composition |
| Composition | hierarchy, framing, negative space | subject and style |
| Continuity | recurring motifs and series language | scene-specific content |

If one image must serve several roles, state the priority order explicitly.

## Write the Instruction

Use direct language:

```text
Use the supplied portrait as the identity reference: preserve facial identity, hairstyle, and glasses.
Use the supplied poster only as a composition reference: preserve the large quiet upper field and bottom title zone, not its subject or typography.
```

Avoid vague instructions such as “make it like this.” Avoid asking the model to copy protected branding, signatures, or a living artist's exact style.

## Cover-Specific Rules

- Preserve required logos and exact product features through deterministic composition when native rendering may distort them.
- Reserve text-safe space according to the target platform crop.
- For hybrid covers, generate the clean hero visual first and add exact typography in HTML.
- Record every preservation constraint and source path in `manifest.json` or `brief.md`.

## Failure Handling

If runtime-native generation is unavailable, keep the completed prompt and reference-role notes, mark the asset `failed`, and report the pending work. Do not silently switch to external APIs, command-line providers, or legacy backends.
