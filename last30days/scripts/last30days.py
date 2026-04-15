#!/usr/bin/env python3
"""
last30days - Research a topic from the last 30 days on Reddit + X + YouTube + Web.

Usage:
    python3 last30days.py <topic> [options]

Options:
    --mock              Use fixtures instead of real API calls
    --emit=MODE         Output mode: compact|json|md|context|path (default: compact)
    --sources=MODE      Source selection: auto|reddit|x|both (default: auto)
    --quick             Faster research with fewer sources (8-12 each)
    --deep              Comprehensive research with more sources (50-70 Reddit, 40-60 X)
    --debug             Enable verbose debug logging
    --store             Persist findings to SQLite database
    --diagnose          Show source availability diagnostics and exit
"""

import argparse
import atexit
import json
import os
import signal
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

# Add lib to path
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

# ---------------------------------------------------------------------------
# Global timeout & child process management
# ---------------------------------------------------------------------------
_child_pids: set = set()
_child_pids_lock = threading.Lock()

TIMEOUT_PROFILES = {
    "quick":   {"global": 90,  "future": 30, "reddit_future": 60,  "youtube_future": 60,  "hackernews_future": 30,  "polymarket_future": 15,  "arxiv_future": 30,  "patent_future": 30,  "book_future": 30,  "http": 15, "enrich_per": 8,  "enrich_total": 30, "enrich_max_items": 10},
    "default": {"global": 180, "future": 60, "reddit_future": 90,  "youtube_future": 90,  "hackernews_future": 60,  "polymarket_future": 30,  "arxiv_future": 30,  "patent_future": 30,  "book_future": 30,  "http": 30, "enrich_per": 15, "enrich_total": 45, "enrich_max_items": 15},
    "deep":    {"global": 300, "future": 90, "reddit_future": 120, "youtube_future": 120, "hackernews_future": 90,  "polymarket_future": 45,  "arxiv_future": 45,  "patent_future": 45,  "book_future": 45,  "http": 30, "enrich_per": 15, "enrich_total": 60, "enrich_max_items": 25},
}


def register_child_pid(pid: int):
    """Track a child process for cleanup."""
    with _child_pids_lock:
        _child_pids.add(pid)


def unregister_child_pid(pid: int):
    """Remove a child process from tracking."""
    with _child_pids_lock:
        _child_pids.discard(pid)


def _cleanup_children():
    """Kill all tracked child processes."""
    with _child_pids_lock:
        pids = list(_child_pids)
    for pid in pids:
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
        except (ProcessLookupError, PermissionError, OSError):
            pass


atexit.register(_cleanup_children)


def _install_global_timeout(timeout_seconds: int):
    """Install a global timeout watchdog.

    Uses SIGALRM on Unix, threading.Timer as fallback.
    """
    if hasattr(signal, 'SIGALRM'):
        def _handler(signum, frame):
            sys.stderr.write(f"\n[TIMEOUT] Global timeout ({timeout_seconds}s) exceeded. Cleaning up.\n")
            sys.stderr.flush()
            _cleanup_children()
            sys.exit(1)
        signal.signal(signal.SIGALRM, _handler)
        signal.alarm(timeout_seconds)
    else:
        # Windows fallback
        def _watchdog():
            sys.stderr.write(f"\n[TIMEOUT] Global timeout ({timeout_seconds}s) exceeded. Cleaning up.\n")
            sys.stderr.flush()
            _cleanup_children()
            os._exit(1)
        timer = threading.Timer(timeout_seconds, _watchdog)
        timer.daemon = True
        timer.start()

from lib import (
    arxiv,
    bird_x,
    books,
    dates,
    dedupe,
    gemini_reddit,
    hackernews,
    native_reddit,
    patents,
    polymarket,
    entity_extract,
    env,
    http,
    models,
    normalize,
    openai_reddit,
    reddit_enrich,
    render,
    schema,
    score,
    ui,
    websearch,
    xai_x,
    youtube_yt,
    # Chinese platforms
    bilibili,
    zhihu,
    weibo,
    douyin,
    baidu,
    # Translation support
    translate,
)


def load_fixture(name: str) -> dict:
    """Load a fixture file."""
    fixture_path = SCRIPT_DIR.parent / "fixtures" / name
    if fixture_path.exists():
        with open(fixture_path) as f:
            return json.load(f)
    return {}


def _search_reddit(
    topic: str,
    config: dict,
    selected_models: dict,
    from_date: str,
    to_date: str,
    depth: str,
    mock: bool,
    reddit_source: str = "openai",
) -> tuple:
    """Search Reddit via best available backend (runs in thread).

    Args:
        reddit_source: 'gemini', 'openai', or 'native'

    Returns:
        Tuple of (reddit_items, raw_response, error)
    """
    raw_response = None
    reddit_error = None

    if mock:
        raw_response = load_fixture("openai_sample.json")
        reddit_items = openai_reddit.parse_reddit_response(raw_response or {})
        return reddit_items, raw_response, reddit_error

    # --- Route to the appropriate backend ---
    if reddit_source == 'gemini':
        # Gemini Search Grounding backend
        try:
            raw_response = gemini_reddit.search_reddit(
                config["GEMINI_API_KEY"],
                topic,
                from_date,
                to_date,
                depth=depth,
                model=selected_models.get("gemini"),
            )
        except http.HTTPError as e:
            raw_response = {"error": str(e)}
            reddit_error = f"Gemini API error: {e}"
        except Exception as e:
            raw_response = {"error": str(e)}
            reddit_error = f"{type(e).__name__}: {e}"

        reddit_items = gemini_reddit.parse_reddit_response(raw_response or {})

    elif reddit_source == 'openai':
        # OpenAI Responses API backend (original)
        try:
            raw_response = openai_reddit.search_reddit(
                config["OPENAI_API_KEY"],
                selected_models["openai"],
                topic,
                from_date,
                to_date,
                depth=depth,
            )
        except http.HTTPError as e:
            raw_response = {"error": str(e)}
            reddit_error = f"API error: {e}"
        except Exception as e:
            raw_response = {"error": str(e)}
            reddit_error = f"{type(e).__name__}: {e}"

        reddit_items = openai_reddit.parse_reddit_response(raw_response or {})

        # Quick retry with simpler query if few results (OpenAI only)
        if len(reddit_items) < 5 and not reddit_error:
            core = openai_reddit._extract_core_subject(topic)
            if core.lower() != topic.lower():
                try:
                    retry_raw = openai_reddit.search_reddit(
                        config["OPENAI_API_KEY"],
                        selected_models["openai"],
                        core,
                        from_date, to_date,
                        depth=depth,
                    )
                    retry_items = openai_reddit.parse_reddit_response(retry_raw)
                    existing_urls = {item.get("url") for item in reddit_items}
                    for item in retry_items:
                        if item.get("url") not in existing_urls:
                            reddit_items.append(item)
                except Exception:
                    pass

        # Subreddit-targeted fallback if still < 3 results (OpenAI only)
        if len(reddit_items) < 3 and not reddit_error:
            sub_query = openai_reddit._build_subreddit_query(topic)
            try:
                sub_raw = openai_reddit.search_reddit(
                    config["OPENAI_API_KEY"],
                    selected_models["openai"],
                    sub_query,
                    from_date, to_date,
                    depth=depth,
                )
                sub_items = openai_reddit.parse_reddit_response(sub_raw)
                existing_urls = {item.get("url") for item in reddit_items}
                for item in sub_items:
                    if item.get("url") not in existing_urls:
                        reddit_items.append(item)
            except Exception:
                pass

    else:
        # Native Reddit JSON backend (no API key)
        try:
            raw_response = native_reddit.search_reddit(
                topic,
                from_date,
                to_date,
                depth=depth,
            )
        except http.HTTPError as e:
            raw_response = {"error": str(e)}
            reddit_error = f"Reddit API error: {e}"
        except Exception as e:
            raw_response = {"error": str(e)}
            reddit_error = f"{type(e).__name__}: {e}"

        reddit_items = native_reddit.parse_reddit_response(raw_response or {})

    return reddit_items, raw_response, reddit_error


