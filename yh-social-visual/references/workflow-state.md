# Workflow State

Use `manifest.json` as the resumable source of truth. Keep `brief.md` human-readable and the manifest machine-readable.

## Asset States

| State | Meaning |
| --- | --- |
| `planned` | The asset exists in the package plan but no production work has started. |
| `awaiting-generation` | A native prompt is ready and the raster has not been generated. |
| `generated` | A native raster exists in the task directory. |
| `awaiting-composition` | Source visuals exist but HTML composition is incomplete. |
| `rendered` | A final-size output exists but has not passed validation. |
| `validated` | The final output passed required checks. |
| `failed` | Production failed; preserve the prompt, error summary, and retry context. |

Move forward through the states. Move backward only when the source, copy, layout, or platform target changes.

## Manifest Shape

```json
{
  "schema_version": 1,
  "title": "Example topic",
  "mode": "package",
  "platforms": ["xiaohongshu"],
  "render_strategy": "auto",
  "created_at": "2026-06-19T00:00:00.000Z",
  "updated_at": "2026-06-19T00:00:00.000Z",
  "assets": [
    {
      "id": "xiaohongshu-01-cover",
      "platform": "xiaohongshu",
      "role": "cover",
      "strategy": "html",
      "state": "planned",
      "prompt": null,
      "source": null,
      "html": "html/index.html",
      "output": "output/xiaohongshu-01-cover.png",
      "error": null
    }
  ]
}
```

Use task-relative paths so the task directory remains portable.

## Story-scroll Role

`story-scroll` is an asset role inside `article` mode, not a new mode or schema version. Its default strategy is `hybrid`, size is `2400×900`, and output is `output/article-story-scroll.png`. Use the standard state sequence:

```text
planned → awaiting-generation → generated → awaiting-composition → rendered → validated
```

Do not advance the asset to `awaiting-composition` until the native base has been viewed and its actual nodes, route, balance, and text-safe regions have been accepted. Store the reviewed base in `sources/`; record normalized node coordinates and fact sources in `brief.md` and HTML attributes.

## Resume Rules

1. Read the manifest before touching task files.
2. Verify that every recorded source, HTML, prompt, and output path exists when its state implies existence.
3. Resume the earliest incomplete state rather than rebuilding completed work.
4. Preserve existing final files by default. Create a versioned sibling unless replacement was explicitly requested.
5. Mark an asset `failed` with a concise error instead of deleting its context.
6. Finish only when every requested asset is `validated` or explicitly reported as `failed`.

Use `scripts/set-asset-state.mjs` to update one asset safely.
