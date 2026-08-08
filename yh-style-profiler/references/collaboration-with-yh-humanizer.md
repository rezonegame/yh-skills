# yh-style-profiler 与 yh-humanizer 的协同

## 分工

- **yh-style-profiler**：正向信号注入——"写成用户的样子"
- **yh-humanizer**：负向信号去除——"去掉AI味"

## 推荐流程

### 协同写作（article-factory 流程中）

1. **article-factory** 生成初稿
2. **yh-style-profiler** 加载风格画像，按用户风格改写
3. **yh-humanizer** 去除残留AI味
4. **yh-style-profiler/scripts/self-check.py** 做偏差自检，标出"最不像用户"的句子
5. 人工修正标注的偏差句

### 单独润色（yh-humanizer 场景中）

1. 如果 yh-style-profiler 的风格画像已存在（`references/style-profile.json`）：
   - yh-humanizer 的"模式A：用户样本校准"可以直接使用画像数据，跳过手动分析
   - 改写完成后运行 `self-check.py` 做偏差验证
2. 如果风格画像不存在：
   - 照常使用 yh-humanizer 的 36 种 AI 模式识别

## 注意事项

- 两个技能不会互相冲突：一个管"像不像用户"，一个管"像不像AI"
- 先做风格注入（profiler），再做去味（humanizer）——顺序不能反
- 如果用户有明确的风格样本但 profiler 未加载，humanizer 仍可手动分析样本