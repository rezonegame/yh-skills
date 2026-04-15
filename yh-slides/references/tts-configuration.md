# TTS 配音配置指南

## 概述

yh-slides 支持为 HTML 输出的演示文稿添加语音旁白（TTS, Text-to-Speech）。

**适用路径**: Path C（零依赖 HTML）和 Path D（富交互 HTML）

---

## 5 种 TTS 引擎

### 1. Edge TTS（免费，推荐）

**简介**: 微软 Edge 浏览器的语音合成引擎，免费使用

**优点**: 免费、支持中文、多种音色、质量不错
**缺点**: 需要网络连接

**安装**:
```bash
pip install edge-tts
```

**使用**:
```python
import asyncio
import edge_tts

async def generate_tts(text, output_file, voice="zh-CN-YunxiNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

asyncio.run(generate_tts("大家好，今天我们来讨论AI的未来", "slide-01.mp3"))
```

**推荐中文音色**:
| 音色 ID | 风格 | 适用场景 |
|---------|------|---------|
| zh-CN-YunxiNeural | 男声，年轻阳光 | 技术分享、产品介绍 |
| zh-CN-XiaoxiaoNeural | 女声，标准 | 通用、培训 |
| zh-CN-YunjianNeural | 男声，沉稳 | 正式商务、咨询报告 |
| zh-CN-XiaoyiNeural | 女声，活泼 | 创意展示、教育 |

---

### 2. OpenAI TTS（高质量）

**简介**: OpenAI 的语音合成 API，质量最高

**优点**: 自然度最高、支持多语言
**缺点**: 付费、需要 API Key

**使用**:
```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="大家好，今天我们来讨论AI的未来"
)
response.stream_to_file("slide-01.mp3")
```

**可选音色**: alloy, echo, fable, onyx, nova, shimmer

---

### 3. Volcano Engine（火山引擎，中文优化）

**简介**: 字节跳动的语音合成服务

**优点**: 中文效果优秀、支持多种方言
**缺点**: 需要注册火山引擎账号

**适用场景**: 中文为主的演示文稿，尤其适合大陆商务场景

---

### 4. Zhihu AI（智谱 AI）

**简介**: 智谱 AI 的语音合成服务

**优点**: 中文优化、支持情感控制
**缺点**: 需要 API Key

---

### 5. Fish Speech（本地，开源）

**简介**: 开源本地语音合成，隐私友好

**优点**: 完全本地运行、隐私安全、可定制音色
**缺点**: 需要 GPU、安装复杂

**适用场景**: 对隐私要求高的内部演示

---

## TTS 工作流

### 步骤 1: 生成脚本
```python
def generate_script(slides_data):
    scripts = []
    for slide in slides_data:
        script = f"{slide['title']}。"
        if slide.get('key_points'):
            for point in slide['key_points']:
                script += f" {point}。"
        scripts.append({"slide_number": slide['number'], "script": script})
    return scripts
```

### 步骤 2: 批量生成音频
```bash
for i in {1..10}; do
  edge-tts --text "$(cat scripts/slide-$i.txt)" \
    --voice zh-CN-YunxiNeural --write-media audio/slide-$i.mp3
done
```

### 步骤 3: 嵌入 HTML

**Path D（多文件 HTML）**:
```html
<section class="slide" data-slide="1" data-audio="audio/slide-01.mp3">
  <h2>幻灯片标题</h2>
  <button class="audio-play" aria-label="播放旁白">🔊</button>
</section>
```

**Path C（单文件 HTML，零依赖）**:
```javascript
// 通过 Web Speech API 实时合成
function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'zh-CN';
    utterance.rate = 0.9;
    speechSynthesis.speak(utterance);
}
```

### 步骤 4: 同步导航
```javascript
class AudioSync {
    constructor(slides) {
        this.slides = slides;
        this.currentAudio = null;
    }
    playForSlide(index) {
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio.currentTime = 0;
        }
        const slide = this.slides[index];
        if (slide.audioFile) {
            this.currentAudio = new Audio(slide.audioFile);
            this.currentAudio.play();
        }
    }
}
```

---

## 语音选择建议

| 内容类型 | 推荐引擎 | 推荐音色 |
|---------|---------|---------|
| 技术分享 | Edge TTS | zh-CN-YunxiNeural |
| 商务报告 | OpenAI TTS | alloy / onyx |
| 教育培训 | Edge TTS | zh-CN-XiaoxiaoNeural |
| 创意展示 | OpenAI TTS | nova |
| 内部汇报 | Fish Speech | 自定义 |

---

## 最佳实践

1. **旁白 ≠ 照读** — 语音内容应该比幻灯片文字更详细
2. **控制时长** — 每张幻灯片的旁白建议 30-60 秒
3. **一致音色** — 整个演示使用同一个音色
4. **可跳过** — 提供静音/跳过选项，不要强制播放
