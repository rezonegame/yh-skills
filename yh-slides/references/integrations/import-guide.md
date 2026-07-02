# 网页/视频/音频导入指南

## 概述

本指南描述如何从外部来源（网页、视频、音频）导入内容，转换为结构化幻灯片数据，然后接入标准 HTML 幻灯片生成流程。

**通用导入流程**:
```
外部来源 → 内容提取 → 结构化处理 → Step 1（内容结构化） → 标准流程
```

---

## 1. 网页导入

使用 Playwright 抓取网页内容，提取正文文本和图片，清理为结构化数据。

### 1.1 环境准备

```bash
pip install playwright beautifulsoup4 lxml
playwright install chromium
```

### 1.2 网页内容提取函数

```python
#!/usr/bin/env python3
"""
网页内容提取工具

功能：
- 使用 Playwright 加载网页
- 提取正文文本（去除导航、页脚等噪音）
- 提取正文图片
- 清理为结构化内容
"""

import asyncio
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from bs4 import BeautifulSoup


async def import_webpage(url: str, output_dir: str = None) -> dict[str, Any]:
    """
    从网页 URL 提取内容，转换为幻灯片结构。

    Args:
        url: 网页 URL
        output_dir: 输出目录

    Returns:
        结构化内容字典
    """
    from playwright.async_api import async_playwright

    if output_dir is None:
        parsed = urlparse(url)
        domain = parsed.netloc.replace(".", "_")
        output_dir = f"web_import_{domain}"

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 设置视口和 User-Agent
        await page.set_viewport_size({"width": 1280, "height": 800})
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception as e:
            print(f"页面加载失败: {e}")
            await browser.close()
            raise

        # 获取页面 HTML
        html_content = await page.content()

        # 提取页面元数据
        title = await page.title()
        meta_description = await page.evaluate("""
            () => {
                const meta = document.querySelector('meta[name="description"]');
                return meta ? meta.content : '';
            }
        """)

        # 提取正文 HTML
        article_html = await page.evaluate("""
            () => {
                // 尝试多种文章容器选择器
                const selectors = [
                    'article',
                    'main',
                    '[role="main"]',
                    '.post-content',
                    '.article-content',
                    '.entry-content',
                    '.content-body',
                    '#content',
                    '.markdown-body'
                ];

                for (const selector of selectors) {
                    const el = document.querySelector(selector);
                    if (el && el.innerText.length > 200) {
                        return el.innerHTML;
                    }
                }

                // 回退：提取 body，移除噪音元素
                const body = document.body.cloneNode(true);
                const noise = body.querySelectorAll(
                    'nav, header, footer, aside, .sidebar, .nav, .menu, ' +
                    '.comments, .comment, .ad, .advertisement, .social, ' +
                    '.share, .related, .recommend, .breadcrumb, ' +
                    'script, style, noscript, iframe'
                );
                noise.forEach(el => el.remove());
                return body.innerHTML;
            }
        """)

        await browser.close()

    # 使用 BeautifulSoup 解析
    soup = BeautifulSoup(article_html, "lxml")

    # 提取图片
    images = _extract_images(soup, url, assets_dir)

    # 提取结构化文本
    sections = _extract_sections(soup)

    # 构建结果
    result = {
        "source": "web",
        "url": url,
        "title": title,
        "description": meta_description,
        "sections": sections,
        "images": images,
        "total_images": len(images),
        "total_sections": len(sections)
    }

    # 保存结果
    output_json = output_dir / "extracted.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"网页导入完成: {title}")
    print(f"提取 {len(sections)} 个内容段落, {len(images)} 张图片")
    print(f"保存至: {output_dir}")

    return result


def _extract_images(soup: BeautifulSoup, base_url: str, assets_dir: Path) -> list[dict]:
    """
    从 HTML 中提取图片信息。

    注意：实际下载图片需要额外的异步处理，
    这里先收集图片 URL 和上下文信息。
    """
    images = []
    seen_urls = set()

    for img_tag in soup.find_all("img"):
        src = img_tag.get("src") or img_tag.get("data-src") or ""
        if not src:
            continue

        # 处理相对 URL
        if src.startswith("//"):
            src = "https:" + src
        elif src.startswith("/"):
            parsed = urlparse(base_url)
            src = f"{parsed.scheme}://{parsed.netloc}{src}"

        # 去重
        if src in seen_urls:
            continue
        seen_urls.add(src)

        # 跳过小图标和追踪像素
        width = int(img_tag.get("width", 0))
        height = int(img_tag.get("height", 0))
        if 0 < width < 50 or 0 < height < 50:
            continue
        if "icon" in src.lower() or "logo" in src.lower():
            continue
        if "pixel" in src.lower() or "tracker" in src.lower():
            continue

        alt_text = img_tag.get("alt", "")

        # 获取上下文：图片前后的文本
        parent = img_tag.find_parent(["p", "figure", "div"])
        context = ""
        if parent:
            context = parent.get_text(strip=True)[:200]

        images.append({
            "url": src,
            "alt": alt_text,
            "context": context,
            "filename": _generate_filename(src)
        })

    return images


def _extract_sections(soup: BeautifulSoup) -> list[dict]:
    """
    从 HTML 中提取结构化文本段落。
    """
    sections = []

    # 按 h2/h3 分段
    current_section = {
        "heading": "",
        "level": 0,
        "content": [],
        "lists": []
    }

    for element in soup.children:
        if isinstance(element, str):
            # 文本节点
            text = element.strip()
            if text:
                current_section["content"].append(text)
            continue

        tag = element.name

        if tag in ("h1", "h2", "h3", "h4"):
            # 保存上一个 section
            if current_section["content"] or current_section["lists"]:
                sections.append(current_section)

            current_section = {
                "heading": element.get_text(strip=True),
                "level": int(tag[1]),
                "content": [],
                "lists": []
            }

        elif tag == "p":
            text = element.get_text(strip=True)
            if text:
                current_section["content"].append(text)

        elif tag in ("ul", "ol"):
            items = [li.get_text(strip=True) for li in element.find_all("li")]
            if items:
                current_section["lists"].append({
                    "type": "ordered" if tag == "ol" else "unordered",
                    "items": items
                })

        elif tag == "blockquote":
            text = element.get_text(strip=True)
            if text:
                current_section["content"].append(f"> {text}")

        elif tag == "pre" or tag == "code":
            text = element.get_text(strip=True)
            if text:
                current_section["content"].append(f"```\n{text}\n```")

        elif tag == "figure":
            caption = element.find("figcaption")
            if caption:
                current_section["content"].append(
                    f"[图片: {caption.get_text(strip=True)}]"
                )

    # 保存最后一个 section
    if current_section["content"] or current_section["lists"]:
        sections.append(current_section)

    return sections


def _generate_filename(url: str) -> str:
    """从 URL 生成文件名"""
    parsed = urlparse(url)
    path = parsed.path
    name = Path(path).stem

    # 清理特殊字符
    name = re.sub(r'[^a-zA-Z0-9_\-\u4e00-\u9fff]', '_', name)
    if not name:
        name = "image"

    return f"{name}.jpg"


def convert_web_to_slides(extracted: dict) -> list[dict]:
    """
    将网页提取结果转换为幻灯片结构。

    Returns:
        幻灯片列表，每个元素包含 title、content、images 等字段
    """
    slides = []

    # 第一页：封面
    slides.append({
        "type": "cover",
        "title": extracted["title"],
        "subtitle": extracted["description"][:80] if extracted["description"] else "",
        "source_url": extracted["url"]
    })

    # 后续页：按章节分段
    for section in extracted["sections"]:
        if not section["heading"] and not section["content"]:
            continue

        # 判断幻灯片类型
        slide_type = "title-content"
        if section["lists"]:
            slide_type = "list"
        elif section["content"] and any("[图片:" in c for c in section["content"]):
            slide_type = "image-text"

        # 内容合并（限制每页字数）
        content_text = " ".join(section["content"])
        if len(content_text) > 500:
            # 拆分为多页
            chunks = _split_text(content_text, 400)
            for i, chunk in enumerate(chunks):
                is_first = i == 0
                slides.append({
                    "type": slide_type,
                    "title": section["heading"] if is_first else "",
                    "content": chunk,
                    "lists": section["lists"] if is_first else [],
                    "source_url": extracted["url"]
                })
        else:
            slides.append({
                "type": slide_type,
                "title": section["heading"],
                "content": content_text,
                "lists": section.get("lists", []),
                "source_url": extracted["url"]
            })

    return slides


def _split_text(text: str, max_length: int) -> list[str]:
    """按句子拆分长文本"""
    sentences = re.split(r'(?<=[。！？\n])', text)
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) > max_length:
            if current:
                chunks.append(current.strip())
            current = sentence
        else:
            current += sentence

    if current.strip():
        chunks.append(current.strip())

    return chunks


# ==================== 命令行入口 ====================
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python import_web.py <URL> [输出目录]")
        sys.exit(1)

    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None

    result = asyncio.run(import_webpage(url, output))
    slides = convert_web_to_slides(result)

    print(f"\n转换为 {len(slides)} 张幻灯片:")
    for i, slide in enumerate(slides):
        title = slide.get("title", "(无标题)")
        print(f"  #{i+1} [{slide['type']}] {title[:40]}")
```

