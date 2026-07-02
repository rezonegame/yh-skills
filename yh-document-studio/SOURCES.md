# SOURCES · 上游来源详细记录

本文件记录 yh-document-studio 每个采用了上游内容的部分：来源技能、源路径、GitHub URL（或本地路径+备份位置）、采用了什么、改了什么。

> **设计原则**：kami 的全部文件在本技能内**完整复制、一个字节不改**（见 `SKILL.md` Provenance 节）。所有新功能（美学包、印刷档、注入脚本）都是外层包裹，不编辑 kami 复制件中的任何原文件。本文件追踪的是「借鉴自其它技能的设计/资产」的来源。

---

## 1. kami（主体）

- **GitHub**: https://github.com/tw93/kami
- **作者**: tw93（Kaku · Waza · Kami 三部曲之一）
- **源路径**: `C:\Users\wudao\OneDrive\skills\kami\`
- **备份位置**: `C:\Users\wudao\SkillsBackup\20260621\kami\`
- **采用了什么**:
  - **完整复制**：9 类文档模板（`assets/templates/*.html`）、14 个图表（`assets/diagrams/`）、14 个脚本（`scripts/`）、全部 references、assets、tokens.json、build.py、CHEATSHEET.md、AGENTS.md
  - SKILL.md 流程骨架（语言判定 → 意图抽取 → 文档类型 → 素材 → 提纯 → 规格加载 → 填模板）
- **改了什么**: **kami 复制件中的原文件零修改**。仅在本技能**自有**的新增文件（themes/、print/、inject-override.py、print-spec.md、SOURCES.md）和 SKILL.md（本技能自己的，非 kami 原件）中加入新内容。
- **核验方法**: `diff -r skills/kami skills/yh-document-studio` 应只显示 yh-document-studio 的新增文件，kami 侧无任何"Only in kami"。

---

## 2. frontend-design（美学思路借鉴）

- **GitHub**: https://github.com/anthropics/skills （路径 `skills/frontend-design/`）
- **源路径**: `C:\Users\wudao\OneDrive\skills\frontend-design\`
- **备份位置**: `C:\Users\wudao\SkillsBackup\20260621\frontend-design\`
- **采用了什么**:
  - "避免 AI slop"的美学判断原则（不用 Inter/Roboto、不用紫色渐变白底、不做千篇一律的布局）
  - "先定美学方向再写代码"的工作思路
- **改了什么**: 不直接复制任何文件。原则融入 `SKILL.md` 的「Step 1.6 美学选择」章节，作为选择/推荐美学包时的判断依据。
- **为什么不直接用**: frontend-design 是"实时生成任意美学"，本技能走"预设 5 套成品"路线（质量可控），只取其判断原则。

---

## 3. theme-factory（美学包色源 + 主题机制借鉴）

- **GitHub**: https://github.com/anthropics/skills （路径 `skills/theme-factory/`）
- **源路径**: `C:\Users\wudao\OneDrive\skills\theme-factory\`
- **备份位置**: `C:\Users\wudao\SkillsBackup\20260621\theme-factory\`
- **采用了什么**:
  - **机制**：「一个主题 = 调色板 + 字体配对，可套用到产物上」这个模型，转化为本技能的「美学包 = `:root` 覆盖 + 背景覆盖」。
  - **色源**（仅取色值，不取字体）：
    - `themes/minimal-mono.css` ← `themes/modern-minimalist.md`（炭灰/板岩灰）
    - `themes/editorial-warm.css` ← `themes/golden-hour.md`（赭石/棕/米）
    - `themes/natural-essay.css` ← `themes/forest-canopy.md`（森林绿/鼠尾草/象牙）
    - `themes/business-cool.css` ← `themes/ocean-depths.md`（深海蓝/青，已调整为更克制的灰蓝商务调）
- **改了什么**:
  - **不采用 theme-factory 的字体**（DejaVu Sans / FreeSerif / FreeSans 质量不足），所有美学包统一用 kami 同级字体（CN: TsangerJinKai02，EN: Charter，JA: YuMincho）。
  - **不直接搬主题成品**：theme-factory 主题偏营销 pitch 调（"Best Used For: presentations/pitches"），本技能只取其色值作起点，最终色值经视觉调试。
  - 色值从 markdown 描述改写为 CSS `:root` 变量 + `@page`/`html,body` 背景覆盖。
- **丢弃的 theme-factory 主题**（不采用，记录原因）:
  - `sunset-boulevard`：营销 pitch 调，非文档调
  - `arctic-frost`：医疗/科技风太冷，文档场景窄
  - `desert-rose`：时尚/美妆太垂直
  - `botanical-garden`：色彩太跳，文档显花
  - `tech-innovation`：典型 AI slop（霓虹青），违反 frontend-design 原则
  - `midnight-galaxy`：太戏剧化/神秘，不适合严肃文档

---

## 4. print-design（印刷标准抽取）

- **GitHub**: ❌ 无公开仓库（中文社区技能）
- **源路径**: `C:\Users\wudao\OneDrive\skills\print-design\`
- **备份位置**: `C:\Users\wudao\SkillsBackup\20260621\print-design\`
- **采用了什么**:
  - 印刷生产检查清单（Design/Pre-Press/Export/Proofing/Print 五阶段）
  - 纸张尺寸表（A/B/C 系列）
  - 出血 3mm / 安全区 5mm / 300 DPI / CMYK / PDF/X 等物理标准
  - 常见错误表（RGB mode、低分辨率、无出血等）
- **改了什么**: 抽取为本技能的 `references/print-spec.md`，并**适配浏览器打印路径**：
  - 明确标注哪些标准浏览器打印能做（出血/安全区/裁切线/300DPI）、哪些做不到（CMYK/PDF/X）
  - CMYK/PDF-X 仅作为「专业印厂可选后处理」提示，不集成进自动流程
  - 去掉桌游配件印刷尺寸（非文档场景，不在本技能范围）
- **配套资产**: `assets/print/print-mode.css` 实现浏览器可做的部分（`@page margin:0`、安全区 padding、裁切线伪元素）。

---

## 5. web-artifacts-builder（设计参考，未直接采用）

- **GitHub**: https://github.com/anthropics/skills （路径 `skills/web-artifacts-builder/`）
- **源路径**: `C:\Users\wudao\OneDrive\skills\web-artifacts-builder\`
- **备份位置**: `C:\Users\wudao\SkillsBackup\20260621\web-artifacts-builder\`
- **采用了什么**: 仅作设计参考——「把多文件工程打包成单文件 HTML 产物」的思路。
- **改了什么/为什么不直接用**: kami 已有 `build.py` 完成同等职能（HTML 产物 + PDF 元数据注入），本技能直接复用 kami 的 build.py，不引入 web-artifacts-builder 的 React/Vite/shadcn 工程链（那是给 claude.ai artifact 用的，与本技能的文档场景不符）。

---

## 版本追踪

- **整合日期**: 2026-06-21
- **上游技能处理**: kami / frontend-design / theme-factory / web-artifacts-builder / print-design 已备份至 `C:\Users\wudao\SkillsBackup\20260621\` 并从 `OneDrive\skills\` 删除（详见该目录 MANIFEST.md）。
- **升级本技能时**: 如需查询上游最新版本，对有 GitHub 的 4 个技能访问上述 URL；对 print-design 查本地备份。
