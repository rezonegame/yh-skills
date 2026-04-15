#!/usr/bin/env python3
"""
yh-slides 内置图片工具集（v2 — 增强稳定性版）。

支持:
- generate: 文生图 (Gemini 3.1 Flash Image / Imagen 4.0)
- edit: 基于现有图片 + 自然语言指令进行编辑
- extract-style: 从参考图提取风格描述
- clean-bg: 从生成图中去除文字提取干净背景
- batch: 从 JSON 任务文件批量顺序生成（带冷却/重试/断点续传）

API Key 来源:
1. --api-key 参数
2. GEMINI_API_KEY 环境变量
3. .env 文件 (当前目录及父目录)
4. yh-slides 技能目录下的 .env 文件

稳定性设计:
- 所有 API 调用均带指数退避 + 抖动的统一重试引擎
- 429 速率限制自动读取 Retry-After header
- 500/502/503 服务端错误自动重试
- 超时自动增加 timeout 时长重试
- 连接错误等待后重试
- 批量模式自适应冷却：失败后自动加倍间隔
"""

import sys
import json
import base64
import argparse
import os
import time
import random
from pathlib import Path
from typing import Optional

try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def _check_requests():
    """确保 requests 库已安装。"""
    if not HAS_REQUESTS:
        print("错误: 需要安装 requests 库。运行: pip install requests")
        sys.exit(1)


# ─── API Key 查找 ───────────────────────────────────────────────


def find_api_key() -> Optional[str]:
    """从多个来源查找 API Key。

    优先级（从高到低）：
    1. 环境变量 GEMINI_API_KEY
    2. --api-key 参数（由调用方在 _require_api_key 中处理）
    3. yh-slides 技能目录下的 .env（最优先，技能专用 key）
    4. ~/.claude/.env（用户全局配置）
    5. 当前工作目录及父目录的 .env
    """
    # 1. 环境变量
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key

    # 2. 技能目录下的 .env（最优先，技能专用 key）
    skill_dir = Path(__file__).resolve().parent.parent
    env_file = skill_dir / ".env"
    if env_file.exists():
        api_key = _read_env_key(env_file)
        if api_key:
            return api_key

    # 3. 用户全局 ~/.claude/.env
    home_env = Path.home() / ".claude" / ".env"
    if home_env.exists():
        api_key = _read_env_key(home_env)
        if api_key:
            return api_key

    # 4. 当前工作目录及父目录（最低优先级）
    current_dir = Path.cwd()
    for parent in [current_dir] + list(current_dir.parents):
        env_file = parent / ".env"
        if env_file.exists():
            api_key = _read_env_key(env_file)
            if api_key:
                return api_key

    return None


def _read_env_key(env_file: Path) -> Optional[str]:
    with open(env_file, "r") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                if key:
                    return key
    return None


