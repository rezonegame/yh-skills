# Adoption Decisions

## C. Untrusted Input Profile
- Source: microsoft/markitdown
- Source URL: https://github.com/microsoft/markitdown
- License: MIT
- Material adopted: input trust levels, rejection rules, archive limits, cache safety
- Material excluded: remote conversion, visual-fidelity claims
- Test: scripts/scan_input_policy.py + 4 adversarial fixtures
- Rollback: delete references/security/, scripts/scan_input_policy.py, fixtures/security/, and the untrusted input section in SKILL.md
- Date: 2026-07-28
