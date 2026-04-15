"""Weibo (微博) search module for last30days skill.

Supports two modes:
1. API mode: Requires WEIBO_ACCESS_TOKEN (official API)
2. Public mode: Uses mobile web interface (no API key required)
"""

import re
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from . import dates


def search_weibo(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
    access_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Search Weibo for posts on a topic.

    Args:
        topic: Search topic/keyword
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: Research depth (quick/default/deep)
        access_token: Optional Weibo access token for API mode

    Returns:
        Dict with raw post data (contains 'items' list or 'error' on failure)
    """
    # Convert depth string to int
    depth_map = {"quick": 10, "default": 20, "deep": 30}
    depth_int = depth_map.get(depth, 20)

    # 如果有access_token，使用API模式
    if access_token:
        return _search_weibo_api(topic, from_date, to_date, depth_int, access_token)
    else:
        return _search_weibo_public(topic, from_date, to_date, depth_int)


def _search_weibo_api(
    topic: str,
    from_date: str,
    to_date: str,
    depth_int: int,
    token: str,
) -> Dict[str, Any]:
    """Search Weibo using official API."""
    import requests

    api_url = "https://api.weibo.com/2/search/topics.json"

    headers = {
        "Authorization": f"Bearer {token}",
    }

    params = {
        "q": topic,
        "count": min(depth_int, 50),
    }

    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = []
        statuses = data.get("statuses", [])

        for status in statuses[:depth_int]:
            # 提取文本
            text = status.get("text", "")
            # 清理HTML标签
            text = re.sub(r'<[^>]+>', '', text)

            # 提取作者信息
            user = status.get("user", {})
            author_screen_name = user.get("screen_name", "")
            author_id = user.get("id", "")

            # 构建URL
            mid = status.get("mid", "")
            url = f"https://weibo.com/{author_id}/{mid}"

            # 提取互动数据
            reposts_count = status.get("reposts_count", 0)
            comments_count = status.get("comments_count", 0)
            attitudes_count = status.get("attitudes_count", 0)

            # 提取发布时间
            created_at = status.get("created_at", "")
            if created_at:
                try:
                    # 微博时间格式: "Tue May 31 20:12:45 +0800 2024"
                    created_date = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
                except:
                    created_date = None
            else:
                created_date = None

            # 检查日期范围
            if created_date:
                if not dates.is_date_in_range(created_date, from_date, to_date):
                    continue

            items.append({
                "id": mid,
                "text": text,
                "url": url,
                "author_handle": author_screen_name,
                "date": created_date,
                "engagement": {
                    "reposts": reposts_count,
                    "comments": comments_count,
                    "likes": attitudes_count,
                },
            })

        return {"items": items}

    except Exception as e:
        return {"items": [], "error": str(e)}


def _search_weibo_public(
    topic: str,
    from_date: str,
    to_date: str,
    depth_int: int,
) -> Dict[str, Any]:
    """Search Weibo using mobile web interface (no API key required)."""
    import requests

    # 微博移动端搜索接口
    search_url = "https://m.weibo.cn/api/container/getIndex"

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
        "Referer": "https://m.weibo.cn/search",
    }

    params = {
        "containerid": f"100103type=1&q={topic}",
        "page_type": "searchall",
        "page": 1,
    }

    try:
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = []

        # 检查返回数据结构
        if data.get("ok") != 1:
            return {"items": [], "error": "微博API返回错误"}

        # 获取卡片列表
        cards = data.get("data", {}).get("cards", [])

        for card in cards[:depth_int]:
            card_group = card.get("card_group", [])

            for item in card_group:
                # 提取微博数据
                mblog = item.get("mblog", {})
                if not mblog:
                    continue

                # 提取文本
                text = mblog.get("text", "")
                # 清理HTML标签和emoji
                text = re.sub(r'<[^>]+>', '', text)
                text = re.sub(r'\[\S+\]', '', text)  # 移除[表情]等

                # 提取作者信息
                user = mblog.get("user", {})
                author_screen_name = user.get("screen_name", "")
                author_id = user.get("id", "")

                # 构建URL
                mid = mblog.get("mid", "")
                url = f"https://weibo.com/{author_id}/{mid}"

                # 提取互动数据
                reposts_count = mblog.get("reposts_count", 0)
                comments_count = mblog.get("comments_count", 0)
                attitudes_count = mblog.get("attitudes_count", 0)

                # 提取发布时间
                created_at = mblog.get("created_at", "")
                if created_at:
                    try:
                        # 尝试解析不同格式
                        if "分钟前" in created_at:
                            created_date = (datetime.now() - timedelta(minutes=int(created_at.replace("分钟前", "")))).strftime("%Y-%m-%d")
                        elif "小时前" in created_at:
                            created_date = (datetime.now() - timedelta(hours=int(created_at.replace("小时前", "")))).strftime("%Y-%m-%d")
                        elif "今天" in created_at:
                            created_date = datetime.now().strftime("%Y-%m-%d")
                        else:
                            # 尝试标准格式
                            created_date = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
                    except:
                        created_date = None
                else:
                    created_date = None

                # 检查日期范围（宽松模式，因为公共接口时间可能不准）
                if created_date and created_date < from_date:
                    continue

                items.append({
                    "id": mid,
                    "text": text[:500],  # 限制长度
                    "url": url,
                    "author_handle": author_screen_name,
                    "date": created_date,
                    "engagement": {
                        "reposts": reposts_count,
                        "comments": comments_count,
                        "likes": attitudes_count,
                    },
                })

                if len(items) >= depth_int:
                    break

            if len(items) >= depth_int:
                break

        return {"items": items}

    except Exception as e:
        return {"items": [], "error": str(e)}


def get_weibo_hot(token: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get Weibo hot topics list.

    Args:
        token: Optional Weibo access token

    Returns:
        List of hot topic data
    """
    import requests

    # 微博热搜API（公共接口）
    hot_url = "https://weibo.com/ajax/side/hotSearch"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://weibo.com",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.get(hot_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = []
        hot_list = data.get("data", {}).get("realtime", [])

        for item in hot_list[:50]:  # 只取前50个热搜
            word = item.get("word", "")
            # 移除表情符号
            word = re.sub(r'\[\S+\]', '', word).strip()

            if not word:
                continue

            # 构建搜索链接
            encoded_word = requests.utils.quote(word)
            url = f"https://s.weibo.com/weibo?q={encoded_word}"

            # 热度值
            hot_value = item.get("num", 0)
            # 解析热度（如"123万"）
            if isinstance(hot_value, str):
                hot_match = re.search(r'([\d.]+)(万|亿)?', hot_value)
                if hot_match:
                    num = float(hot_match.group(1))
                    unit = hot_match.group(2)
                    if unit == "万":
                        hot_score = num * 10000
                    elif unit == "亿":
                        hot_score = num * 100000000
                    else:
                        hot_score = num
                else:
                    hot_score = 0
            else:
                hot_score = hot_value

            # 分类
            category = item.get("category", "")

            items.append({
                "id": f"WB_HOT_{word}",
                "text": word,
                "url": url,
                "author_handle": "微博热搜",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "engagement": {
                    "hot_score": hot_score,
                    "category": category,
                },
            })

        return items

    except Exception as e:
        print(f"获取微博热搜出错: {e}")
        return []


def parse_weibo_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Weibo API response into the format expected by last30days.

    Args:
        response: Raw response from search_weibo or get_weibo_hot

    Returns:
        List of parsed post data
    """
    return response.get("items", [])

