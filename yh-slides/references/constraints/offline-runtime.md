# Offline Runtime Rules

## Fully Offline Core

These paths must run without network access, assuming local Python/Node dependencies are installed:

- `2A / Path A`: constrained HTML to editable PPTX.
- `2A-S / Path S`: SVG to native editable PPTX.
- `2A-T / Template Fill`: local PPTX template analysis/fill through absorbed scripts and dependencies.
- `2B-R / FigEdit Reconstruction`: local independent FigEdit skill plus installed OCR/CV/PPTX dependencies; no cloud API is required.
- `2D / Path C`: local HTML magazine/Swiss/minimal decks.
- `2D-P / Presenter Mode`: local HTML presenter window with notes.
- QA scripts: class preflight, Swiss validation, visual QA where a local browser is available, SVG/PPTX checks.

## Online Enhancements

These may use the network but cannot be hard requirements:

- AI image generation.
- Web fact checking and source research.
- Cloud TTS.
- Upstream vendor sync.
- External stock-image search.

## Required Fallbacks

- Image generation unavailable: use user assets, local placeholders, or mark `待替换素材`; do not invent visual facts.
- Web research unavailable: mark `待核查数据`; do not promote placeholders into facts.
- Cloud TTS unavailable: keep notes/presenter script and skip audio export.
- CDN unavailable: all HTML must continue with local fonts and JS.

## Check Command

Run before treating the skill as offline-ready:

```bash
python scripts/check_offline_ready.py
```

After absorbing or changing local assets, also run:

```bash
python scripts/build_asset_registry.py
python scripts/check_upstream_locks.py
python scripts/check_yh_slides_integrity.py
python scripts/skill_creator_self_audit.py
```
