# Release gate

`python scripts/release_gate.py <manifest.json>` is the final private-release gate. The manifest must bind one `yh-document-studio` version to the current Git SHA, an exact package SHA-256, required archive members, required source files, and non-empty validation evidence files.

The gate is intentionally fail-closed. A render or validation candidate is written beside the final artifact and promoted with an atomic replace only after all deterministic checks pass. A failed candidate is removed; the last successful PDF or PPTX remains untouched.

Minimal manifest shape:

```json
{
  "identity": {"name": "yh-document-studio", "version": "2026.08.08", "git_sha": "<40-hex>"},
  "package": {"path": "dist/kami.zip", "sha256": "<64-hex>", "required_members": ["SKILL.md"]},
  "required_files": ["SKILL.md", "scripts/release_gate.py"],
  "validation_evidence": ["artifacts/release-validation.txt"]
}
```