def _search_x(
    topic: str,
    config: dict,
    selected_models: dict,
    from_date: str,
    to_date: str,
    depth: str,
    mock: bool,
    x_source: str = "xai",
) -> tuple:
    """Search X via Bird CLI or xAI (runs in thread).

    Args:
        x_source: 'bird' or 'xai' - which backend to use

    Returns:
        Tuple of (x_items, raw_response, error)
    """
    raw_response = None
    x_error = None

    if mock:
        raw_response = load_fixture("xai_sample.json")
        x_items = xai_x.parse_x_response(raw_response or {})
        return x_items, raw_response, x_error

    # Use Bird if specified
    if x_source == "bird":
        try:
            raw_response = bird_x.search_x(
                topic,
                from_date,
                to_date,
                depth=depth,
            )
        except Exception as e:
            raw_response = {"error": str(e)}
            x_error = f"{type(e).__name__}: {e}"

        x_items = bird_x.parse_bird_response(raw_response or {})

        # Check for error in response (Bird returns list on success, dict on error)
        if raw_response and isinstance(raw_response, dict) and raw_response.get("error") and not x_error:
            x_error = raw_response["error"]

        return x_items, raw_response, x_error

    # Use xAI (original behavior)
    try:
        raw_response = xai_x.search_x(
            config["XAI_API_KEY"],
            selected_models["xai"],
            topic,
            from_date,
            to_date,
            depth=depth,
        )
    except http.HTTPError as e:
        raw_response = {"error": str(e)}
        x_error = f"API error: {e}"
    except Exception as e:
        raw_response = {"error": str(e)}
        x_error = f"{type(e).__name__}: {e}"

    x_items = xai_x.parse_x_response(raw_response or {})

    return x_items, raw_response, x_error


def _search_youtube(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str,
) -> tuple:
    """Search YouTube via yt-dlp (runs in thread).

    Returns:
        Tuple of (youtube_items, youtube_error)
    """
    youtube_error = None

    try:
        response = youtube_yt.search_and_transcribe(
            topic, from_date, to_date, depth=depth,
        )
    except Exception as e:
        return [], f"{type(e).__name__}: {e}"

    youtube_items = youtube_yt.parse_youtube_response(response)

    if response.get("error"):
        youtube_error = response["error"]

    return youtube_items, youtube_error


def _search_hackernews(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str,
) -> tuple:
    """Search Hacker News via Algolia (runs in thread).

    Returns:
        Tuple of (hn_items, hn_error)
    """
    hn_error = None

    try:
        response = hackernews.search_hackernews(
            topic, from_date, to_date, depth=depth,
        )
    except Exception as e:
        return [], f"{type(e).__name__}: {e}"

    hn_items = hackernews.parse_hackernews_response(response)

    if response.get("error"):
        hn_error = response["error"]

    return hn_items, hn_error


def _search_polymarket(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str,
) -> tuple:
    """Search Polymarket via Gamma API (runs in thread).

    Returns:
        Tuple of (pm_items, pm_error)
    """
    pm_error = None

    try:
        response = polymarket.search_polymarket(
            topic, from_date, to_date, depth=depth,
        )
    except Exception as e:
        return [], f"{type(e).__name__}: {e}"

    pm_items = polymarket.parse_polymarket_response(response, topic=topic)

    if response.get("error"):
        pm_error = response["error"]

    return pm_items, pm_error


def _search_arxiv(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str,
) -> tuple:
    """Search arXiv via public Atom API (runs in thread).

    Returns:
        Tuple of (arxiv_items, arxiv_error)
    """
    arxiv_error = None

    try:
        response = arxiv.search_arxiv(
            topic, from_date, to_date, depth=depth,
        )
    except Exception as e:
        return [], f"{type(e).__name__}: {e}"

    arxiv_items = arxiv.parse_arxiv_response(response, topic=topic)

    if response.get("error"):
        arxiv_error = response["error"]

    return arxiv_items, arxiv_error


def _search_patents(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str,
) -> tuple:
    """Search patents via PatentsView API (runs in thread).

    Returns:
        Tuple of (patent_items, patent_error)
    """
    patent_error = None

    try:
        response = patents.search_patents(
            topic, from_date, to_date, depth=depth,
        )
    except Exception as e:
        return [], f"{type(e).__name__}: {e}"

    patent_items = patents.parse_patents_response(response, topic=topic)

    if response.get("error"):
        patent_error = response["error"]

    return patent_items, patent_error


def _search_books(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str,
) -> tuple:
    """Search Google Books via public API (runs in thread).

    Returns:
        Tuple of (book_items, book_error)
    """
    book_error = None

    try:
        response = books.search_books(
            topic, from_date, to_date, depth=depth,
        )
    except Exception as e:
        return [], f"{type(e).__name__}: {e}"

    book_items = books.parse_books_response(response, topic=topic)

    if response.get("error"):
        book_error = response["error"]

    return book_items, book_error


def _search_bilibili(
    topic: str,
    from_date: str,
    to_date: str,
    depth: str,
) -> tuple:
    """Search Bilibili via public API (runs in thread).

    Returns:
        Tuple of (bilibili_items, bilibili_error)
    """
    bilibili_error = None

    try:
        response = bilibili.search_bilibili(
            topic, from_date, to_date, depth=depth,
        )
    except Exception as e:
        return [], f"{type(e).__name__}: {e}"

    bilibili_items = bilibili.parse_bilibili_response(response)

    if response.get("error"):
        bilibili_error = response["error"]

    return bilibili_items, bilibili_error


def _search_zhihu(
    topic: str,
    config: dict,
    from_date: str,
    to_date: str,
    depth: str,
) -> tuple:
    """Search Zhihu via public API (runs in thread).

    Returns:
        Tuple of (zhihu_items, zhihu_error)
    """
    zhihu_error = None

    try:
        response = zhihu.search_zhihu(
            topic, from_date, to_date, depth=depth,
            cookie=config.get("ZHIHU_COOKIE"),
        )
    except Exception as e:
        return [], f"{type(e).__name__}: {e}"

    zhihu_items = zhihu.parse_zhihu_response(response)

    if response.get("error"):
        zhihu_error = response["error"]

    return zhihu_items, zhihu_error


def _search_weibo(
    topic: str,
    config: dict,
    from_date: str,
    to_date: str,
    depth: str,
) -> tuple:
    """Search Weibo via public API (runs in thread).

    Returns:
        Tuple of (weibo_items, weibo_error)
    """
    weibo_error = None

    try:
        response = weibo.search_weibo(
            topic, from_date, to_date, depth=depth,
            access_token=config.get("WEIBO_ACCESS_TOKEN"),
        )
    except Exception as e:
        return [], f"{type(e).__name__}: {e}"

    weibo_items = weibo.parse_weibo_response(response)

    if response.get("error"):
        weibo_error = response["error"]

    return weibo_items, weibo_error


def _search_douyin(
    topic: str,
    config: dict,
    from_date: str,
    to_date: str,
    depth: str,
) -> tuple:
    """Search Douyin via TikHub API or public API (runs in thread).

    Returns:
        Tuple of (douyin_items, douyin_error)
    """
    douyin_error = None

    try:
        response = douyin.search_douyin(
            topic, from_date, to_date, depth=depth,
            api_key=config.get("TIKHUB_API_KEY"),
        )
    except Exception as e:
        return [], f"{type(e).__name__}: {e}"

    douyin_items = douyin.parse_douyin_response(response)

    if response.get("error"):
        douyin_error = response["error"]

    return douyin_items, douyin_error


def _search_baidu(
    topic: str,
    config: dict,
    from_date: str,
    to_date: str,
    depth: str,
) -> tuple:
    """Search Baidu via public API (runs in thread).

    Returns:
        Tuple of (baidu_items, baidu_error)
    """
    baidu_error = None

    try:
        response = baidu.search_baidu(
            topic, from_date, to_date, depth=depth,
            api_key=config.get("BAIDU_API_KEY"),
            secret_key=config.get("BAIDU_SECRET_KEY"),
        )
    except Exception as e:
        return [], f"{type(e).__name__}: {e}"

    baidu_items = baidu.parse_baidu_response(response)

    if response.get("error"):
        baidu_error = response["error"]

    return baidu_items, baidu_error


def _search_web(
    topic: str,
    config: dict,
    from_date: str,
    to_date: str,
    depth: str,
) -> tuple:
    """Search the web via native API backend (runs in thread).

    Uses the best available backend: Parallel AI > Brave > OpenRouter.

    Returns:
        Tuple of (web_items, web_error)
        web_items are raw dicts ready for websearch.normalize_websearch_items()
    """
    from lib import brave_search, parallel_search, openrouter_search

    backend = env.get_web_search_source(config)
    if not backend:
        return [], "No web search API keys configured"

    web_error = None
    raw_results = []

    try:
        if backend == "parallel":
            raw_results = parallel_search.search_web(
                topic, from_date, to_date, config["PARALLEL_API_KEY"], depth=depth,
            )
        elif backend == "brave":
            raw_results = brave_search.search_web(
                topic, from_date, to_date, config["BRAVE_API_KEY"], depth=depth,
            )
        elif backend == "openrouter":
            raw_results = openrouter_search.search_web(
                topic, from_date, to_date, config["OPENROUTER_API_KEY"], depth=depth,
            )
    except Exception as e:
        return [], f"{type(e).__name__}: {e}"

    # Add IDs and date_confidence for websearch.normalize_websearch_items()
    for i, item in enumerate(raw_results):
        item.setdefault("id", f"W{i+1}")
        if item.get("date") and not item.get("date_confidence"):
            item["date_confidence"] = "med"
        elif not item.get("date"):
            item["date_confidence"] = "low"
        item.setdefault("why_relevant", "")

    return raw_results, web_error


