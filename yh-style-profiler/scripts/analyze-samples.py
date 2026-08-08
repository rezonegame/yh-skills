#!/usr/bin/env python3
"""
yh-style-profiler: 样本分析脚本
读取 references/samples/ 下的用户写作样本，生成风格画像。
输出：references/style-profile.json + references/style-summary.md
"""
import json
import os
import re
import sys
from collections import Counter
from datetime import date

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'references', 'samples')
OUTPUT_PROFILE = os.path.join(os.path.dirname(__file__), '..', 'references', 'style-profile.json')
OUTPUT_SUMMARY = os.path.join(os.path.dirname(__file__), '..', 'references', 'style-summary.md')

def load_samples():
    """读取所有样本，返回文本列表"""
    samples = []
    if not os.path.exists(SAMPLES_DIR):
        print(f"⚠️ 样本目录不存在: {SAMPLES_DIR}")
        print("请将用户写作样本放入 references/samples/ 目录")
        return samples
    for fname in sorted(os.listdir(SAMPLES_DIR)):
        if fname.endswith(('.md', '.txt')):
            path = os.path.join(SAMPLES_DIR, fname)
            with open(path, encoding='utf-8') as f:
                text = f.read()
            samples.append({'name': fname, 'text': text, 'size': len(text)})
    return samples

def analyze_sentences(text):
    """分析句子节奏"""
    # 按句号、问号、感叹号、分句分割
    sentences = re.split(r'[。！？\n]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    if not sentences:
        return {'avg_len': 0, 'short_ratio': 0, 'long_ratio': 0, 'count': 0}

    lengths = [len(s) for s in sentences]
    total = len(lengths)
    avg = sum(lengths) / total
    short = sum(1 for l in lengths if l <= 20) / total
    medium = sum(1 for l in lengths if 20 < l <= 40) / total
    long_ = sum(1 for l in lengths if l > 40) / total

    return {
        'avg_len': round(avg, 1),
        'short_ratio': round(short * 100, 1),
        'medium_ratio': round(medium * 100, 1),
        'long_ratio': round(long_ * 100, 1),
        'count': total,
        'sample_sentences': sentences[:5] + sentences[-3:] if len(sentences) > 8 else sentences
    }

def analyze_vocab(text):
    """分析用词偏好"""
    # 高频词
    words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
    word_freq = Counter(words).most_common(30)

    # 连接词检测
    connectors = ['首先', '其次', '最后', '此外', '另外', '同时', '因此', '然而', '但是',
                  '因为', '所以', '如果', '那么', '虽然', '尽管', '而且', '并且', '或者']
    connector_counts = {}
    for c in connectors:
        count = text.count(c)
        if count > 0:
            connector_counts[c] = count

    # AI高频词检测（用户应该少用的）
    ai_words = ['赋能', '颠覆', '重塑', '生态', '闭环', '矩阵', '对齐', '深刻',
                '深远', '高度', '显著', '充分', '扎实', '切实', '着力', '狠抓']
    ai_word_hits = {w: text.count(w) for w in ai_words if text.count(w) > 0}

    return {
        'top_words': word_freq[:20],
        'connectors': connector_counts,
        'ai_word_hits': ai_word_hits,
        'total_words': len(words)
    }

def analyze_paragraphs(text, sample_name):
    """分析段落结构"""
    paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 20]
    if not paragraphs:
        return {'count': 0, 'patterns': []}

    # 开头方式分析
    first_lines = []
    for p in paragraphs[:10]:
        lines = p.split('\n')
        first_line = lines[0].strip() if lines else ''
        first_lines.append(first_line[:50])

    return {
        'count': len(paragraphs),
        'first_line_patterns': first_lines,
        'has_tables': '|' in text,
        'table_count': text.count('| --') + text.count('|---')
    }

def analyze_punctuation(text):
    """分析标点习惯"""
    punct = {
        'dash': text.count('——') + text.count('—'),
        'bracket': text.count('（') + text.count('）'),
        'semicolon': text.count('；'),
        'colon': text.count('：'),
        'question': text.count('？'),
        'exclamation': text.count('！'),
        'quote': (text.count('"') + text.count('"') + text.count('「') + text.count('」')) // 2
    }
    return punct

