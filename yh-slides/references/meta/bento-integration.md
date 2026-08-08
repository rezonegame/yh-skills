# Bento Integration Decision Record

## Decision

Add Bento as `2D-B / Bento Deck`, an optional adapter inside the existing 2D
family. It is not a default path and does not rename or supersede Path C/D/E.

## Complementarity

| `yh-slides` retains | Bento contributes |
|---|---|
| Intent, route selection, narrative, visual direction, provenance and QA | Browser-native editable slide document/player |
| PPTX, academic and reconstruction routes | Stable object IDs, state variants, morph, notes and comments |
| Local asset strategy and screenshot quality gate | One self-contained `.bento.html` review/editing artifact |

## Controlled scope

The local shell is a release artifact acquired 2026-08-01 and pinned in
`provenance/upstream-locks/bento.source.json`. Its Cloudflare Insights beacon
was removed before vendoring so the default artifact remains offline. The
adapter does not include Bento's network collaboration workflow, hosted update
path, template gallery, or automatic runtime update behavior.

## Refresh checklist

1. Review upstream commit, release artifact, format compatibility and MIT/
   third-party notices.
2. Scan the candidate shell for remote runtime, analytics and telemetry.
3. Remove nonessential telemetry only if the license and notice obligations
   remain satisfied; record original and patched hashes.
4. Update the source lock, registry, contract, tests and integrity checks.
5. Run offline, generator, validator and full skill self-audits.