def _run_supplemental(
    topic: str,
    reddit_items: list,
    x_items: list,
    from_date: str,
    to_date: str,
    depth: str,
    x_source: str,
    progress: ui.ProgressDisplay = None,
    skip_reddit: bool = False,
    resolved_handle: str = None,
) -> tuple:
    """Run Phase 2 supplemental searches based on entities from Phase 1.

    Extracts handles/subreddits from initial results, then runs targeted
    searches to find additional content the broad search missed.

    Args:
        topic: Original search topic
        reddit_items: Phase 1 Reddit items (raw dicts)
        x_items: Phase 1 X items (raw dicts)
        from_date: Start date
        to_date: End date
        depth: Research depth
        x_source: 'bird' or 'xai'
        progress: Optional progress display
        skip_reddit: If True, skip Reddit supplemental (e.g. rate-limited)
        resolved_handle: X handle resolved by the agent (without @), searched unfiltered

    Returns:
        Tuple of (supplemental_reddit, supplemental_x)
    """
    # Depth-dependent caps
    if depth == "default":
        max_handles = 3
        max_subs = 3
        count_per = 3
    else:  # deep
        max_handles = 5
        max_subs = 5
        count_per = 5

    # Extract entities from Phase 1 results
    entities = entity_extract.extract_entities(
        reddit_items, x_items,
        max_handles=max_handles,
        max_subreddits=max_subs,
    )

    has_handles = entities["x_handles"] and x_source == "bird"
    has_subs = entities["reddit_subreddits"] and not skip_reddit

    # Always run unfiltered search for resolved handle (even if entity-extracted).
    # Entity-extracted handles get topic-filtered queries (from:handle topic),
    # but resolved handles need UNFILTERED search (from:handle) to find posts
    # that don't mention the topic string (e.g. Dor Brothers' viral tweet about
    # Logan Paul doesn't contain "dor brothers" in the text).
    has_resolved = bool(resolved_handle) and x_source == "bird"

    if not has_handles and not has_subs and not has_resolved:
        return [], []

    parts = []
    if has_resolved:
        parts.append(f"@{resolved_handle} (resolved)")
    if has_handles:
        parts.append(f"@{', @'.join(entities['x_handles'][:3])}")
    if has_subs:
        parts.append(f"r/{', r/'.join(entities['reddit_subreddits'][:3])}")
    sys.stderr.write(f"[Phase 2] Drilling into {' + '.join(parts)}\n")
    sys.stderr.flush()

    supplemental_reddit = []
    supplemental_x = []

    # Collect existing URLs to avoid adding duplicates before dedupe
    existing_urls = set()
    for item in reddit_items:
        existing_urls.add(item.get("url", ""))
    for item in x_items:
        existing_urls.add(item.get("url", ""))

    # Run supplemental searches in parallel
    reddit_future = None
    x_future = None
    resolved_future = None

    max_workers = sum([bool(has_subs), bool(has_handles), bool(has_resolved)])
    with ThreadPoolExecutor(max_workers=max(max_workers, 1)) as executor:
        if has_subs:
            reddit_future = executor.submit(
                openai_reddit.search_subreddits,
                entities["reddit_subreddits"],
                topic,
                from_date,
                to_date,
                count_per,
            )

        if has_handles:
            x_future = executor.submit(
                bird_x.search_handles,
                entities["x_handles"],
                topic,
                from_date,
                count_per,
            )

        if has_resolved:
            # Resolved handle: search unfiltered (topic=None) to get all recent posts
            resolved_future = executor.submit(
                bird_x.search_handles,
                [resolved_handle],
                None,  # No topic filter - get all recent activity
                from_date,
                10,  # More results for the topic entity
            )

        if reddit_future:
            try:
                raw_reddit = reddit_future.result(timeout=30)
                # Filter out URLs already found in Phase 1
                supplemental_reddit = [
                    item for item in raw_reddit
                    if item.get("url", "") not in existing_urls
                ]
            except TimeoutError:
                sys.stderr.write("[Phase 2] Supplemental Reddit timed out (30s)\n")
            except Exception as e:
                sys.stderr.write(f"[Phase 2] Supplemental Reddit error: {e}\n")

        if x_future:
            try:
                raw_x = x_future.result(timeout=30)
                supplemental_x = [
                    item for item in raw_x
                    if item.get("url", "") not in existing_urls
                ]
            except TimeoutError:
                sys.stderr.write("[Phase 2] Supplemental X timed out (30s)\n")
            except Exception as e:
                sys.stderr.write(f"[Phase 2] Supplemental X error: {e}\n")

        if resolved_future:
            try:
                raw_resolved = resolved_future.result(timeout=30)
                # Lower relevance for unfiltered handle posts (no topic keyword signal)
                for item in raw_resolved:
                    item["relevance"] = 0.5
                resolved_new = [
                    item for item in raw_resolved
                    if item.get("url", "") not in existing_urls
                ]
                supplemental_x.extend(resolved_new)
                if resolved_new:
                    sys.stderr.write(f"[Phase 2] +{len(resolved_new)} from @{resolved_handle}\n")
            except TimeoutError:
                sys.stderr.write(f"[Phase 2] Resolved handle @{resolved_handle} timed out (30s)\n")
            except Exception as e:
                sys.stderr.write(f"[Phase 2] Resolved handle error: {e}\n")

    if supplemental_reddit or supplemental_x:
        sys.stderr.write(
            f"[Phase 2] +{len(supplemental_reddit)} Reddit, +{len(supplemental_x)} X\n"
        )
        sys.stderr.flush()

    return supplemental_reddit, supplemental_x


