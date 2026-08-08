# Style Profile Contract

An optional personal style profile is a JSON file outside the skill directory.
Load it only when `YH_SLIDES_STYLE_PROFILE` explicitly names an absolute file.
It records user-confirmed `palette`, `typography`, `density`, and
`preferred_route`; it cannot carry secrets, model/provider fields, scripts, or
project-specific requirements. Explicit instructions in the current project
always win.

```powershell
python scripts/validate_style_profile.py C:\private\slides-style.json --explicit-route 2A
```
