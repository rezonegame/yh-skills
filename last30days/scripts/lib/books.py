"""Google Books search via public API (free, no auth required for basic search).

Uses www.googleapis.com/books/v1/volumes for book discovery.
No API key needed for basic search - just HTTP calls via stdlib urllib.
"""

import re
import sys
from typing import Any, Dict, List
from urllib.parse import urlencode

from . import http

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"

DEPTH_CONFIG = {
    "quick": 5,
    "default": 10,
    "deep": 15,
}


def _log(msg: str):
    """Log to stderr (only in TTY mode)."""
    if sys.stderr.isatty():
        sys.stderr.write(f"[Books] {msg}\n")
        sys.stderr.flush()


def search_books(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> Dict[str, Any]:
    """Search Google Books via public API.

    Args:
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: 'quick', 'default', or 'deep'

    Returns:
        Dict with 'books' list and optional 'error'.
    """
    count = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])

    # Build year range for filter
    from_year = from_date[:4] if len(from_date) >= 4 else "2025"
    to_year = to_date[:4] if len(to_date) >= 4 else "2026"

    params = {
        "q": f"{topic} published:{from_year}-{to_year}",
        "orderBy": "newest",
        "maxResults": str(count),
        "printType": "books",
    }
    url = f"{GOOGLE_BOOKS_URL}?{urlencode(params)}"

    _log(f"Searching for '{topic}' ({from_year}-{to_year}, count={count})")

    try:
        response = http.request("GET", url, timeout=30, retries=2)
    except http.HTTPError as e:
        _log(f"Search failed: {e}")
        return {"books": [], "error": str(e)}
    except Exception as e:
        _log(f"Search failed: {e}")
        return {"books": [], "error": str(e)}

    books = response.get("items", [])
    _log(f"Found {len(books)} books")
    return {"books": books}


def parse_books_response(response: Dict[str, Any], topic: str = "") -> List[Dict[str, Any]]:
    """Parse Google Books response into normalized item dicts.

    Args:
        response: Raw response dict from search_books()
        topic: Original search topic

    Returns:
        List of item dicts ready for normalization.
    """
    books = response.get("books", [])
    if not books:
        return []

    items = []
    for i, book in enumerate(books):
        volume_info = book.get("volumeInfo", {})
        title = volume_info.get("title", "")
        authors = volume_info.get("authors", [])
        publisher = volume_info.get("publisher", "")
        published_date = volume_info.get("publishedDate", "")
        description = volume_info.get("description", "")
        page_count = volume_info.get("pageCount")
        info_link = volume_info.get("infoLink", "")

        # Extract ISBN
        isbn = ""
        industry_ids = volume_info.get("industryIdentifiers", [])
        for id_entry in industry_ids:
            if id_entry.get("type") in ("ISBN_13", "ISBN_10"):
                isbn = id_entry.get("identifier", "")
                break

        # Clean date: Google Books returns "YYYY", "YYYY-MM", or "YYYY-MM-DD"
        date_str = None
        if published_date:
            # Normalize to YYYY-MM-DD
            parts = published_date.split("-")
            if len(parts) == 1:
                date_str = f"{parts[0]}-01-01"
            elif len(parts) == 2:
                date_str = f"{parts[0]}-{parts[1]}-01"
            else:
                date_str = published_date

        # Relevance: position-based decay
        rank_score = max(0.3, 1.0 - (i * 0.05))

        items.append({
            "book_id": book.get("id", ""),
            "title": title,
            "url": info_link,
            "authors": authors,
            "publisher": publisher,
            "published_date": date_str,
            "description": description[:400] if description else "",
            "isbn": isbn,
            "page_count": page_count,
            "date": date_str,
            "relevance": round(rank_score, 2),
            "why_relevant": f"Book: {title[:60]}",
        })

    return items