def run_research(
    topic: str,
    sources: str,
    config: dict,
    selected_models: dict,
    from_date: str,
    to_date: str,
    depth: str = "default",
    mock: bool = False,
    progress: ui.ProgressDisplay = None,
    x_source: str = "xai",
    run_youtube: bool = False,
    timeouts: dict = None,
    resolved_handle: str = None,
    reddit_source: str = "openai",
    use_chinese_platforms: bool = True,
) -> tuple:
    """Run the research pipeline.

    Returns:
        Tuple of (reddit_items, x_items, youtube_items, hackernews_items, polymarket_items,
                  arxiv_items, patent_items, book_items, web_items, web_needed,
                  bilibili_items, zhihu_items, weibo_items, douyin_items, baidu_items,
                  raw_openai, raw_xai, raw_reddit_enriched,
                  reddit_error, x_error, youtube_error, hackernews_error, polymarket_error,
                  arxiv_error, patent_error, book_error, web_error,
                  bilibili_error, zhihu_error, weibo_error, douyin_error, baidu_error)

    Note: web_needed is True when web search should be performed by the assistant
    (i.e., no native web search API keys are configured). When native web search
    runs, web_items will be populated and web_needed will be False.
    """
    if timeouts is None:
        timeouts = TIMEOUT_PROFILES[depth]
    future_timeout = timeouts["future"]

    # Detect if topic is in Chinese and prepare search topics
    is_chinese = translate.detect_chinese(topic)

    # Prepare search topics for different platform groups
    if is_chinese:
        # For Chinese input:
        # - Chinese platforms use original Chinese topic
        # - Overseas platforms use translated topics (en, ru, fr, de, ar)
        chinese_topic = topic
        overseas_topics = translate.get_search_topics(topic)
        # Filter out the original Chinese topic from overseas topics
        overseas_topics = [t for t in overseas_topics if t["lang"] != "original" and t["topic"] != topic]
        # If no translations available, use English as default
        if not overseas_topics:
            overseas_topics = [{"lang": "en", "topic": translate.translate_topic(topic, "en")}]
        sys.stderr.write(f"[Multi-language] Chinese platforms: '{chinese_topic}' | Overseas platforms: {len(overseas_topics)} languages\n")
        sys.stderr.flush()
    else:
        # For non-Chinese input, use original topic for all platforms
        chinese_topic = topic
        overseas_topics = [{"lang": "original", "topic": topic}]

    # Primary topic for display purposes
    primary_topic = overseas_topics[0]["topic"]

    reddit_items = []
    x_items = []
    youtube_items = []
    hackernews_items = []
    polymarket_items = []
    arxiv_items = []
    patent_items = []
    book_items = []
    web_items = []
    bilibili_items = []
    zhihu_items = []
    weibo_items = []
    douyin_items = []
    baidu_items = []
    raw_openai = None
    raw_xai = None
    raw_reddit_enriched = []
    reddit_error = None
    x_error = None
    youtube_error = None
    hackernews_error = None
    polymarket_error = None
    arxiv_error = None
    patent_error = None
    book_error = None
    web_error = None
    bilibili_error = None
    zhihu_error = None
    weibo_error = None
    douyin_error = None
    baidu_error = None

    # Determine web search mode
    do_web = sources in ("all", "web", "reddit-web", "x-web")
    web_backend = env.get_web_search_source(config) if do_web else None
    web_needed = do_web and not web_backend

    # Web-only mode
    if sources == "web":
        if web_backend:
            # Native web search available — run it
            sys.stderr.write(f"[web] Searching via {web_backend}\n")
            sys.stderr.flush()
            try:
                web_items, web_error = _search_web(topic, config, from_date, to_date, depth)
                if web_error and progress:
                    progress.show_error(f"Web error: {web_error}")
            except Exception as e:
                web_error = f"{type(e).__name__}: {e}"
                if progress:
                    progress.show_error(f"Web error: {e}")
            sys.stderr.write(f"[web] {len(web_items)} results\n")
            sys.stderr.flush()
        else:
            # No native backend — assistant handles WebSearch
            if progress:
                progress.start_web_only()
                progress.end_web_only()
        # Still run YouTube in web-only mode if yt-dlp is available
        if run_youtube:
            if progress:
                progress.start_youtube()
            try:
                youtube_items, youtube_error = _search_youtube(topic, from_date, to_date, depth)
                if youtube_error and progress:
                    progress.show_error(f"YouTube error: {youtube_error}")
            except Exception as e:
                youtube_error = f"{type(e).__name__}: {e}"
                if progress:
                    progress.show_error(f"YouTube error: {e}")
            if progress:
                progress.end_youtube(len(youtube_items))
        return reddit_items, x_items, youtube_items, hackernews_items, polymarket_items, arxiv_items, patent_items, book_items, web_items, web_needed, bilibili_items, zhihu_items, weibo_items, douyin_items, baidu_items, raw_openai, raw_xai, raw_reddit_enriched, reddit_error, x_error, youtube_error, hackernews_error, polymarket_error, arxiv_error, patent_error, book_error, web_error, bilibili_error, zhihu_error, weibo_error, douyin_error, baidu_error

    # Determine which searches to run
    do_reddit = sources in ("both", "reddit", "all", "reddit-web")
    do_x = sources in ("both", "x", "all", "x-web")
    do_hackernews = True  # HN is always available (no API key)
    do_polymarket = True  # Polymarket is always available (no API key)
    do_arxiv = True       # arXiv is always available (no API key)
    do_patents = True     # PatentsView is always available (no API key)
    do_books = True       # Google Books basic is always available (no API key)
    do_chinese = use_chinese_platforms  # Chinese platforms are always available (public APIs)

    # Run Reddit, X, YouTube, HN, Polymarket, arXiv, Patents, Books, Web, and Chinese platforms in parallel
    reddit_futures = []
    x_futures = []
    youtube_futures = []
    hackernews_futures = []
    polymarket_futures = []
    arxiv_futures = []
    patent_futures = []
    book_futures = []
    web_futures = []
    bilibili_future = None
    zhihu_future = None
    weibo_future = None
    douyin_future = None
    baidu_future = None

    # Calculate max workers: multiply by number of overseas topics for parallel multi-language search
    num_overseas_topics = len(overseas_topics)
    max_workers = (
        (2 if do_reddit else 0) * num_overseas_topics +
        (1 if do_x else 0) * num_overseas_topics +
        (1 if run_youtube else 0) * num_overseas_topics +
        (1 if do_hackernews else 0) * num_overseas_topics +
        (1 if do_polymarket else 0) * num_overseas_topics +
        (1 if do_arxiv else 0) * num_overseas_topics +
        (1 if do_patents else 0) * num_overseas_topics +
        (1 if do_books else 0) * num_overseas_topics +
        (1 if web_backend else 0) * num_overseas_topics +
        (5 if do_chinese else 0)
    )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit overseas platform searches for each language topic
        if do_reddit:
            if progress:
                progress.start_reddit()
            for topic_info in overseas_topics:
                search_topic = topic_info["topic"]
                lang = topic_info["lang"]
                sys.stderr.write(f"[Reddit-{lang}] Searching: {search_topic}\n")
                sys.stderr.flush()
                reddit_futures.append(executor.submit(
                    _search_reddit, search_topic, config, selected_models,
                    from_date, to_date, depth, mock, reddit_source
                ))

        if do_x:
            if progress:
                progress.start_x()
            for topic_info in overseas_topics:
                search_topic = topic_info["topic"]
                lang = topic_info["lang"]
                sys.stderr.write(f"[X-{lang}] Searching: {search_topic}\n")
                sys.stderr.flush()
                x_futures.append(executor.submit(
                    _search_x, search_topic, config, selected_models,
                    from_date, to_date, depth, mock, x_source
                ))

        if run_youtube:
            if progress:
                progress.start_youtube()
            for topic_info in overseas_topics:
                search_topic = topic_info["topic"]
                lang = topic_info["lang"]
                sys.stderr.write(f"[YouTube-{lang}] Searching: {search_topic}\n")
                sys.stderr.flush()
                youtube_futures.append(executor.submit(
                    _search_youtube, search_topic, from_date, to_date, depth
                ))

        if do_hackernews:
            if progress:
                progress.start_hackernews()
            for topic_info in overseas_topics:
                search_topic = topic_info["topic"]
                lang = topic_info["lang"]
                hackernews_futures.append(executor.submit(
                    _search_hackernews, search_topic, from_date, to_date, depth
                ))

        if do_polymarket:
            if progress:
                progress.start_polymarket()
            for topic_info in overseas_topics:
                search_topic = topic_info["topic"]
                polymarket_futures.append(executor.submit(
                    _search_polymarket, search_topic, from_date, to_date, depth
                ))

        if do_arxiv:
            if progress:
                progress.start_arxiv()
            for topic_info in overseas_topics:
                search_topic = topic_info["topic"]
                arxiv_futures.append(executor.submit(
                    _search_arxiv, search_topic, from_date, to_date, depth
                ))

        if do_patents:
            if progress:
                progress.start_patents()
            for topic_info in overseas_topics:
                search_topic = topic_info["topic"]
                patent_futures.append(executor.submit(
                    _search_patents, search_topic, from_date, to_date, depth
                ))

        if do_books:
            if progress:
                progress.start_books()
            for topic_info in overseas_topics:
                search_topic = topic_info["topic"]
                book_futures.append(executor.submit(
                    _search_books, search_topic, from_date, to_date, depth
                ))

        if web_backend:
            sys.stderr.write(f"[web] Searching via {web_backend}\n")
            sys.stderr.flush()
            for topic_info in overseas_topics:
                search_topic = topic_info["topic"]
                web_futures.append(executor.submit(
                    _search_web, search_topic, config, from_date, to_date, depth
                ))

        # Chinese platform searches (always available with public APIs)
        if do_chinese:
            # Use original Chinese topic for Chinese platforms
            chinese_topic = topic if is_chinese else primary_topic

            sys.stderr.write(f"[Bilibili] Searching: {chinese_topic}\n")
            sys.stderr.flush()
            bilibili_future = executor.submit(
                _search_bilibili, chinese_topic, from_date, to_date, depth
            )

            sys.stderr.write(f"[Zhihu] Searching: {chinese_topic}\n")
            sys.stderr.flush()
            zhihu_future = executor.submit(
                _search_zhihu, chinese_topic, config, from_date, to_date, depth
            )

            sys.stderr.write(f"[Weibo] Searching: {chinese_topic}\n")
            sys.stderr.flush()
            weibo_future = executor.submit(
                _search_weibo, chinese_topic, config, from_date, to_date, depth
            )

            sys.stderr.write(f"[Douyin] Searching: {chinese_topic}\n")
            sys.stderr.flush()
            douyin_future = executor.submit(
                _search_douyin, chinese_topic, config, from_date, to_date, depth
            )

            sys.stderr.write(f"[Baidu] Searching: {chinese_topic}\n")
            sys.stderr.flush()
            baidu_future = executor.submit(
                _search_baidu, chinese_topic, config, from_date, to_date, depth
            )

        # --- Collect results ---

        # Reddit (special: 3-tuple return: items, raw_response, error)
        if reddit_futures:
            for f in reddit_futures:
                try:
                    items, raw_resp, err = f.result(timeout=future_timeout)
                    reddit_items.extend(items)
                    raw_openai = raw_resp or raw_openai
                    if err:
                        reddit_error = err
                except TimeoutError:
                    reddit_error = f"Reddit timed out after {future_timeout}s"
                except Exception as e:
                    reddit_error = f"Reddit {e}"
            # Deduplicate Reddit results by URL
            seen = set()
            reddit_items = [
                item for item in reddit_items
                if not (item.get("url", "") in seen or seen.add(item.get("url", "")))
            ]
            if reddit_error and progress:
                progress.show_error(f"Reddit error: {reddit_error}")
            if progress:
                progress.end_reddit(len(reddit_items))

        # X (special: 3-tuple return: items, raw_response, error)
        if x_futures:
            for f in x_futures:
                try:
                    items, raw_resp, err = f.result(timeout=future_timeout)
                    x_items.extend(items)
                    raw_xai = raw_resp or raw_xai
                    if err:
                        x_error = err
                except TimeoutError:
                    x_error = f"X timed out after {future_timeout}s"
                except Exception as e:
                    x_error = f"X {e}"
            # Deduplicate X results by URL
            seen = set()
            x_items = [
                item for item in x_items
                if not (item.get("url", "") in seen or seen.add(item.get("url", "")))
            ]
            if x_error and progress:
                progress.show_error(f"X error: {x_error}")
            if progress:
                progress.end_x(len(x_items))

        # YouTube (2-tuple: items, error)
        if youtube_futures:
            all_items = []
            for f in youtube_futures:
                try:
                    items, err = f.result(timeout=future_timeout)
                    all_items.extend(items or [])
                    if err and not youtube_error:
                        youtube_error = err
                except TimeoutError:
                    youtube_error = f"YouTube timed out after {future_timeout}s"
                except Exception as e:
                    youtube_error = f"YouTube {e}"
            seen = set()
            youtube_items = [
                item for item in all_items
                if not (item.get("url", "") in seen or seen.add(item.get("url", "")))
            ]
            if youtube_error and progress:
                progress.show_error(f"YouTube error: {youtube_error}")
            if progress:
                progress.end_youtube(len(youtube_items))

        # HackerNews (2-tuple: items, error)
        if hackernews_futures:
            all_items = []
            for f in hackernews_futures:
                try:
                    items, err = f.result(timeout=future_timeout)
                    all_items.extend(items or [])
                    if err and not hackernews_error:
                        hackernews_error = err
                except TimeoutError:
                    hackernews_error = f"HN timed out after {future_timeout}s"
                except Exception as e:
                    hackernews_error = f"HN {e}"
            seen = set()
            hackernews_items = [
                item for item in all_items
                if not (item.get("url", "") in seen or seen.add(item.get("url", "")))
            ]
            if hackernews_error and progress:
                progress.show_error(f"HN error: {hackernews_error}")
            if progress:
                progress.end_hackernews(len(hackernews_items))

        # Polymarket (2-tuple: items, error)
        if polymarket_futures:
            all_items = []
            for f in polymarket_futures:
                try:
                    items, err = f.result(timeout=future_timeout)
                    all_items.extend(items or [])
                    if err and not polymarket_error:
                        polymarket_error = err
                except TimeoutError:
                    polymarket_error = f"Polymarket timed out after {future_timeout}s"
                except Exception as e:
                    polymarket_error = f"Polymarket {e}"
            seen = set()
            polymarket_items = [
                item for item in all_items
                if not (item.get("url", "") in seen or seen.add(item.get("url", "")))
            ]
            if polymarket_error and progress:
                progress.show_error(f"Polymarket error: {polymarket_error}")
            if progress:
                progress.end_polymarket(len(polymarket_items))

        # arXiv (2-tuple: items, error)
        if arxiv_futures:
            all_items = []
            for f in arxiv_futures:
                try:
                    items, err = f.result(timeout=future_timeout)
                    all_items.extend(items or [])
                    if err and not arxiv_error:
                        arxiv_error = err
                except TimeoutError:
                    arxiv_error = f"arXiv timed out after {future_timeout}s"
                except Exception as e:
                    arxiv_error = f"arXiv {e}"
            seen = set()
            arxiv_items = [
                item for item in all_items
                if not (item.get("url", "") in seen or seen.add(item.get("url", "")))
            ]
            if arxiv_error and progress:
                progress.show_error(f"arXiv error: {arxiv_error}")
            if progress:
                progress.end_arxiv(len(arxiv_items))

        # Patents (2-tuple: items, error)
        if patent_futures:
            all_items = []
            for f in patent_futures:
                try:
                    items, err = f.result(timeout=future_timeout)
                    all_items.extend(items or [])
                    if err and not patent_error:
                        patent_error = err
                except TimeoutError:
                    patent_error = f"Patents timed out after {future_timeout}s"
                except Exception as e:
                    patent_error = f"Patents {e}"
            seen = set()
            patent_items = [
                item for item in all_items
                if not (item.get("url", "") in seen or seen.add(item.get("url", "")))
            ]
            if patent_error and progress:
                progress.show_error(f"Patents error: {patent_error}")
            if progress:
                progress.end_patents(len(patent_items))

        # Books (2-tuple: items, error)
        if book_futures:
            all_items = []
            for f in book_futures:
                try:
                    items, err = f.result(timeout=future_timeout)
                    all_items.extend(items or [])
                    if err and not book_error:
                        book_error = err
                except TimeoutError:
                    book_error = f"Books timed out after {future_timeout}s"
                except Exception as e:
                    book_error = f"Books {e}"
            seen = set()
            book_items = [
                item for item in all_items
                if not (item.get("url", "") in seen or seen.add(item.get("url", "")))
            ]
            if book_error and progress:
                progress.show_error(f"Books error: {book_error}")
            if progress:
                progress.end_books(len(book_items))

        # Web (2-tuple: items, error)
        if web_futures:
            all_items = []
            for f in web_futures:
                try:
                    items, err = f.result(timeout=future_timeout)
                    all_items.extend(items or [])
                    if err and not web_error:
                        web_error = err
                except TimeoutError:
                    web_error = f"Web timed out after {future_timeout}s"
                except Exception as e:
                    web_error = f"Web {e}"
            seen = set()
            web_items = [
                item for item in all_items
                if not (item.get("url", "") in seen or seen.add(item.get("url", "")))
            ]
            if web_error and progress:
                progress.show_error(f"Web error: {web_error}")
            sys.stderr.write(f"[web] {len(web_items)} results\n")
            sys.stderr.flush()

        # --- Chinese platform results (single futures, 2-tuple: items, error) ---

        if bilibili_future:
            try:
                bilibili_items, bilibili_error = bilibili_future.result(timeout=future_timeout)
                if bilibili_error and progress:
                    progress.show_error(f"Bilibili error: {bilibili_error}")
            except TimeoutError:
                bilibili_error = f"Bilibili search timed out after {future_timeout}s"
                if progress:
                    progress.show_error(bilibili_error)
            except Exception as e:
                bilibili_error = f"{type(e).__name__}: {e}"
                if progress:
                    progress.show_error(f"Bilibili error: {e}")
            sys.stderr.write(f"[Bilibili] {len(bilibili_items)} results\n")
            sys.stderr.flush()

        if zhihu_future:
            try:
                zhihu_items, zhihu_error = zhihu_future.result(timeout=future_timeout)
                if zhihu_error and progress:
                    progress.show_error(f"Zhihu error: {zhihu_error}")
            except TimeoutError:
                zhihu_error = f"Zhihu search timed out after {future_timeout}s"
                if progress:
                    progress.show_error(zhihu_error)
            except Exception as e:
                zhihu_error = f"{type(e).__name__}: {e}"
                if progress:
                    progress.show_error(f"Zhihu error: {e}")
            sys.stderr.write(f"[Zhihu] {len(zhihu_items)} results\n")
            sys.stderr.flush()

        if weibo_future:
            try:
                weibo_items, weibo_error = weibo_future.result(timeout=future_timeout)
                if weibo_error and progress:
                    progress.show_error(f"Weibo error: {weibo_error}")
            except TimeoutError:
                weibo_error = f"Weibo search timed out after {future_timeout}s"
                if progress:
                    progress.show_error(weibo_error)
            except Exception as e:
                weibo_error = f"{type(e).__name__}: {e}"
                if progress:
                    progress.show_error(f"Weibo error: {e}")
            sys.stderr.write(f"[Weibo] {len(weibo_items)} results\n")
            sys.stderr.flush()

        if douyin_future:
            try:
                douyin_items, douyin_error = douyin_future.result(timeout=future_timeout)
                if douyin_error and progress:
                    progress.show_error(f"Douyin error: {douyin_error}")
            except TimeoutError:
                douyin_error = f"Douyin search timed out after {future_timeout}s"
                if progress:
                    progress.show_error(douyin_error)
            except Exception as e:
                douyin_error = f"{type(e).__name__}: {e}"
                if progress:
                    progress.show_error(f"Douyin error: {e}")
            sys.stderr.write(f"[Douyin] {len(douyin_items)} results\n")
            sys.stderr.flush()

        if baidu_future:
            try:
                baidu_items, baidu_error = baidu_future.result(timeout=future_timeout)
                if baidu_error and progress:
                    progress.show_error(f"Baidu error: {baidu_error}")
            except TimeoutError:
                baidu_error = f"Baidu search timed out after {future_timeout}s"
                if progress:
                    progress.show_error(baidu_error)
            except Exception as e:
                baidu_error = f"{type(e).__name__}: {e}"
                if progress:
                    progress.show_error(f"Baidu error: {e}")
            sys.stderr.write(f"[Baidu] {len(baidu_items)} results\n")
            sys.stderr.flush()

    # Enrich Reddit items with real data (parallel, capped)
    enrich_max = timeouts["enrich_max_items"]
    enrich_total_timeout = timeouts["enrich_total"]
    items_to_enrich = reddit_items[:enrich_max]
    rate_limited = False  # Set True if Reddit returns 429 during enrichment

    if items_to_enrich:
        if progress:
            progress.start_reddit_enrich(1, len(items_to_enrich))

        if mock:
            # Sequential mock enrichment (fast, no need for parallelism)
            for i, item in enumerate(items_to_enrich):
                if progress and i > 0:
                    progress.update_reddit_enrich(i + 1, len(items_to_enrich))
                try:
                    mock_thread = load_fixture("reddit_thread_sample.json")
                    reddit_items[i] = reddit_enrich.enrich_reddit_item(item, mock_thread)
                except Exception as e:
                    if progress:
                        progress.show_error(f"Enrich failed for {item.get('url', 'unknown')}: {e}")
                raw_reddit_enriched.append(reddit_items[i])
        else:
            # Parallel enrichment with bounded concurrency and total timeout
            # Uses short HTTP timeout (10s) and 1 retry to fail fast on 429
            completed_count = 0
            rate_limited = False
            with ThreadPoolExecutor(max_workers=5) as enrich_pool:
                futures = {
                    enrich_pool.submit(reddit_enrich.enrich_reddit_item, item): i
                    for i, item in enumerate(items_to_enrich)
                }
                try:
                    for future in as_completed(futures, timeout=enrich_total_timeout):
                        idx = futures[future]
                        completed_count += 1
                        if progress:
                            progress.update_reddit_enrich(completed_count, len(items_to_enrich))
                        try:
                            reddit_items[idx] = future.result(timeout=timeouts["enrich_per"])
                        except reddit_enrich.RedditRateLimitError:
                            rate_limited = True
                            if progress:
                                progress.show_error(
                                    "Reddit rate-limited (429) — skipping remaining enrichment"
                                )
                            # Cancel remaining futures and bail
                            for f in futures:
                                f.cancel()
                            break
                        except Exception as e:
                            if progress:
                                progress.show_error(
                                    f"Enrich failed for {items_to_enrich[idx].get('url', 'unknown')}: {e}"
                                )
                        raw_reddit_enriched.append(reddit_items[idx])
                except TimeoutError:
                    if progress:
                        progress.show_error(
                            f"Enrichment timed out after {enrich_total_timeout}s "
                            f"({completed_count}/{len(items_to_enrich)} done)"
                        )
                    # Keep unenriched items as-is
                    for idx in futures.values():
                        if reddit_items[idx] not in raw_reddit_enriched:
                            raw_reddit_enriched.append(reddit_items[idx])

        if progress:
            progress.end_reddit_enrich()

    # Enrich HN stories with comments
    if hackernews_items:
        try:
            hackernews_items = hackernews.enrich_top_stories(hackernews_items, depth=depth)
        except Exception as e:
            sys.stderr.write(f"[HN] Enrichment error: {e}\n")
            sys.stderr.flush()

    # Phase 2: Supplemental search based on entities from Phase 1
    # Skip on --quick (speed matters), mock mode, or if Reddit is rate-limiting
    if depth != "quick" and not mock and (reddit_items or x_items):
        sup_reddit, sup_x = _run_supplemental(
            topic, reddit_items, x_items,
            from_date, to_date, depth, x_source, progress,
            skip_reddit=rate_limited,
            resolved_handle=resolved_handle,
        )
        if sup_reddit:
            reddit_items.extend(sup_reddit)
        if sup_x:
            x_items.extend(sup_x)

    return reddit_items, x_items, youtube_items, hackernews_items, polymarket_items, arxiv_items, patent_items, book_items, web_items, web_needed, bilibili_items, zhihu_items, weibo_items, douyin_items, baidu_items, raw_openai, raw_xai, raw_reddit_enriched, reddit_error, x_error, youtube_error, hackernews_error, polymarket_error, arxiv_error, patent_error, book_error, web_error, bilibili_error, zhihu_error, weibo_error, douyin_error, baidu_error


