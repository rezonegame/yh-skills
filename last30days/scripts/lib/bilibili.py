"""Bilibili (B站) search module for last30days skill.

Uses B站 public search API (free, no API key required).
API: https://api.bilibili.com/x/web-interface/search/type
"""

import re
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from . import dates


def search_bilibili(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> Dict[str, Any]:
    """Search Bilibili for videos on a topic.

    Args:
        topic: Search topic/keyword
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: Research depth (quick/default/deep)

    Returns:
        Dict with raw video data (contains 'items' list or 'error' on failure)
    """
    import requests

    # Convert depth string to int
    depth_map = {"quick": 10, "default": 20, "deep": 30}
    depth_int = depth_map.get(depth, 20)

    # B站搜索API
    search_url = "https://api.bilibili.com/x/web-interface/search/type"

    # 搜索参数
    params = {
        "search_type": "video",  # 搜索视频
        "keyword": topic,
        "page": 1,
        "order": "pubdate",  # 按发布日期排序
        "pagesize": min(depth_int, 50),  # B站API限制每页最多50条
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com",
    }

    try:
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("code") != 0:
            return {"items": [], "error": f"B站API错误: {data.get('message', 'Unknown error')}"}

        items = []
        videos = data.get("data", {}).get("result", [])

        for video in videos[:depth_int]:
            # 解析视频数据
            title = video.get("title", "")
            # 清理HTML标签
            title = re.sub(r'<[^>]+>', '', title)

            # 提取发布时间 (B站返回的是时间戳)
            pubdate = video.get("pubdate", 0)
            if pubdate:
                pub_date = datetime.fromtimestamp(pubdate).strftime("%Y-%m-%d")
            else:
                pub_date = None

            # 构建URL
            bvid = video.get("bvid", "")
            url = f"https://www.bilibili.com/video/{bvid}"

            # 提取作者信息
            author = video.get("author", "")
            mid = video.get("mid", "")

            # 提取互动数据
            play = video.get("play", 0)
            danmaku = video.get("video_review", 0)  # 弹幕数
            favorites = video.get("favorites", 0)
            likes = video.get("like", 0)
            comments = video.get("review", 0)

            # 检查日期范围
            if pub_date:
                if not dates.is_date_in_range(pub_date, from_date, to_date):
                    continue

            items.append({
                "id": bvid,
                "title": title,
                "url": url,
                "bvid": bvid,
                "channel_name": author,
                "date": pub_date,
                "engagement": {
                    "views": play,
                    "danmaku": danmaku,
                    "comments": comments,
                    "favorites": favorites,
                    "likes": likes,
                },
            })

        return {"items": items}

    except Exception as e:
        return {"items": [], "error": str(e)}


def get_bilibili_hot() -> List[Dict[str, Any]]:
    """Get Bilibili hot videos list.

    Returns:
        List of hot video data
    """
    import requests

    hot_url = "https://api.bilibili.com/x/web-interface/popular"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com",
    }

    try:
        response = requests.get(hot_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("code") != 0:
            return []

        items = []
        videos = data.get("data", {}).get("list", [])

        for video in videos[:20]:  # 只取前20个热门视频
            title = video.get("title", "")
            title = re.sub(r'<[^>]+>', '', title)

            bvid = video.get("bvid", "")
            url = f"https://www.bilibili.com/video/{bvid}"

            owner = video.get("owner", {})
            author = owner.get("name", "")

            stat = video.get("stat", {})
            play = stat.get("view", 0)
            danmaku = stat.get("danmaku", 0)
            likes = stat.get("like", 0)
            comments = stat.get("reply", 0)
            favorites = stat.get("favorite", 0)

            pubdate = video.get("pubdate", 0)
            if pubdate:
                pub_date = datetime.fromtimestamp(pubdate).strftime("%Y-%m-%d")
            else:
                pub_date = None

            items.append({
                "id": bvid,
                "title": title,
                "url": url,
                "bvid": bvid,
                "channel_name": author,
                "date": pub_date,
                "engagement": {
                    "views": play,
                    "danmaku": danmaku,
                    "comments": comments,
                    "favorites": favorites,
                    "likes": likes,
                },
            })

        return items

    except Exception as e:
        print(f"获取B站热门出错: {e}")
        return []


def parse_bilibili_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Bilibili API response into the format expected by last30days.

    Args:
        response: Raw response from search_bilibili or get_bilibili_hot

    Returns:
        List of parsed video data
    """
    return response.get("items", [])

