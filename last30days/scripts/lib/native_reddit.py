"""Native Reddit JSON client for Reddit discovery (no API key required).

Uses Reddit's public search JSON endpoint as a zero-dependency fallback
when no LLM API keys (OpenAI/Gemini) are configured.
"""

import re
import sys
import time
import urllib.parse
from typing import Any, Dict, List, Optional

from . import http, dates

# Depth configurations: max results to request
DEPTH_CONFIG = {
    "quick": 15,
    "default": 30,
    "deep": 50,
}

# Reddit search sort options
SORT_OPTIONS = ["relevance", "new", "top"]


def _log_error(msg: str):
    """Log error to stderr."""
    sys.stderr.write(f"[NATIVE-REDDIT ERROR] {msg}\n")
    sys.stderr.flush()


def _log_info(msg: str):
    """Log info to stderr."""
    sys.stderr.write(f"[NATIVE-REDDIT] {msg}\n")
    sys.stderr.flush()


def _extract_core_subject(topic: str) -> str:
    """Extract core subject from verbose query for search.

    Same logic as openai_reddit._extract_core_subject().
    """
    noise = ['best', 'top', 'how to', 'tips for', 'practices', 'features',
             'killer', 'guide', 'tutorial', 'recommendations', 'advice',
             'prompting', 'using', 'for', 'with', 'the', 'of', 'in', 'on']
    words = topic.lower().split()
    result = [w for w in words if w not in noise]
    return ' '.join(result[:4]) or topic  # Keep max 4 words


def search_reddit(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> Dict[str, Any]:
    """Search Reddit using the native JSON search endpoint.

    Args:
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: Research depth - "quick", "default", or "deep"

    Returns:
        Dict with "items" key containing raw search results
    """
    limit = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])
    core_topic = _extract_core_subject(topic)

    _log_info(f"Searching Reddit natively for: '{core_topic}' (depth={depth}, limit={limit})")

    all_items = []
    seen_urls = set()

    # Try multiple sort strategies to get diverse results
    sort_modes = ["relevance", "new"] if depth != "deep" else ["relevance", "new", "top"]

    for sort_mode in sort_modes:
        try:
            query = urllib.parse.quote_plus(core_topic)
            url = (
                f"https://www.reddit.com/search.json"
                f"?q={query}"
                f"&sort={sort_mode}"
                f"&t=month"  # Restrict to last month
                f"&limit={min(limit, 100)}"  # Reddit caps at 100
                f"&raw_json=1"
                f"&type=link"  # Only posts, not comments
            )

            headers = {
                "User-Agent": http.USER_AGENT,
                "Accept": "application/json",
            }

            data = http.get(url, headers=headers, timeout=20, retries=2)

            children = data.get("data", {}).get("children", [])
            _log_info(f"  sort={sort_mode}: {len(children)} results")

            for child in children:
                if child.get("kind") != "t3":  # t3 = link/submission
                    continue
                post = child.get("data", {})
                permalink = post.get("permalink", "")
                if not permalink:
                    continue

                post_url = f"https://www.reddit.com{permalink}"
                if post_url in seen_urls:
                    continue
                seen_urls.add(post_url)

                # Parse date from created_utc
                post_date = None
                created_utc = post.get("created_utc")
                if created_utc:
                    post_date = dates.timestamp_to_date(created_utc)

                # Build relevance score from Reddit's own signals
                score = post.get("score", 0)
                num_comments = post.get("num_comments", 0)
                # Normalize relevance: high upvotes + comments = high relevance
                relevance = min(1.0, 0.4 + (score / 500) * 0.3 + (num_comments / 100) * 0.3)

                item = {
                    "title": str(post.get("title", "")).strip(),
                    "url": post_url,
                    "subreddit": str(post.get("subreddit", "")).strip(),
                    "date": post_date,
                    "why_relevant": f"Found via Reddit search (sort={sort_mode})",
                    "relevance": round(relevance, 2),
                    # Extra fields for enrichment compatibility
                    "_score": score,
                    "_num_comments": num_comments,
                }

                all_items.append(item)

        except http.HTTPError as e:
            if e.status_code == 429:
                _log_info(f"Reddit rate-limited (429) on sort={sort_mode}. Stopping search.")
                # Wait before any further requests
                time.sleep(2)
                break
            _log_error(f"HTTP error on sort={sort_mode}: {e}")
        except Exception as e:
            _log_error(f"Error on sort={sort_mode}: {e}")

    # If original topic differs from core, try a retry with full topic
    if len(all_items) < 5 and core_topic.lower() != topic.lower():
        _log_info(f"Few results ({len(all_items)}), retrying with full topic: '{topic}'")
        try:
            query = urllib.parse.quote_plus(topic)
            url = (
                f"https://www.reddit.com/search.json"
                f"?q={query}"
                f"&sort=relevance"
                f"&t=month"
                f"&limit={min(limit, 100)}"
                f"&raw_json=1"
                f"&type=link"
            )
            headers = {
                "User-Agent": http.USER_AGENT,
                "Accept": "application/json",
            }
            data = http.get(url, headers=headers, timeout=20, retries=2)
            children = data.get("data", {}).get("children", [])
            for child in children:
                if child.get("kind") != "t3":
                    continue
                post = child.get("data", {})
                permalink = post.get("permalink", "")
                if not permalink:
                    continue
                post_url = f"https://www.reddit.com{permalink}"
                if post_url in seen_urls:
                    continue
                seen_urls.add(post_url)

                post_date = None
                created_utc = post.get("created_utc")
                if created_utc:
                    post_date = dates.timestamp_to_date(created_utc)

                score = post.get("score", 0)
                num_comments = post.get("num_comments", 0)
                relevance = min(1.0, 0.4 + (score / 500) * 0.3 + (num_comments / 100) * 0.3)

                all_items.append({
                    "title": str(post.get("title", "")).strip(),
                    "url": post_url,
                    "subreddit": str(post.get("subreddit", "")).strip(),
                    "date": post_date,
                    "why_relevant": "Found via Reddit search (full topic retry)",
                    "relevance": round(relevance, 2),
                    "_score": score,
                    "_num_comments": num_comments,
                })
        except Exception as e:
            _log_error(f"Full topic retry failed: {e}")

    _log_info(f"Total unique results: {len(all_items)}")
    return {"items": all_items}


def parse_reddit_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse native Reddit response to extract Reddit items.

    Args:
        response: Response dict from search_reddit()

    Returns:
        List of item dicts (same format as openai_reddit output)
    """
    items = response.get("items", [])

    if "error" in response:
        _log_error(f"Response error: {response['error']}")
        return []

    # Clean and assign IDs
    clean_items = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            continue

        url = item.get("url", "")
        if not url or "reddit.com" not in url:
            continue

        clean_item = {
            "id": f"R{i+1}",
            "title": str(item.get("title", "")).strip(),
            "url": url,
            "subreddit": str(item.get("subreddit", "")).strip().lstrip("r/"),
            "date": item.get("date"),
            "why_relevant": str(item.get("why_relevant", "")).strip(),
            "relevance": min(1.0, max(0.0, float(item.get("relevance", 0.5)))),
        }

        # Validate date format
        if clean_item["date"]:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(clean_item["date"])):
                clean_item["date"] = None

        clean_items.append(clean_item)

    return clean_items