def main():
    # Fix Unicode output on Windows (cp1252 can't encode emoji)
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Research a topic from the last N days on Reddit + X"
    )
    parser.add_argument("topic", nargs="?", help="Topic to research")
    parser.add_argument("--mock", action="store_true", help="Use fixtures")
    parser.add_argument(
        "--emit",
        choices=["compact", "json", "md", "context", "path"],
        default="compact",
        help="Output mode",
    )
    parser.add_argument(
        "--sources",
        choices=["auto", "reddit", "x", "both"],
        default="auto",
        help="Source selection",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Faster research with fewer sources (8-12 each)",
    )
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Comprehensive research with more sources (50-70 Reddit, 40-60 X)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose debug logging",
    )
    parser.add_argument(
        "--include-web",
        action="store_true",
        help="Include general web search alongside Reddit/X (lower weighted)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        choices=range(1, 31),
        metavar="N",
        help="Number of days to look back (1-30, default: 30)",
    )
    parser.add_argument(
        "--store",
        action="store_true",
        help="Persist findings to SQLite database (~/.local/share/last30days/research.db)",
    )
    parser.add_argument(
        "--diagnose",
        action="store_true",
        help="Show source availability diagnostics and exit",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=None,
        metavar="SECS",
        help="Global timeout in seconds (default: 180, quick: 90, deep: 300)",
    )
    parser.add_argument(
        "--x-handle",
        type=str,
        default=None,
        metavar="HANDLE",
        help="Resolved X handle for topic entity (without @). Searched unfiltered in Phase 2.",
    )

    args = parser.parse_args()

    # Enable debug logging if requested
    if args.debug:
        os.environ["LAST30DAYS_DEBUG"] = "1"
        # Re-import http to pick up debug flag
        from lib import http as http_module
        http_module.DEBUG = True

    # Determine depth
    if args.quick and args.deep:
        print("Error: Cannot use both --quick and --deep", file=sys.stderr)
        sys.exit(1)
    elif args.quick:
        depth = "quick"
    elif args.deep:
        depth = "deep"
    else:
        depth = "default"

    # Install global timeout watchdog
    timeouts = TIMEOUT_PROFILES[depth]
    global_timeout = args.timeout or timeouts["global"]
    _install_global_timeout(global_timeout)

    # Load config and expose to subprocesses
    config = env.get_config()
    for k, v in config.items():
        if v is not None:
            os.environ[k] = str(v)

    # Auto-detect Bird (no prompts - just use it if available)
    x_source_status = env.get_x_source_status(config)
    x_source = x_source_status["source"]  # 'bird', 'xai', or None

    # Auto-detect yt-dlp for YouTube search
    has_ytdlp = env.is_ytdlp_available()

    # --diagnose: show source availability and exit
    if args.diagnose:
        web_source = env.get_web_search_source(config)
        reddit_source = env.get_reddit_source(config)
        diag = {
            "reddit_source": reddit_source,
            "openai": bool(config.get("OPENAI_API_KEY")),
            "gemini": bool(config.get("GEMINI_API_KEY")),
            "xai": bool(config.get("XAI_API_KEY")),
            "x_source": x_source_status["source"],
            "bird_installed": x_source_status["bird_installed"],
            "bird_authenticated": x_source_status["bird_authenticated"],
            "bird_username": x_source_status.get("bird_username"),
            "youtube": has_ytdlp,
            "hackernews": True,
            "polymarket": True,
            "web_search_backend": web_source,
            "parallel_ai": bool(config.get("PARALLEL_API_KEY")),
            "brave": bool(config.get("BRAVE_API_KEY")),
            "openrouter": bool(config.get("OPENROUTER_API_KEY")),
        }
        print(json.dumps(diag, indent=2))
        sys.exit(0)

    # Validate topic (--diagnose doesn't need one)
    if not args.topic:
        print("Error: Please provide a topic to research.", file=sys.stderr)
        print("Usage: python3 last30days.py <topic> [options]", file=sys.stderr)
        sys.exit(1)

    # Initialize progress display with topic
    progress = ui.ProgressDisplay(args.topic, show_banner=True)

    # Show diagnostic banner when sources are missing
    web_source = env.get_web_search_source(config)
    reddit_source = env.get_reddit_source(config)
    diag = {
        "reddit_source": reddit_source,
        "openai": bool(config.get("OPENAI_API_KEY")),
        "gemini": bool(config.get("GEMINI_API_KEY")),
        "xai": bool(config.get("XAI_API_KEY")),
        "x_source": x_source_status["source"],
        "bird_installed": x_source_status["bird_installed"],
        "bird_authenticated": x_source_status["bird_authenticated"],
        "bird_username": x_source_status.get("bird_username"),
        "youtube": has_ytdlp,
        "hackernews": True,
        "polymarket": True,
        "web_search_backend": web_source,
    }
    ui.show_diagnostic_banner(diag)

    # Check available sources (accounting for Bird auto-detection)
    available = env.get_available_sources(config)

    # Override available if Bird is ready
    if x_source == 'bird':
        if available == 'reddit':
            available = 'both'  # Now have both Reddit + X (via Bird)
        elif available == 'web':
            available = 'x'  # Now have X via Bird

    # Mock mode can work without keys
    if args.mock:
        if args.sources == "auto":
            sources = "both"
        else:
            sources = args.sources
    else:
        # Validate requested sources against available
        sources, error = env.validate_sources(args.sources, available, args.include_web)
        if error:
            # If it's a warning about WebSearch fallback, print but continue
            if "WebSearch fallback" in error:
                print(f"Note: {error}", file=sys.stderr)
            else:
                print(f"Error: {error}", file=sys.stderr)
                sys.exit(1)

    # Get date range
    from_date, to_date = dates.get_date_range(args.days)

    # Check what keys are missing for promo messaging
    missing_keys = env.get_missing_keys(config)

    # Show NUX / promo for missing keys BEFORE research
    if missing_keys != 'none':
        progress.show_promo(missing_keys, diag=diag)

    # Select models
    if args.mock:
        # Use mock models
        mock_openai_models = load_fixture("models_openai_sample.json").get("data", [])
        mock_xai_models = load_fixture("models_xai_sample.json").get("data", [])
        selected_models = models.get_models(
            {
                "OPENAI_API_KEY": "mock",
                "XAI_API_KEY": "mock",
                **config,
            },
            mock_openai_models,
            mock_xai_models,
        )
    else:
        selected_models = models.get_models(config)

    # Determine mode string
    if sources == "all":
        mode = "all"  # reddit + x + web
    elif sources == "both":
        mode = "both"  # reddit + x
    elif sources == "reddit":
        mode = "reddit-only"
    elif sources == "reddit-web":
        mode = "reddit-web"
    elif sources == "x":
        mode = "x-only"
    elif sources == "x-web":
        mode = "x-web"
    elif sources == "web":
        mode = "web-only"
    else:
        mode = sources

    # Run research
    reddit_items, x_items, youtube_items, hackernews_items, polymarket_items, arxiv_items, patent_items, book_items, web_items, web_needed, bilibili_items, zhihu_items, weibo_items, douyin_items, baidu_items, raw_openai, raw_xai, raw_reddit_enriched, reddit_error, x_error, youtube_error, hackernews_error, polymarket_error, arxiv_error, patent_error, book_error, web_error, bilibili_error, zhihu_error, weibo_error, douyin_error, baidu_error = run_research(
        args.topic,
        sources,
        config,
        selected_models,
        from_date,
        to_date,
        depth,
        args.mock,
        progress,
        x_source=x_source or "xai",
        run_youtube=has_ytdlp,
        timeouts=timeouts,
        resolved_handle=args.x_handle,
        reddit_source=reddit_source,
        use_chinese_platforms=True,
    )

    # Processing phase
    progress.start_processing()

    # Normalize items
    normalized_reddit = normalize.normalize_reddit_items(reddit_items, from_date, to_date)
    normalized_x = normalize.normalize_x_items(x_items, from_date, to_date)
    normalized_youtube = normalize.normalize_youtube_items(youtube_items, from_date, to_date) if youtube_items else []
    normalized_hn = normalize.normalize_hackernews_items(hackernews_items, from_date, to_date) if hackernews_items else []
    normalized_pm = normalize.normalize_polymarket_items(polymarket_items, from_date, to_date) if polymarket_items else []
    normalized_arxiv = normalize.normalize_arxiv_items(arxiv_items, from_date, to_date) if arxiv_items else []
    normalized_patents = normalize.normalize_patent_items(patent_items, from_date, to_date) if patent_items else []
    normalized_books = normalize.normalize_book_items(book_items, from_date, to_date) if book_items else []
    normalized_web = websearch.normalize_websearch_items(web_items, from_date, to_date) if web_items else []
    # Chinese platforms
    normalized_bilibili = normalize.normalize_bilibili_items(bilibili_items, from_date, to_date) if bilibili_items else []
    normalized_zhihu = normalize.normalize_zhihu_items(zhihu_items, from_date, to_date) if zhihu_items else []
    normalized_weibo = normalize.normalize_weibo_items(weibo_items, from_date, to_date) if weibo_items else []
    normalized_douyin = normalize.normalize_douyin_items(douyin_items, from_date, to_date) if douyin_items else []
    normalized_baidu = normalize.normalize_baidu_items(baidu_items, from_date, to_date) if baidu_items else []

    # Hard date filter: exclude items with verified dates outside the range
    # This is the safety net - even if prompts let old content through, this filters it
    filtered_reddit = normalize.filter_by_date_range(normalized_reddit, from_date, to_date)
    filtered_x = normalize.filter_by_date_range(normalized_x, from_date, to_date)
    # YouTube: skip hard date filter — youtube_yt.py already applies a soft filter
    # that prefers recent videos but keeps older ones for evergreen topics.
    # YouTube content has a longer shelf life than tweets/posts.
    filtered_youtube = normalized_youtube
    filtered_hn = normalize.filter_by_date_range(normalized_hn, from_date, to_date) if normalized_hn else []
    # Polymarket: skip hard date filter - markets are active/traded, updatedAt is fine
    filtered_pm = normalized_pm
    # arXiv: already date-filtered in search_arxiv
    filtered_arxiv = normalized_arxiv
    # Patents: already date-filtered in search_patents
    filtered_patents = normalized_patents
    # Books: skip hard date filter - year-only dates are imprecise
    filtered_books = normalized_books
    filtered_web = normalize.filter_by_date_range(normalized_web, from_date, to_date) if normalized_web else []

    # Score items
    scored_reddit = score.score_reddit_items(filtered_reddit)
    scored_x = score.score_x_items(filtered_x)
    scored_youtube = score.score_youtube_items(filtered_youtube) if filtered_youtube else []
    scored_hn = score.score_hackernews_items(filtered_hn) if filtered_hn else []
    scored_pm = score.score_polymarket_items(filtered_pm) if filtered_pm else []
    scored_arxiv = score.score_arxiv_items(filtered_arxiv) if filtered_arxiv else []
    scored_patents = score.score_patent_items(filtered_patents) if filtered_patents else []
    scored_books = score.score_book_items(filtered_books) if filtered_books else []
    scored_web = score.score_websearch_items(filtered_web) if filtered_web else []
    # Chinese platforms
    scored_bilibili = score.score_bilibili_items(normalized_bilibili) if normalized_bilibili else []
    scored_zhihu = score.score_zhihu_items(normalized_zhihu) if normalized_zhihu else []
    scored_weibo = score.score_weibo_items(normalized_weibo) if normalized_weibo else []
    scored_douyin = score.score_douyin_items(normalized_douyin) if normalized_douyin else []
    scored_baidu = score.score_baidu_items(normalized_baidu) if normalized_baidu else []

    # Sort items
    sorted_reddit = score.sort_items(scored_reddit)
    sorted_x = score.sort_items(scored_x)
    sorted_youtube = score.sort_items(scored_youtube) if scored_youtube else []
    sorted_hn = score.sort_items(scored_hn) if scored_hn else []
    sorted_pm = score.sort_items(scored_pm) if scored_pm else []
    sorted_arxiv = score.sort_items(scored_arxiv) if scored_arxiv else []
    sorted_patents = score.sort_items(scored_patents) if scored_patents else []
    sorted_books = score.sort_items(scored_books) if scored_books else []
    sorted_web = score.sort_items(scored_web) if scored_web else []
    # Chinese platforms
    sorted_bilibili = score.sort_items(scored_bilibili) if scored_bilibili else []
    sorted_zhihu = score.sort_items(scored_zhihu) if scored_zhihu else []
    sorted_weibo = score.sort_items(scored_weibo) if scored_weibo else []
    sorted_douyin = score.sort_items(scored_douyin) if scored_douyin else []
    sorted_baidu = score.sort_items(scored_baidu) if scored_baidu else []

    # Dedupe items
    deduped_reddit = dedupe.dedupe_reddit(sorted_reddit)
    deduped_x = dedupe.dedupe_x(sorted_x)
    deduped_youtube = dedupe.dedupe_youtube(sorted_youtube) if sorted_youtube else []
    deduped_hn = dedupe.dedupe_hackernews(sorted_hn) if sorted_hn else []
    deduped_pm = dedupe.dedupe_polymarket(sorted_pm) if sorted_pm else []
    deduped_arxiv = dedupe.dedupe_arxiv(sorted_arxiv) if sorted_arxiv else []
    deduped_patents = dedupe.dedupe_patents(sorted_patents) if sorted_patents else []
    deduped_books = dedupe.dedupe_books(sorted_books) if sorted_books else []
    deduped_web = websearch.dedupe_websearch(sorted_web) if sorted_web else []
    # Chinese platforms
    deduped_bilibili = dedupe.dedupe_bilibili(sorted_bilibili) if sorted_bilibili else []
    deduped_zhihu = dedupe.dedupe_zhihu(sorted_zhihu) if sorted_zhihu else []
    deduped_weibo = dedupe.dedupe_weibo(sorted_weibo) if sorted_weibo else []
    deduped_douyin = dedupe.dedupe_douyin(sorted_douyin) if sorted_douyin else []
    deduped_baidu = dedupe.dedupe_baidu(sorted_baidu) if sorted_baidu else []

    # Minimum result guarantee: if all Reddit results were filtered out but
    # we had raw results, keep top 3 by relevance regardless of score
    if not deduped_reddit and normalized_reddit:
        print("[REDDIT WARNING] All results scored below threshold, keeping top 3 by relevance", file=sys.stderr)
        by_relevance = sorted(normalized_reddit, key=lambda item: item.relevance, reverse=True)
        deduped_reddit = by_relevance[:3]

    # Cross-source linking: annotate items that discuss the same story
    dedupe.cross_source_link(
        deduped_reddit, deduped_x, deduped_youtube, deduped_hn, deduped_pm, deduped_web,
        deduped_arxiv, deduped_patents, deduped_books,
        deduped_bilibili, deduped_zhihu, deduped_weibo, deduped_douyin, deduped_baidu,
    )

    progress.end_processing()

    # Create report
    report = schema.create_report(
        args.topic,
        from_date,
        to_date,
        mode,
        selected_models.get("openai"),
        selected_models.get("xai"),
    )
    report.reddit = deduped_reddit
    report.x = deduped_x
    report.youtube = deduped_youtube
    report.hackernews = deduped_hn
    report.polymarket = deduped_pm
    report.arxiv = deduped_arxiv
    report.patents = deduped_patents
    report.books = deduped_books
    report.web = deduped_web
    # Chinese platforms
    report.bilibili = deduped_bilibili
    report.zhihu = deduped_zhihu
    report.weibo = deduped_weibo
    report.douyin = deduped_douyin
    report.baidu = deduped_baidu
    # Errors
    report.reddit_error = reddit_error
    report.x_error = x_error
    report.youtube_error = youtube_error
    report.hackernews_error = hackernews_error
    report.polymarket_error = polymarket_error
    report.arxiv_error = arxiv_error
    report.patent_error = patent_error
    report.book_error = book_error
    report.web_error = web_error
    report.bilibili_error = bilibili_error
    report.zhihu_error = zhihu_error
    report.weibo_error = weibo_error
    report.douyin_error = douyin_error
    report.baidu_error = baidu_error
    report.resolved_x_handle = args.x_handle

    # Generate context snippet
    report.context_snippet_md = render.render_context_snippet(report)

    # Write outputs
    render.write_outputs(report, raw_openai, raw_xai, raw_reddit_enriched)

    # Show completion
    if sources == "web":
        progress.show_web_only_complete()
    else:
        progress.show_complete(
            len(deduped_reddit), len(deduped_x), len(deduped_youtube),
            len(deduped_hn), len(deduped_pm),
            len(deduped_arxiv), len(deduped_patents), len(deduped_books),
            len(deduped_bilibili), len(deduped_zhihu), len(deduped_weibo),
            len(deduped_douyin), len(deduped_baidu),
        )

    # Build source info for status footer
    source_info = {}
    if reddit_source == 'native':
        source_info["reddit_backend"] = "Native (free, no API key)"
    if not x_source:
        if x_source_status["bird_installed"]:
            source_info["x_skip_reason"] = "Bird installed but not authenticated — log into x.com in browser"
        else:
            source_info["x_skip_reason"] = "No Bird CLI or XAI_API_KEY (Node.js 22+ needed for Bird)"
    if not has_ytdlp:
        source_info["youtube_skip_reason"] = "yt-dlp not installed — fix: brew install yt-dlp"
    if not web_source:
        source_info["web_skip_reason"] = "assistant will use WebSearch (add BRAVE_API_KEY for native search)"

    # Output result
    output_result(report, args.emit, web_needed, args.topic, from_date, to_date, missing_keys, args.days, source_info)

    # Persist findings to SQLite if requested
    if args.store:
        import store as store_mod
        store_mod.init_db()
        topic_row = store_mod.add_topic(args.topic)
        topic_id = topic_row["id"]
        run_id = store_mod.record_run(topic_id, source_mode=mode, status="completed")

        findings = []
        for item in deduped_reddit:
            findings.append({
                "source": "reddit",
                "url": item.url,
                "title": item.title,
                "author": item.subreddit,
                "content": item.title,
                "engagement_score": item.engagement.score if item.engagement else 0,
                "relevance_score": item.relevance,
            })
        for item in deduped_x:
            findings.append({
                "source": "x",
                "url": item.url,
                "title": item.text[:100],
                "author": item.author_handle,
                "content": item.text,
                "engagement_score": item.engagement.likes if item.engagement else 0,
                "relevance_score": item.relevance,
            })
        for item in deduped_youtube:
            findings.append({
                "source": "youtube",
                "url": item.url,
                "title": item.title,
                "author": item.channel_name,
                "content": item.transcript_snippet[:500] if item.transcript_snippet else item.title,
                "engagement_score": item.engagement.views if item.engagement and item.engagement.views else 0,
                "relevance_score": item.relevance,
            })
        for item in deduped_hn:
            findings.append({
                "source": "hackernews",
                "url": item.hn_url,
                "title": item.title,
                "author": item.author,
                "content": item.title,
                "engagement_score": item.engagement.score if item.engagement else 0,
                "relevance_score": item.relevance,
            })
        for item in deduped_pm:
            findings.append({
                "source": "polymarket",
                "url": item.url,
                "title": item.question,
                "author": "polymarket",
                "content": item.title,
                "engagement_score": item.engagement.volume if item.engagement and item.engagement.volume else 0,
                "relevance_score": item.relevance,
            })
        for item in deduped_arxiv:
            findings.append({
                "source": "arxiv",
                "url": item.url,
                "title": item.title,
                "author": ", ".join(item.authors[:3]),
                "content": item.summary,
                "engagement_score": 0,
                "relevance_score": item.relevance,
            })
        for item in deduped_patents:
            findings.append({
                "source": "patents",
                "url": item.url,
                "title": item.title,
                "author": item.assignee,
                "content": item.abstract,
                "engagement_score": 0,
                "relevance_score": item.relevance,
            })
        for item in deduped_books:
            findings.append({
                "source": "books",
                "url": item.url,
                "title": item.title,
                "author": ", ".join(item.authors[:3]),
                "content": item.description,
                "engagement_score": 0,
                "relevance_score": item.relevance,
            })
        for item in deduped_web:
            findings.append({
                "source": "web",
                "url": item.url,
                "title": item.title,
                "author": item.source_domain,
                "content": item.snippet,
                "engagement_score": 0,
                "relevance_score": item.relevance,
            })

        counts = store_mod.store_findings(run_id, topic_id, findings)
        store_mod.update_run(
            run_id,
            status="completed",
            findings_new=counts["new"],
            findings_updated=counts["updated"],
        )
        sys.stderr.write(
            f"[store] Saved {counts['new']} new, {counts['updated']} updated findings\n"
        )
        sys.stderr.flush()


