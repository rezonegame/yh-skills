# YH Skills Provenance

`yh-source-locks.json` is the shared, machine-readable source register for the six maintained `yh-*` skills.

- `absorbed_commit` identifies an upstream revision whose code or assets were copied into a skill.
- `reviewed_commit` identifies the revision reviewed for a method-only reference or a potential upgrade.
- `baseline_commit_status` records when a historic copied baseline cannot be reconstructed from the original import record. It is a release-review finding, not permission to claim a lock that does not exist.
- `distribution` distinguishes local/private use from material eligible for public redistribution.

Update this file whenever an upstream is re-reviewed or any source material is absorbed. Run `python scripts/validate_yh_skills.py --provenance` before a release.
