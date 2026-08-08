# Fonts Reference

> 本文件包含字体配置的完整规则。SKILL.md 中只保留简要指针。

## Chinese
- Main serif: TsangerJinKai02-W04.ttf (400 weight) + TsangerJinKai02-W05.ttf (500 weight, real bold)
- Templates use dual @font-face declarations: W04 for body text, W05 for headings
- Both files are commercial fonts. Keep them available in the repository for local preview and CDN fallback, but do not bundle them inside Claude Desktop skill ZIPs
- Fallback chain baked into templates: Source Han Serif SC -> Noto Serif CJK SC -> Songti SC -> STSong -> Georgia

## Japanese (best-effort)
- Uses CJK template path, no dedicated `-ja` templates yet
- JP Mincho-first stack: YuMincho -> Hiragino Mincho ProN -> Noto Serif CJK JP -> Source Han Serif JP -> TsangerJinKai02 -> serif
- Visually verify line breaks, punctuation rhythm, and emphasis weight before shipping

## Korean (best-effort)
- Dedicated `-ko` templates use Source Han Serif K Regular / Medium, with the real OTF family name `Source Han Serif KR` kept in every fallback stack
- Fallback: Noto Serif KR / Apple SD Gothic Neo / AppleMyungjo / Charter / Georgia
- The OTFs are OFL-licensed and tracked for local preview / CDN fallback, but excluded from Claude Desktop skill ZIPs to keep the package small

## English
- Single serif: Charter (system-bundled, macOS/iOS), used for both headlines and body
- No separate sans: `--sans: var(--serif)`, one font per page
- Fallback: Georgia (cross-platform) / Palatino / Times New Roman

## Font file placement

Font files next to HTML with relative `@font-face` paths is the most stable setup. `scripts/package-skill.sh` excludes large CJK font files from the Claude Desktop ZIP, so the uploaded package stays under the 6MB package ceiling. Always upload that `package-skill.sh` output, never a hand-zipped checkout (the tracked CJK fonts make it too large and Claude Desktop rejects the upload).

## Font auto-recovery (Claude Desktop)

Before building Chinese or Korean documents, ensure fonts are present. The script tries multiple CDN sources with retry and size validation:

```bash
bash scripts/ensure-fonts.sh
```

It downloads to the XDG user font dir (`${XDG_DATA_HOME:-~/.local/share}/fonts/kami`, override with `KAMI_FONT_DIR`), **not** into the skill's `assets/fonts` -- that keeps the installed skill small so Claude Desktop never trips its size limit. fontconfig scans that dir by default, so WeasyPrint finds `TsangerJinKai02` and `Source Han Serif K` there; online renders fall back to the jsDelivr `@font-face` URL. Run once before building. If all sources fail, the script prints per-language alternatives.
