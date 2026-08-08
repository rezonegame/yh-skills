#!/usr/bin/env python3
"""
PDF Evidence Extraction Pipeline
从 PDF 文档提取结构化证据：文本/图表/公式/表格/图片 → JSON大纲 → Slide-to-Source Register

吸收自 Tosea.ai 的 source-grounded 工作流方法论。
依赖：pip install pymupdf pillow
可选：pip install camelot-py[cv] (表格精确提取)

用法：
    python pdf_evidence_pipeline.py input.pdf [--output-dir ./output] [--max-pages 50]

输出：
    output/
    ├── evidence.json       # 结构化证据清单
    ├── outline.json        # AI 可用的 slide-by-slide 大纲草案
    ├── register.csv        # Slide-to-Source 追溯表
    ├── images/             # 提取的图片/图表
    └── tables/             # 提取的表格 (CSV)
"""

import argparse
import fitz  # PyMuPDF
import json
import os
import re
import csv
from pathlib import Path
from datetime import datetime


def extract_text_blocks(page):
    """提取页面文本块，保留结构"""
    blocks = page.get_text("dict")["blocks"]
    text_items = []
    for block in blocks:
        if block["type"] == 0:  # text block
            for line in block["lines"]:
                text = "".join(span["text"] for span in line["spans"])
                if text.strip():
                    text_items.append({
                        "text": text.strip(),
                        "bbox": [round(c, 1) for c in line["bbox"]],
                        "font_size": max(span["size"] for span in line["spans"]),
                        "font": line["spans"][0]["font"] if line["spans"] else "",
                        "flags": line["spans"][0]["flags"] if line["spans"] else 0,
                    })
    return text_items


def classify_text(text, font_size, font, flags):
    """根据字体特征分类文本角色"""
    is_bold = bool(flags & 16)
    is_italic = bool(flags & 2)
    text_lower = text.lower().strip()

    # 中文标题检测（无加粗标记时，用字号判断）
    # 常见标题模式
    heading_patterns = [
        r'^第[一二三四五六七八九十\d]+[章节篇]',  # 第一章
        r'^\d+\.\d+\s',  # 1.1
        r'^[一二三四五六七八九十]+[、\.]\s',  # 一、
        r'^第[一二三四五六七八九十\d]+部分',  # 第一部分
        r'^摘要$|^引言$|^结论$|^讨论$|^方法$|^结果$|^参考文献$|^Abstract$|^Introduction$|^Conclusion$|^Discussion$|^Method|^Result',
        r'^(?:一|二|三|四|五|六|七|八|九|十)[、\.]',
    ]

    for pat in heading_patterns:
        if re.match(pat, text_lower):
            return "heading1"

    # 字号分级（中文PDF常见）
    if font_size >= 20:
        return "heading1"
    elif font_size >= 16:
        return "heading2"
    elif font_size >= 14:
        return "heading3"
    elif font_size >= 12 and is_bold:
        return "heading3"
    elif text_lower.startswith(("figure", "fig.", "fig ", "图", "table", "tab.", "表")):
        return "caption"
    elif font_size <= 9:
        return "small_text"
    else:
        return "body"


def extract_images(page, page_num, output_dir):
    """提取页面中的图片"""
    images = []
    image_list = page.get_images(full=True)
    for img_idx, img in enumerate(image_list):
        xref = img[0]
        try:
            pix = fitz.Pixmap(page.parent, xref)
            if pix.n - pix.alpha > 3:  # CMYK
                pix = fitz.Pixmap(fitz.csRGB, pix)

            img_name = f"p{page_num+1}_img{img_idx+1}.png"
            img_path = os.path.join(output_dir, "images", img_name)
            os.makedirs(os.path.dirname(img_path), exist_ok=True)
            pix.save(img_path)

            images.append({
                "page": page_num + 1,
                "index": img_idx + 1,
                "width": pix.width,
                "height": pix.height,
                "file": img_name,
                "path": img_path,
            })
            pix = None
        except Exception as e:
            images.append({
                "page": page_num + 1,
                "index": img_idx + 1,
                "error": str(e),
            })
    return images