### 1.3 网页导入输出结构

```json
{
  "source": "web",
  "url": "input/article.html",
  "title": "文章标题",
  "description": "文章描述",
  "sections": [
    {
      "heading": "章节标题",
      "level": 2,
      "content": ["段落文本...", "引用文本..."],
      "lists": [
        {
          "type": "unordered",
          "items": ["要点一", "要点二", "要点三"]
        }
      ]
    }
  ],
  "images": [
    {
      "url": "input/images/photo.jpg",
      "alt": "图片描述",
      "context": "上下文文本",
      "filename": "photo.jpg"
    }
  ]
}
```

---

## 2. 视频导入

从视频文件中提取音频、转录为文本，然后生成幻灯片大纲。

### 2.1 环境准备

```bash
# 音频提取
pip install ffmpeg-python

# 语音转文本（选择一个）
# 方案 A: OpenAI Whisper（本地运行）
pip install openai-whisper

# 方案 B: 使用 OpenAI API
pip install openai

# 关键帧提取
pip install opencv-python
```

### 2.2 视频内容提取函数

```python
#!/usr/bin/env python3
"""
视频内容提取工具

功能：
- 从视频中提取音频
- 使用 Whisper 转录为文本
- 从转录文本生成幻灯片大纲
- 提取关键帧作为幻灯片图片
"""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any


def import_video(video_path: str, output_dir: str = None) -> dict[str, Any]:
    """
    从视频文件中提取内容，转换为幻灯片结构。

    Args:
        video_path: 视频文件路径
        output_dir: 输出目录

    Returns:
        结构化内容字典
    """
    video_path = Path(video_path)
    if not video_path.exists():
        raise FileNotFoundError(f"视频文件不存在: {video_path}")

    if output_dir is None:
        output_dir = f"video_import_{video_path.stem}"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    # Step 1: 提取音频
    audio_path = _extract_audio(video_path, assets_dir)

    # Step 2: 转录文本
    transcript = _transcribe_audio(audio_path)

    # Step 3: 提取关键帧
    keyframes = _extract_keyframes(video_path, assets_dir)

    # Step 4: 生成幻灯片大纲
    slides = _generate_outline_from_transcript(transcript)

    # Step 5: 关联关键帧到幻灯片
    _assign_keyframes_to_slides(slides, keyframes)

    result = {
        "source": "video",
        "video_path": str(video_path),
        "title": video_path.stem,
        "transcript": transcript,
        "keyframes": keyframes,
        "slides": slides,
        "total_slides": len(slides),
        "audio_path": str(audio_path)
    }

    # 保存结果
    output_json = output_dir / "extracted.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"视频导入完成: {video_path.name}")
    print(f"转录时长: {len(transcript) / 1000:.1f} 秒")
    print(f"生成 {len(slides)} 张幻灯片, {len(keyframes)} 个关键帧")
    print(f"保存至: {output_dir}")

    return result


def _extract_audio(video_path: Path, output_dir: Path) -> Path:
    """
    使用 ffmpeg 从视频中提取音频。
    """
    audio_path = output_dir / "audio.mp3"

    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-vn",                    # 无视频
        "-acodec", "libmp3lame",  # MP3 编码
        "-ab", "160k",            # 比特率
        "-ar", "44100",           # 采样率
        "-y",                     # 覆盖输出
        str(audio_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"音频提取失败: {result.stderr}")

    print(f"音频已提取: {audio_path}")
    return audio_path


def _transcribe_audio(audio_path: Path) -> str:
    """
    使用 Whisper 将音频转录为文本。

    优先使用本地 Whisper（免费），回退到 OpenAI API。
    """
    try:
        import whisper

        print("使用本地 Whisper 转录...")
        model = whisper.load_model("base")  # base 模型平衡速度和精度
        result = model.transcribe(str(audio_path), language="zh")
        return result["text"]

    except ImportError:
        pass

    try:
        from openai import OpenAI

        print("使用 OpenAI Whisper API 转录...")
        client = OpenAI()

        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="zh",
                response_format="verbose_json"
            )

        return transcript.text

    except Exception as e:
        raise RuntimeError(f"转录失败: {e}。请安装 whisper 或配置 OpenAI API key。)


def _extract_keyframes(video_path: Path, output_dir: Path, interval: int = 30) -> list[dict]:
    """
    使用 ffmpeg 每隔 N 秒提取一帧关键帧。

    Args:
        video_path: 视频文件路径
        output_dir: 输出目录
        interval: 提取间隔（秒）

    Returns:
        关键帧信息列表
    """
    keyframes_dir = output_dir / "keyframes"
    keyframes_dir.mkdir(exist_ok=True)

    # 获取视频时长
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]
    duration_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    duration = float(duration_result.stdout.strip())

    # 计算提取时间点
    timestamps = list(range(0, int(duration), interval))
    if timestamps[-1] < duration - 5:
        timestamps.append(int(duration))

    keyframes = []
    for i, ts in enumerate(timestamps):
        output_path = keyframes_dir / f"frame_{ts:04d}.jpg"
        cmd = [
            "ffmpeg", "-ss", str(ts),
            "-i", str(video_path),
            "-vframes", "1",
            "-q:v", "2",
            "-y",
            str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            keyframes.append({
                "timestamp": ts,
                "filename": f"keyframes/frame_{ts:04d}.jpg",
                "filepath": str(output_path)
            })

    return keyframes


def _generate_outline_from_transcript(transcript: str) -> list[dict]:
    """
    从转录文本中生成幻灯片大纲。

    策略：
    1. 按句子分段
    2. 每组 3-5 句作为一页幻灯片
    3. 提取关键词作为标题
    """
    # 分句
    sentences = re.split(r'(?<=[。！？.!?\n])\s*', transcript)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]

    # 按语义分组（每页 3-5 句）
    slides = []
    current_content = []
    current_length = 0
    max_length = 200  # 每页最大字符数

    for sentence in sentences:
        if current_length + len(sentence) > max_length and current_content:
            # 生成幻灯片
            slide = _create_slide_from_sentences(current_content)
            slides.append(slide)
            current_content = []
            current_length = 0

        current_content.append(sentence)
        current_length += len(sentence)

    # 最后一组
    if current_content:
        slide = _create_slide_from_sentences(current_content)
        slides.append(slide)

    return slides


def _create_slide_from_sentences(sentences: list[str]) -> dict:
    """
    从一组句子创建幻灯片数据。
    """
    full_text = " ".join(sentences)

    # 提取标题：第一句话的前 20 个字符，或在标点处截断
    first_sentence = sentences[0]
    title_match = re.match(r'^(.{5,25}?)[，。！？,!?]', first_sentence)
    title = title_match.group(1) if title_match else first_sentence[:20]

    return {
        "type": "title-content",
        "title": title,
        "content": full_text,
        "keyframe": None,
        "timestamp_start": None,
        "timestamp_end": None
    }


def _assign_keyframes_to_slides(slides: list[dict], keyframes: list[dict]) -> None:
    """
    将关键帧分配给幻灯片（基于时间戳均匀分配）。
    """
    if not keyframes or not slides:
        return

    frames_per_slide = max(1, len(keyframes) // len(slides))

    for i, slide in enumerate(slides):
        start_idx = i * frames_per_slide
        end_idx = start_idx + frames_per_slide

        if start_idx < len(keyframes):
            slide["keyframe"] = keyframes[start_idx]["filename"]
            slide["timestamp_start"] = keyframes[start_idx]["timestamp"]

        if end_idx < len(keyframes):
            slide["timestamp_end"] = keyframes[end_idx]["timestamp"]
        elif keyframes:
            slide["timestamp_end"] = keyframes[-1]["timestamp"]
```

