# Game Metadata Reference

MeepleLM 数据集包含 BGG (BoardGameGeek) 上 **167,352** 款游戏的排名数据、**10,000** 款热门游戏的详细信息、**207** 款测试集游戏，以及 **1,727** 本结构化规则书。

---

## Table of Contents

- [数据集统计总览](#数据集统计总览)
- [boardgames_ranks.csv 格式](#boardgames_rankscsv-格式)
- [game_info JSONL 格式](#game_info-jsonl-格式)
- [测试集游戏样本](#测试集游戏样本)
- [BGG Top 50 快速参考](#bgg-top-50-快速参考)
- [数据集来源](#数据集来源)

---

## 数据集统计总览

| 数据集 | 规模 | 格式 | 说明 |
|--------|------|------|------|
| `boardgames_ranks.csv` | **167,352** 款 | CSV | BGG 全量游戏排名 (ID, Rank, Bayesaverage) |
| `game_info/bgg_*.jsonl` | **10,000** 款 (10 files x 1000) | JSONL | 热门游戏详细信息 (含 mechanics, categories) |
| `test_games_list.json` | **207** 款 | JSON | 论文评估测试集，覆盖 diverse genres |
| `rulebooks/` | **1,727** 本 | Markdown | 结构化规则书语料 (Part 1/Part 2 分段) |
| `reviews/` | **150,000+** 条 | JSONL | 过滤后的高质量评测 |
| `finetuning/MeepleLM/` | **17,559** 条 (test) | Alpaca JSON | 含 MDA CoT 的微调数据 |

---

## boardgames_ranks.csv 格式

167,352 行，16 列：

| 列名 | 说明 |
|------|------|
| `id` | BGG 游戏 ID |
| `name` | 游戏名称 |
| `yearpublished` | 出版年份 |
| `rank` | BGG 总排名 (1=最佳) |
| `bayesaverage` | 贝叶斯加权平均分 |
| `average` | 用户原始平均分 |
| `usersrated` | 评分人数 |
| `is_expansion` | 是否为扩展 (0/1) |
| `abstracts_rank` | 抽象游戏排名 |
| `cgs_rank` | 自定义游戏系统排名 |
| `childrensgames_rank` | 儿童游戏排名 |
| `familygames_rank` | 家庭游戏排名 |
| `partygames_rank` | 派对游戏排名 |
| `strategygames_rank` | 策略游戏排名 |
| `thematic_rank` | 主题游戏排名 |
| `wargames_rank` | 战棋排名 |

---

## game_info JSONL 格式

10,000 款游戏，分布在 `bgg_1.jsonl` 至 `bgg_10.jsonl`，每文件 1,000 条。每条记录 27 个字段：

| 字段 | 说明 |
|------|------|
| `id` | BGG 游戏 ID |
| `name` | 游戏名称 |
| `description` | 游戏描述 |
| `yearpublished` | 出版年份 |
| `minplayers` / `maxplayers` | 玩家人数范围 |
| `playingtime` | 游戏时长（分钟） |
| `minage` | 最低年龄 |
| `categories` | 分类标签列表 |
| `mechanisms` | 机制标签列表 |
| `designers` | 设计师列表 |
| `community_stats` | 社区统计（评分人数、平均分、标准差等） |
| `ranks` | 各类别排名 |
| `polls` | 投票数据（建议人数等） |
| `poll_summary_numplayers` | 最佳/推荐人数摘要 |

---

## 测试集游戏样本

论文评估使用的 207 款测试集游戏覆盖了广泛的机制和复杂度。

**部分确认识别出的测试游戏：**

| ID | 游戏名称 | 备注 |
|----|----------|------|
| 126163 | **Tzolk'in: The Mayan Calendar** | 工人放置，齿轮机制 |
| 224517 | **Brass: Birmingham** | 经济，网络构建 |
| 161936 | **Pandemic Legacy: Season 1** | 合作，传承类 |
| 342942 | **Ark Nova** | 引擎构建，手牌管理 |
| 233078 | **Twilight Imperium: Fourth Edition** | 4X，谈判，战争 |
| 316554 | **Dune: Imperium** | 工人放置，牌库构建 |
| 127518 | **A Distant Plain** | COIN 系列，反叛乱战棋 |
| 39953 | **A Game of Thrones: The Card Game** | LCG，手牌管理 |
| 178054 | **A Study in Emerald** | 目前绝版，隐藏身份 |
| 270633 | **Aeon's End: The New Age** | 合作，牌库构建（无洗牌） |
| 4098 | **Age of Steam** | 铁路构建，pick-up and deliver |
| 361545 | **Twilight Inscription** | 纸笔游戏 (Roll & Write) |
| 410201 | **Wyrmspan** | 龙主题，Wingspan 变体 |
| 338960 | **Slay the Spire: The Board Game** | 电子游戏改编，Roguelike |

---

## BGG Top 50 快速参考

截至 2026 年初的数据快照（基于 `boardgames_ranks.csv`）：

| Rank | ID | Name | Year |
|------|--------|------|------|
| 1 | 224517 | Brass: Birmingham | 2018 |
| 2 | 161936 | Pandemic Legacy: Season 1 | 2015 |
| 3 | 342942 | Ark Nova | 2021 |
| 4 | 174430 | Gloomhaven | 2017 |
| 5 | 233078 | Twilight Imperium: Fourth Edition | 2017 |
| 6 | 316554 | Dune: Imperium | 2020 |
| 7 | 167791 | Terraforming Mars | 2016 |
| 8 | 115746 | War of the Ring: Second Edition | 2011 |
| 9 | 187645 | Star Wars: Rebellion | 2016 |
| 10 | 397598 | Dune: Imperium - Uprising | 2023 |
| 11 | 162886 | Spirit Island | 2017 |
| 12 | 291457 | Gloomhaven: Jaws of the Lion | 2020 |
| 13 | 220308 | Gaia Project | 2017 |
| 14 | 12333 | Twilight Struggle | 2005 |
| 15 | 182028 | Through the Ages: A New Story | 2015 |
| 16 | 84876 | The Castles of Burgundy | 2011 |
| 17 | 193738 | Great Western Trail | 2016 |
| 18 | 246900 | Eclipse: Second Dawn | 2020 |
| 19 | 169786 | Scythe | 2016 |
| 20 | 28720 | Brass: Lancashire | 2007 |
| 21 | 173346 | 7 Wonders Duel | 2015 |
| 22 | 295770 | Frosthaven | 2022 |
| 23 | 167355 | Nemesis | 2018 |
| 24 | 266507 | Clank! Legacy | 2019 |
| 25 | 177736 | A Feast for Odin | 2016 |
| 26 | 124361 | Concordia | 2013 |
| 27 | 341169 | Great Western Trail: 2nd Ed | 2021 |
| 28 | 312484 | Lost Ruins of Arnak | 2020 |
| 29 | 205637 | Arkham Horror: TCG | 2016 |
| 30 | 237182 | Root | 2018 |
| 31 | 192135 | Too Many Bones | 2017 |
| 32 | 120677 | Terra Mystica | 2012 |
| 33 | 266192 | Wingspan | 2019 |
| 34 | 373106 | Sky Team | 2023 |
| 35 | 164928 | Orleans | 2014 |
| 36 | 421006 | LOTR: Duel for Middle-earth | 2024 |
| 37 | 96848 | Mage Knight Board Game | 2011 |
| 38 | 251247 | Barrage | 2019 |
| 39 | 338960 | Slay the Spire: Board Game | 2024 |
| 40 | 324856 | The Crew: Mission Deep Sea | 2021 |
| 41 | 199792 | Everdell | 2018 |
| 42 | 418059 | SETI | 2024 |
| 43 | 183394 | Viticulture Essential Edition | 2015 |
| 44 | 321608 | Hegemony | 2023 |
| 45 | 366013 | Heat: Pedal to the Metal | 2022 |
| 46 | 285774 | Marvel Champions: TCG | 2019 |
| 47 | 521 | Crokinole | 1876 |
| 48 | 284378 | Kanban EV | 2020 |
| 49 | 175914 | Food Chain Magnate | 2015 |
| 50 | 247763 | Underwater Cities | 2018 |

---

## 数据集来源

- **GitHub**: https://github.com/leroy9472/MeepleLM/tree/main/data
- **论文**: arXiv:2601.07251
- **数据源**: BoardGameGeek (BGG)
