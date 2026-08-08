# Asset Intent Contract

Before a final project image is generated or edited, optionally create
`asset-intent.json`. It makes the operation, destination, and preservation
constraints explicit without changing image-provider routing.

`generate` needs a safe destination and non-destructive filename. `edit` also
needs input references and immutable constraints. Validate with:

```powershell
python scripts/validate_asset_intent.py asset-intent.json --project-root <dir>
```