def _require_api_key(api_key: Optional[str]) -> str:
    if not api_key:
        api_key = find_api_key()
    if not api_key:
        print("错误: 未找到 GEMINI_API_KEY!")
        print("请通过以下方式之一配置:")
        print("  1. 传递 --api-key 参数")
        print("  2. 设置 GEMINI_API_KEY 环境变量")
        print("  3. 在项目目录创建 .env 文件")
        print("  4. 获取 API Key: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    return api_key


# ─── 重试引擎 ─────────────────────────────────────────────────


class _RetryableError(Exception):
    """信号：当前操作应当重试。可选 delay_hint 建议等待时长。"""

    def __init__(self, message, delay_hint=None):
        super().__init__(message)
        self.delay_hint = delay_hint


class _FatalError(Exception):
    """信号：当前操作不应重试（客户端错误、安全过滤等）。"""

    pass


def _with_retry(fn, description, max_retries=3, base_delay=5.0, max_delay=120.0):
    """带指数退避 + 抖动的统一重试引擎。

    fn(attempt_number) 应当:
      - 返回结果（表示成功）
      - 抛出 _RetryableError（可重试的错误，可附带 delay_hint）
      - 抛出 _FatalError（不可重试的错误）
      - 抛出 requests.Timeout / requests.ConnectionError（自动重试）
    """
    for attempt in range(1, max_retries + 1):
        try:
            suffix = f" (重试 {attempt}/{max_retries})" if attempt > 1 else ""
            print(f"{description}{suffix}")
            result = fn(attempt)
            return result

        except _RetryableError as e:
            if attempt >= max_retries:
                print(f"❌ {description}: 达到最大重试次数 ({max_retries})")
                return None
            # 使用 delay_hint（如 Retry-After）或指数退避
            if e.delay_hint:
                delay = min(e.delay_hint, max_delay)
            else:
                delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            jitter = delay * random.uniform(0, 0.3)
            total_delay = delay + jitter
            print(f"  ↳ {e}，等待 {total_delay:.1f}s 后重试...")
            time.sleep(total_delay)

        except _FatalError as e:
            print(f"❌ {description}: {e}")
            return None

        except requests.exceptions.Timeout:
            if attempt >= max_retries:
                print(f"❌ {description}: 请求超时，已达最大重试次数")
                return None
            timeout_delay = 5 + attempt * 3
            print(f"  ↳ 请求超时，等待 {timeout_delay}s 后重试...")
            time.sleep(timeout_delay)

        except requests.exceptions.ConnectionError:
            if attempt >= max_retries:
                print(f"❌ {description}: 连接失败，已达最大重试次数")
                return None
            print(f"  ↳ 连接错误，等待 10s 后重试...")
            time.sleep(10)

        except Exception as e:
            print(f"❌ {description} 异常: {e}")
            return None

    return None


def _handle_http_status(response, description="API调用"):
    """检查 HTTP 状态码，成功返回 JSON，否则抛出重试/致命错误。"""
    status = response.status_code

    if status == 200:
        return response.json()

    elif status == 429:
        # 速率限制 — 尝试读取 Retry-After header
        retry_after_raw = response.headers.get("Retry-After")
        try:
            delay = float(retry_after_raw)
        except (TypeError, ValueError):
            delay = 15.0
        raise _RetryableError(
            f"速率限制 (429)", delay_hint=max(delay, 10.0)
        )

    elif status >= 500:
        raise _RetryableError(
            f"服务端错误 ({status})", delay_hint=8.0
        )

    else:
        # 400, 401, 403 等客户端错误 — 不重试
        raise _FatalError(
            f"API 错误 ({status}): {response.text[:300]}"
        )


# ─── 图片生成 (generate) ───────────────────────────────────────


def generate_with_gemini(
    prompt: str,
    api_key: str,
    output_path: str = "generated_image.png",
    aspect_ratio: str = "16:9",
    image_size: str = "2K",
    max_retries: int = 3,
) -> bool:
    """使用 Gemini 3.1 Flash Image 生成图片，带完整重试逻辑。"""
    _check_requests()

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-3.1-flash-image-preview:generateContent?key={api_key}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": image_size,
            },
        },
    }

    def _attempt(attempt_num):
        # 每次重试增加 timeout，防止大图生成超时
        timeout = 180 + (attempt_num - 1) * 60
        response = requests.post(url, json=payload, timeout=timeout)
        result = _handle_http_status(response, "Gemini 生成")

        # 检查安全过滤
        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            finish_reason = candidate.get("finishReason", "")
            if finish_reason == "SAFETY":
                raise _FatalError("图片被安全过滤器阻止，请修改提示词")

            if "content" in candidate and "parts" in candidate["content"]:
                for part in candidate["content"]["parts"]:
                    if "inlineData" in part:
                        image_b64 = part["inlineData"].get("data")
                        if image_b64:
                            _save_image(base64.b64decode(image_b64), output_path)
                            print(f"✅ 已保存: {output_path}")
                            return True

        # 200 但无图片数据 — 暂时性问题，重试
        raise _RetryableError("响应中没有图片数据", delay_hint=5.0)

    result = _with_retry(
        _attempt, "Gemini 3.1 Flash Image 生成中", max_retries
    )
    return bool(result)