def extract_tables_heuristic(page, page_num):
    """启发式表格检测——基于文本对齐和间距"""
    blocks = page.get_text("dict")["blocks"]
    tables = []

    for block in blocks:
        if block["type"] != 0:
            continue
        lines = block["lines"]
        if len(lines) < 3:
            continue

        # 检测列状排列：多行中有相似 x 坐标的文本
        x_positions = []
        for line in lines:
            spans = line.get("spans", [])
            if spans:
                x_positions.append(spans[0]["bbox"][0])

        # 如果有规律的列对齐（3列以上），可能是表格
        unique_x = list(set(round(x) for x in x_positions))
        if len(unique_x) >= 3 and len(lines) >= 4:
            # 提取为表格结构
            rows = []
            for line in lines:
                cells = []
                current_cell = ""
                last_x = None
                for span in line.get("spans", []):
                    x = span["bbox"][0]
                    if last_x is not None and abs(x - last_x) > 50:
                        cells.append(current_cell.strip())
                        current_cell = span["text"]
                    else:
                        current_cell += span["text"]
                    last_x = x
                if current_cell.strip():
                    cells.append(current_cell.strip())
                if cells:
                    rows.append(cells)

            if len(rows) >= 3 and any(len(r) >= 2 for r in rows):
                tables.append({
                    "page": page_num + 1,
                    "rows": len(rows),
                    "cols": max(len(r) for r in rows),
                    "data": rows[:10],  # 前10行预览
                })

    return tables


def detect_formulas(text_blocks):
    """检测可能的数学公式"""
    formulas = []
    formula_patterns = [
        r'[∑∏∫∇∂√∞±≤≥≠≈∝∈∉⊂⊃∪∩]',
        r'[a-zA-Z]\s*=\s*[^=\n]{5,}',
        r'\b(eq|equation|公式)\.?\s*\d+',
        r'\$.*\$',
        r'\\[a-zA-Z]+',  # LaTeX commands
    ]

    for block in text_blocks:
        text = block.get("text", "")
        for pattern in formula_patterns:
            matches = re.findall(pattern, text)
            if matches:
                formulas.append({
                    "text": text[:200],
                    "page": block.get("page", 0),
                })
                break

    return formulas


def generate_outline(evidence):
    """基于提取的证据生成 slide-by-slide 大纲草案"""
    outline = []
    slide_num = 1

    # 封面
    outline.append({
        "slide": slide_num,
        "type": "cover",
        "title": evidence.get("title", "Untitled"),
        "subtitle": evidence.get("first_heading", ""),
        "source": evidence.get("source_file", ""),
    })
    slide_num += 1

    # 目录
    if evidence.get("headings"):
        outline.append({
            "slide": slide_num,
            "type": "agenda",
            "title": "目录",
            "items": [h["text"] for h in evidence["headings"][:8]],
        })
        slide_num += 1

    # 按一级标题分组
    current_section = None
    for heading in evidence.get("headings", []):
        if heading["level"] in ("heading1", "heading2"):
            if current_section:
                outline.append(current_section)
                slide_num += 1

            current_section = {
                "slide": slide_num,
                "type": "section_divider" if heading["level"] == "heading1" else "content",
                "title": heading["text"],
                "source_page": heading["page"],
                "key_points": [],
                "evidence": [],
            }
        elif current_section and heading["level"] == "heading3":
            current_section["key_points"].append(heading["text"])

    if current_section:
        outline.append(current_section)
        slide_num += 1

    # 数据/图表页
    if evidence.get("images"):
        for i, img in enumerate(evidence["images"][:10]):
            outline.append({
                "slide": slide_num,
                "type": "data",
                "title": f"Figure from p.{img['page']}",
                "image_ref": img["file"],
                "source_page": img["page"],
            })
            slide_num += 1

    # 表格页
    if evidence.get("tables"):
        for i, tbl in enumerate(evidence["tables"][:5]):
            outline.append({
                "slide": slide_num,
                "type": "table",
                "title": f"Table from p.{tbl['page']}",
                "rows": tbl["rows"],
                "cols": tbl["cols"],
                "source_page": tbl["page"],
            })
            slide_num += 1

    # 总结
    outline.append({
        "slide": slide_num,
        "type": "closing",
        "title": "总结",
        "key_points": [h["text"] for h in evidence.get("headings", []) if h["level"] == "heading1"][:5],
    })

    return outline


def generate_register(outline, source_file):
    """生成 Slide-to-Source 追溯表"""
    register = []
    for slide in outline:
        page = slide.get("source_page", "")
        title = slide.get("title", "")
        slide_type = slide.get("type", "")

        # 提取关键 claim
        claims = []
        if slide.get("key_points"):
            claims.extend(slide["key_points"][:3])
        if slide.get("items"):
            claims.extend(slide["items"][:3])

        if claims:
            for claim in claims:
                register.append({
                    "slide": slide["slide"],
                    "claim": claim,
                    "source_file": source_file,
                    "source_page": page,
                    "type": slide_type,
                })
        elif title:
            register.append({
                "slide": slide["slide"],
                "claim": title,
                "source_file": source_file,
                "source_page": page,
                "type": slide_type,
            })

    return register


