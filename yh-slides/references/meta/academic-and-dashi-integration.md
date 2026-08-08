# Academic PPTX and Dashi Integration Audit

Audit date: 2026-07-31.

Pinned sources:

- `Gabberflast/academic-pptx-skill` at
  `9f2b703ffe8d1449851617665ab1ffb3516d54ac`.
- `chuspeeism/dashi-ppt-skill` at
  `7cb23347f91cda1a5519eafc8c040704e389535a` (v0.4.11).

## Capability comparison

| Area | Existing `yh-slides` | Academic source | Dashi source | Integration decision |
|---|---|---|---|---|
| Output | PPTX, image PPTX, hybrid, HTML, presenter and React paths | Defers file creation to another PPTX skill | Browser editor with HTML/PDF/PPTX export | Keep all `yh-slides` paths; absorb no new runtime |
| Intake | Strong Step 0 intent, route and collaboration choices | Academic context detection | Theme/media confirmation and acceptance list | Keep Step 0; add academic mode and acceptance framing |
| Narrative | Action titles, one idea per page, ghost-deck principle | SCR/funnel/answer-first, one argument, early research question | Canonical page content before layout | Add explicit academic spine and freeze facts before layout |
| Evidence | Chart insight and basic borrowed-figure sources | On-slide citation for claims/data/figures, one exhibit per result, references | Recompute insight after data change | Expand the academic contract and validator |
| Architecture | Flexible page archetypes and path-neutral deck plan | Research question, lean methods, result sequence, conclusion, Q&A appendix | Role/priority-driven page briefs | Add academic architecture without making it global |
| Layout selection | Asset registry, template mining, uniqueness checks | Communication-first academic patterns | Capacity-aware candidate layouts and structural families | Add candidate discipline; retain local templates and sample checkpoint |
| Visual style | Broad user-selectable style system | Restrained academic defaults | Twelve bundled themes | Keep user/brand choice; academic defaults are overridable; do not import themes |
| QA | P0–P3, visual screenshots, offline and integrity gates | Ghost deck, legibility, citations, timing | Goal/copy/variant checks and template-copy leakage | Add academic v2 tests and provenance gates |

## Absorbed from the academic source

- `structured_argument` and `visual_narrative` academic modes;
- SCR, funnel-answer and answer-first narrative spines;
- explicit main claim and early research question;
- one exhibit, insight and annotation per results page;
- citations for non-original claims, data and figures;
- conclusion as the last argumentative page, references before appendix;
- timing ceiling, skippable pages and prebuilt Q&A appendix;
- high contrast, color-independent encoding, acronym and body-size checks;
- semantic academic slide patterns expressed independently of PptxGenJS.

## Absorbed from Dashi at method level

- freeze one canonical page content package before layout choice;
- select layouts by content capacity and media needs;
- compare structurally different layout families;
- keep facts stable across layout/style alternatives;
- prevent template demo copy from leaking into delivery;
- update chart interpretation whenever data changes;
- use acceptance criteria before rendering and route-specific QA afterward.

## Explicitly not absorbed

- Dashi's theme packages, 1020 layouts, editor runtime, generators, installer,
  export service and proprietary export component;
- its automatic version check, local preview protocol and schema/runtime;
- the academic source's PptxGenJS snippets and PDF guide;
- any rule that would replace `yh-slides` Step 0, product paths, brand priority,
  checkpoints, asset registry or visual QA.

## License boundary

The academic repository root contains an MIT license, while its `SKILL.md`
frontmatter still says “Proprietary” and points to a non-existent
`LICENSE.txt`. Because those declarations conflict, this integration uses an
independent method-level rewrite and copies no code or PDF content. The root MIT
license is retained in `assets/external-licenses/` for provenance.

Dashi is AGPL-3.0 and its current export component has an additional proprietary
restriction. This integration copies no Dashi code, templates, themes, assets or
runtime. Only general workflow ideas were independently restated. The boundary
is recorded in `assets/external-licenses/dashi-ppt-skill-AGPL-3.0-method-only.md`.
