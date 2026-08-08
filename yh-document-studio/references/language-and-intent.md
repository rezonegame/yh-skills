本文件包含语言判定、意图抽取和美学选择的完整规则。SKILL.md 中只保留简要指针。

---

## Step 1 · Decide the language

**Match the user's language.** Chinese -> `*.html` / `slides-weasy.html`. English -> `*-en.html` / `slides-weasy-en.html`. Japanese -> CJK path (`.html` / `slides-weasy.html`) as best-effort, JP Mincho first, visual QA before shipping. Korean -> dedicated `*-ko.html` / `slides-weasy-ko.html` family as best-effort, visual QA before shipping. Reference docs are shared English specs.

When ambiguous (e.g. a one-word command like "resume"), ask a one-liner rather than guess.

| User language | HTML templates | Slides (PDF default) | Slides (PPTX fallback) |
|---|---|---|---|
| Chinese (primary) | `*.html` | `slides-weasy.html` | `slides.py` |
| English | `*-en.html` | `slides-weasy-en.html` | `slides-en.py` |
| Japanese (best-effort) | `*.html` | `slides-weasy.html` | `slides.py` |
| Korean (best-effort) | `*-ko.html` | `slides-weasy-ko.html` | n/a (use `slides-en.py` only if PPTX is required) |
| Other languages (best-effort) | choose CJK or EN path by script coverage, then verify manually | choose `slides-weasy.html` or `slides-weasy-en.html`, then verify manually | use `slides.py` / `slides-en.py` only if PPTX is required |

> Default to the WeasyPrint HTML path; fall back to PPTX (`slides*.py`) only when the user explicitly needs an editable deck.

Always use `CHEATSHEET.md` and `references/*.md` for design, writing, production, and diagram guidance.

Code blocks with `class="language-*"` are highlighted only when optional `Pygments` is installed in the build environment. Without it, PDFs still render and code blocks stay monochrome.

---

## Step 1.5 · Intent extraction (silent checklist)

Before choosing a template, verify these four dimensions are clear. Do not ask unless 2+ are missing and cannot be inferred from context.

| Dimension | What to extract | Example |
|---|---|---|
| **Purpose** | Why this document exists | Persuade investor vs. align internal team vs. close a candidate |
| **Audience** | Who reads it, what they already know | Technical CTO (skip basics) vs. non-technical board (explain terms) |
| **Constraint** | Hard limits on length, format, tone, or delivery | "One page max", "formal English", "print-ready A4" |
| **Success** | What outcome counts as success | They schedule a meeting / they approve the budget / they understand the architecture |

Rules:
- If the conversation already answered a dimension, skip it silently.
- If a dimension can be inferred from the document type (e.g. resume purpose is always "get an interview"), skip it.
- If 2+ dimensions are genuinely unclear, ask in a single compact question (max 2 sub-questions).
- Never ask all four as a checklist. This is a background verification, not a form.

---

## Step 1.6 · Pick the aesthetic (yh-document-studio 新增)

在意图抽取后、选模板前，确定美学包。这是 yh-document-studio 相对 kami 的核心新增能力。

### 5 套美学包

| # | 名称 | 调性 | 适用 | 色源 |
|---|------|------|------|------|
| 1 | `parchment-ink` | 温暖纸面 + 墨蓝 + 衬线（**默认 = 原 kami**） | 编辑/出版/正式文档 | kami 原 tokens |
| 2 | `minimal-mono` | 极简黑白灰（"简单版/裸文"） | 内部备忘、纯文本感、屏幕阅读 | theme-factory modern-minimalist |
| 3 | `business-cool` | 灰蓝商务冷调 | 报表、研报、估值、商业文档 | theme-factory ocean-depths 调整 |
| 4 | `editorial-warm` | 赭石棕暖调社论 | 随笔、杂志调、品牌叙事、年度总结 | theme-factory golden-hour |
| 5 | `natural-essay` | 森林绿鼠尾草自然调 | 可持续/健康/环保/教育类长文 | theme-factory forest-canopy |

> 所有美学包共用 kami 同级字体（CN: TsangerJinKai02，EN: Charter，JA: YuMincho），不用 theme-factory 的廉价系统字体。

### 选择规则

- **用户明确指定** → 直接用（如"用商务风""换个简单版""极简黑白"）。
- **未指定但内容调性明显** → 推荐最匹配的一套并说明理由，等用户确认：
  - "商业报告/研报/估值/财务" → 推荐 `business-cool`
  - "随笔/杂志/品牌故事/年度总结" → 推荐 `editorial-warm`
  - "环保/健康/可持续/教育" → 推荐 `natural-essay`
  - "简单版/裸文/纯文本感/内部备忘" → 推荐 `minimal-mono`
  - 正式编辑/出版/无特殊调性 → `parchment-ink`（默认）
- **完全无信号** → 默认 `parchment-ink`（= 原 kami），不问。

### 避免 AI slop（借鉴 frontend-design）

选/调美学时避开：Inter/Roboto/Arial 等通用字体、紫色渐变白底、千篇一律的圆角和居中布局、霓虹饱和色（如 `tech-innovation` 风的纯青）。美学要有调性、有意图。

### 如何应用美学

美学切换通过 `scripts/inject-override.py` 在产物 HTML 的 `</head>` 前注入对应 `assets/themes/<name>.css` 实现（覆盖 `:root` + `@page` 背景），**不修改 kami 模板原文件**。具体在 Step 4.x 导出档位时一并执行。
