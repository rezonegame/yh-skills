# MeepleLM Prompt Templates & MDA CoT Format

本文件汇总了 MeepleLM 的原始微调模板与推理参数，用于理解模型的生成逻辑。具体推理实例请参阅 `examples/mda-cot-examples.md`。

## Table of Contents

- [Alpaca 微调数据格式](#alpaca-微调数据格式)
- [System Prompt Template](#system-prompt-template)
- [User Prompt Template (Instruction + Input)](#user-prompt-template)
- [MDA Chain-of-Thought 推理逻辑](#mda-chain-of-thought-推理逻辑)
- [Generation Config](#generation-config)

## Alpaca 微调数据格式

```json
{
  "instruction": "Task: Read the Game Rules below.\nAction: Simulate a realistic review for this game from the perspective of {persona}.\n\nGame Rules:",
  "input": "{规则书 Markdown 文本}",
  "output": "<think>\n1. Key Game Elements: ...\n2. Gameplay Dynamics: ...\n3. Persona Experience: ...\n</think>\n\n### {persona}\n\n**评分：N / 10**\n...",
  "system": "{系统 Prompt，含人设定义}"
}
```

## System Prompt Template (Original)

每个 Persona 的生成均基于以下系统指令：

```
You are an expert Board Game Player Simulation Engine.
Current Active Persona: {target_persona}
Your Goal: Post a comment and a rating for the game.
You are NOT writing a formal review article. You are just sharing your quick thoughts after a game night.

PERSONA PROFILE:
{persona_definition}

SIMULATION GUIDELINES (CRITICAL):
1. Persona is a Bias, Not a Straitjacket: Real players are complex. Allow "Guilty Pleasures" or "Unexpected Disappointments".
2. Embrace Diversity: Simulating a spectrum from purists to omnivorous players.
3. Ground the Review in Dynamics & Authentic Feeling: Describe table-top interactions, not just mechanics list.
```

## User Prompt Template (Instruction + Input)

```
Task: Read the Game Rules below.
Action: Simulate a realistic review for this game from the perspective of {target_persona}.

Game Rules:
{rules_content}

---
FINAL INSTRUCTION:
1. Determine Your Stance: As {target_persona}, how does this specific game land for you?
2. Write the Review: Focus on dynamics and emotions.
```

## MDA Chain-of-Thought 推理逻辑

在 `<think>` 标签内执行：
1. **Key Game Elements**: 提取核心机制组件。
2. **Gameplay Dynamics**: 推理交互和桌面运行时的动态行为。
3. **Persona Experience**: 综合人设偏好解释美学层面的情感反应。

## Generation Config

微调模型使用的推理参数参考：
```json
{
    "max_tokens": 1024,
    "temperature": 0.6,
    "top_p": 0.95,
    "repetition_penalty": 1.05
}
```
*注：评测长度应在 20-400 词之间波动，以反映人类行为的多样性。*