---

## 3. 音频导入

从纯音频文件中提取内容，适用于播客、录音、讲座等场景。

### 3.1 环境准备

```bash
# 语音转文本
pip install openai-whisper

# 或者使用 Edge TTS（从文本生成语音，反向场景）
pip install edge-tts
```

### 3.2 音频内容提取函数

```python
#!/usr/bin/env python3
"""
音频内容提取工具

功能：
- 转录音频为文本
- 生成幻灯片大纲
- 支持长音频分段处理
"""

import json
from pathlib import Path
from typing import Any


def import_audio(audio_path: str, output_dir: str = None) -> dict[str, Any]:
    """
    从音频文件中提取内容，转换为幻灯片结构。

    Args:
        audio_path: 音频文件路径（mp3, wav, m4a, flac）
        output_dir: 输出目录

    Returns:
        结构化内容字典
    """
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")

    if output_dir is None:
        output_dir = f"audio_import_{audio_path.stem}"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: 转录
    transcript = _transcribe(audio_path)

    # Step 2: 生成大纲
    slides = _generate_outline(transcript)

    result = {
        "source": "audio",
        "audio_path": str(audio_path),
        "title": audio_path.stem,
        "transcript": transcript,
        "slides": slides,
        "total_slides": len(slides)
    }

    # 保存
    output_json = output_dir / "extracted.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"音频导入完成: {audio_path.name}")
    print(f"生成 {len(slides)} 张幻灯片")

    return result


def _transcribe(audio_path: Path) -> str:
    """
    转录音频文件为文本。
    """
    try:
        import whisper

        print("使用本地 Whisper 转录...")
        model = whisper.load_model("base")
        result = model.transcribe(str(audio_path), language="zh")

        # 如果有分段信息，返回完整文本
        return result["text"]

    except ImportError:
        from openai import OpenAI

        print("使用 OpenAI Whisper API 转录...")
        client = OpenAI()

        # 大文件需要分段上传（OpenAI 限制 25MB）
        file_size = audio_path.stat().st_size
        max_size = 25 * 1024 * 1024  # 25MB

        if file_size > max_size:
            print(f"文件较大 ({file_size / 1024 / 1024:.1f}MB)，使用 ffmpeg 分段...")
            return _transcribe_large_audio(audio_path, client)

        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="zh"
            )

        return transcript.text


def _transcribe_large_audio(audio_path: Path, client) -> str:
    """
    分段转录大音频文件。
    """
    import subprocess
    import tempfile

    segments_dir = Path(tempfile.mkdtemp())
    full_text = []

    # 分段：每 10 分钟
    segment_duration = 600  # 秒

    # 获取总时长
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    result = subprocess.run(probe_cmd, capture_output=True, text=True)
    total_duration = float(result.stdout.strip())

    # 分段提取
    segment = 0
    start_time = 0

    while start_time < total_duration:
        segment_path = segments_dir / f"segment_{segment:03d}.mp3"
        cmd = [
            "ffmpeg", "-ss", str(start_time),
            "-t", str(segment_duration),
            "-i", str(audio_path),
            "-acodec", "libmp3lame",
            "-y", str(segment_path)
        ]
        subprocess.run(cmd, capture_output=True, text=True)

        # 转录分段
        with open(segment_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="zh"
            )
        full_text.append(transcript.text)

        start_time += segment_duration
        segment += 1

    # 清理临时文件
    import shutil
    shutil.rmtree(segments_dir, ignore_errors=True)

    return " ".join(full_text)


def _generate_outline(transcript: str) -> list[dict]:
    """
    从转录文本生成幻灯片大纲（与视频导入共享逻辑）。
    """
    import re

    sentences = re.split(r'(?<=[。！？.!?\n])\s*', transcript)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]

    slides = []
    current_content = []
    current_length = 0
    max_length = 200

    for sentence in sentences:
        if current_length + len(sentence) > max_length and current_content:
            first = sentences[0] if sentences else ""
            title_match = re.match(r'^(.{5,25}?)[，。！？,!?]', first)
            title = title_match.group(1) if title_match else first[:20]

            slides.append({
                "type": "title-content",
                "title": title,
                "content": " ".join(current_content)
            })

            current_content = []
            current_length = 0

        current_content.append(sentence)
        current_length += len(sentence)

    if current_content:
        first = current_content[0]
        title_match = re.match(r'^(.{5,25}?)[，。！？,!?]', first)
        title = title_match.group(1) if title_match else first[:20]

        slides.append({
            "type": "title-content",
            "title": title,
            "content": " ".join(current_content)
        })

    return slides
```

