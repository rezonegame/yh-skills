# 播客脚本包（podcast-pack，可选）

**用途**：把资料转成双人对话播客脚本，用于音频制作或轻量传播。

**启发来源**：notebookllama 的 generate_podcast。

**条目类型**：`synthesis`（脚本是综合改写）

**可选性声明**：本包是**可选插件式**导出。TTS 合成需要额外依赖（本地模型或云服务如 ElevenLabs），脚本生成本身不依赖 TTS。无 TTS 时只产出脚本 markdown。

**产出结构**：
```
podcast-pack/
├── USAGE.md
├── INDEX.md
├── script.md           # 双人对话脚本
├── show-notes.md       # 节目说明（要点 + 引用）
└── audio/              # 可选，仅当 TTS 可用
    └── episode.mp3
```

**script.md 结构**：
```markdown
---
id: podcast_001
type: synthesis
title: [主题] 播客脚本
citable: false
trust_role: synthesis
sources: [src_001, src_002, src_004]
---
# [标题]

## 角色设定
- 主持人（A）：引导、提问、总结
- 嘉宾（B）：深入讲解、举例、互动

## 脚本

**A**：欢迎收听[节目名]。今天我们聊[主题]。B，先给大家说说这是怎么回事？

**B**：简单说，[一句话概述，源自 src_001]。举个例子，[具体例子 src_002]。

**A**：这让我想到[追问]。那[关键问题]呢？

**B**：[回答，源自 src_004]。不过要注意[限定/反面]。

**A**：总结一下，[要点]。

## 节目要点
1. [要点1]
2. [要点2]

## 引用
- src_001：[...]
- src_002：[...]
```

**脚本写作原则**：
- 对话自然，不要把论文硬塞进对话。
- 主持人的提问要像真人（好奇、追问、不懂就问）。
- 嘉宾的回答要有具体例子，不要全是抽象概念。
- 保留争议和限定，不要为了流畅回避复杂。
- 每个事实点带 source 溯源（在 show-notes 里）。

**TTS 降级路径**：
- 本地 TTS 优先（如 XTreaming/Piper/edge-tts）。
- 云 TTS 可选（ElevenLabs 等），需用户配置 API key。
- 无 TTS → 只出 script.md，USAGE.md 注明"脚本已就绪，需自行合成音频"。

**USAGE.md 要点**：
- 适合想用音频形式传播/通勤学习的人。
- `citable: false`——对话是改写，引用事实回原文。
- TTS 是可选依赖，不强求。
