# 图片后端选择策略

`yh-slides` 使用 **auto-runtime** 作为默认生图策略：优先使用当前 agent/runtime 暴露的原生图片能力；如果没有原生图片工具、原生工具无法稳定落盘，或用户显式要求 API 后端，才退到脚本化的 Gemini / Imagen 后端。

---

## 核心结论

- **运行时原生图片能力不是 API key**。Codex Image2 等 agent-native backend 属于当前 runtime 暴露的工具能力，不能被 `scripts/generate_image.py` 当作普通 HTTP API 调用。
- **Gemini / Imagen 是脚本后端**。只要配置 `GEMINI_API_KEY`，就可以在任意 CLI、容器、自动化任务中通过 `generate_image.py` 批量生成、重试、断点续传。
- **默认推荐：原生优先，API 兜底**。在任何 CLI / agent 环境中，只要存在可用的原生生图工具，就优先使用原生工具；只有用户明确指定 API、原生工具不可用、无法稳定落盘或原生工具明确失败时，才使用运行环境变量或显式 `YH_SKILLS_ENV_FILE` 中的 API key 调用 Gemini / Imagen。

---

## 后端类型

| 类型 | 代表 | 调用方式 | 适合 |
|---|---|---|---|
| agent-native backend | Codex Image2 / `image_gen` | 由当前 agent 直接调用原生生图工具 | 交互式高质量图、封面、关键页、少量精品图 |
| script/API backend | Gemini / Imagen | `scripts/generate_image.py` + `GEMINI_API_KEY` | 批量生成、断点续传、容器环境、可复现生产 |

---

## 优先级

1. **用户当前请求显式指定**：`codex-image2` / `gemini` / `imagen` 优先级最高。
2. **运行时原生工具可用**：如果当前 CLI / agent runtime 暴露了原生图片工具，默认使用原生工具。
3. **原生工具不能满足落盘/批量要求**：如果当前原生工具无法稳定保存到项目目录，或没有批量/断点续传能力，再使用 `generate_image.py --model gemini`。
4. **非 Codex / 容器环境**：只有在没有原生图片工具时，默认使用 `generate_image.py --model gemini`。
5. **Gemini 失败**：脚本内可 fallback 到 Imagen。

---

## 明确指定后端

### 指定 Codex Image2

用户可以说：

```text
这次所有图片用 Codex Image2 生成。
```

处理规则：
- 如果当前 runtime 有原生图片工具，直接使用。
- 如果当前 runtime 没有原生图片工具，停止并说明不可用，建议改用 Gemini API。
- 不要尝试让 Python 脚本调用 Codex Image2。

### 指定 Gemini

```bash
python scripts/generate_image.py generate "prompt" --model gemini --output images/01-cover.png
python scripts/generate_image.py batch --tasks tasks.json --model gemini --image-size 2K --skip-existing
```

### 指定 Imagen

```bash
python scripts/generate_image.py generate "prompt" --model imagen --output images/01-cover.png
python scripts/generate_image.py batch --tasks tasks.json --model imagen --skip-existing
```

---

## 路径建议

### Path A

默认优先用 Codex Image2 生成局部插画；如果没有原生图片工具或需要脚本化，使用 Gemini。图片仍必须是素材，prompt 必须包含 `no text in image`。

### 2B / Path B

先生成 `tasks.json` 作为 prompt manifest。

- 有原生图片工具：优先逐张用原生工具生成整页图，并保存到 `images/`。
- 原生工具不可用或无法稳定落盘：使用 `generate_image.py batch --tasks tasks.json --model gemini`。
- 非 Codex / 容器环境：仍先检查是否有该环境的原生图片工具；没有时再用 Gemini batch。

### 2C / Path H

底图可以来自原生生图工具或 API fallback；默认仍优先原生工具。2C 的底图 prompt 必须禁止正文文字、标题、题目和答案文字，文字层由 PPT 原生文本框承担。

### 2B-R / FigEdit Reconstruction

2B-R 不属于生图后端链路，也不需要 Gemini API。它通过独立 FigEdit 对已经存在的位图做 OCR/CV 测量、语义拆解、SVG 和原生 PPTX 重建。不要调用背景擦除、图片编辑或文字框 JSON 提取。

### Path C magazine

`references/aesthetics/magazine/image-prompts.md` 只定义配图槽位、比例和提示词规则，不绑定具体后端。后端按 auto-runtime 策略决定。

---

## 失败与回退

- 原生 Codex Image2 不可用：回退 Gemini，或提示用户切换环境。
- 原生工具无法稳定保存到目标目录：使用 Gemini batch。
- Gemini 未配置 `GEMINI_API_KEY`：提示用户配置 key 或改用当前 runtime 原生图片工具。
- 用户显式指定某后端但不可用：不要静默切换，先说明并给出推荐 fallback。
