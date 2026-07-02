#!/usr/bin/env python3
"""inject-override.py · yh-document-studio

把美学包 / 印刷档 override CSS 注入到产物 HTML 的 </head> 前。

设计：
- 纯标准库（re + pathlib + argparse），不依赖第三方。
- 以内联 <style> 方式注入（而非 <link>），因为产物 HTML 可能被移动，
  相对路径 link 会失效。内联保证产物自包含。
- 不修改 kami 模板原文件，只改"产物"（用户工作目录里 build 出来的副本）。
- 默认美学 parchment-ink 是空覆盖，跳过注入 = 等价原 kami。

用法：
    python inject-override.py <html_file>                      # 不注入任何 override
    python inject-override.py <html_file> --theme minimal-mono # 注入美学包
    python inject-override.py <html_file> --print              # 注入印刷档
    python inject-override.py <html_file> --theme business-cool --print

退出码：
    0  成功（含"无需注入"）
    1  参数错误 / 文件找不到 / 注入失败
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# 脚本位于 scripts/，技能根是其父目录
SKILL_ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = SKILL_ROOT / "assets" / "themes"
PRINT_DIR = SKILL_ROOT / "assets" / "print"

VALID_THEMES = ["parchment-ink", "minimal-mono", "business-cool", "editorial-warm", "natural-essay"]
DEFAULT_THEME = "parchment-ink"  # 空覆盖，跳过注入


def read_css(path: Path) -> str:
    """读取 CSS 文件，去掉外层块注释便于内联（保留规则注释）。"""
    return path.read_text(encoding="utf-8")


def inject(html: str, css_blocks: list[tuple[str, str]]) -> str:
    """把多个 (label, css) 块拼成一个 <style>，插入 </head> 前。

    若 HTML 无 </head>，退化为插到 <body 前；再不行插到开头。
    每个块带来源标签注释，方便排查。
    """
    if not css_blocks:
        return html

    parts = []
    for label, css in css_blocks:
        # 去掉纯注释的空覆盖文件内容，避免无意义内联
        stripped = css.strip()
        if not stripped or not any(c in stripped for c in "{};"):
            # 只含注释/空白，跳过
            continue
        parts.append(f"/* === yh-document-studio override: {label} === */\n{css}")
    if not parts:
        return html  # 全是空覆盖，无需注入

    style_tag = "<style data-yh-studio-overrides>\n" + "\n\n".join(parts) + "\n</style>\n"

    # 优先 </head>
    if re.search(r"</head>", html, re.IGNORECASE):
        return re.sub(r"</head>", style_tag + "</head>", html, count=1, flags=re.IGNORECASE)
    # 退化：<body
    m = re.search(r"<body\b", html, re.IGNORECASE)
    if m:
        return html[: m.start()] + style_tag + html[m.start() :]
    # 再退化：开头
    return style_tag + html


def main() -> int:
    parser = argparse.ArgumentParser(
        description="把美学包/印刷档 override CSS 注入到产物 HTML。",
        usage="python inject-override.py <html_file> [--theme NAME] [--print]",
    )
    parser.add_argument("html_file", help="要注入的产物 HTML 路径")
    parser.add_argument(
        "--theme",
        default=None,
        choices=VALID_THEMES,
        help=f"美学包名称（默认 {DEFAULT_THEME}，空覆盖不注入）",
    )
    parser.add_argument("--print", dest="print_mode", action="store_true", help="注入印刷档 override")
    args = parser.parse_args()

    html_path = Path(args.html_file)
    if not html_path.is_file():
        print(f"ERROR: HTML 文件不存在: {html_path}", file=sys.stderr)
        return 1

    html = html_path.read_text(encoding="utf-8")
    css_blocks: list[tuple[str, str]] = []

    # 美学包（parchment-ink 是空覆盖，跳过）
    theme = args.theme or DEFAULT_THEME
    if theme != DEFAULT_THEME:
        theme_path = THEMES_DIR / f"{theme}.css"
        if not theme_path.is_file():
            print(f"ERROR: 美学包文件不存在: {theme_path}", file=sys.stderr)
            return 1
        css_blocks.append((f"theme/{theme}", read_css(theme_path)))

    # 印刷档
    if args.print_mode:
        print_path = PRINT_DIR / "print-mode.css"
        if not print_path.is_file():
            print(f"ERROR: 印刷档文件不存在: {print_path}", file=sys.stderr)
            return 1
        css_blocks.append(("print/print-mode", read_css(print_path)))

    if not css_blocks:
        print(f"无需注入（theme={theme} 为空覆盖，--print 未指定）。文件未改动: {html_path}")
        return 0

    new_html = inject(html, css_blocks)
    if new_html == html:
        print(f"WARNING: 所有 override 均为空覆盖，文件未改动: {html_path}")
        return 0

    html_path.write_text(new_html, encoding="utf-8")
    labels = ", ".join(label for label, _ in css_blocks)
    print(f"已注入 [{labels}] 到 {html_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
