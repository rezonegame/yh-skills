# Adoption Decisions

## G. Writing Pre-mode: Real Evidence Anchors (写作前置模式)
- Source: 数字生命卡兹克「活人感写作」方法论拆解（微信公众号文章，2026-08-07）
- Source URL: https://mp.weixin.qq.com/s/eejoV1hhaZoqofh1LC-WTw
- Material adopted: 五类证据锚点（时间/场景/数字代价/失败经历/原话对话）强制收集模板 + "活人感在写之前锁定"前置原则 + 平台适配参数。作为 yh-humanizer 的生成前置模式，与既有事后改写互补。
- Material excluded: 编造亲历感、伪造虚构细节、一次性提示词母版（改造成可复用模板，而非单次 prompt）
- Rationale: 现有 36 模式/节奏/三轴/自审已覆盖文章大部分；唯一真增量是"写作前强制填证据"的输入门，正好补上 humanizer 作为事后改写器的盲区
- Test: 需在后续任务中验证"干净但空"文本经前置模式后是否补足代价轴/位置轴证据
- Rollback: 删除 references/evidence-anchors.md + SKILL.md 中"写作前置模式"一节 + 参考索引行 + 本条
- Date: 2026-08-07

## F. Voice Profiles Without Factual Drift
- Source: Aboudjem/humanizer-skill
- Source URL: https://github.com/Aboudjem/humanizer-skill
- License: MIT
- Material adopted: opt-in voice profile structure, profile-spec maintenance pattern
- Material excluded: authorship claims, invented experience
- Test: 6 eval cases (5 profile-specific + 1 no-profile baseline)
- Rollback: delete references/voice-profiles.md, evals/, and the 模式D section in SKILL.md
- Date: 2026-07-28