def generate_with_imagen(
    prompt: str,
    api_key: str,
    output_path: str = "generated_image.png",
    aspect_ratio: str = "1:1",
    max_retries: int = 3,
) -> bool:
    """使用 Imagen 4.0 生成图片，带完整重试逻辑。"""
    _check_requests()

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/imagen-4.0-generate-001:predict?key={api_key}"
    )

    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "aspectRatio": aspect_ratio,
            "sampleCount": 1,
            "safetyFilterLevel": "block_some",
        },
    }

    def _attempt(attempt_num):
        timeout = 60 + (attempt_num - 1) * 30
        response = requests.post(url, json=payload, timeout=timeout)
        result = _handle_http_status(response, "Imagen 生成")

        if "images" in result and len(result["images"]) > 0:
            image_b64 = result["images"][0].get("imageBytes")
            if image_b64:
                _save_image(base64.b64decode(image_b64), output_path)
                print(f"✅ 已保存: {output_path}")
                return True

        raise _RetryableError("响应中没有图片数据", delay_hint=5.0)

    result = _with_retry(
        _attempt, "Imagen 4.0 生成中", max_retries
    )
    return bool(result)


def generate_image(
    prompt: str,
    model: str = "gemini",
    output_path: str = "generated_image.png",
    api_key: Optional[str] = None,
    aspect_ratio: str = "16:9",
    image_size: str = "2K",
    max_retries: int = 3,
    cooldown: float = 0,
) -> bool:
    """统一入口：生成图片，支持 Gemini → Imagen 自动降级。"""
    api_key = _require_api_key(api_key)

    success = False
    if model == "gemini":
        success = generate_with_gemini(
            prompt, api_key, output_path, aspect_ratio, image_size, max_retries
        )
        if not success:
            print("⚠️ Gemini 生成失败，尝试 Imagen 4.0 备用方案...")
            success = generate_with_imagen(
                prompt, api_key, output_path, aspect_ratio, max_retries
            )
    elif model == "imagen":
        success = generate_with_imagen(
            prompt, api_key, output_path, aspect_ratio, max_retries
        )
    else:
        print(f"未知模型: {model}")
        return False

    # 生成后冷却，防止连续调用触发限速
    if success and cooldown > 0:
        print(f"⏳ 冷却等待 {cooldown:.0f}s...")
        time.sleep(cooldown)

    return success


# ─── 图片编辑 (edit) ────────────────────────────────────────────


def edit_image(
    edit_instruction: str,
    image_path: str,
    output_path: str = "edited_image.png",
    api_key: Optional[str] = None,
    max_retries: int = 3,
) -> bool:
    """基于现有图片 + 自然语言指令进行编辑（Gemini 多模态），带完整重试。"""
    api_key = _require_api_key(api_key)
    _check_requests()

    image_b64 = _load_image_base64(image_path)
    if not image_b64:
        return False

    mime_type = _guess_mime_type(image_path)

    prompt = (
        f"根据以下指令修改这张PPT页面：{edit_instruction}\n"
        f"保持原有的内容结构和设计风格，只按照指令进行修改。"
    )

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-3.1-flash-image-preview:generateContent?key={api_key}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"inlineData": {"mimeType": mime_type, "data": image_b64}},
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
        },
    }

    def _attempt(attempt_num):
        timeout = 120 + (attempt_num - 1) * 60
        response = requests.post(url, json=payload, timeout=timeout)
        result = _handle_http_status(response, "图片编辑")

        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                for part in candidate["content"]["parts"]:
                    if "inlineData" in part:
                        img_b64 = part["inlineData"].get("data")
                        if img_b64:
                            _save_image(base64.b64decode(img_b64), output_path)
                            print(f"✅ 已保存: {output_path}")
                            return True

        raise _RetryableError("响应中没有图片数据", delay_hint=5.0)

    short_desc = edit_instruction[:40] + ("..." if len(edit_instruction) > 40 else "")
    result = _with_retry(
        _attempt, f"图片编辑: {short_desc}", max_retries
    )
    return bool(result)


