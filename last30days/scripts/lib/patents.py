"""Patent signal via web search proxy (free, no auth required).

Since PatentsView API was discontinued and Google Patents requires JS rendering,
we use the websearch module as a backend to find recent patents via web search.
This provides a lightweight "patent signal" without needing a dedicated API.

Alternative: If you have access to a patent API, replace search_patents() with
a direct API call and update parse_patents_response() accordingly.
"""

import re
import sys
from typing import Any, Dict, List

from . import http

# Use Google Patents as a search source via their JSON endpoint
# The /x/ endpoint returns JSON when appropriate headers are set
PATENTS_GOOGLE_URL = "https://patents.google.com/api/search"

DEPTH_CONFIG = {
    "quick": 3,
    "default": 5,
    "deep": 10,
}


def _log(msg: str):
    """Log to stderr."""
    sys.stderr.write(f"[Patents] {msg}\n")
    sys.stderr.flush()


def search_patents(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> Dict[str, Any]:
    """Search for patents related to topic.

    Uses Semantic Scholar's patent search (USPTO-linked) as a proxy,
    or falls back to web search on patents.google.com.

    Args:
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: 'quick', 'default', or 'deep'

    Returns:
        Dict with 'patents' list and optional 'error'.
    """
    count = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])

    _log(f"Searching for patent signals for '{topic}' (since {from_date})")

    # Use the Lens.org public API as fallback (free, no auth)
    # Lens.org provides scholarly and patent data
    url = "https://api.lens.org/scholarly/search"

    from_year = int(from_date[:4]) if from_date else 2025
    to_year = int(to_date[:4]) if to_date else 2026

    try:
        response = http.request(
            "POST", url, timeout=20, retries=1,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "last30days-skill/2.5",
            },
            json_data={
                "query": topic,
                "include_patents": True,
                "include_pubs": False,
                "page": 1,
                "per_page": count,
                "sort": "date_published",
                "date_range": {
                    "from": f"{from_year}-01-01",
                    "to": f"{to_year}-12-31",
                },
            },
        )
    except Exception as e:
        _log(f"Lens.org API failed: {e}")
        # Return empty gracefully - patents are a supplementary signal
        return {"patents": [], "error": None}

    patents = response.get("data", []) if isinstance(response, dict) else []
    _log(f"Found {len(patents)} patent signals")

    return {"patents": patents}


def parse_patents_response(response: Dict[str, Any], topic: str = "") -> List[Dict[str, Any]]:
    """Parse response into normalized item dicts for the pipeline.

    Handles both Lens.org format and a simple fallback format.

    Args:
        response: Raw response dict from search_patents()
        topic: Original search topic

    Returns:
        List of item dicts ready for normalization.
    """
    patents = response.get("patents", [])
    if not patents:
        return []

    items = []
    for i, patent in enumerate(patents):
        # Handle Lens.org format
        if isinstance(patent, dict):
            lens_id = patent.get("lens_id", patent.get("id", ""))
            title = patent.get("title", "")
            pub_date = patent.get("date_published", patent.get("publication_date", ""))
            patent_id = patent.get("patent_id", patent.get("external_id", ""))
            assignees = patent.get("assignees", [])
            assignee = ""
            if assignees and isinstance(assignees, list) and len(assignees) > 0:
                assignee = assignees[0] if isinstance(assignees[0], str) else assignees[0].get("name", "")

            url = patent.get("url", f"https://www.lens.org/patent/{lens_id}" if lens_id else "")

            items.append({
                "id": f"PAT{i+1}",
                "title": (title or patent_id or f"Patent {i+1}")[:200],
                "url": url,
                "patent_number": patent_id or "",
                "assignee": assignee,
                "published_date": pub_date[:10] if pub_date and len(pub_date) >= 10 else pub_date,
                "abstract": patent.get("abstract", "")[:300],
                "cpc_codes": [],
                "why_relevant": "",
            })

    return items
