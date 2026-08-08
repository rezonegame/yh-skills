#!/usr/bin/env bash
# 王虹手写风 HTML → 逐页 PNG 渲染（Linux 版，使用 google-chrome headless + @font-face 注入）
# 用法: scripts/render_wanghong.sh <html-file> [N|all] [out-dir] [font-file]
#   字体默认取 ~/.local/share/fonts/LXGWWenKai-Regular.ttf，可用第 4 参或 WANGHONG_FONT_PATH 覆盖。
# 来源: z-wanghong-handwritten-ppt (tjxj/z-skills, MIT) 的 render.sh 适配 Linux
set -euo pipefail

CHROME="${CHROME_BIN:-$(command -v google-chrome || command -v google-chrome-stable || echo '')}"
FILE="${1:-}"
COUNT="${2:-all}"
OUT="${3:-}"
FONT_FILE="${4:-${WANGHONG_FONT_PATH:-$HOME/.local/share/fonts/LXGWWenKai-Regular.ttf}}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -z "$CHROME" || ! -x "$CHROME" ]]; then
  echo "error: google-chrome 未找到，请设置 CHROME_BIN 环境变量" >&2
  exit 1
fi
if [[ -z "$FILE" || ! -f "$FILE" ]]; then
  echo "usage: render_wanghong.sh <html-file> [N|all] [out-dir] [font-file]" >&2
  exit 1
fi
if [[ -z "$FONT_FILE" || ! -f "$FONT_FILE" ]]; then
  echo "error: 未找到霞鹜文楷字体文件: $FONT_FILE" >&2
  echo "下载: https://github.com/lxgw/LxgwWenKai/releases （放 ~/.local/share/fonts/ 后 fc-cache -f）" >&2
  exit 1
fi

STEM="$(basename "${FILE%.*}")"

if [[ "$COUNT" == "all" ]]; then
  COUNT="$(grep -c '<section class="slide' "$FILE" || true)"
fi
if [[ -z "$COUNT" || "$COUNT" -lt 1 ]]; then
  echo "error: no slides found" >&2
  exit 1
fi

if [[ -z "$OUT" ]]; then
  OUT="$(dirname "$FILE")/${STEM}-png"
fi
mkdir -p "$OUT"

RENDER_DIR="$(mktemp -d "/tmp/wanghong-ppt-render.XXXXXX")"
RENDER_HTML="$RENDER_DIR/deck.html"
trap 'rm -f "$RENDER_HTML"; rmdir "$RENDER_DIR"' EXIT
python3 "$SCRIPT_DIR/prepare_render_html.py" "$FILE" "$FONT_FILE" "$RENDER_HTML"

# 字体预检：确认注入后字体可用
if ! FONT_CHECK="$("$CHROME" \
  --headless=new \
  --allow-file-access-from-files \
  --disable-gpu \
  --hide-scrollbars \
  --no-sandbox \
  --virtual-time-budget=5000 \
  --dump-dom \
  "file://$RENDER_HTML#/1" 2>/dev/null)"; then
  echo "error: Chrome 字体预检失败" >&2
  exit 1
fi
if [[ "$FONT_CHECK" != *'data-wanghong-font-ready="yes"'* ]]; then
  echo "error: 手写字体加载失败（检查字体文件是否为霞鹜文楷）" >&2
  exit 1
fi

for i in $(seq 1 "$COUNT"); do
  target="$OUT/${STEM}_$(printf '%02d' "$i").png"
  "$CHROME" \
    --headless=new \
    --allow-file-access-from-files \
    --disable-gpu \
    --hide-scrollbars \
    --no-sandbox \
    --virtual-time-budget=5000 \
    --window-size=1920,1080 \
    --screenshot="$target" \
    "file://$RENDER_HTML#/$i" >/dev/null 2>&1 || true
  if [[ ! -s "$target" ]]; then
    echo "error: failed to render slide $i" >&2
    exit 1
  fi
  echo "rendered: $target"
done

echo "done: $COUNT slide(s)"
