#!/usr/bin/env python3
"""
yh-style-profiler: 偏差自检脚本
读取文本，对照风格画像，标出"最不像你"的句子。
"""
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROFILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'references', 'style-profile.json')

def load_profile():
    with open(PROFILE_PATH, encoding='utf-8') as f:
        return json.load(f)

def check_sentence_rhythm(sentences, profile):
    """检查句子节奏是否偏离画像"""
    rhythm = profile['profile']['sentence_rhythm']
    target_avg = rhythm['avg_length']
    target_short = rhythm['short_ratio']
    target_long = rhythm['long_ratio']

    # 计算当前文本的节奏
    lengths = [len(s) for s in sentences if len(s) > 5]
    if not lengths:
        return []

    current_avg = sum(lengths) / len(lengths)
    current_short = sum(1 for l in lengths if l <= 20) / len(lengths) * 100
    current_long = sum(1 for l in lengths if l > 40) / len(lengths) * 100

    issues = []
    if abs(current_avg - target_avg) > target_avg * 0.2:
        direction = "偏长" if current_avg > target_avg else "偏短"
        issues.append(f"⚠️ 平均句长偏离（目标{target_avg}字，当前{current_avg:.1f}字，{direction}）")
    if current_short < target_short * 0.7:
        issues.append(f"⚠️ 短句比例偏低（目标{target_short:.0f}%，当前{current_short:.0f}%）")
    if current_long > target_long * 1.5:
        issues.append(f"⚠️ 长句比例偏高（目标{target_long:.0f}%，当前{current_long:.0f}%）")

    # 找连续长句
    consecutive_long = 0
    for i, s in enumerate(sentences):
        if len(s) > 50:
            consecutive_long += 1
            if consecutive_long >= 3:
                start = max(0, i - 3)
                issues.append(f"⚠️ 连续{consecutive_long}句超长句（>50字）：第{start+1}-{i+1}句")
                break
        else:
            consecutive_long = 0

    return issues

def check_ai_words(text, profile):
    """检查AI高频词"""
    vocab = profile['profile']['vocabulary']
    ai_hits = vocab.get('ai_word_hits', {})

    # 扩展AI词列表
    ai_words = ['赋能', '颠覆', '重塑', '生态', '闭环', '矩阵', '对齐', '深刻',
                '深远', '高度', '显著', '充分', '扎实', '切实', '着力', '狠抓',
                '值得深思', '引人深思', '令人反思', '充满活力', '令人叹为观止',
                '标志着', '开启了', '见证了', '致力于', '不仅……更']

    issues = []
    for word in ai_words:
        count = text.count(word)
        if count > 0:
            # 找到出现位置
            idx = text.find(word)
            context_start = max(0, idx - 20)
            context_end = min(len(text), idx + len(word) + 20)
            context = text[context_start:context_end].replace('\n', ' ')
            issues.append(f"❌ AI高频词 '{word}' 出现{count}次（上下文：...{context}...）")

    return issues

def check_paragraph_structure(text, profile):
    """检查段落结构"""
    paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 20]
    issues = []

    # 检查连续无观点段落
    no_opinion_count = 0
    for p in paragraphs:
        lines = p.split('\n')
        first_line = lines[0].strip()
        # 判断是否有观点（包含判断词、观点词）
        opinion_words = ['应该', '值得', '关键', '问题', '本质', '核心', '宁可', '不要']
        if first_line and first_line[0] in '->#|\\':
            continue  # 跳过列表项和标题
        has_opinion = any(w in first_line for w in opinion_words)
        if not has_opinion and len(first_line) > 10:
            no_opinion_count += 1
            if no_opinion_count >= 3:
                issues.append(f"⚠️ 连续{no_opinion_count}段无观点陈述（第一句：{first_line[:40]}...）")
                break
        else:
            no_opinion_count = 0

    # 检查"另外""此外"堆砌
    if text.count('另外') > 3 or text.count('此外') > 3:
        issues.append(f"⚠️ '另外'+'此外'共出现{text.count('另外') + text.count('此外')}次，可能陷入堆砌")

    return issues

def check_endings(text):
    """检查结尾"""
    last_paragraphs = [p for p in text.split('\n\n') if len(p.strip()) > 30][-3:]
    last_text = ' '.join(last_paragraphs)

    issues = []
    cliches = ['综上所述', '总而言之', '值得深思', '引人深思', '未来充满希望',
               '任重道远', '意义深远', '具有重要的参考价值', '值得进一步探讨']
    for c in cliches:
        if c in last_text:
            issues.append(f"❌ 结尾出现套话 '{c}'")

    return issues

def main():
    print("=" * 50)
    print("YH Style Profiler — 偏差自检")
    print("=" * 50)

    if not os.path.exists(PROFILE_PATH):
        print("❌ 风格画像不存在，请先运行 analyze-samples.py")
        sys.exit(1)

    profile = load_profile()

    # 从标准输入读取文本
    if len(sys.argv) > 1 and sys.argv[1] != '-':
        text_path = sys.argv[1]
        with open(text_path, encoding='utf-8') as f:
            text = f.read()
    else:
        print("请输入待检查的文本（输入后按 Ctrl+D 结束）：")
        text = sys.stdin.read()

    if not text.strip():
        print("❌ 没有输入文本")
        sys.exit(1)

    # 分割句子
    sentences = [s.strip() for s in re.split(r'[。！？\n]', text) if len(s.strip()) > 5]

    print(f"\n📄 文本长度：{len(text)} 字，{len(sentences)} 句")
    print()

    # 逐项检查
    all_issues = []

    print("📊 句子节奏检查")
    rhythm_issues = check_sentence_rhythm(sentences, profile)
    for i in rhythm_issues:
        print(f"  {i}")
    all_issues.extend(rhythm_issues)
    print()

    print("📊 AI高频词检查")
    word_issues = check_ai_words(text, profile)
    for i in word_issues:
        print(f"  {i}")
    all_issues.extend(word_issues)
    print()

    print("📊 段落结构检查")
    para_issues = check_paragraph_structure(text, profile)
    for i in para_issues:
        print(f"  {i}")
    all_issues.extend(para_issues)
    print()

    print("📊 结尾检查")
    end_issues = check_endings(text)
    for i in end_issues:
        print(f"  {i}")
    all_issues.extend(end_issues)
    print()

    # 综合评分
    total_checks = len(all_issues)
    critical = sum(1 for i in all_issues if i.startswith('❌'))
    warnings = sum(1 for i in all_issues if i.startswith('⚠️'))

    print("=" * 50)
    print(f"📊 风格偏差报告")
    print(f"  致命问题（❌）：{critical}")
    print(f"  警告（⚠️）：{warnings}")
    print(f"  未触发问题的句子估算（✅）：{max(0, len(sentences) - critical - warnings) if sentences else 0}")
    print()

    if critical == 0 and warnings == 0:
        print("✅ 风格匹配度：优秀！无明显偏差")
    elif critical == 0 and warnings <= 3:
        print("🟡 风格匹配度：良好（少量警告，建议修正）")
    else:
        print("🔴 风格匹配度：需返修")
        print(f"\n❌ 必须修正的问题：")
        for i in all_issues:
            if i.startswith('❌'):
                print(f"  {i}")
        print(f"\n⚠️ 建议修正的问题：")
        for i in all_issues:
            if i.startswith('⚠️'):
                print(f"  {i}")

    return 1 if critical > 0 or warnings > 3 else 0

if __name__ == '__main__':
    raise SystemExit(main())
