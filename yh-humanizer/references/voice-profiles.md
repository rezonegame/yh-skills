# Optional Voice Profiles

Use a voice profile only when the user selects it or explicitly asks for a calibrated tone. If the user supplies representative writing samples or asks to write "like me", prefer `yh-style-profiler`; personal evidence is more reliable than a generic preset.

Profiles change cadence, diction, and paragraph rhythm. They never change facts, citations, quoted text, narrator identity, or lived experience.

## Selection rules

1. User samples or an existing personal profile → use `yh-style-profiler`.
2. User explicitly names a profile → use that profile.
3. User asks for a broad tone but provides no samples → recommend one profile and state the tradeoff.
4. No tone request → use `neutral`; do not silently impose a strong voice.

## Profiles

| Profile | Cadence and diction | Suitable for | Avoid for |
|---|---|---|---|
| `neutral` | Standard written Chinese, varied medium-length sentences | general editing | work needing a strong personal voice |
| `conversational` | Shorter sentences, restrained spoken phrasing | blogs, public-account drafts, explainers | legal, academic, or formal reporting |
| `editorial` | Long-short alternation, precise judgment, controlled imagery | columns, criticism, reflective reviews | simple instructions or urgent notices |
| `technical` | Explicit definitions and logic, minimal rhetoric | product, engineering, API, tutorials | narrative or intimate memoir |
| `narrative` | Concrete scenes, temporal movement, sensory detail already supported by the source | features, travel, memoir drafts | analysis or technical documentation |
| `crisp-business` | Compact claims, explicit implications, restrained tone | internal analysis and memos | intimate or literary writing |

Legacy aliases remain valid: `quiet-editorial` → `editorial`, `plain-technical` → `technical`, `warm-column` → `conversational`, and `curated-reading` → `editorial` with the curated-intellectualism guide.

## Factual invariants

- Preserve every name, organization, brand, number, date, percentage, amount, URL, citation, and direct quotation.
- Preserve first-person boundaries. A profile cannot introduce "我" or an experience absent from the source.
- Do not infer motives, emotions, relationships, or chronology merely to make prose feel vivid.
- If a requested profile conflicts with the document type, say so and recommend a safer profile.

## Verification

After editing, check that cadence and diction match the selected profile and that all factual invariants remain intact. Run `python scripts/validate_voice_profile_cases.py` when maintaining this reference; use `python scripts/validate_factuality_cases.py` for narrator and fact regressions.
