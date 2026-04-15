"""Baidu (百度) search module for last30days skill.

Supports two modes:
1. API mode: Requires BAIDU_API_KEY + BAIDU_SECRET_KEY (official API)
2. Public mode: Uses public web interface (limited, requires cookies)
"""

import re
import json
import base64
import hashlib
import time
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from . import dates


def search_baidu(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Search Baidu for web content on a topic.

    Args:
        topic: Search topic/keyword
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: Research depth (quick/default/deep)
        api_key: Baidu API key
        secret_key: Baidu Secret Key

    Returns:
        Dict with raw search result data (contains 'items' list or 'error' on failure)
    """
    # Convert depth string to int
    depth_map = {"quick": 10, "default": 20, "deep": 30}
    depth_int = depth_map.get(depth, 20)

    # 如果有API密钥，使用官方API
    if api_key and secret_key:
        return _search_baidu_api(topic, from_date, to_date, depth_int, api_key, secret_key)
    else:
        return _search_baidu_public(topic, from_date, to_date, depth_int)


def _search_baidu_api(
    topic: str,
    from_date: str,
    to_date: str,
    depth_int: int,
    api_key: str,
    secret_key: str,
) -> Dict[str, Any]:
    """Search Baidu using official API."""
    import requests

    # 百度搜索API端点
    api_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/plugin/comparable_search"

    # 获取access token
    access_token = _get_baidu_access_token(api_key, secret_key)
    if not access_token:
        return {"items": [], "error": "获取百度access token失败"}

    headers = {
        "Content-Type": "application/json",
    }

    params = {
        "access_token": access_token,
    }

    data = {
        "query": topic,
        "top_num": min(depth_int, 20),
    }

    try:
        response = requests.post(api_url, params=params, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()

        items = []

        # 解析返回结果
        if "result" in result:
            results = result["result"]

            for item in results[:depth_int]:
                title = item.get("title", "")
                url = item.get("url", "")
                snippet = item.get("content", "")
                source = item.get("source", "")

                # 清理HTML标签
                title = re.sub(r'<[^>]+>', '', title)
                snippet = re.sub(r'<[^>]+>', '', snippet)

                # 提取域名
                from urllib.parse import urlparse
                domain = urlparse(url).netloc

                items.append({
                    "id": hashlib.md5(url.encode()).hexdigest()[:16],
                    "title": title,
                    "snippet": snippet[:500],
                    "url": url,
                    "source_domain": domain,
                    "date": None,  # 百度API不直接提供日期
                    "engagement": None,  # 百度API不提供互动数据
                })

        return {"items": items}

    except Exception as e:
        return {"items": [], "error": str(e)}


def _get_baidu_access_token(api_key: str, secret_key: str) -> Optional[str]:
    """Get Baidu API access token."""
    import requests

    token_url = "https://aip.baidubce.com/oauth/2.0/token"

    params = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret_key,
    }

    try:
        response = requests.post(token_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return data.get("access_token")

    except Exception as e:
        print(f"获取百度access token出错: {e}")
        return None


def _search_baidu_public(
    topic: str,
    from_date: str,
    to_date: str,
    depth_int: int,
) -> Dict[str, Any]:
    """Search Baidu using public web interface (limited).

    Note: Baidu public interface has strict anti-scraping measures.
    For production use, consider using the official API.
    """
    import requests

    # 百度搜索URL
    search_url = "https://www.baidu.com/s"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    params = {
        "wd": topic,
        "rn": str(min(depth_int, 50)),
        "pn": "0",
    }

    try:
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        # 解析HTML响应
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(response.text, 'html.parser')
        items = []

        # 查找搜索结果
        results = soup.find_all('div', class_='result')

        for result in results[:depth_int]:
            # 提取标题和链接
            title_tag = result.find('h3')
            if not title_tag:
                continue

            a_tag = title_tag.find('a')
            if not a_tag:
                continue

            title = a_tag.get_text(strip=True)
            url = a_tag.get('href', '')

            # 百度的链接需要解析才能得到真实URL
            # 这里简化处理，直接使用百度链接

            # 提取摘要
            snippet_tag = result.find('div', class_='c-abstract')
            if not snippet_tag:
                snippet_tag = result.find('div', class_='c-span-last')

            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""

            # 提取来源
            source_tag = result.find('span', class_='c-color-gray')
            source = source_tag.get_text(strip=True) if source_tag else ""

            # 提取域名
            from urllib.parse import urlparse
            domain = urlparse(url).netloc

            # 清理数据
            title = re.sub(r'\s+', ' ', title)
            snippet = re.sub(r'\s+', ' ', snippet)

            if title and url:
                items.append({
                    "id": hashlib.md5(url.encode()).hexdigest()[:16],
                    "title": title,
                    "snippet": snippet[:500],
                    "url": url,
                    "source_domain": domain or source,
                    "date": None,
                    "engagement": None,
                })

        return {"items": items}

    except ImportError:
        return {"items": [], "error": "需要安装beautifulsoup4: pip install beautifulsoup4"}
    except Exception as e:
        return {"items": [], "error": str(e)}


def get_baidu_hot(
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Get Baidu hot search topics list.

    Args:
        api_key: Baidu API key
        secret_key: Baidu Secret Key

    Returns:
        List of hot topic data
    """
    import requests

    # 百度热搜URL
    hot_url = "https://top.baidu.com/api/board"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://top.baidu.com/",
    }

    params = {
        "platform": "web",
        "showed_tab": "realtime",
    }

    try:
        response = requests.get(hot_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        items = []

        # 解析热搜数据
        if "data" in data and "cards" in data["data"]:
            cards = data["data"]["cards"]

            for card in cards:
                hot_content = card.get("content", [])

                for item in hot_content[:50]:  # 只取前50个热搜
                    title = item.get("word", "")
                    if not title:
                        continue

                    # 热度值
                    hot_score = item.get("hotScore", 0)

                    # 摘要
                    desc = item.get("desc", "")

                    # 构建搜索链接
                    encoded_title = requests.utils.quote(title)
                    url = f"https://www.baidu.com/s?wd={encoded_title}"

                    # 分类
                    category = item.get("category", "")

                    items.append({
                        "id": f"BD_HOT_{hashlib.md5(title.encode()).hexdigest()[:8]}",
                        "title": title,
                        "snippet": desc[:300] if desc else "",
                        "url": url,
                        "source_domain": "baidu.com",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "engagement": {
                            "hot_score": hot_score,
                            "category": category,
                        },
                    })

        return items

    except Exception as e:
        print(f"获取百度热搜出错: {e}")
        return []


def parse_baidu_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Baidu API response into the format expected by last30days.

    Args:
        response: Raw response from search_baidu or get_baidu_hot

    Returns:
        List of parsed search result data
    """
    return response.get("items", [])
