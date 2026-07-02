# 5 分钟快速上手（Quick Start）

> 这里只讲 3 个最常见场景。每个场景都是完整的命令序列，复制即用。

---

## 场景 A：企业 PPT（可编辑 PPTX，Path A）

适用：需要在 PowerPoint 里编辑文字、调整布局

### 1. 建项目目录

```bash
mkdir -p "C:\PPTX\myproject\images" "C:\PPTX\myproject\slides" "C:\PPTX\myproject\output"
```

### 2. 准备内容

告诉 Claude：「我要做一份 8 页的产品介绍，受众是销售团队，走 Path A，项目名 myproject」

Claude 会：
- Step 0 先确认协作模式（全自动 / 引导式 / 一步一步 / 自定义）
- Step 1 按协作模式确认必要需求字段
- Step 3 输出逐页大纲供确认
- Step 4 从风格库筛选并给出 3 个设计方向
- Step 5 生成 HTML 幻灯片

### 3. 生成插画（可选，选了风格后）

```bash
python scripts/generate_image.py \
  batch --tasks "C:\PPTX\myproject\tasks.json" \
  --cooldown 8 --skip-existing --image-size 2K
```

### 4. 转成 PPTX

```bash
node scripts/html2pptx.js \
  "C:\PPTX\myproject\slides\slide-01.html" \
  "C:\PPTX\myproject\slides\slide-02.html" \
  -o "C:\PPTX\myproject\output\myproject.pptx"
```

### 5. 质量检查

对照 `references/constraints/quality-checklist.md` 的 Path A P0 检查清单：
- HTML 尺寸 720pt × 405pt ✓
- 所有元素 `position: absolute` ✓
- 图片路径是本地相对路径 ✓

**出了问题？** → 查 [constraints/failure-modes.md](../constraints/failure-modes.md) 的 FM-A-* 部分

---

## 场景 B：电子杂志分享页（Path C magazine）

适用：个人分享、团队汇报、网页展示，追求精品视觉

### 1. 选种子文件

```
Read: assets/seeds/path-c-magazine-seed.html
```
（Claude 会自动读，你只需要提出需求）

### 2. 选主题色

从 `references/aesthetics/magazine/themes.md` 选一套，直接替换 `:root` 块：

| 场景 | 推荐主题 |
|------|---------|
| 学术 / 严肃 | 墨水经典（默认） |
| 科技 / 产品 | 靛蓝瓷 |
| 温暖 / 人文 | 沙丘 |
| 自然 / 生态 | 森林墨 |
| 复古 / 手作 | 牛皮纸 |

### 3. 画节奏表（Claude 会做，你来确认）

例如 8 页：
```
01: hero-dark   02: light   03: dark    04: hero-light
05: light       06: dark    07: light   08: hero-dark
```

### 4. 让 Claude 填充内容

告诉 Claude 每页的标题和要点，Claude 从 `references/aesthetics/magazine/layouts.md` 选合适布局填充。

### 5. 质量检查

```bash
# 检查 class 名（在 output 目录运行）
diff <(grep -oE 'class="[^"]+"' index.html | grep -oE '[a-z][a-z0-9-]+' | sort -u) \
     <(grep -oE '\.[a-z][a-z0-9-]+' path-c-magazine-seed.html | sort -u)

# 检查主题标记
grep -oE 'class="slide [^"]+"' index.html | sort | uniq -c
```

**出了问题？** → 查 [constraints/failure-modes.md](../constraints/failure-modes.md) 的 FM-C-* 部分

---

## 场景 C：含配音的演示（Path D + TTS）

适用：教学课件、产品 Demo、自动播放演示

### 1. 选种子文件

```
Read: assets/seeds/path-d-animated-seed.html
```

### 2. 准备每页配音文本

例如：
```
Page 01: "欢迎大家，今天我们聊一聊 AI 辅助设计的新范式。"
Page 02: "首先来看一个数据——83% 的设计师表示..."
```

### 3. 生成 TTS 音频

```bash
# 使用 TTS 服务（需配置 references/integrations/tts-configuration.md）
python tts.py --text "欢迎大家..." --output audio/s01.mp3
```

### 4. 验证

浏览器打开 index.html，按翻页键，确认：
- 每页音频自动播放 ✓
- 进度条与音频同步 ✓
- GSAP 动画流畅 ✓

**出了问题？** → 查 [constraints/failure-modes.md](../constraints/failure-modes.md) 的 FM-D-* 部分

---

## 最常见错误

| 错误 | 根因 | 快速修复 |
|------|------|---------|
| Path A PPTX 位置全错 | 忘写 `position:absolute` | 补 absolute，重新 html2pptx |
| Path C 页面样式塌 | 发明了新 class | 运行 class-preflight diff 命令 |
| Path B 图片有乱码文字 | prompt 没写 `no text in image` | 重生成，加 no text |
| Path D 音频不播放 | 路径错误或浏览器自动播放限制 | 改成相对路径；用按钮触发 |

详细排查见 [constraints/failure-modes.md](../constraints/failure-modes.md)