---

## 4. 通用导入流程

### 4.1 流程图

```
┌─────────────────────────────────────────────────┐
│                   用户输入                        │
│          (URL / 视频文件 / 音频文件)               │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │   检测输入类型        │
          └──────────┬───────────┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
 ┌─────────┐  ┌──────────┐  ┌──────────┐
 │  网页    │  │  视频     │  │  音频    │
 │  导入    │  │  导入     │  │  导入    │
 └────┬────┘  └────┬─────┘  └────┬─────┘
      │            │              │
      ▼            ▼              ▼
 ┌─────────┐  ┌──────────┐  ┌──────────┐
 │ Playwright│ │ ffmpeg + │  │ Whisper  │
 │ + BS4    │  │ Whisper  │  │ 转录     │
 └────┬────┘  └────┬─────┘  └────┬─────┘
      │            │              │
      └────────────┼──────────────┘
                   │
                   ▼
          ┌──────────────────────┐
          │  结构化内容 (JSON)    │
          │  - 标题 / 章节        │
          │  - 正文文本           │
          │  - 图片              │
          │  - 关键帧            │
          └──────────┬───────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  内容确认（用户交互）   │
          │  - 查看提取结果        │
          │  - 调整分段           │
          │  - 确认幻灯片数量      │
          └──────────┬───────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  Step 1: 内容结构化   │
          │  → Step 2: 设计风格   │
          │  → Step 3: HTML 生成  │
          └──────────────────────┘
```

