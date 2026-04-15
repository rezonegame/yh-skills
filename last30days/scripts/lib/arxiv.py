"""Academic paper search via Semantic Scholar API (free, no auth required).

Fallback for arXiv when the arXiv API is rate-limited or slow.
Semantic Scholar provides paper metadata from multiple sources including arXiv.
No API key needed for basic search (rate-limited to ~100 req/5min without key).
"""

import re
import sys
from typing import Any, Dict, List
from urllib.parse import urlencode

from . import http

SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1"

DEPTH_CONFIG = {
    "quick": 5,
    "default": 10,
    "deep": 20,
}

# Fields to request from the API
PAPER_FIELDS = "paperId,title,abstract,authors,year,publicationDate,externalIds,citationCount,url,openAccessPdf"


def _log(msg: str):
    """Log to stderr."""
    sys.stderr.write(f"[ArXiv] {msg}\n")
    sys.stderr.flush()


def search_arxiv(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> Dict[str, Any]:
    """Search academic papers via Semantic Scholar API.

    Uses Semantic Scholar's keyword search API which indexes papers from
    arXiv, PubMed, and other academic sources.

    Args:
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        depth: 'quick', 'default', or 'deep'
        to_date: End date (YYYY-MM-DD) - used for filtering

    Returns:
        Dict with 'papers' list and optional 'error'.
    """
    count = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])
    url = f"{SEMANTIC_SCHOLAR_URL}/paper/search"

    params = {
        "query": topic,
        "limit": str(count),
        "fields": PAPER_FIELDS,
        "sort": "publicationDate:desc",
    }

    _log(f"Searching Semantic Scholar for '{topic}' (since {from_date}, count={count})")

    try:
        from urllib.parse import urlencode
        full_url = f"{url}?{urlencode(params)}"
        response = http.request(
            "GET", full_url, timeout=30, retries=2,
            headers={"User-Agent": "last30days-skill/2.5"},
        )
    except http.HTTPError as e:
        _log(f"Semantic Scholar failed: {e}")
        return {"papers": [], "error": str(e)}
    except Exception as e:
        _log(f"Search failed: {e}")
        return {"papers": [], "error": str(e)}

    papers = response.get("data", []) if isinstance(response, dict) else []
    _log(f"Found {len(papers)} papers from Semantic Scholar")

    # Apply date filter
    from_year = int(from_date[:4]) if from_date and len(from_date) >= 4 else None
    to_year = int(to_date[:4]) if to_date and len(to_date) >= 4 else None

    filtered = []
    for paper in papers:
        pub_date = paper.get("publicationDate", "")
        if not pub_date:
            filtered.append(paper)
            continue

        # Semantic Scholar returns dates like "2026-03-15" or just "2026-03"
        paper_year = int(pub_date[:4]) if len(pub_date) >= 4 else None
        if paper_year is None:
            filtered.append(paper)
            continue

        if from_year and paper_year < from_year:
            continue
        if to_year and paper_year > to_year:
            continue
        filtered.append(paper)

    return {"papers": filtered}


def parse_arxiv_response(response: Dict[str, Any], topic: str = "") -> List[Dict[str, Any]]:
    """Parse Semantic Scholar response into normalized item dicts.

    Args:
        response: Raw response dict from search_arxiv()
        topic: Original search topic

    Returns:
        List of item dicts ready for normalization.
    """
    papers = response.get("papers", [])
    if not papers:
        return []

    items = []
    for i, paper in enumerate(papers):
        paper_id = paper.get("paperId", "")
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")
        pub_date = paper.get("publicationDate", "")
        year = paper.get("year")
        url = paper.get("url", "")

        # Extract arXiv ID if available
        external_ids = paper.get("externalIds", {}) or {}
        arxiv_id = external_ids.get("ArXiv", "")
        doi = external_ids.get("DOI", "")
        pmid = external_ids.get("PubMed", "")

        # Build proper URLs
        if arxiv_id:
            abs_url = f"https://arxiv.org/abs/{arxiv_id}"
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
        else:
            abs_url = url or f"https://www.semanticscholar.org/paper/{paper_id}"
            pdf_url = ""

        # Authors
        authors_data = paper.get("authors", []) or []
        authors = []
        for author in authors_data:
            if isinstance(author, dict):
                name = author.get("name", "")
                if name:
                    authors.append(name)

        # Citation count as engagement signal
        citations = paper.get("citationCount", 0) or 0

        # Open access PDF
        oa_pdf = paper.get("openAccessPdf", {}) or {}
        if oa_pdf and oa_pdf.get("url") and not pdf_url:
            pdf_url = oa_pdf["url"]

        items.append({
            "id": f"AR{i+1}",
            "title": title[:200],
            "url": abs_url,
            "pdf_url": pdf_url,
            "authors": authors,
            "published_date": pub_date,
            "year": year,
            "summary": (abstract or "")[:500],
            "categories": [],  # Semantic Scholar doesn't provide arXiv categories directly
            "citation_count": citations,
            "doi": doi,
            "pmid": pmid,
            "arxiv_id": arxiv_id,
            "why_relevant": "",
        })

    return items
