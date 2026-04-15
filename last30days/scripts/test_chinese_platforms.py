"""Test Chinese platform integration for last30days v2.9.8-global."""

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

# Direct imports to avoid http.py naming conflict
import lib.schema as schema
import lib.normalize as normalize
import lib.score as score
import lib.dedupe as dedupe


def test_bilibili_item():
    """Test BilibiliItem schema and scoring."""
    print("Testing BilibiliItem...")

    item = schema.BilibiliItem(
        id="test_bv",
        title="测试视频",
        url="https://www.bilibili.com/video/test123",
        bvid="test123",
        channel_name="测试UP主",
        date="2026-04-01",
        engagement=schema.Engagement(
            views=10000,
            danmaku=500,
            likes=1000,
            num_comments=200,
            favorites=300,
        ),
    )

    # Test to_dict
    d = item.to_dict()
    assert d["id"] == "test_bv"
    assert d["title"] == "测试视频"
    assert d["engagement"]["views"] == 10000
    assert d["engagement"]["danmaku"] == 500

    # Test scoring
    scored = score.score_bilibili_items([item])[0]
    assert scored.score > 0
    assert scored.subs.engagement > 0

    print(f"  [OK] BilibiliItem score: {scored.score}")
    print(f"  [OK] Engagement: {scored.subs.engagement}")


def test_zhihu_item():
    """Test ZhihuItem schema and scoring."""
    print("Testing ZhihuItem...")

    item = schema.ZhihuItem(
        id="test_zh",
        title="如何学好Python？",
        excerpt="Python是一门很好的编程语言...",
        url="https://zhuanlan.zhihu.com/p/12345",
        author="知乎用户",
        date="2026-04-01",
        engagement=schema.Engagement(
            voteups=1000,
            num_comments=200,
            thanks=50,
            collects=300,
        ),
    )

    d = item.to_dict()
    assert d["id"] == "test_zh"
    assert d["title"] == "如何学好Python？"
    assert d["engagement"]["voteups"] == 1000

    scored = score.score_zhihu_items([item])[0]
    assert scored.score > 0
    assert scored.subs.engagement > 0

    print(f"  [OK] ZhihuItem score: {scored.score}")
    print(f"  [OK] Engagement: {scored.subs.engagement}")


def test_weibo_item():
    """Test WeiboItem schema and scoring."""
    print("Testing WeiboItem...")

    item = schema.WeiboItem(
        id="test_wb",
        text="这是一条测试微博 #测试",
        url="https://weibo.com/123456/789",
        author_handle="测试用户",
        date="2026-04-01",
        engagement=schema.Engagement(
            likes=500,
            reposts=100,
            num_comments=50,
        ),
    )

    d = item.to_dict()
    assert d["id"] == "test_wb"
    assert d["text"] == "这是一条测试微博 #测试"
    assert d["engagement"]["likes"] == 500

    scored = score.score_weibo_items([item])[0]
    assert scored.score > 0

    print(f"  [OK] WeiboItem score: {scored.score}")


def test_douyin_item():
    """Test DouyinItem schema and scoring."""
    print("Testing DouyinItem...")

    item = schema.DouyinItem(
        id="test_dy",
        text="这是抖音测试视频 #抖音 #热门",
        url="https://www.douyin.com/video/123",
        author_handle="抖音用户",
        date="2026-04-01",
        engagement=schema.Engagement(
            views=100000,
            likes=10000,
            num_comments=500,
            shares=200,
        ),
        hashtags=["#抖音", "#热门"],
    )

    d = item.to_dict()
    assert d["id"] == "test_dy"
    assert d["hashtags"] == ["#抖音", "#热门"]

    scored = score.score_douyin_items([item])[0]
    assert scored.score > 0

    print(f"  [OK] DouyinItem score: {scored.score}")


def test_baidu_item():
    """Test BaiduItem schema and scoring."""
    print("Testing BaiduItem...")

    item = schema.BaiduItem(
        id="test_bd",
        title="百度搜索结果",
        url="https://example.com/article",
        source_domain="example.com",
        snippet="这是搜索结果摘要...",
        date="2026-04-01",
    )

    d = item.to_dict()
    assert d["id"] == "test_bd"
    assert d["source_domain"] == "example.com"

    scored = score.score_baidu_items([item])[0]
    assert scored.score >= 0  # Baidu has no engagement, score might be lower

    print(f"  [OK] BaiduItem score: {scored.score}")


