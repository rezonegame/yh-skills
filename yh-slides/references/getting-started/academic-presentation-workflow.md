# Academic Presentation Workflow

This is an academic communication layer, not a new output path. Run normal
`yh-slides` Step 0 and choose any suitable PPTX/HTML route; then use this
workflow for content, evidence and rehearsal decisions.

## 1. Choose the communication mode

- `structured_argument` — default for conferences, seminars, thesis defences,
  grants, lab meetings and policy briefings. Priority: argument, evidence,
  layout, then aesthetics.
- `visual_narrative` — public engagement, science communication and
  keynote-like talks. It may use a looser scene sequence, but claims and
  borrowed evidence still need citations.

The user-selected institutional template, brand system or visual direction can
override the academic visual defaults. It cannot override evidence accuracy,
legibility or citation requirements.

## 2. Freeze the argument before choosing layouts

Write one sentence for each:

1. audience decision or belief change;
2. research question;
3. one main claim;
4. strongest evidence;
5. limitation or boundary;
6. final implication.

Then choose one narrative spine:

- `scr`: situation → complication → resolution;
- `funnel_answer`: broad context → gap → question → answer;
- `answer_first`: answer → evidence → implications, for senior or
  time-pressured audiences.

For every page, freeze one canonical content package before layout selection:
action title, purpose, audience move, required facts, key numbers and source
citations. Alternative layouts may shorten, reorder or re-emphasize that
package; they must not invent a different story. See
`references/aesthetics/content-layout-candidates.md`.

## 3. Build the academic architecture

A common structure is:

1. cover;
2. motivation/context (one or two pages);
3. dedicated research question by the third substantive page;
4. evaluator-needed methods only;
5. results, one finding and one exhibit per page;
6. discussion, limitations and implications;
7. conclusions that answer the question;
8. useful contact/next step when needed;
9. references;
10. appendix with three to five likely Q&A answers.

One argument per deck and one job per page. Move supporting analyses that do not
advance the live argument to the appendix. For talks longer than about 15
slides, use section dividers or a restrained breadcrumb.

## 4. Apply evidence discipline

- Cite each non-original claim, data point, figure or quotation on the page
  where it appears.
- Put the complete source list on the references page before the appendix.
- Prefer a chart to a table for trends; use a table when exact lookup matters.
- Rebuild dense paper figures when practical. A talk figure needs readable
  labels, a visible finding annotation and only the elements discussed aloud.
- Results pages use one primary exhibit and explicitly state the implication.
- When chart data changes, rewrite the title, annotation and insight from the
  new data; never retain a template conclusion.

## 5. Use communication-first visual defaults

These are defaults, not a mandatory global theme:

- 16:9 canvas, generous margins and high contrast;
- one primary sans-serif family and no more than three functional colors;
- title about 24–28 pt, body at least 20 pt, chart labels about 16–18 pt,
  citations about 12–14 pt;
- no decorative icon or effect without a communication job;
- results often work best as exhibit left, interpretation right;
- do not rely on color alone; define acronyms and use direct language.

The `yh-slides` visual system may choose a different typography scale or
composition when the route or template requires it, but the final render must
preserve legibility and hierarchy.

## 6. Budget and rehearse

- Plan no more than one live slide per minute. Typical targets: 8–10 slides for
  10 minutes, 12–14 for 15 minutes, 15–18 for 20 minutes.
- Assign `estimated_seconds` and mark genuinely removable pages `skippable`.
- Rehearse to finish one or two minutes early.
- Prepare three to five appendix slides for likely methodological, robustness
  or interpretation questions.

## 7. Run the academic gates

1. Read only the action titles: do they form a complete argument?
2. Inspect every results page: one exhibit, one finding, one annotation?
3. Inspect every borrowed item: on-slide citation and full reference?
4. Inspect the ending: useful conclusion/contact screen, not generic thanks?
5. Validate `academic-deck.json` and cross-check the page order with
   `deck-plan.json`.
6. Continue with the normal route-specific build, render and P0/P1 visual QA.