def output_result(
    report: schema.Report,
    emit_mode: str,
    web_needed: bool = False,
    topic: str = "",
    from_date: str = "",
    to_date: str = "",
    missing_keys: str = "none",
    days: int = 30,
    source_info: dict = None,
):
    """Output the result based on emit mode."""
    if emit_mode == "compact":
        print(render.render_compact(report, missing_keys=missing_keys))
        # Append source status footer
        print(render.render_source_status(report, source_info))
    elif emit_mode == "json":
        print(json.dumps(report.to_dict(), indent=2))
    elif emit_mode == "md":
        print(render.render_full_report(report))
    elif emit_mode == "context":
        print(report.context_snippet_md)
    elif emit_mode == "path":
        print(render.get_context_path())

    # Output WebSearch instructions if needed
    if web_needed:
        print("\n" + "="*60)
        print("### WEBSEARCH REQUIRED ###")
        print("="*60)
        print(f"Topic: {topic}")
        print(f"Date range: {from_date} to {to_date}")
        print("")
        print("Assistant: Use your web search tool to find 8-15 relevant web pages.")
        print("EXCLUDE: reddit.com, x.com, twitter.com (already covered above)")
        print(f"INCLUDE: blogs, docs, news, tutorials from the last {days} days")
        print("")
        print("After searching, synthesize WebSearch results WITH the Reddit/X")
        print("results above. WebSearch items should rank LOWER than comparable")
        print("Reddit/X items (they lack engagement metrics).")
        print("="*60)


if __name__ == "__main__":
    main()
