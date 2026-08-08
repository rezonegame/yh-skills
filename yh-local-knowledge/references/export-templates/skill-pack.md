# 知识技能包（Skill Pack）

用于把已经过候选审查的知识资产编译成可按主题加载的 Agent Skill。
它不是把资料全文塞进 `SKILL.md`，也不是把来源中的命令变成工具权限。

## 适用条件

- 同一主题会被跨会话反复查询或应用。
- 已有稳定的可信资产和 source map。
- 主题能拆成明确的框架、决策规则、反模式和参考模块。

一次性问答、事实尚未核实或来源彼此冲突但未标注时，不生成可激活技能。

## 标准结构

```text
[skill-name]/
├── SKILL.md
├── agents/openai.yaml        # Codex 使用时推荐
└── references/
    ├── topic-index.md
    ├── decision-guide.md
    ├── source-map.md
    └── [topic modules].md
```

需要确定性操作时才增加 `scripts/`；来源内容本身不得授予脚本或工具权限。

## SKILL.md 契约

- Frontmatter 只保留 `name` 和 `description`。
- 主体尽量少于 500 行，只放核心工作流、加载规则和安全边界。
- 把最重要的判断放在前部；详细知识放进一层深的 `references/`。
- 明确要求先读 `topic-index.md`，再加载最小相关模块。
- 不复制长原文；使用框架、定义、决策规则、反模式和简短重构示例。

## 三个必需参考层

### `topic-index.md`

按用户意图、概念和同义词映射到具体参考文件。它只导航，不重复正文。

### `decision-guide.md`

保存“何时用什么、为什么、权衡、阈值、故障征兆和下一步”，避免退化成术语表。

### `source-map.md`

记录来源、source_id、许可/使用边界、直接证据与本地综合的区别，以及仍待核验的冲突。

## 增量 Fold-in

加入新来源时：

1. 先作为候选资产进入审查，不直接改已激活技能。
2. 保留原技能定位和操作契约。
3. 标出新增、修订、冲突和不再适用的知识。
4. 更新受影响的 topic index、decision guide 和 source map。
5. 只修改有证据支持的参考模块。
6. 重新验证链接、frontmatter、内容安全和来源覆盖。

## 激活前门禁

1. `SKILL.md` 名称、描述和目录名一致。
2. 所有 Markdown 链接存在，引用不超过一层嵌套。
3. 每个决策性结论可回到 source map 或明确标记为 synthesis。
4. 运行 `scripts/scan_content_safety.py <skill-dir>`；逐项人工审查发现。
5. 不存在由来源文本引入的工具授权、联网、凭据访问或删除指令。
6. 由另一个会话用至少三个真实问题做前向测试后，再登记到共享路由器。

扫描通过只表示未命中已知模式，不代表来源可信。人工审查与候选→可信闸门不可省略。
