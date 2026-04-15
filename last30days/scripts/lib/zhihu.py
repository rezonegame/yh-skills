"""Zhihu (知乎) search module for last30days skill.

Uses 知乎 public search API (free, no API key required).
API: https://www.zhihu.com/api/v4/search_v3
"""

import re
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from . import dates


def search_zhihu(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
    cookie: Optional[str] = None,
) -> Dict[str, Any]:
    """Search Zhihu for content on a topic.

    Args:
        topic: Search topic/keyword
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: Research depth (quick/default/deep)
        cookie: Optional Zhihu cookie for better access

    Returns:
        Dict with raw content data (contains 'items' list or 'error' on failure)
    """
    import requests

    # Convert depth string to int
    depth_map = {"quick": 10, "default": 20, "deep": 30}
    depth_int = depth_map.get(depth, 20)

    # 知乎搜索API
    search_url = "https://www.zhihu.com/api/v4/search_v3"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.zhihu.com/search",
    }

    if cookie:
        headers["Cookie"] = cookie

    params = {
        "guzzles": "true",  # 启用高亮
        "q": topic,
        "correction": 1,
        "offset": 0,
        "limit": min(depth_int, 20),
    }

    try:
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = []
        results = data.get("data", [])

        for result in results[:depth_int]:
            object_type = result.get("type", "")

            # 只处理回答和文章
            if object_type not in ["search_answer", "search_article"]:
                continue

            # 提取通用字段
            highlight = result.get("highlight", {})
            title = highlight.get("title", "")
            description = highlight.get("description", "")

            # 清理HTML标签
            title = re.sub(r'<[^>]+>', '', title)
            description = re.sub(r'<[^>]+>', '', description)

            # 提取对象数据
            obj = result.get("object", {})

            # 获取作者信息
            author = obj.get("author", {})
            author_name = author.get("name", "匿名用户")

            # 获取URL
            if object_type == "search_answer":
                question = obj.get("question", {})
                url = question.get("url", "")
                question_id = question.get("id", "")
                answer_id = obj.get("id", "")
                if not url:
                    url = f"https://www.zhihu.com/question/{question_id}/answer/{answer_id}"
            else:  # article
                url = obj.get("url", "")
                if not url:
                    article_id = obj.get("id", "")
                    url = f"https://zhuanlan.zhihu.com/p/{article_id}"

            # 获取互动数据
            voteup_count = obj.get("voteup_count", 0)
            comment_count = obj.get("comment_count", 0)
            thanks_count = obj.get("thanks_count", 0)
            collect_count = obj.get("collect_count", 0)

            # 获取创建时间
            created_time = obj.get("created_time", 0)
            if created_time:
                created_date = datetime.fromtimestamp(created_time).strftime("%Y-%m-%d")
            else:
                created_date = None

            # 检查日期范围
            if created_date:
                if not dates.is_date_in_range(created_date, from_date, to_date):
                    continue

            items.append({
                "id": obj.get("id", ""),
                "title": title,
                "excerpt": description[:500],  # 限制摘要长度
                "url": url,
                "author": author_name,
                "date": created_date,
                "engagement": {
                    "voteups": voteup_count,
                    "comments": comment_count,
                    "thanks": thanks_count,
                    "collects": collect_count,
                },
            })

        return {"items": items}

    except Exception as e:
        return {"items": [], "error": str(e)}


def get_zhihu_hot(cookie: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get Zhihu hot questions list.

    Args:
        cookie: Optional Zhihu cookie for better access

    Returns:
        List of hot question data
    """
    import requests

    hot_url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.zhihu.com/hot",
    }

    if cookie:
        headers["Cookie"] = cookie

    try:
        response = requests.get(hot_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = []
        hot_list = data.get("data", [])

        for item in hot_list[:30]:  # 只取前30个热榜
            target = item.get("target", "")

            if isinstance(target, str):
                import json
                target = json.loads(target)

            title = target.get("title", "")
            question_id = target.get("id", "")
            url = f"https://www.zhihu.com/question/{question_id}"

            # 热度值
            hot_value = item.get("detail_text", "")
            # 提取数字
            hot_match = re.search(r'[\d.]+', hot_value)
            hot_score = float(hot_match.group()) if hot_match else 0

            # 摘要
            excerpt = target.get("excerpt", "")

            # 作者（通常是问题提出者）
            author = target.get("author", {})
            author_name = author.get("name", "知乎用户")

            # 互动数据（粗略估算）
            answer_count = target.get("answer_count", 0)
            followers_count = target.get("followers_count", 0)

            items.append({
                "id": f"ZH_HOT_{question_id}",
                "title": title,
                "excerpt": excerpt[:300] if excerpt else "",
                "url": url,
                "author": author_name,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "engagement": {
                    "hot_score": hot_score,
                    "answers": answer_count,
                    "followers": followers_count,
                },
            })

        return items

    except Exception as e:
        print(f"获取知乎热榜出错: {e}")
        return []


def parse_zhihu_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Zhihu API response into the format expected by last30days.

    Args:
        response: Raw response from search_zhihu or get_zhihu_hot

    Returns:
        List of parsed content data
    """
    return response.get("items", [])

