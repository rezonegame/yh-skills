# 复古版画/图章质感 recipe

## 适用场景
写实照片、AI 生图、设计稿 → 复古版画（木刻/图章/老报纸）质感。
适合中国风、历史题材、传统匠心、古法制作、天然有机品牌调性的视觉统一。
**典型用途**：桌游原画批量统一版画风、课件/长图配图加旧纸质感、中国风产品宣传图。

## 来源
公众号《版式设计很简单》文章「中国风质感，不如试试这样做！一股复古中式美！」
（https://mp.weixin.qq.com/s/hvOEElVDRB_hcBpiXy_hbA，2026-08-07 吸收）
原教程用 PS「滤镜库→素描→图章」+ AI「图像描摹」+ 纸纹叠加；本 recipe 用
`scripts/retro_print.py` 纯 Python 复刻，可批量、离线、参数化。

## 核心原理（为什么这样调）
| 原教程步骤 | 本管线实现 | 效果 |
|-----------|-----------|------|
| PS 图章滤镜（灰度+去细节+二值化） | `stamp_filter()`：medianBlur + Otsu/自适应阈值 | 把连续影调压成黑白块面，细节变"块" |
| 图层样式去白 | `--transparent` 输出透明底 | 白底消失，可叠在任何版式上 |
| 纸纹叠加（混合模式+不透明度） | `generate_paper_texture()` + addWeighted | 旧纸张、手工、触感 |
| （可选）AI 图像描摹矢量化 | 无需（本管线直接输出位图） | 如需矢量，用 potrace 二次处理 |

## 流程

### 1. 判定是否走本 recipe
- 输入是照片/生图/设计稿，目标是"复古版画/图章/木刻/老报纸"质感 → 走本 recipe
- 目标是**直接生成**版画风图片（没有现成图）→ 走主生图流程，prompt 用下方风格词，不调脚本

### 2. 生图风格词（无源图时）
```
黑白木刻版画风格，高对比块面化，粗犷刻痕边缘，旧纸张纹理，
手工印刷质感，墨色不均匀，留白疏朗，中文画面文字（如需要），复古中国风氛围
```
负面：`渐变平滑、照片写实、彩色、现代印刷、锐利矢量边缘`

### 3. 后处理（有源图时，推荐）
```bash
# 默认：黑墨浅纸
python3 scripts/retro_print.py 输入.png -o 输出目录/

# 批量统一风格（卡牌/系列图）
python3 scripts/retro_print.py a.png b.png c.png -o out/ --blur 13

# 细节少、块面感强（大图/复杂场景）
python3 scripts/retro_print.py photo.jpg -o out/ --blur 15

# 白墨黑底（暗色版式）
python3 scripts/retro_print.py photo.jpg -o out/ --invert

# 去白透明底（叠加到其他版式/卡牌上）
python3 scripts/retro_print.py art.png -o out/ --transparent

# 关闭纸纹（只要纯版画，给用户自己加材质）
python3 scripts/retro_print.py photo.jpg -o out/ --no-paper
```

### 4. 调参速查
| 目标 | 调整 |
|------|------|
| 更块面、更粗犷 | `--blur` 加大（11/13/15） |
| 保留更多细节 | `--blur` 减小（5/7） |
| 光影层次丢失 | `--mode adaptive` |
| 明暗反了 | `--invert` |
| 纸感太强/太弱 | `--paper-alpha 0.2~0.5` |
| 要干净矢量感 | `--no-paper --no-grain` |

### 5. 自检检查表
- [ ] 主体是否可辨识（块面化后轮廓是否保留）
- [ ] 纸纹/颗粒是否自然（不是脏噪点）
- [ ] 批量时参数一致 → 风格统一
- [ ] 透明底输出用于叠加时，边缘是否干净
- [ ] 中文文字（如有）是否仍可读（blur 过大可能毁字）

## 注意（Pitfalls）
- **blur 核必须是奇数**，否则 OpenCV 报错
- **小图慎用大 blur**（如 200px 图用 blur 15 会糊成色块）；先放大或减小 blur
- 深色照片/低对比图 Otsu 可能全黑或全白，改用 `--mode adaptive` 或手动 `--mode fixed --thresh`
- 透明底输出格式是 PNG（jpg 不支持 alpha）
- 本管线是**后处理**，不是生图：AI 生图后叠加使用效果最佳
