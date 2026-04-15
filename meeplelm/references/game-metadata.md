# Game Metadata Reference

MeepleLM 包含 BGG (BoardGameGeek) 16.7W 款游戏的索引、10,000 款热门游戏的详细数据以及 1,727 本结构化规则书。

## 数据集概览

| 数据集 | 路径 | 规模 | 说明 |
|--------|------|------|------|
| **排名索引** | `data/metadata/boardgames_ranks.csv` | **16.7W** 款 | 包含 BGG 全量游戏总排名及细分榜单排名 |
| **详细信息** | `data/metadata/game_info/bgg_*.jsonl` | **10,000** 款 | 热门游戏的 27 个详细字段数据 |
| **测试集清单** | `data/metadata/test_games_list.json` | **207** 款 | 论文核心评估使用的代表性游戏集合 |
| **规则书库** | `data/rulebooks/` | **1,727** 本 | Markdown 格式规则语料 |
| **结构化评测** | `data/reviews/` | **15W+** 条 | BGG 用户真实历史评测数据 |

## boardgames_ranks.csv 字段说明

包含 `id`, `name`, `rank`, `bayesaverage`, `is_expansion` 以及各分类排名（如 `strategygames_rank`, `partygames_rank`）。

## 部分测试集样本 (BGG Top 50 示例)

| ID | Name | Core Mechanics |
|----|------|----------------|
| 224517 | **Brass: Birmingham** | 核心策略，经济模拟 |
| 161936 | **Pandemic Legacy: S1** | 合作，传承系统 |
| 342942 | **Ark Nova** | 引擎构建，手牌管理 |
| 233078 | **Twilight Imperium 4** | 4X，谈判，战争 |
| 316554 | **Dune: Imperium** | 工人放置，牌库构建 |

---
*详见 `data/metadata` 下的对应文件获取原始数据。*
