# Intake Guidance

Use a non-blocking preflight note when a request is actionable but leaves a material production choice unstated.

## Decision Rule

Proceed with an explicit assumption when a safe, reversible default exists. Ask first only when the missing choice would make the deliverable unusable, overwrite work, or violate a preservation constraint.

Material inferred choices include platform or ratio, mode, rendering strategy, exact-text requirements, and whether the request includes adaptation or only visual support. Do not announce trivial defaults.

## Preflight Format

Keep the note concise and place it before task initialization or image generation:

```text
执行说明：我先按 [mode] 处理，因为 [evidence]。
未指定 [material choice]，暂按 [default] 制作；这是执行默认值，不代表已确认目标平台。本次只做 [scope]，不扩展 [excluded scope]。
如果目标是 [alternative A] 或 [alternative B]，构图或比例会不同；我先继续当前方案，你可以随时切换。
```

Use only informative lines. Usually two or three are enough.

## Existing Long Article

```text
执行说明：我先按 article 模式制作封面和正文插图，不改编文章内容。
你没有指定发布平台，我暂按通用长文、兼容微信公众号的规格处理；这不是对目标平台的确认。本次不扩展小红书、微博或短视频封面。
如果实际发布到小红书或知乎，构图方案会不同；我先继续当前方案。
```

## Illustration-specific Guidance

- If an exact image count is requested but strong anchors are insufficient, state which concepts are core and which are optional weak candidates. Do not silently add filler.
- A project retrospective, growth story, or product evolution does not automatically create a `story-scroll`. Briefly suggest it only when it would materially help; create it only after an explicit request.
- If names, dates, quantities, achievements, or experience facts are missing, state that they will be omitted, abstracted, or left pending.
- Exact titles, labels, numbers, dates, and logos should prompt an HTML or hybrid recommendation.
- Image-led abstract or emotional arguments with no exact text normally route to native; do not suggest HTML merely because a cover exists.

## Scope Guard

Distinguish:

- **Known**: explicitly stated by the user or stored preference.
- **Inferred**: selected from context and announced before execution.
- **Excluded**: outside the current request and not generated automatically.

Record inferred platform, strategy, candidate strength, and excluded scope in `brief.md` so a resumed task preserves the assumptions.