def process_pdf(pdf_path, output_dir, max_pages=50):
    """主处理函数"""
    doc = fitz.open(pdf_path)
    total_pages = min(len(doc), max_pages)

    os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "tables"), exist_ok=True)

    all_evidence = {
        "source_file": os.path.basename(pdf_path),
        "processed_at": datetime.now().isoformat(),
        "total_pages": len(doc),
        "processed_pages": total_pages,
        "title": "",
        "first_heading": "",
        "headings": [],
        "body_text": [],
        "images": [],
        "tables": [],
        "formulas": [],
    }

    print(f"Processing {pdf_path}: {len(doc)} pages (max {total_pages})")

    for page_num in range(total_pages):
        page = doc[page_num]

        # 1. 提取文本块
        text_blocks_raw = extract_text_blocks(page)

        # 2. 分类文本
        for tb in text_blocks_raw:
            role = classify_text(tb["text"], tb["font_size"], tb["font"], tb["flags"])
            tb["role"] = role
            tb["page"] = page_num + 1

            if role in ("heading1", "heading2", "heading3"):
                all_evidence["headings"].append({
                    "text": tb["text"],
                    "level": role,
                    "page": page_num + 1,
                    "bbox": tb["bbox"],
                })
                if not all_evidence["title"] and role == "heading1":
                    all_evidence["title"] = tb["text"]
                if not all_evidence["first_heading"] and role in ("heading1", "heading2"):
                    all_evidence["first_heading"] = tb["text"]
            elif role == "body":
                all_evidence["body_text"].append({
                    "text": tb["text"],
                    "page": page_num + 1,
                })

        # 3. 提取图片
        images = extract_images(page, page_num, output_dir)
        all_evidence["images"].extend(images)

        # 4. 启发式表格检测
        tables = extract_tables_heuristic(page, page_num)
        all_evidence["tables"].extend(tables)

        # 5. 公式检测
        formulas = detect_formulas(text_blocks_raw)
        for f in formulas:
            f["page"] = page_num + 1
        all_evidence["formulas"].extend(formulas)

        if (page_num + 1) % 10 == 0:
            print(f"  Page {page_num + 1}/{total_pages}")

    doc.close()

    # 生成大纲
    outline = generate_outline(all_evidence)

    # 生成追溯表
    register = generate_register(outline, all_evidence["source_file"])

    # 保存结果
    evidence_path = os.path.join(output_dir, "evidence.json")
    with open(evidence_path, "w", encoding="utf-8") as f:
        json.dump(all_evidence, f, ensure_ascii=False, indent=2)

    outline_path = os.path.join(output_dir, "outline.json")
    with open(outline_path, "w", encoding="utf-8") as f:
        json.dump(outline, f, ensure_ascii=False, indent=2)

    register_path = os.path.join(output_dir, "register.csv")
    with open(register_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["slide", "claim", "source_file", "source_page", "type"])
        writer.writeheader()
        writer.writerows(register)

    # 摘要
    print(f"\n=== Extraction Summary ===")
    print(f"  Pages: {total_pages}")
    print(f"  Headings: {len(all_evidence['headings'])} (H1: {sum(1 for h in all_evidence['headings'] if h['level']=='heading1')})")
    print(f"  Body text blocks: {len(all_evidence['body_text'])}")
    print(f"  Images: {len(all_evidence['images'])}")
    print(f"  Tables: {len(all_evidence['tables'])}")
    print(f"  Formulas: {len(all_evidence['formulas'])}")
    print(f"  Outline slides: {len(outline)}")
    print(f"  Register entries: {len(register)}")
    print(f"\n  Output: {output_dir}/")
    print(f"    evidence.json ({os.path.getsize(evidence_path)//1024}KB)")
    print(f"    outline.json ({os.path.getsize(outline_path)//1024}KB)")
    print(f"    register.csv ({os.path.getsize(register_path)//1024}KB)")

    return all_evidence, outline, register


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Evidence Extraction Pipeline")
    parser.add_argument("pdf", help="Input PDF file path")
    parser.add_argument("--output-dir", "-o", default="./output", help="Output directory")
    parser.add_argument("--max-pages", "-m", type=int, default=50, help="Max pages to process")
    args = parser.parse_args()

    process_pdf(args.pdf, args.output_dir, args.max_pages)