### 4.2 统一内容格式

所有导入源最终输出为统一的 `extracted.json` 格式：

```json
{
  "source": "web | video | audio",
  "source_info": {
    "url": "...",
    "file_path": "...",
    "duration": "..."
  },
  "title": "演示文稿标题",
  "description": "描述文本",
  "slides": [
    {
      "index": 1,
      "type": "cover | title-content | image-text | data | list",
      "title": "幻灯片标题",
      "content": "正文内容",
      "images": ["image_filename.jpg"],
      "keyframe": "keyframe_0030.jpg",
      "notes": "演讲者备注"
    }
  ],
  "assets": {
    "images": ["assets/img1.jpg", "assets/img2.jpg"],
    "keyframes": ["assets/keyframes/frame_0000.jpg"],
    "audio": "assets/audio.mp3"
  }
}

### 4.3 路由到标准流程

导入完成并经用户确认后，进入标准 HTML 幻灯片流程：

| 标准步骤 | 导入后的对应动作 |
|----------|-----------------|
| Step 1: 内容结构化 | 直接使用导入的 JSON 数据，跳过手动输入 |
| Step 2: 设计风格 | 正常执行，选择设计风格 |
| Step 3: HTML 生成 | 正常执行，使用导入的内容和选定的风格 |

### 4.4 依赖安装汇总

```bash
# 所有导入功能的完整依赖
pip install \
  playwright \
  beautifulsoup4 \
  lxml \
  ffmpeg-python \
  opencv-python \
  Pillow \
  openai-whisper \
  python-pptx

# 安装 Playwright 浏览器
playwright install chromium

# ffmpeg 需要系统安装
# Windows: winget install Gyan.FFmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```
