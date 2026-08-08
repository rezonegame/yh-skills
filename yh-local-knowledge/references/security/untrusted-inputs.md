# Untrusted Input Profile

Use `--untrusted` for files received from outside the workspace or whose origin is uncertain. Trusted local files keep the normal conversion path; untrusted files must pass structural checks before any converter runs.

## Trust levels

| Level | Typical source | Handling |
|---|---|---|
| `trusted-local` | A local path the user explicitly identifies and trusts | Normal local conversion |
| `local-untrusted` | Downloads, attachments, dragged files, or unknown-origin archives | Bounded structural scan, then conversion only if accepted |
| `remote` | URL or network path | Do not fetch in this skill; require an explicitly authorized access workflow first |

## Structural rejection rules

- Reject symlinks whose resolved target escapes the declared source root.
- Reject remote-looking paths and network protocols.
- For ZIP-based containers (`.zip`, `.docx`, `.pptx`, `.xlsx`, `.epub`), enforce nesting depth, member count, member size, compression ratio, and total uncompressed-size limits.
- Default archive ceilings are depth 3, 500 members, 100 MB per member, and 500 MB total uncompressed data. Lower them for constrained environments.
- Do not execute PDF JavaScript, Office macros, ActiveX, OLE payloads, or embedded executables. Unsupported embedded content is skipped and recorded.
- Do not trust image metadata; strip or ignore sensitive EXIF fields in downstream export when relevant.

Run:

```powershell
python scripts/normalize.py <workspace> --source-root inbox --untrusted
```

Rejected files appear as `rejected_untrusted_input` records and are never sent to a converter or written into the normalized cache. A rejection record should preserve the source hash when readable, converter=`none`, status, and a bounded error message without echoing attacker-controlled content.

## Cache and output safety

- A failed conversion must never replace a valid cached output.
- Reuse normalized output only when the source hash and converter environment still match.
- Write normalized text atomically and strip invisible Unicode controls.
- Keep raw inputs immutable; version trusted assets instead of overwriting them.

## Content safety after normalization

Run the advisory content scan:

```powershell
python scripts/scan_content_safety.py <workspace>/.knowledge/normalized
```

The scan flags known English/Chinese instruction-override and exfiltration-shaped language without echoing the source text. A clean scan is not a trust decision: visible paraphrases and domain-specific attacks can still pass. Keep findings and unreviewed normalized content out of trusted assets and generated skill packs until a human reviews them.

Maintainers can regenerate the bounded adversarial archive fixtures with `python scripts/create_fixtures.py`; never run those fixtures through an unsafe extractor.