def test_normalize():
    """Test normalize functions for Chinese platforms."""
    print("Testing normalize functions...")

    # Test Bilibili normalize
    raw_bilibili = [{
        "id": "bv123",
        "title": "测试",
        "url": "https://bilibili.com/v/bv123",
        "bvid": "bv123",
        "channel_name": "UP主",
        "date": "2026-04-01",
        "engagement": {"views": 1000, "likes": 100},
    }]

    normalized = normalize.normalize_bilibili_items(raw_bilibili, "2026-03-01", "2026-04-30")
    assert len(normalized) == 1
    assert isinstance(normalized[0], schema.BilibiliItem)
    print("  [OK] Bilibili normalize")

    # Test Zhihu normalize
    raw_zhihu = [{
        "id": "zh123",
        "title": "问题",
        "excerpt": "描述",
        "url": "https://zhihu.com/q/123",
        "author": "用户",
        "date": "2026-04-01",
        "engagement": {"voteups": 100, "comments": 10},
    }]

    normalized = normalize.normalize_zhihu_items(raw_zhihu, "2026-03-01", "2026-04-30")
    assert len(normalized) == 1
    assert isinstance(normalized[0], schema.ZhihuItem)
    print("  [OK] Zhihu normalize")


def test_dedupe():
    """Test dedupe functions for Chinese platforms."""
    print("Testing dedupe functions...")

    items = [
        schema.BilibiliItem(
            id="bv1",
            title="测试视频标题",
            url="https://bilibili.com/v/1",
            bvid="bv1",
            channel_name="UP主",
            date="2026-04-01",
            score=50,
        ),
        schema.BilibiliItem(
            id="bv2",
            title="测试视频标题",  # Duplicate title
            url="https://bilibili.com/v/2",
            bvid="bv2",
            channel_name="UP主2",
            date="2026-04-01",
            score=40,
        ),
    ]

    deduped = dedupe.dedupe_bilibili(items, threshold=0.7)
    assert len(deduped) == 1  # One duplicate removed
    assert deduped[0].id == "bv1"  # Higher score kept

    print("  [OK] Bilibili dedupe")


def test_report_integration():
    """Test Report with Chinese platform fields."""
    print("Testing Report integration...")

    report = schema.create_report(
        topic="测试主题",
        from_date="2026-03-01",
        to_date="2026-04-30",
        mode="all",
    )

    # Add Chinese platform items
    report.bilibili = [
        schema.BilibiliItem(
            id="bv1",
            title="B站视频",
            url="https://bilibili.com/v/1",
            bvid="bv1",
            channel_name="UP主",
            date="2026-04-01",
            score=80,
        ),
    ]

    report.zhihu = [
        schema.ZhihuItem(
            id="zh1",
            title="知乎问题",
            excerpt="描述",
            url="https://zhihu.com/q/1",
            author="用户",
            date="2026-04-01",
            score=70,
        ),
    ]

    # Test to_dict
    d = report.to_dict()
    assert "bilibili" in d
    assert "zhihu" in d
    assert len(d["bilibili"]) == 1
    assert len(d["zhihu"]) == 1
    assert d["bilibili"][0]["title"] == "B站视频"

    print("  [OK] Report integration")


def main():
    """Run all tests."""
    print("=" * 50)
    print("last30days v2.9.8-global - Chinese Platform Tests")
    print("=" * 50)
    print()

    try:
        test_bilibili_item()
        test_zhihu_item()
        test_weibo_item()
        test_douyin_item()
        test_baidu_item()
        test_normalize()
        test_dedupe()
        test_report_integration()

        print()
        print("=" * 50)
        print("[OK] All tests passed!")
        print("=" * 50)
        return 0

    except AssertionError as e:
        print()
        print("=" * 50)
        print("[FAIL] Test failed: {e}")
        print("=" * 50)
        return 1
    except Exception as e:
        print()
        print("=" * 50)
        print("[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 50)
        return 1


if __name__ == "__main__":
    sys.exit(main())
