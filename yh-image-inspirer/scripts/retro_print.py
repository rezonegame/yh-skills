#!/usr/bin/env python3
"""
retro_print.py — 复古版画/图章质感后处理管线
================================================
来源：公众号文章《中国风质感，不如试试这样做！一股复古中式美！》（版式设计很简单）
复刻 PS「滤镜库→素描→图章」+ 去白 + 纸质纹理叠加 三步效果，纯 OpenCV/numpy 实现。

用途：把写实照片 / AI 生图 / 设计稿批量转成复古版画（木刻/图章/老报纸）质感，
适合中国风、历史题材、传统匠心品牌的视觉统一。

用法：
  python3 retro_print.py 输入.png [输入2.png ...] -o 输出目录 [选项]

选项：
  --blur N        中值滤波核（越大细节越少、块面感越强，默认 9，奇数）
  --mode MODE     二值化模式：otsu(默认) / adaptive / fixed
  --thresh N      fixed 模式的阈值 (0-255，默认 128)
  --invert        反相（白墨黑底，默认黑墨浅底）
  --no-paper      关闭纸纹叠加
  --paper-alpha F 纸纹强度 0~1（默认 0.35）
  --no-grain      关闭颗粒噪声
  --transparent   输出透明底（去白，PNG），供叠加在其他版式上
  --check         只输出诊断信息不写文件

示例：
  python3 retro_print.py photo.jpg -o out/                          # 默认黑墨浅纸
  python3 retro_print.py a.png b.png c.png -o out/ --blur 13        # 批量，更块面化
  python3 retro_print.py art.jpg -o out/ --transparent              # 去白透明底
"""
import argparse
import os
import sys

import cv2
import numpy as np


def load_image(path):
    """读取图片，RGBA 先合成到白底。返回 BGR ndarray。"""
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return None
    if img.shape[2] == 4:
        alpha = img[:, :, 3:4].astype(np.float32) / 255.0
        bgr = img[:, :, :3].astype(np.float32) * alpha + 255.0 * (1 - alpha)
        return bgr.astype(np.uint8)
    if img.shape[2] == 3:
        return img
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


def stamp_filter(img, blur_ksize=9, mode="otsu", thresh_val=128, invert=False):
    """PS 图章滤镜近似：灰度 → 中值滤波去细节 → 二值化。返回二值图(0/255)。"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if blur_ksize > 1:
        gray = cv2.medianBlur(gray, blur_ksize)
    if mode == "adaptive":
        bw = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15
        )
    elif mode == "fixed":
        _, bw = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
    else:  # otsu
        _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if invert:
        bw = cv2.bitwise_not(bw)
    return bw


def generate_paper_texture(w, h, seed=42):
    """程序生成仿古纸纹：颗粒 + 纤维 + 泛黄 + 暗角。避免外部素材依赖。"""
    rng = np.random.default_rng(seed)
    noise = rng.normal(128, 30, (h, w)).astype(np.float32)
    fiber = cv2.GaussianBlur(noise, (1, 15), 0)
    base = np.full((h, w), 232, dtype=np.float32)
    mottle = cv2.GaussianBlur(
        rng.normal(0, 8, (h, w)).astype(np.float32), (101, 101), 0
    )
    paper = base + fiber * 0.15 + mottle
    yy, xx = np.mgrid[0:h, 0:w]
    cy, cx = h / 2, w / 2
    dist = np.sqrt(((xx - cx) / (w / 2)) ** 2 + ((yy - cy) / (h / 2)) ** 2)
    vignette = 1.0 - np.clip(dist - 0.7, 0, 1) * 0.25
    paper = np.clip(paper * vignette, 0, 255).astype(np.uint8)
    return cv2.cvtColor(paper, cv2.COLOR_GRAY2BGR)


def retro_print(img, blur_ksize=9, mode="otsu", thresh_val=128, invert=False,
                paper=True, paper_alpha=0.35, grain=True, transparent=False):
    """完整管线：原图 → 版画二值 → 正片叠底上纸 → 颗粒。

    返回 RGBA 结果（transparent=False 时 alpha=255 不透明）。
    """
    bw = stamp_filter(img, blur_ksize, mode, thresh_val, invert)
    h, w = bw.shape

    # 墨色与纸色（正片叠底思路：黑色保留，白色=纸色）
    ink_color = 30 if not invert else 245   # 黑墨浅底 / 白墨
    paper_color = 245 if not invert else 30

    result = np.full((h, w, 3), paper_color, dtype=np.uint8)
    ink_mask = bw < 128
    result[ink_mask] = ink_color

    if paper:
        paper_img = generate_paper_texture(w, h)
        result = cv2.addWeighted(result, 1 - paper_alpha, paper_img, paper_alpha, 0)

    if grain:
        rng = np.random.default_rng(7)
        result = np.clip(
            result.astype(np.float32) + rng.normal(0, 6, result.shape).astype(np.float32),
            0, 255,
        ).astype(np.uint8)

    # 输出 RGBA
    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[:, :, :3] = result
    if transparent:
        # 墨色区域不透明，纸色区域透明（去白）
        alpha = np.where(ink_mask, 255, 0).astype(np.uint8)
        out[:, :, 3] = alpha
    else:
        out[:, :, 3] = 255
    return out


def main():
    ap = argparse.ArgumentParser(description="复古版画/图章质感后处理管线")
    ap.add_argument("inputs", nargs="+", help="输入图片路径（可多个）")
    ap.add_argument("-o", "--out", default="out", help="输出目录（默认 out/）")
    ap.add_argument("--blur", type=int, default=9, help="中值滤波核，奇数，默认 9")
    ap.add_argument("--mode", default="otsu", choices=["otsu", "adaptive", "fixed"])
    ap.add_argument("--thresh", type=int, default=128, help="fixed 模式阈值")
    ap.add_argument("--invert", action="store_true", help="反相（白墨黑底）")
    ap.add_argument("--no-paper", action="store_true", help="关闭纸纹")
    ap.add_argument("--paper-alpha", type=float, default=0.35, help="纸纹强度 0~1")
    ap.add_argument("--no-grain", action="store_true", help="关闭颗粒")
    ap.add_argument("--transparent", action="store_true", help="去白透明底(PNG)")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    ok = 0
    for src in args.inputs:
        if not os.path.exists(src):
            print(f"SKIP: 不存在 {src}")
            continue
        img = load_image(src)
        if img is None:
            print(f"ERROR: 无法读取 {src}")
            continue
        result = retro_print(
            img,
            blur_ksize=args.blur,
            mode=args.mode,
            thresh_val=args.thresh,
            invert=args.invert,
            paper=not args.no_paper,
            paper_alpha=args.paper_alpha,
            grain=not args.no_grain,
            transparent=args.transparent,
        )
        stem = os.path.splitext(os.path.basename(src))[0]
        ext = "png" if args.transparent else "jpg"
        dst = os.path.join(args.out, f"{stem}_retro.{ext}")
        cv2.imwrite(dst, result)
        print(f"OK: {src} -> {dst}")
        ok += 1
    print(f"完成 {ok}/{len(args.inputs)} 张")


if __name__ == "__main__":
    main()