# ─── 风格提取 (extract-style) ───────────────────────────────────


def extract_style(
    image_path: str,
    api_key: Optional[str] = None,
    max_retries: int = 2,
) -> Optional[str]:
    """从参考图片提取风格描述，带完整重试。"""
    api_key = _require_api_key(api_key)
    _check_requests()

    image_b64 = _load_image_base64(image_path)
    if not image_b64:
        return None

    mime_type = _guess_mime_type(image_path)

    prompt = (
        "你是一位专业的 PPT 设计分析师。分析这张图片并提取详细的风格描述，"
        "用于生成具有相似视觉风格的 PPT 幻灯片。\n\n"
        "重点关注：\n"
        "1. 色板：主色、辅色、强调色、背景色\n"
        "2. 字体风格：印象（衬线/无衬线、粗细、字号层级）\n"
        "3. 设计元素：装饰图案、形状、图标风格、边框、阴影\n"
        "4. 整体情绪：专业、活泼、极简、商务、创意等\n"
        "5. 布局倾向：内容排列方式、间距偏好\n\n"
        "输出一段简洁的中文风格描述，可直接用作 PPT 生成的风格提示词。"
    )

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-2.5-flash:generateContent?key={api_key}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"inlineData": {"mimeType": mime_type, "data": image_b64}},
                ]
            }
        ],
    }

    def _attempt(attempt_num):
        timeout = 60 + (attempt_num - 1) * 30
        response = requests.post(url, json=payload, timeout=timeout)
        result = _handle_http_status(response, "风格提取")

        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                for part in candidate["content"]["parts"]:
                    if "text" in part:
                        style_desc = part["text"]
                        print(f"\n--- 风格描述 ---\n{style_desc}\n")
                        return style_desc

        raise _RetryableError("响应中没有文本数据", delay_hint=3.0)

    return _with_retry(_attempt, "风格提取中", max_retries)


# ─── 背景提取 (clean-bg) ────────────────────────────────────────


def clean_background(
    image_path: str,
    output_path: str = "clean_bg.png",
    api_key: Optional[str] = None,
    max_retries: int = 3,
) -> bool:
    """从生成图中去除文字和插画，保留干净背景，带完整重试。"""
    api_key = _require_api_key(api_key)
    _check_requests()

    image_b64 = _load_image_base64(image_path)
    if not image_b64:
        return False

    mime_type = _guess_mime_type(image_path)

    prompt = (
        "你是一位专业的图片文字&图片擦除专家。你的任务是从原始图片中移除文字和配图，"
        "输出一张无任何文字和图表内容、干净纯净的底板图。\n"
        "<requirements>\n"
        "- 彻底移除页面中的所有文字、插画、图表。必须确保所有文字都被完全去除。\n"
        "- 保持原背景设计的完整性（包括渐变、纹理、图案、线条、色块等）。保留原图的文本框和色块。\n"
        "- 对于被前景元素遮挡的背景区域，要智能填补，使背景保持无缝和完整。\n"
        "- 输出图片的尺寸、风格、配色必须和原图完全一致。\n"
        "- 请勿新增任何元素。\n"
        "</requirements>\n\n"
        "注意，**任意位置的, 所有的**文字和图表都应该被彻底移除，"
        "**输出不应该包含任何文字和图表。**"
    )

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-3.1-flash-image-preview:generateContent?key={api_key}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"inlineData": {"mimeType": mime_type, "data": image_b64}},
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
        },
    }

    def _attempt(attempt_num):
        timeout = 120 + (attempt_num - 1) * 60
        response = requests.post(url, json=payload, timeout=timeout)
        result = _handle_http_status(response, "背景提取")

        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                for part in candidate["content"]["parts"]:
                    if "inlineData" in part:
                        img_b64 = part["inlineData"].get("data")
                        if img_b64:
                            _save_image(base64.b64decode(img_b64), output_path)
                            print(f"✅ 已保存: {output_path}")
                            return True

        raise _RetryableError("响应中没有图片数据", delay_hint=5.0)

    result = _with_retry(_attempt, "背景提取中", max_retries)
    return bool(result)