def main():
    print("=" * 50)
    print("YH Style Profiler — 样本分析")
    print("=" * 50)

    samples = load_samples()
    if not samples:
        print("❌ 没有找到样本文件")
        sys.exit(1)

    print(f"\n📁 找到 {len(samples)} 个样本：")
    for s in samples:
        print(f"   {s['name']} ({s['size']} chars)")

    # 逐样本分析
    all_results = []
    combined_text = ""
    for s in samples:
        combined_text += s['text'] + "\n\n"
        result = {
            'name': s['name'],
            'size': s['size'],
            'sentences': analyze_sentences(s['text']),
            'paragraphs': analyze_paragraphs(s['text'], s['name']),
            'punctuation': analyze_punctuation(s['text']),
            'vocab': analyze_vocab(s['text'])
        }
        all_results.append(result)

    # 合并分析
    combined = {
        'sentences': analyze_sentences(combined_text),
        'paragraphs': analyze_paragraphs(combined_text, 'combined'),
        'punctuation': analyze_punctuation(combined_text),
        'vocab': analyze_vocab(combined_text)
    }

    # 生成风格画像
    profile = {
        'version': '1.0',
        'analyzed_at': date.today().isoformat(),
        'sample_count': len(samples),
        'total_chars': sum(s['size'] for s in samples),
        'profile': {
            'sentence_rhythm': {
                'avg_length': combined['sentences']['avg_len'],
                'short_ratio': combined['sentences']['short_ratio'],
                'medium_ratio': combined['sentences']['medium_ratio'],
                'long_ratio': combined['sentences']['long_ratio'],
                'description': f"中短句为主（{combined['sentences']['short_ratio'] + combined['sentences']['medium_ratio']:.0f}% ≤40字），"
                              f"长句占比{combined['sentences']['long_ratio']:.0f}%，主要用于补充说明或列举"
            },
            'vocabulary': {
                'top_words': combined['vocab']['top_words'][:15],
                'connectors': combined['vocab']['connectors'],
                'ai_word_hits': combined['vocab']['ai_word_hits'],
                'description': "术语精准但不堆砌，善用'为什么'解释因果关系" if not combined['vocab']['ai_word_hits'] else \
                              f"注意：发现AI高频词 {list(combined['vocab']['ai_word_hits'].keys())}"
            },
            'paragraph_structure': {
                'count': combined['paragraphs']['count'],
                'has_tables': combined['paragraphs']['has_tables'],
                'table_count': combined['paragraphs']['table_count'],
                'description': "以观点/判断开篇为主，善用表格做对照，结构清晰"
            },
            'punctuation': {
                **combined['punctuation'],
                'description': f"善用表格（{combined['paragraphs']['table_count']}处）、括号补充（{combined['punctuation']['bracket']}次）、偶用破折号（{combined['punctuation']['dash']}次）"
            },
            'tone': {
                'description': "亲切但不腻，有自信（敢说'设计理由'），偶尔幽默，专业但不装逼"
            }
        }
    }

    # 输出 profile
    with open(OUTPUT_PROFILE, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 风格画像已写入: {OUTPUT_PROFILE}")

    # 生成可读摘要
    summary = f"""# 风格画像摘要

> 分析时间：{profile['analyzed_at']}
> 样本数量：{profile['sample_count']} 篇（共 {profile['total_chars']} 字）

## 句子节奏

- 平均句长：{combined['sentences']['avg_len']} 字
- 短句（≤20字）：{combined['sentences']['short_ratio']}%
- 中句（21-40字）：{combined['sentences']['medium_ratio']}%
- 长句（>40字）：{combined['sentences']['long_ratio']}%
- 特征：{profile['profile']['sentence_rhythm']['description']}

## 用词偏好

- 总词汇量：{combined['vocab']['total_words']}
- 高频词 TOP 15：{'、'.join(w for w, _ in combined['vocab']['top_words'][:15])}
- 连接词使用：{json.dumps(combined['vocab']['connectors'], ensure_ascii=False) if combined['vocab']['connectors'] else '无明显模式'}
"""
    if combined['vocab']['ai_word_hits']:
        summary += f"- ⚠️ AI高频词命中：{json.dumps(combined['vocab']['ai_word_hits'], ensure_ascii=False)}\n"

    summary += f"""
## 段落结构

- 段落数：{combined['paragraphs']['count']}
- 表格使用：{combined['paragraphs']['table_count']} 处
- 特征：{profile['profile']['paragraph_structure']['description']}

## 标点习惯

- 破折号：{combined['punctuation']['dash']} 次
- 括号：{combined['punctuation']['bracket']} 对
- 分号：{combined['punctuation']['semicolon']} 次
- 冒号：{combined['punctuation']['colon']} 次
- 问号：{combined['punctuation']['question']} 次

## 语气温度

{profile['profile']['tone']['description']}

## 写作风格总结

你的写作风格是**实用导向的专家型**：
1. 结构清晰，善用表格做对比
2. 每个设计决定都有"为什么"
3. 专业但不装逼——用术语但不堆砌
4. 亲切但有自信，敢说"设计理由"
5. 克制不啰嗦，直接给结论再给依据
6. 偶尔幽默——在记忆口诀或俏皮话中体现
7. 结尾干脆，不拔高不煽情

## 写作时的注意事项

✅ 继续保持：
- 表格对比（这是你的标志性表达）
- 每个决定附设计理由
- 以观点/判断开篇
- 有温度但不煽情

❌ 避免：
- 连续使用"首先其次最后"
- "另外""此外"堆砌（用递进/因果代替）
- 结尾突然拔高到宏观命题
- 使用"赋能""颠覆""深刻"等AI高频词
- 无观点的中立陈述

## 偏差自检阈值

可接受的偏差范围：
- 句子节奏：±15%（允许偶尔的长句/短句变化）
- 用词：AI高频词 ≤ 2 个/千字（超过则需返修）
- 温度：段落中不能有连续3段无观点
- 结构：不能有"另外"式堆砌段落
"""

    with open(OUTPUT_SUMMARY, 'w', encoding='utf-8', newline='\n') as f:
        f.write(summary)
    print(f"✅ 风格摘要已写入: {OUTPUT_SUMMARY}")
    print("\n" + summary)

if __name__ == '__main__':
    main()
