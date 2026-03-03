"""Gemini Search Grounding client for Reddit discovery."""

import json
import re
import sys
import urllib.parse
from typing import Any, Dict, List, Optional

from . import http

# Default model — generous free tier, fast, supports google_search tool
DEFAULT_MODEL = "gemini-2.5-flash"

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# Depth configurations: (min, max) threads to request
DEPTH_CONFIG = {
    "quick": (15, 25),
    "default": (30, 50),
    "deep": (70, 100),
}

REDDIT_SEARCH_PROMPT = """Find Reddit discussion threads about: {topic}

STEP 1: EXTRACT THE CORE SUBJECT
Get the MAIN NOUN/PRODUCT/TOPIC:
- "best nano banana prompting practices" → "nano banana"
- "killer features of clawdbot" → "clawdbot"
- "top Claude Code skills" → "Claude Code"
DO NOT include "best", "top", "tips", "practices", "features" in your search.

STEP 2: SEARCH BROADLY
Search for the core subject on Reddit:
1. "[core subject] site:reddit.com"
2. "reddit [core subject]"
3. "[core subject] reddit"

Return as many relevant threads as you find. We filter by date server-side.

STEP 3: INCLUDE ALL MATCHES
- Include ALL threads about the core subject
- Set date to "YYYY-MM-DD" if you can determine it, otherwise null
- We verify dates and filter old content server-side
- DO NOT pre-filter aggressively - include anything relevant

REQUIRED: URLs must contain "/r/" AND "/comments/"
REJECT: developers.reddit.com, business.reddit.com

Find {min_items}-{max_items} threads. Return MORE rather than fewer.

Return JSON with "items" array. Each item has: title, url, subreddit, date (YYYY-MM-DD or null), why_relevant, relevance (0-1 float).

IMPORTANT: Return ONLY valid JSON block. NO MARKDOWN formatting, NO other text. Just the raw JSON object starting with {{ and ending with }}."""


def _log_error(msg: str):
    """Log error to stderr."""
    sys.stderr.write(f"[GEMINI-REDDIT ERROR] {msg}\n")
    sys.stderr.flush()


def _log_info(msg: str):
    """Log info to stderr."""
    sys.stderr.write(f"[GEMINI-REDDIT] {msg}\n")
    sys.stderr.flush()


def search_reddit(
    api_key: str,
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
    model: str = None,
) -> Dict[str, Any]:
    """Search Reddit for relevant threads using Gemini Search Grounding.

    Args:
        api_key: Gemini API key
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: Research depth - "quick", "default", or "deep"
        model: Model to use (default: gemini-2.5-flash)

    Returns:
        Raw API response
    """
    if model is None:
        model = DEFAULT_MODEL

    min_items, max_items = DEPTH_CONFIG.get(depth, DEPTH_CONFIG["default"])

    # Build the prompt
    input_text = REDDIT_SEARCH_PROMPT.format(
        topic=topic,
        from_date=from_date,
        to_date=to_date,
        min_items=min_items,
        max_items=max_items,
    )

    # Construct Gemini request payload with Google Search Grounding
    payload = {
        "contents": [{
            "parts": [{"text": input_text}]
        }],
        "tools": [{
            "google_search": {}
        }]
    }

    # Adjust timeout based on depth
    timeout = 90 if depth == "quick" else 120 if depth == "default" else 180

    url = GEMINI_API_URL.format(model=model) + f"?key={api_key}"

    _log_info(f"Searching via {model} with Google Search Grounding")

    try:
        return http.post(url, payload, headers={"Content-Type": "application/json"}, timeout=timeout)
    except http.HTTPError as e:
        _log_error(f"Gemini API error: {e}")
        raise


def parse_reddit_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Gemini response to extract Reddit items.

    Args:
        response: Raw API response

    Returns:
        List of item dicts (same format as openai_reddit output)
    """
    items = []

    # Check for API errors
    if "error" in response:
        error = response["error"]
        err_msg = error.get("message", str(error)) if isinstance(error, dict) else str(error)
        _log_error(f"Gemini API error: {err_msg}")
        return items

    # Extract text from Gemini response structure
    # Gemini returns: candidates[0].content.parts[0].text
    output_text = ""
    candidates = response.get("candidates", [])
    if candidates:
        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        for part in parts:
            if "text" in part:
                output_text = part["text"]
                break

    if not output_text:
        _log_error(f"No output text found in Gemini response. Keys present: {list(response.keys())}")
        return items

    # Clean up markdown JSON block if present
    output_text = output_text.strip()
    if output_text.startswith("```json"):
        output_text = output_text[7:]
    elif output_text.startswith("```"):
        output_text = output_text[3:]
    if output_text.endswith("```"):
        output_text = output_text[:-3]
    output_text = output_text.strip()

    try:
        data = json.loads(output_text)
        items = data.get("items", [])
    except json.JSONDecodeError as e:
        # Fallback: try to extract JSON from mixed text
        json_match = re.search(r'\{[\s\S]*"items"[\s\S]*\}', output_text)
        if json_match:
            try:
                data = json.loads(json_match.group())
                items = data.get("items", [])
            except json.JSONDecodeError:
                _log_error(f"Failed to parse JSON from Gemini response: {e}")
                return []
        else:
            _log_error(f"Failed to parse JSON from Gemini response: {e}")
            _log_error(f"Raw output was: {output_text[:500]}...")
            return []

    # Validate and clean items (same logic as openai_reddit)
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
