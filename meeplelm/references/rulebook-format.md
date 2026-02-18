# Rulebook Format Reference

MeepleLM 使用标准化的 Markdown 格式规则书。以下为格式规范和示例。

---

## 格式规范

规则书统一使用 `## Comprehensive Reference Manual` 标题，包含以下标准章节：

1. **Lore & Objective** — 背景故事与游戏目标
2. **Components** — 游戏组件清单
3. **Setup** — 设置步骤
4. **Gameplay Flow** — 回合流程
5. **Core Mechanics** — 核心机制详解
6. **Scoring & End Game** — 计分与终局条件
7. **FAQ or Edge Cases** — 常见问题与边缘情况

---

## 示例：Modern Art (BGG #118)

```markdown
## Comprehensive Reference Manual

1. **Lore & Objective**
In Modern Art, players are art dealers competing to earn the most money over four rounds
by strategically auctioning and collecting paintings. The player with the highest cash
total at the end of the fourth round wins.

2. **Components**
- 70 painting cards from 5 artists (12-16 cards each)
- Money: Each player starts with $100
- 5 Museum screens
- Auction hammer token
- Artist Value tiles: $30, $20, $10

3. **Setup**
- Shuffle all 70 painting cards.
- Deal cards based on player count (3p: 10, 4p: 9, 5p: 8).
- Each player receives a Museum screen and $100.

4. **Gameplay Flow**
- On their turn, the Auctioneer selects one painting and conducts an auction.
- Winner pays the Auctioneer (or the bank if Auctioneer wins).
- Round ends when the 5th painting by any artist is played.

5. **Core Mechanics**
- **Open Auction (+):** Free bidding, highest wins.
- **Once-Around Auction:** Clockwise single bid, Auctioneer has final bid.
- **Hidden Auction (o):** Simultaneous secret bids.
- **Fixed Price Auction ({}):** Auctioneer sets price, clockwise acceptance.
- **Double Auction (==):** Two paintings by same artist, combined auction.

6. **Scoring & End Game**
- Round-end: Top 3 artists ranked by paintings played → assigned $30/$20/$10 values.
- Values accumulate across rounds.
- 4th round scored, then game ends. Highest cash wins.
```

---

## 用户输入适配

当用户提供的游戏规则不符合上述标准格式时，在 MDA 推理前先进行信息提取：
1. 识别核心机制（回合结构、资源、胜利条件、玩家互动方式）
2. 提取关键决策点和张力来源
3. 整理为结构化摘要后再进行 Persona 模拟
