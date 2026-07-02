#!/usr/bin/env python3
"""Create a labeled contact sheet and report blank or duplicate slide images."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageStat


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def natural_key(path: Path) -> list[object]:
    return [int(part) if part.isdigit() else part.casefold() for part in re.split(r"(\d+)", path.name)]


def find_images(input_dir: Path, pattern: str) -> list[Path]:
    return sorted(
        (path for path in input_dir.glob(pattern) if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES),
        key=natural_key,
    )


def load_font(size: int) -> ImageFont.ImageFont:
    for candidate in ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/msyh.ttc"):
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def image_variance(image: Image.Image) -> float:
    grayscale = image.convert("L").resize((128, 72))
    return float(ImageStat.Stat(grayscale).var[0])


def pixel_digest(image: Image.Image) -> str:
    normalized = image.convert("RGB").resize((256, 144))
    return hashlib.sha256(normalized.tobytes()).hexdigest()


def build_report(paths: list[Path], blank_threshold: float) -> dict:
    records = []
    digest_to_names: dict[str, list[str]] = {}
    for path in paths:
        with Image.open(path) as source:
            image = source.copy()
        variance = image_variance(image)
        digest = pixel_digest(image)
        digest_to_names.setdefault(digest, []).append(path.name)
        records.append(
            {
                "file": path.name,
                "width": image.width,
                "height": image.height,
                "variance": round(variance, 3),
                "near_blank": variance <= blank_threshold,
                "digest": digest,
            }
        )
    duplicates = [names for names in digest_to_names.values() if len(names) > 1]
    return {
        "schema": "yh_slides_contact_sheet_report.v1",
        "image_count": len(records),
        "blank_threshold": blank_threshold,
        "near_blank": [record["file"] for record in records if record["near_blank"]],
        "duplicate_groups": duplicates,
        "images": records,
    }


def render_sheet(paths: list[Path], output: Path, columns: int, thumb_width: int, thumb_height: int) -> None:
    label_height = 42
    gap = 18
    margin = 24
    rows = math.ceil(len(paths) / columns)
    sheet_width = margin * 2 + columns * thumb_width + (columns - 1) * gap
    sheet_height = margin * 2 + rows * (thumb_height + label_height) + (rows - 1) * gap
    sheet = Image.new("RGB", (sheet_width, sheet_height), "#E9E9E9")
    draw = ImageDraw.Draw(sheet)
    font = load_font(22)

    for index, path in enumerate(paths):
        row, column = divmod(index, columns)
        x = margin + column * (thumb_width + gap)
        y = margin + row * (thumb_height + label_height + gap)
        with Image.open(path) as source:
            image = source.convert("RGB")
        thumb = ImageOps.contain(image, (thumb_width, thumb_height), Image.Resampling.LANCZOS)
        tile = Image.new("RGB", (thumb_width, thumb_height), "white")
        tile.paste(thumb, ((thumb_width - thumb.width) // 2, (thumb_height - thumb.height) // 2))
        sheet.paste(tile, (x, y))
        draw.rectangle((x, y, x + thumb_width - 1, y + thumb_height - 1), outline="#B8B8B8", width=1)
        label = f"{index + 1:02d}  {path.name}"
        draw.text((x, y + thumb_height + 8), label, fill="#202020", font=font)

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path, help="Directory containing rendered slide images")
    parser.add_argument("--pattern", default="*", help="Glob pattern inside input_dir (default: *)")
    parser.add_argument("--output", type=Path, required=True, help="Contact-sheet image path")
    parser.add_argument("--report", type=Path, help="Optional JSON QA report path")
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--thumb-width", type=int, default=400)
    parser.add_argument("--thumb-height", type=int, default=225)
    parser.add_argument("--blank-threshold", type=float, default=2.0)
    parser.add_argument("--strict", action="store_true", help="Return non-zero for near-blank or duplicate images")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.columns < 1 or args.thumb_width < 1 or args.thumb_height < 1:
        raise SystemExit("columns and thumbnail dimensions must be positive")
    paths = find_images(args.input_dir, args.pattern)
    if not paths:
        raise SystemExit(f"no images found in {args.input_dir} matching {args.pattern!r}")

    report = build_report(paths, args.blank_threshold)
    render_sheet(paths, args.output, args.columns, args.thumb_width, args.thumb_height)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Wrote {args.output} with {len(paths)} images.")
    if report["near_blank"]:
        print("Near-blank images: " + ", ".join(report["near_blank"]))
    if report["duplicate_groups"]:
        print("Duplicate groups: " + "; ".join(", ".join(group) for group in report["duplicate_groups"]))
    return 1 if args.strict and (report["near_blank"] or report["duplicate_groups"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
