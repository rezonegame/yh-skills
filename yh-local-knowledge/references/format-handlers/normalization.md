# 格式归一化手册（Format Normalization）

本手册定义 yh-local-knowledge 如何把杂乱的多格式原始资料转换成可索引、可提取的 markdown。它是"格式零门槛"支柱的核心。

核心理念：**原始资料永不修改。** 所有转换产物写入 `.knowledge/normalized/` 这个只读中间层，sync/index/extract 都基于这一层工作，不直接碰二进制原文。

## 为什么需要归一化

用户丢进 `原始资料/` 的资料往往是 PDF/Word/Excel/PPT/图片/网页/音频混杂。LLM 无法直接读二进制。如果不归一化，技能只能"索引得到、提取不动"——这是当前最大的有效性缺口。

归一化把所有格式统一成 markdown 后，后续的 index/extract/review/export 都只面对文本，工作流彻底简化。

## 三级降级链

归一化按优先级尝试三级转换器，命中即停：

### Tier 1：markitdown（首选，全格式覆盖）

检测：`scripts/normalize.py --status` 输出 `markitdown: true`，或 `python scripts/bootstrap.py --check` 退出码 0。

安装（如果没装）：
```bash
python scripts/bootstrap.py --install        # 核心格式(PDF/Word/Excel/PPT/HTML)
python scripts/bootstrap.py --install-all    # 全格式(加音频/YouTube/EPub等)
# 或手动
pip install 'markitdown[pdf,docx,pptx,xlsx]>=0.1.7,<0.2'
```

覆盖范围：
- 文档：PDF、Word(.doc/.docx)、PowerPoint(.ppt/.pptx)、Excel(.xls/.xlsx)、EPub、RST
- 网页：HTML、URL（注意安全，见下）
- 图片：JPG/PNG/GIF/BMP/WEBP/TIFF（OCR，需 markitdown-ocr 或支持视觉的模型）
- 音频：MP3/WAV/M4A（语音转写，需 ffmpeg）
- 其他：ZIP（解包后逐个转换）、YouTube（字幕，需联网）

调用方式（脚本已封装，无需手写）：
- CLI：`markitdown 原始资料/x.pdf -o .knowledge/normalized/原始资料/x.md`
- Python：优先用 `convert_local(path)`（安全，只处理本地文件），不要用 `convert()`（它会接受 URL/远程 URI，有安全面问题）

### Tier 2：系统工具（markitdown 不可用时）

检测：`pandoc` 或 `pdftotext` 在 PATH 中。

覆盖范围（部分）：
- PDF → `pdftotext x.pdf out.txt`（必须输出到文件，不要 stdout；大文件用 `-f/-l` 分页）
- Word/EPub/RST → `pandoc x.docx -o out.md`

### Tier 3：metadata-only（都没有）

无可用的转换器时，只记录文件元数据（路径/大小/类型/时间戳），不提取内容。manifest 标 `normalization_status: fallback_metadata_only`。

**绝不编造内容。** 如果某个 PDF 没转出来，就在 source-map 里如实写"该文件未能提取内容，需用户确认或补工具"，不要假装读到了。

## 归一化纪律（learn-before-process）

遇到特定格式或特殊情况时，**先读本目录下对应的 `*-notes.md` 再动手**，不要盲目转换：

- 复杂表格/排版 → `pdf-notes.md`
- 多 sheet / 大数据量 → `excel-notes.md`
- 带样式/修订的 Word → `docx-notes.md`
- 扫描件 / 需 OCR → `image-notes.md`
- 音频/视频 → `audio-notes.md`

这是借鉴 kb-retriever 的 learn-before-process 纪律：格式专属的正确处理方法沉淀成手册，遇到先学再用，防止 agent 把二进制乱塞进上下文或选错工具。

## 渐进式检索纪律（提取阶段适用）

归一化后提取知识时，遵守 kb-retriever 的检索纪律，控制 token：

1. **grep-first**：先在 `.knowledge/normalized/` 用关键词定位，不要整文件读。
2. **局部窗口**：定位到后用 Read 的 offset/limit 只读命中附近，不整文件加载。
3. **禁整文件读**：任何归一化产物超过 ~2000 行时，禁止一次性 Read，必须分段。
4. **PDF 先转再 grep**：转出的 `.md` 是检索对象，不要对二进制 PDF 直接 grep。

## 输出位置与命名

```
[workspace]/
├── 原始资料/                    ← 永不修改
│   ├── report.pdf
│   ├── notes.docx
│   └── data.xlsx
└── .knowledge/
    └── normalized/              ← 只读中间层
        ├── 原始资料/            ← 按源根命名空间，避免跨根同名冲突
        │   ├── report.md
        │   ├── notes.md
        │   └── data.md
        └── (其他源根)/
```

- 归一化产物按"源根名/原文件名.md"组织，保留来源可追溯。
- 同名文件跨源根不会冲突（因为有源根命名空间）。
- 增量：源文件未变（hash/mtime 一致）时跳过重转换，标 `normalized_cached`。

## manifest 字段（向前兼容）

归一化结果回写到 `manifest.json` 的每个 file 条目：

```json
{
  "source_id": "src_001",
  "path": "原始资料/report.pdf",
  "type": ".pdf",
  "status": "indexed",
  "normalized_path": ".knowledge/normalized/原始资料/report.md",
  "normalization_status": "normalized",
  "normalization_error": null
}
```

`normalization_status` 取值：
- `not_required`：文本格式（md/txt/csv/json），无需转换。
- `normalized`：已成功转成 markdown。
- `normalized_cached`：增量命中缓存，未重转换。
- `fallback_metadata_only`：无可用转换器或转换失败，只记录元数据。
- `failed`：转换出错，`normalization_error` 记录原因。
- `skipped`：被策略跳过（如用户配置忽略某格式）。

这些字段对现有 schema 是新增（`additionalProperties: true`），旧工作区不带这些字段也能正常工作。

## 安全约束

- 本地文件用 `convert_local()`，不用 `convert()`——后者接受 URL/远程 URI，有路径遍历和远程请求风险。
- 不可信来源的文件，先查毒或隔离再归一化。
- 归一化不执行原文里的代码、不打开外部链接、不联网抓取（markitdown 的 URL 抓取是可选能力，默认不启用）。

## 何时重新归一化

- 源文件 hash/mtime 变化（增量同步检测到）→ 重新归一化，更新对应资产标 `needs_review`。
- 缓存 manifest 记录实际 `markitdown_version`。转换器版本变化但源文件未变时，状态改为 `renormalization_review_required`，保留已审核的 normalized 资产；用户确认后才用 `--force-renormalize` 覆盖。
- MarkItDown 0.1.7 修复了 DOCX OMML 数学公式转换；本技能固定兼容范围为 `>=0.1.7,<0.2`，并用普通 DOCX 与 OMML DOCX 双回归验证标题、表格、正文和公式。
- 用户手动要求"重新提取这个文件"→ 删除该文件的 normalized 产物后重跑。
