# Academic Deck Contract v2

Use this optional, path-neutral contract for research talks, seminars, thesis
defences, grant briefings, lab meetings, invited lectures, policy briefings and
evidence-led public engagement. It complements `deck-plan.json`; it does not
replace the normal `yh-slides` intent, route, brand, build or visual QA gates.

```powershell
python scripts/validate_academic_deck.py academic-deck.json --deck-plan deck-plan.json
```

New academic projects should use `schema: "yh_slides_academic_deck.v2"`.
Schema-less files remain accepted as the earlier lightweight contract so old
projects do not break.

## Top-level fields

| Field | Rule |
|---|---|
| `schema` | `yh_slides_academic_deck.v2` |
| `mode` | `structured_argument` or `visual_narrative` |
| `talk_type` | Conference, seminar, defence, grant, lab, lecture, policy or public-engagement enum used by the validator |
| `talk_minutes` | Positive number; live slide count may not exceed one slide per minute |
| `narrative_spine` | `scr`, `funnel_answer` or `answer_first` |
| `main_claim` | The one claim the audience should remember |
| `research_question` | Required in `structured_argument` mode |
| `accessibility` | `high_contrast`, `color_independent` and `acronyms_defined` must all be `true` |
| `pages` | Ordered page list; IDs must match `deck-plan.json` when cross-validated |

`structured_argument` is the default recommendation for conference, seminar,
defence, grant, lab and policy settings. `visual_narrative` is for public
engagement or keynote-like academic communication; it relaxes the dedicated
research-question page, not evidence or citation discipline.

## Page contract

Every substantive page (`context`, `research_question`, `methods`, `results`,
`discussion`, `implications`, `conclusions`, `appendix`) needs:

- `id`, `role`, a complete action `title`, `purpose`, and `audience_move`;
- one job and one audience move;
- optional `body_word_count` no higher than 40 and `body_font_pt` at least 20;
- optional `estimated_seconds` and `skippable` for rehearsal planning.

The ordered action titles are the ghost deck: they must read as a coherent
argument, not topic labels such as “Background”, “Methods” or “Results”.

A `results` page additionally needs exactly one primary `exhibits` entry, a
concrete `insight`, and a visible `annotation` that states the “so what”. Rebuild
paper figures when practical so labels, hierarchy and emphasis fit the talk;
do not copy a dense paper figure merely because it already exists.

## Evidence and citations

Use `evidence` when a page contains a claim, data point, figure, quotation or
other evidence:

```json
{
  "kind": "data",
  "original": false,
  "citation": "Lee et al., 2025"
}
```

Every item with `original: false` requires an in-slide `citation`. Legacy
`borrowed_figure`, `borrowed_claim` and `borrowed_data` flags require non-empty
`sources`. Any sourced deck must contain one `references` page. References come
after the argumentative conclusion and before any appendix.

The deck author remains responsible for rights, permissions and the accuracy of
citations. A citation is not a substitute for permission when permission is
required.

## Required argument ending

- `structured_argument` contains exactly one `research_question` page within
  the first three substantive pages.
- Academic v2 contains exactly one `conclusions` page. It is the last
  argumentative page and directly answers the research question or main claim.
- After conclusions, only contact/next-step, references and appendix pages may
  follow.
- Appendix pages form one final contiguous block and use action titles too.
- Do not end with a blank, generic “Thank You” or generic “Q&A” slide. Put
  contact or a QR code on a useful conclusion/contact screen instead.

## Minimal example

```json
{
  "schema": "yh_slides_academic_deck.v2",
  "mode": "structured_argument",
  "talk_type": "conference",
  "talk_minutes": 12,
  "narrative_spine": "scr",
  "main_claim": "A short intervention improves retention.",
  "research_question": "Does the intervention improve week-two retention?",
  "accessibility": {
    "high_contrast": true,
    "color_independent": true,
    "acronyms_defined": true
  },
  "pages": [
    {"id": "cover", "role": "cover"},
    {
      "id": "question",
      "role": "research_question",
      "title": "We test whether a ten-minute intervention improves retention.",
      "purpose": "State the test",
      "audience_move": "Understand the research question"
    },
    {
      "id": "finding",
      "role": "results",
      "title": "The intervention improved retention by 18 percentage points.",
      "purpose": "Show the primary result",
      "audience_move": "Trust the effect",
      "exhibits": ["retention chart"],
      "insight": "The effect survives cohort adjustment.",
      "annotation": "+18 pp after adjustment",
      "evidence": [{"kind": "data", "original": true}]
    },
    {
      "id": "conclusion",
      "role": "conclusions",
      "title": "A ten-minute intervention is a low-cost retention tool.",
      "purpose": "Answer the research question",
      "audience_move": "Adopt the intervention"
    }
  ]
}
```

For narrative patterns, timing, Q&A planning and academic visual defaults, read
`references/getting-started/academic-presentation-workflow.md`.
