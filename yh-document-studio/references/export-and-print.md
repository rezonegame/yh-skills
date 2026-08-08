本文件包含输出格式自动选择和印刷导出档位的完整规则。SKILL.md 中只保留简要指针。

---

## Step 4.5 · Auto-select output format

Do not ask the user which format to export. Decide from context:

| Signal | Output | Why |
|---|---|---|
| Any document request | HTML + PDF | PDF is the default deliverable, HTML is the source |
| Slides / PPT / deck | HTML + PDF + PPTX | Presentations need a projectable format |
| "分享" / "发朋友圈" / "share" / "post" / "preview" | + PNG | Social platforms and messaging need images |
| "嵌入" / "插图" / "embed in another doc" | PNG only | Used as material inside other documents |
| User explicitly says a format | Follow the user | Explicit request overrides auto-selection |

PDF always ships for document templates. Landing pages ship as a ready-to-serve static HTML file. PPTX follows slides. PNG follows sharing context. The user should never need to think about formats.

---

## Step 4.6 · Pick the export tier (yh-document-studio 新增)

build 前明确导出档位。这决定是否注入印刷档 override。详见 `references/print-spec.md`。

### 三档定义

| 档位 | 用途 | 行为 |
|------|------|------|
| **屏幕版**（默认） | 屏幕/邮件/网盘阅读的 PDF | 不注入 print override，= 原 kami 行为 |
| **印刷版（本地）** | 本地/办公/快印店打印 | 注入 `assets/print/print-mode.css`：出血 + 安全区 + 裁切线 |
| **印刷版（专业）** | 专业印厂（画册/大批量/专色） | 印刷版（本地）基础上，提示用户读 `references/print-spec.md` 第 4 节做 CMYK/PDF-X 后处理 |

### 选择规则

- 用户说"送印/印刷/打印/print-ready" → 问"本地打印还是专业印厂？"，分别走印刷版（本地）/印刷版（专业）。
- 用户没提印刷 → 默认**屏幕版**，不问。
- 浏览器打印路径**做不到** CMYK 和 PDF/X-4（只输出 RGB 普通 PDF）；专业印厂场景必须在 `print-spec.md` 第 4 节后处理。如实告知用户这一限制，不要隐瞒。

### 注入命令（build 后、浏览器打印前）

```bash
# 仅美学包（屏幕版）
python scripts/inject-override.py <产物.html> --theme <美学包名>

# 美学包 + 印刷档
python scripts/inject-override.py <产物.html> --theme <美学包名> --print

# parchment-ink（默认美学，空覆盖，脚本自动跳过美学注入）
python scripts/inject-override.py <产物.html> --print
```

### 浏览器打印手动步骤（印刷档必读）

注入后用浏览器打开产物 HTML，Ctrl+P 打印对话框**必须**：
1. 目标：另存为 PDF
2. 边距：**无**（让 `@page margin:0` 生效）
3. **取消勾选"页眉和页脚"**（否则破坏出血）
4. **勾选"背景图形"**（否则 `@page`/body 背景色不打印）

> 印刷档水印（屏幕顶部蓝色条）只在屏幕显示，打印时不出现——它就是来提醒你上面这 4 步的。
