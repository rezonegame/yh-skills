# Offline Upgrade Policy

## Non-Negotiables

- Preserve `yh-slides` strong guidance: Step 0 intent panel, route codes, collaboration level, checkpointing, recommended options, alternatives, custom entry, and risk notes.
- Vendor assets are resources, not a replacement workflow.
- Offline core must work without GitHub, CDNs, remote skill installation, or remote slide runtimes.
- Online AI image generation, web research, and cloud TTS are enhancements only.

## What May Be Absorbed

- Template files, seed decks, CSS themes, layouts, runtime JS, animation JS, validators, chart/icon libraries, and minimal scripts needed for local execution.
- Upstream docs needed to use those assets safely.
- Smoke fixtures for local validation.

## What Should Not Be Vendored Into Main Workflow Text

- Whole README marketing sections.
- Large generated exports or screenshots not needed by templates.
- Upstream installation instructions that conflict with local offline mode.
- Any code without license/provenance.

## Update Process

1. Create a backup under `backups/pre-offline-upgrade-<timestamp>/`.
2. Update pinned vendor checkout deliberately.
3. Copy or retain license files.
4. Patch runtime assets to local fonts/scripts.
5. Rebuild `asset-registry.json`.
6. Run integrity and offline checks.
7. Update `upstreams.md` and evolution notes.
