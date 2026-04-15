"""Douyin (抖音) search module for last30days skill.

Supports two modes:
1. TikHub API mode: Requires TIKHUB_API_KEY (recommended)
2. Public mode: Uses public web interface (limited)
"""

import re
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from . import dates


def search_douyin(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Search Douyin for videos on a topic.

    Args:
        topic: Search topic/keyword
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: Research depth (quick/default/deep)
        api_key: TikHub API key (or TIKHUB_API_KEY env var)

    Returns:
        Dict with raw video data (contains 'items' list or 'error' on failure)
    """
    # Convert depth string to int
    depth_map = {"quick": 10, "default": 20, "deep": 30}
    depth_int = depth_map.get(depth, 20)

    # 如果有api_key，使用TikHub API
    if api_key:
        return _search_douyin_tikhub(topic, from_date, to_date, depth_int, api_key)
    else:
        return _search_douyin_public(topic, from_date, to_date, depth_int)


def _search_douyin_tikhub(
    topic: str,
    from_date: str,
    to_date: str,
    depth_int: int,
    api_key: str,
) -> Dict[str, Any]:
    """Search Douyin using TikHub API."""
    import requests

    # TikHub API端点
    api_url = "https://api.tikhub.com/api/douyin/search/videos"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    params = {
        "keyword": topic,
        "count": min(depth, 20),
        "sort_type": 0,  # 0: 综合排序, 1: 最新发布
    }

    try:
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = []

        if data.get("code") != 0:
            return {"items": [], "error": f"TikHub API错误: {data.get('message', 'Unknown error')}"}

        videos = data.get("data", {}).get("aweme_list", [])

        for video in videos[:depth_int]:
            # 提取视频数据
            aweme_id = video.get("aweme_id", "")
            desc = video.get("desc", "")

            # 提取作者信息
            author = video.get("author", {})
            author_name = author.get("nickname", "")
            author_id = author.get("unique_id", "") or author.get("sec_uid", "")

            # 构建URL
            url = f"https://www.douyin.com/video/{aweme_id}"

            # 提取互动数据
            statistics = video.get("statistics", {})
            play_count = statistics.get("play_count", 0)
            digg_count = statistics.get("digg_count", 0)  # 点赞
            comment_count = statistics.get("comment_count", 0)
            share_count = statistics.get("share_count", 0)
            collect_count = statistics.get("collect_count", 0)  # 收藏

            # 提取发布时间
            create_time = video.get("create_time", 0)
            if create_time:
                created_date = datetime.fromtimestamp(create_time).strftime("%Y-%m-%d")
            else:
                created_date = None

            # 检查日期范围
            if created_date:
                if not dates.is_date_in_range(created_date, from_date, to_date):
                    continue

            # 提取话题标签
            hashtags = []
            text_extra = video.get("text_extra", [])
            for tag in text_extra:
                hashtag_name = tag.get("hashtag_name", "")
                if hashtag_name:
                    hashtags.append(f"#{hashtag_name}")

            items.append({
                "id": aweme_id,
                "text": desc[:500],  # 限制长度
                "url": url,
                "author_handle": author_name,
                "date": created_date,
                "engagement": {
                    "views": play_count,
                    "likes": digg_count,
                    "comments": comment_count,
                    "shares": share_count,
                    "collects": collect_count,
                },
                "hashtags": hashtags,
            })

        return {"items": items}

    except Exception as e:
        return {"items": [], "error": str(e)}


def _search_douyin_public(
    topic: str,
    from_date: str,
    to_date: str,
    depth_int: int,
) -> Dict[str, Any]:
    """Search Douyin using public web interface (limited results).

    Note: Public interface has limitations and may require cookies for better results.
    """
    import requests

    # 抖音搜索接口（需要cookies才能正常工作）
    search_url = "https://www.douyin.com/aweme/v1/web/general/search/single/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.douyin.com/",
    }

    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "search_channel": "aweme_video_web",
        "sort_type": "0",
        "publish_time": "0",
        "keyword": topic,
        "search_source": "normal_search",
        "query_correct_type": "1",
        "is_filter_search": "0",
        "from_group_id": "",
        "offset": "0",
        "count": str(min(depth_int, 20)),
    }

    try:
        response = requests.get(search_url, params=params, headers=headers, timeout=10)

        # 抖音返回的是script标签中的JSON
        if response.status_code != 200:
            return {"items": [], "error": f"抖音公共搜索失败: HTTP {response.status_code}"}

        # 尝试解析响应
        # 实际使用中，抖音需要更复杂的处理（包括ttwid cookie）
        # 这里提供一个基础框架

        return {"items": [], "error": "抖音公共接口需要有效的cookie才能正常工作，建议使用TikHub API"}

    except Exception as e:
        return {"items": [], "error": str(e)}


def get_douyin_hot(api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get Douyin hot videos list.

    Args:
        api_key: TikHub API key

    Returns:
        List of hot video data
    """
    if api_key:
        return _get_douyin_hot_tikhub(api_key)
    else:
        return _get_douyin_hot_public()


def _get_douyin_hot_tikhub(api_key: str) -> List[Dict[str, Any]]:
    """Get Douyin hot videos using TikHub API."""
    import requests

    # TikHub API端点
    api_url = "https://api.tikhub.com/api/douyin/hot/feed/list"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = []

        if data.get("code") != 0:
            return {"items": [], "error": f"TikHub API错误: {data.get('message', 'Unknown error')}"}

        videos = data.get("data", {}).get("aweme_list", [])

        for video in videos[:20]:  # 只取前20个热门视频
            aweme_id = video.get("aweme_id", "")
            desc = video.get("desc", "")

            author = video.get("author", {})
            author_name = author.get("nickname", "")

            url = f"https://www.douyin.com/video/{aweme_id}"

            statistics = video.get("statistics", {})
            play_count = statistics.get("play_count", 0)
            digg_count = statistics.get("digg_count", 0)
            comment_count = statistics.get("comment_count", 0)

            # 热度值（基于播放和点赞）
            hot_score = play_count + digg_count * 10

            create_time = video.get("create_time", 0)
            if create_time:
                created_date = datetime.fromtimestamp(create_time).strftime("%Y-%m-%d")
            else:
                created_date = None

            items.append({
                "id": aweme_id,
                "text": desc[:300],
                "url": url,
                "author_handle": author_name,
                "date": created_date,
                "engagement": {
                    "views": play_count,
                    "likes": digg_count,
                    "comments": comment_count,
                    "hot_score": hot_score,
                },
            })

        return items

    except Exception as e:
        print(f"TikHub获取抖音热门出错: {e}")
        return []


def _get_douyin_hot_public() -> List[Dict[str, Any]]:
    """Get Douyin hot videos using public interface (limited)."""
    import requests

    # 抖音热门页面
    hot_url = "https://www.douyin.com/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.douyin.com/",
    }

    try:
        response = requests.get(hot_url, headers=headers, timeout=10)

        # 抖音热门数据在页面中的script标签里
        # 需要正则匹配和JSON解析
        # 这里提供一个基础框架

        print("注意: 抖音热门需要有效的cookie才能正常工作")
        print("建议使用TikHub API: https://www.tikhub.com/")

        return []

    except Exception as e:
        print(f"获取抖音热门出错: {e}")
        return []


def parse_douyin_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Douyin API response into the format expected by last30days.

    Args:
        response: Raw response from search_douyin or get_douyin_hot

    Returns:
        List of parsed video data
    """
    return response.get("items", [])