# ─── 批量生成 (batch) ───────────────────────────────────────────


def batch_generate(
    tasks_file: str,
    cooldown: float = 8.0,
    max_retries: int = 5,
    skip_existing: bool = False,
    model: str = "gemini",
    api_key: Optional[str] = None,
    image_size: str = "2K",
    aspect_ratio: str = "16:9",
) -> bool:
    """从 JSON 任务文件批量顺序生成图片。

    严格顺序执行，一张完成后再生成下一张。
    自适应冷却：连续失败时自动加倍间隔，成功后恢复。
    断点续传：使用 skip_existing 跳过已存在的文件。

    tasks.json 格式:
    [
      {"prompt": "描述", "output": "slide-01.png"},
      {"prompt": "描述", "output": "slide-02.png", "image_size": "2K", "model": "gemini"}
    ]
    """
    api_key = _require_api_key(api_key)

    # 读取任务文件
    try:
        with open(tasks_file, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        print(f"错误: 任务文件不存在: {tasks_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"错误: 任务文件 JSON 格式错误: {e}")
        return False

    if not isinstance(tasks, list):
        print('错误: tasks.json 应为数组格式 [{"prompt":..., "output":...}, ...]')
        return False

    if not tasks:
        print("警告: 任务文件为空")
        return True

    total = len(tasks)
    success_count = 0
    fail_count = 0
    skip_count = 0
    failed_tasks = []
    adaptive_cooldown = cooldown

    print(f"\n{'='*60}")
    print(f"📦 批量生成: 共 {total} 张图片")
    print(f"   模型: {model} | 图片尺寸: {image_size}")
    print(f"   冷却间隔: {cooldown}s | 最大重试: {max_retries}")
    print(f"   跳过已存在: {'是' if skip_existing else '否'}")
    print(f"{'='*60}\n")

    for i, task in enumerate(tasks, 1):
        prompt = task.get("prompt", "")
        output = task.get("output", f"slide-{i:02d}.png")
        task_size = task.get("image_size", image_size)
        task_ratio = task.get("aspect_ratio", aspect_ratio)
        task_model = task.get("model", model)

        # 验证 prompt
        if not prompt:
            print(f"[{i}/{total}] ⚠️ 跳过: 无 prompt")
            skip_count += 1
            continue

        # 断点续传：跳过已存在文件
        if skip_existing and Path(output).exists():
            print(f"[{i}/{total}] ⏭️ 跳过已存在: {output}")
            skip_count += 1
            continue

        # 生成
        print(f"\n[{i}/{total}] 🎨 生成中: {output}")
        print(f"  Prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")

        success = generate_image(
            prompt=prompt,
            model=task_model,
            output_path=output,
            api_key=api_key,
            aspect_ratio=task_ratio,
            image_size=task_size,
            max_retries=max_retries,
        )

        if success:
            success_count += 1
            adaptive_cooldown = cooldown  # 成功后恢复正常冷却
        else:
            fail_count += 1
            failed_tasks.append({"index": i, "output": output, "prompt": prompt[:60]})
            # 自适应冷却：失败后加倍，上限 120s
            adaptive_cooldown = min(adaptive_cooldown * 2, 120)
            print(f"  ⚠️ 生成失败，冷却增大至 {adaptive_cooldown:.0f}s")

        # 图片间冷却（最后一张跳过）
        if i < total:
            actual_cooldown = adaptive_cooldown
            print(f"  ⏳ 冷却 {actual_cooldown:.0f}s...")
            time.sleep(actual_cooldown)

    # 汇总报告
    print(f"\n{'='*60}")
    print(f"📊 批量生成完成")
    print(f"   ✅ 成功: {success_count}/{total}")
    print(f"   ❌ 失败: {fail_count}/{total}")
    if skip_count:
        print(f"   ⏭️ 跳过: {skip_count}/{total}")
    if failed_tasks:
        print(f"\n   失败列表:")
        for ft in failed_tasks:
            print(f"   [{ft['index']}] {ft['output']} — {ft['prompt']}...")
    print(f"{'='*60}\n")

    return fail_count == 0


# ─── 工具函数 ────────────────────────────────────────────────────


def _save_image(image_bytes: bytes, output_path: str) -> None:
    output_dir = Path(output_path).parent
    if output_dir and str(output_dir) != "." and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(image_bytes)


def _load_image_base64(image_path: str) -> Optional[str]:
    path = Path(image_path)
    if not path.exists():
        print(f"错误: 图片文件不存在: {image_path}")
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _guess_mime_type(image_path: str) -> str:
    suffix = Path(image_path).suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    return mime_map.get(suffix, "image/png")


# ─── CLI 入口 ───────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="yh-slides 内置图片工具集（v2 增强稳定性版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
子命令:
  generate        文生图 (默认 Gemini → Imagen 降级)
  edit            基于图片 + 指令进行编辑
  extract-style   从参考图提取风格描述
  clean-bg        去除文字提取干净背景
  batch           从 JSON 任务文件批量顺序生成

示例:
  python generate_image.py generate "A sunset over mountains" --cooldown 5
  python generate_image.py edit --image slide.png --prompt "把饼图换成柱状图"
  python generate_image.py extract-style --image reference.png
  python generate_image.py clean-bg --image slide.png -o bg.png
  python generate_image.py batch --tasks slides.json --cooldown 8 --skip-existing
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # ── generate ──
    gen_parser = subparsers.add_parser("generate", help="文生图")
    gen_parser.add_argument("prompt", help="图片描述")
    gen_parser.add_argument(
        "--model", "-m", default="gemini", choices=["gemini", "imagen"]
    )
    gen_parser.add_argument("--output", "-o", default="generated_image.png")
    gen_parser.add_argument(
        "--aspect-ratio",
        "-ar",
        default="16:9",
        choices=[
            "1:1", "2:3", "3:2", "3:4", "4:3",
            "4:5", "5:4", "9:16", "16:9", "21:9",
        ],
    )
    gen_parser.add_argument(
        "--image-size", "-is", default="2K", choices=["512", "1K", "2K", "4K"]
    )
    gen_parser.add_argument("--api-key", help="Google API Key")
    gen_parser.add_argument(
        "--max-retries", type=int, default=3, help="最大重试次数 (默认: 3)"
    )
    gen_parser.add_argument(
        "--cooldown",
        type=float,
        default=0,
        help="生成成功后冷却等待秒数 (默认: 0，批量调用时建议 5-8)",
    )

    # ── edit ──
    edit_parser = subparsers.add_parser("edit", help="基于图片编辑")
    edit_parser.add_argument("--image", "-i", required=True, help="输入图片路径")
    edit_parser.add_argument("--prompt", "-p", required=True, help="编辑指令")
    edit_parser.add_argument("--output", "-o", default="edited_image.png")
    edit_parser.add_argument("--api-key", help="Google API Key")
    edit_parser.add_argument(
        "--max-retries", type=int, default=3, help="最大重试次数 (默认: 3)"
    )

    # ── extract-style ──
    style_parser = subparsers.add_parser("extract-style", help="从图片提取风格")
    style_parser.add_argument("--image", "-i", required=True, help="参考图片路径")
    style_parser.add_argument("--output", "-o", help="保存风格描述到文件 (可选)")
    style_parser.add_argument("--api-key", help="Google API Key")
    style_parser.add_argument(
        "--max-retries", type=int, default=2, help="最大重试次数 (默认: 2)"
    )

    # ── clean-bg ──
    bg_parser = subparsers.add_parser("clean-bg", help="提取干净背景")
    bg_parser.add_argument("--image", "-i", required=True, help="输入图片路径")
    bg_parser.add_argument("--output", "-o", default="clean_bg.png")
    bg_parser.add_argument("--api-key", help="Google API Key")
    bg_parser.add_argument(
        "--max-retries", type=int, default=3, help="最大重试次数 (默认: 3)"
    )

    # ── batch ──
    batch_parser = subparsers.add_parser(
        "batch",
        help="从 JSON 任务文件批量顺序生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
tasks.json 格式:
  [
    {"prompt": "描述文字", "output": "slide-01.png"},
    {"prompt": "描述文字", "output": "slide-02.png", "image_size": "2K"},
    {"prompt": "描述文字", "output": "slide-03.png", "model": "imagen"}
  ]

每个任务对象支持字段:
  prompt       (必须) 图片描述
  output       (必须) 输出文件路径
  image_size   (可选) 覆盖全局 --image-size
  aspect_ratio (可选) 覆盖全局 --aspect-ratio
  model        (可选) 覆盖全局 --model
        """,
    )
    batch_parser.add_argument(
        "--tasks", "-t", required=True, help="JSON 任务文件路径"
    )
    batch_parser.add_argument(
        "--cooldown",
        "-c",
        type=float,
        default=8.0,
        help="每张图片间冷却秒数 (默认: 8，失败后自动加倍)",
    )
    batch_parser.add_argument(
        "--max-retries",
        type=int,
        default=5,
        help="每张图片最大重试次数 (默认: 5)",
    )
    batch_parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="跳过已存在的输出文件（断点续传）",
    )
    batch_parser.add_argument(
        "--model", "-m", default="gemini", choices=["gemini", "imagen"]
    )
    batch_parser.add_argument(
        "--image-size", "-is", default="2K", choices=["512", "1K", "2K", "4K"]
    )
    batch_parser.add_argument(
        "--aspect-ratio",
        "-ar",
        default="16:9",
        choices=[
            "1:1", "2:3", "3:2", "3:4", "4:3",
            "4:5", "5:4", "9:16", "16:9", "21:9",
        ],
    )
    batch_parser.add_argument("--api-key", help="Google API Key")

    args = parser.parse_args()

    # 无子命令时显示帮助
    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "generate":
        success = generate_image(
            prompt=args.prompt,
            model=args.model,
            output_path=args.output,
            api_key=args.api_key,
            aspect_ratio=args.aspect_ratio,
            image_size=args.image_size,
            max_retries=args.max_retries,
            cooldown=args.cooldown,
        )
        if not success:
            sys.exit(1)

    elif args.command == "edit":
        success = edit_image(
            edit_instruction=args.prompt,
            image_path=args.image,
            output_path=args.output,
            api_key=args.api_key,
            max_retries=args.max_retries,
        )
        if not success:
            sys.exit(1)

    elif args.command == "extract-style":
        result = extract_style(
            image_path=args.image,
            api_key=args.api_key,
            max_retries=args.max_retries,
        )
        if result is None:
            sys.exit(1)
        if args.output:
            Path(args.output).write_text(result, encoding="utf-8")
            print(f"风格描述已保存到: {args.output}")

    elif args.command == "clean-bg":
        success = clean_background(
            image_path=args.image,
            output_path=args.output,
            api_key=args.api_key,
            max_retries=args.max_retries,
        )
        if not success:
            sys.exit(1)

    elif args.command == "batch":
        success = batch_generate(
            tasks_file=args.tasks,
            cooldown=args.cooldown,
            max_retries=args.max_retries,
            skip_existing=args.skip_existing,
            model=args.model,
            api_key=args.api_key,
            image_size=args.image_size,
            aspect_ratio=args.aspect_ratio,
        )
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()
