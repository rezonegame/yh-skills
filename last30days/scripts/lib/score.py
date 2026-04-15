"""Popularity-aware scoring for last30days skill."""

import math
import re
from typing import List, Optional, Union

from . import dates, schema

# Score weights for Reddit/X (has engagement)
WEIGHT_RELEVANCE = 0.45
WEIGHT_RECENCY = 0.25
WEIGHT_ENGAGEMENT = 0.30

# WebSearch weights (no engagement, reweighted to 100%)
WEBSEARCH_WEIGHT_RELEVANCE = 0.55
WEBSEARCH_WEIGHT_RECENCY = 0.45
WEBSEARCH_SOURCE_PENALTY = 15  # Points deducted for lacking engagement

# WebSearch date confidence adjustments
WEBSEARCH_VERIFIED_BONUS = 10   # Bonus for URL-verified recent date (high confidence)
WEBSEARCH_NO_DATE_PENALTY = 20  # Heavy penalty for no date signals (low confidence)

# Default engagement score for unknown
DEFAULT_ENGAGEMENT = 35
UNKNOWN_ENGAGEMENT_PENALTY = 3


def log1p_safe(x: Optional[int]) -> float:
    """Safe log1p that handles None and negative values."""
    if x is None or x < 0:
        return 0.0
    return math.log1p(x)


def compute_reddit_engagement_raw(engagement: Optional[schema.Engagement]) -> Optional[float]:
    """Compute raw engagement score for Reddit item.

    Formula: 0.55*log1p(score) + 0.40*log1p(num_comments) + 0.05*(upvote_ratio*10)
    """
    if engagement is None:
        return None

    if engagement.score is None and engagement.num_comments is None:
        return None

    score = log1p_safe(engagement.score)
    comments = log1p_safe(engagement.num_comments)
    ratio = (engagement.upvote_ratio or 0.5) * 10

    return 0.55 * score + 0.40 * comments + 0.05 * ratio


def compute_x_engagement_raw(engagement: Optional[schema.Engagement]) -> Optional[float]:
    """Compute raw engagement score for X item.

    Formula: 0.55*log1p(likes) + 0.25*log1p(reposts) + 0.15*log1p(replies) + 0.05*log1p(quotes)
    """
    if engagement is None:
        return None

    if engagement.likes is None and engagement.reposts is None:
        return None

    likes = log1p_safe(engagement.likes)
    reposts = log1p_safe(engagement.reposts)
    replies = log1p_safe(engagement.replies)
    quotes = log1p_safe(engagement.quotes)

    return 0.55 * likes + 0.25 * reposts + 0.15 * replies + 0.05 * quotes


def normalize_to_100(values: List[float], default: float = 50) -> List[float]:
    """Normalize a list of values to 0-100 scale.

    Args:
        values: Raw values (None values are preserved)
        default: Default value for None entries

    Returns:
        Normalized values
    """
    # Filter out None
    valid = [v for v in values if v is not None]
    if not valid:
        return [default if v is None else 50 for v in values]

    min_val = min(valid)
    max_val = max(valid)
    range_val = max_val - min_val

    if range_val == 0:
        return [50 if v is None else 50 for v in values]

    result = []
    for v in values:
        if v is None:
            result.append(None)
        else:
            normalized = ((v - min_val) / range_val) * 100
            result.append(normalized)

    return result


def score_reddit_items(items: List[schema.RedditItem]) -> List[schema.RedditItem]:
    """Compute scores for Reddit items.

    Args:
        items: List of Reddit items

    Returns:
        Items with updated scores
    """
    if not items:
        return items

    # Compute raw engagement scores
    eng_raw = [compute_reddit_engagement_raw(item.engagement) for item in items]

    # Normalize engagement to 0-100
    eng_normalized = normalize_to_100(eng_raw)

    for i, item in enumerate(items):
        # Relevance subscore (model-provided, convert to 0-100)
        rel_score = int(item.relevance * 100)

        # Recency subscore
        rec_score = dates.recency_score(item.date)

        # Engagement subscore
        if eng_normalized[i] is not None:
            eng_score = int(eng_normalized[i])
        else:
            eng_score = DEFAULT_ENGAGEMENT

        # Store subscores
        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )

        # Compute overall score
        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score +
            WEIGHT_ENGAGEMENT * eng_score
        )

        # Apply penalty for unknown engagement
        if eng_raw[i] is None:
            overall -= UNKNOWN_ENGAGEMENT_PENALTY

        # Apply penalty for low date confidence
        if item.date_confidence == "low":
            overall -= 5
        elif item.date_confidence == "med":
            overall -= 2

        item.score = max(0, min(100, int(overall)))

    return items


def score_x_items(items: List[schema.XItem]) -> List[schema.XItem]:
    """Compute scores for X items.

    Args:
        items: List of X items

    Returns:
        Items with updated scores
    """
    if not items:
        return items

    # Compute raw engagement scores
    eng_raw = [compute_x_engagement_raw(item.engagement) for item in items]

    # Normalize engagement to 0-100
    eng_normalized = normalize_to_100(eng_raw)

    for i, item in enumerate(items):
        # Relevance subscore (model-provided, convert to 0-100)
        rel_score = int(item.relevance * 100)

        # Recency subscore
        rec_score = dates.recency_score(item.date)

        # Engagement subscore
        if eng_normalized[i] is not None:
            eng_score = int(eng_normalized[i])
        else:
            eng_score = DEFAULT_ENGAGEMENT

        # Store subscores
        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )

        # Compute overall score
        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score +
            WEIGHT_ENGAGEMENT * eng_score
        )

        # Apply penalty for unknown engagement
        if eng_raw[i] is None:
            overall -= UNKNOWN_ENGAGEMENT_PENALTY

        # Apply penalty for low date confidence
        if item.date_confidence == "low":
            overall -= 5
        elif item.date_confidence == "med":
            overall -= 2

        item.score = max(0, min(100, int(overall)))

    return items


def compute_youtube_engagement_raw(engagement: Optional[schema.Engagement]) -> Optional[float]:
    """Compute raw engagement score for YouTube item.

    Formula: 0.50*log1p(views) + 0.35*log1p(likes) + 0.15*log1p(comments)
    Views dominate on YouTube — they're the primary discovery signal.
    """
    if engagement is None:
        return None

    if engagement.views is None and engagement.likes is None:
        return None

    views = log1p_safe(engagement.views)
    likes = log1p_safe(engagement.likes)
    comments = log1p_safe(engagement.num_comments)

    return 0.50 * views + 0.35 * likes + 0.15 * comments


def score_youtube_items(items: List[schema.YouTubeItem]) -> List[schema.YouTubeItem]:
    """Compute scores for YouTube items.

    Uses same weight structure as Reddit/X (relevance + recency + engagement).
    """
    if not items:
        return items

    eng_raw = [compute_youtube_engagement_raw(item.engagement) for item in items]
    eng_normalized = normalize_to_100(eng_raw)

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        if eng_normalized[i] is not None:
            eng_score = int(eng_normalized[i])
        else:
            eng_score = DEFAULT_ENGAGEMENT

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score +
            WEIGHT_ENGAGEMENT * eng_score
        )

        if eng_raw[i] is None:
            overall -= UNKNOWN_ENGAGEMENT_PENALTY

        item.score = max(0, min(100, int(overall)))

    return items


def compute_hackernews_engagement_raw(engagement: Optional[schema.Engagement]) -> Optional[float]:
    """Compute raw engagement score for Hacker News item.

    Formula: 0.55*log1p(points) + 0.45*log1p(num_comments)
    Points are the primary signal on HN; comments indicate depth of discussion.
    """
    if engagement is None:
        return None

    if engagement.score is None and engagement.num_comments is None:
        return None

    points = log1p_safe(engagement.score)
    comments = log1p_safe(engagement.num_comments)

    return 0.55 * points + 0.45 * comments


def score_hackernews_items(items: List[schema.HackerNewsItem]) -> List[schema.HackerNewsItem]:
    """Compute scores for Hacker News items.

    Uses same weight structure as Reddit/X (relevance + recency + engagement).
    """
    if not items:
        return items

    eng_raw = [compute_hackernews_engagement_raw(item.engagement) for item in items]
    eng_normalized = normalize_to_100(eng_raw)

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        if eng_normalized[i] is not None:
            eng_score = int(eng_normalized[i])
        else:
            eng_score = DEFAULT_ENGAGEMENT

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score +
            WEIGHT_ENGAGEMENT * eng_score
        )

        if eng_raw[i] is None:
            overall -= UNKNOWN_ENGAGEMENT_PENALTY

        item.score = max(0, min(100, int(overall)))

    return items


def compute_polymarket_engagement_raw(engagement: Optional[schema.Engagement]) -> Optional[float]:
    """Compute raw engagement score for Polymarket item.

    Formula: 0.60*log1p(volume) + 0.40*log1p(liquidity)
    Volume is the primary signal (money flowing); liquidity indicates market depth.
    """
    if engagement is None:
        return None

    if engagement.volume is None and engagement.liquidity is None:
        return None

    volume = math.log1p(engagement.volume or 0)
    liquidity = math.log1p(engagement.liquidity or 0)

    return 0.60 * volume + 0.40 * liquidity


def score_polymarket_items(items: List[schema.PolymarketItem]) -> List[schema.PolymarketItem]:
    """Compute scores for Polymarket items.

    Uses same weight structure as Reddit/X (relevance + recency + engagement).
    """
    if not items:
        return items

    eng_raw = [compute_polymarket_engagement_raw(item.engagement) for item in items]
    eng_normalized = normalize_to_100(eng_raw)

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        if eng_normalized[i] is not None:
            eng_score = int(eng_normalized[i])
        else:
            eng_score = DEFAULT_ENGAGEMENT

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score +
            WEIGHT_ENGAGEMENT * eng_score
        )

        if eng_raw[i] is None:
            overall -= UNKNOWN_ENGAGEMENT_PENALTY

        item.score = max(0, min(100, int(overall)))

    return items


def score_arxiv_items(items: List[schema.ArxivItem]) -> List[schema.ArxivItem]:
    """Compute scores for arXiv items.

    Uses websearch-like weights (relevance + recency, no engagement data).
    arXiv has no direct engagement metrics available from the API.
    """
    if not items:
        return items

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=0,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score
        )

        # Apply date confidence adjustment
        if item.date_confidence == "med":
            overall -= 2

        item.score = max(0, min(100, int(overall)))

    return items


def score_patent_items(items: List[schema.PatentItem]) -> List[schema.PatentItem]:
    """Compute scores for patent items.

    Uses websearch-like weights (relevance + recency, no engagement data).
    """
    if not items:
        return items

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=0,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score
        )

        item.score = max(0, min(100, int(overall)))

    return items


def score_book_items(items: List[schema.BookItem]) -> List[schema.BookItem]:
    """Compute scores for book items.

    Uses websearch-like weights (relevance + recency, no engagement data).
    """
    if not items:
        return items

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=0,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score
        )

        # Book dates are less precise (year-only common)
        if item.date_confidence == "med":
            overall -= 2

        item.score = max(0, min(100, int(overall)))

    return items


def compute_tiktok_engagement_raw(engagement: Optional[schema.Engagement]) -> Optional[float]:
    """Compute raw engagement score for TikTok item.

    Formula: 0.40*log1p(views) + 0.35*log1p(likes) + 0.15*log1p(comments) + 0.10*log1p(shares)
    Views dominate on TikTok, but shares are a strong virality signal.
    """
    if engagement is None:
        return None

    if engagement.views is None and engagement.likes is None:
        return None

    views = log1p_safe(engagement.views)
    likes = log1p_safe(engagement.likes)
    comments = log1p_safe(engagement.num_comments)
    shares = log1p_safe(engagement.shares)

    return 0.40 * views + 0.35 * likes + 0.15 * comments + 0.10 * shares


def score_tiktok_items(items: List[schema.TikTokItem]) -> List[schema.TikTokItem]:
    """Compute scores for TikTok items.

    Uses same weight structure as Reddit/X (relevance + recency + engagement).
    """
    if not items:
        return items

    eng_raw = [compute_tiktok_engagement_raw(item.engagement) for item in items]
    eng_normalized = normalize_to_100(eng_raw)

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        if eng_normalized[i] is not None:
            eng_score = int(eng_normalized[i])
        else:
            eng_score = DEFAULT_ENGAGEMENT

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score +
            WEIGHT_ENGAGEMENT * eng_score
        )

        if eng_raw[i] is None:
            overall -= UNKNOWN_ENGAGEMENT_PENALTY

        # TikTok dates are often less precise
        if item.date_confidence == "low":
            overall -= 5
        elif item.date_confidence == "med":
            overall -= 2

        item.score = max(0, min(100, int(overall)))

    return items


def compute_instagram_engagement_raw(engagement: Optional[schema.Engagement]) -> Optional[float]:
    """Compute raw engagement score for Instagram item.

    Formula: 0.60*log1p(likes) + 0.40*log1p(comments)
    Likes are the primary signal on Instagram; comments indicate depth.
    """
    if engagement is None:
        return None

    if engagement.likes is None and engagement.num_comments is None:
        return None

    likes = log1p_safe(engagement.likes)
    comments = log1p_safe(engagement.num_comments)

    return 0.60 * likes + 0.40 * comments


def score_instagram_items(items: List[schema.InstagramItem]) -> List[schema.InstagramItem]:
    """Compute scores for Instagram items.

    Uses same weight structure as Reddit/X (relevance + recency + engagement).
    """
    if not items:
        return items

    eng_raw = [compute_instagram_engagement_raw(item.engagement) for item in items]
    eng_normalized = normalize_to_100(eng_raw)

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        if eng_normalized[i] is not None:
            eng_score = int(eng_normalized[i])
        else:
            eng_score = DEFAULT_ENGAGEMENT

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score +
            WEIGHT_ENGAGEMENT * eng_score
        )

        if eng_raw[i] is None:
            overall -= UNKNOWN_ENGAGEMENT_PENALTY

        item.score = max(0, min(100, int(overall)))

    return items


def score_bluesky_items(items: List[schema.BlueskyItem]) -> List[schema.BlueskyItem]:
    """Compute scores for Bluesky items.

    Uses same engagement formula as X (likes + reposts + replies + quotes).
    """
    if not items:
        return items

    eng_raw = [compute_x_engagement_raw(item.engagement) for item in items]
    eng_normalized = normalize_to_100(eng_raw)

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        if eng_normalized[i] is not None:
            eng_score = int(eng_normalized[i])
        else:
            eng_score = DEFAULT_ENGAGEMENT

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score +
            WEIGHT_ENGAGEMENT * eng_score
        )

        if eng_raw[i] is None:
            overall -= UNKNOWN_ENGAGEMENT_PENALTY

        item.score = max(0, min(100, int(overall)))

    return items


def score_truthsocial_items(items: List[schema.TruthSocialItem]) -> List[schema.TruthSocialItem]:
    """Compute scores for Truth Social items.

    Uses same engagement formula as X (likes + reposts + replies).
    """
    if not items:
        return items

    eng_raw = [compute_x_engagement_raw(item.engagement) for item in items]
    eng_normalized = normalize_to_100(eng_raw)

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        if eng_normalized[i] is not None:
            eng_score = int(eng_normalized[i])
        else:
            eng_score = DEFAULT_ENGAGEMENT

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score +
            WEIGHT_ENGAGEMENT * eng_score
        )

        if eng_raw[i] is None:
            overall -= UNKNOWN_ENGAGEMENT_PENALTY

        item.score = max(0, min(100, int(overall)))

    return items


def compute_bilibili_engagement_raw(engagement: Optional[schema.Engagement]) -> Optional[float]:
    """Compute raw engagement score for Bilibili item.

    Formula: 0.40*log1p(views) + 0.25*log1p(danmaku) + 0.20*log1p(likes) + 0.10*log1p(comments) + 0.05*log1p(favorites)
    Views dominate on Bilibili, but danmaku (bullet comments) are a unique engagement signal.
    """
    if engagement is None:
        return None

    if engagement.views is None and engagement.likes is None:
        return None

    views = log1p_safe(engagement.views)
    danmaku = log1p_safe(engagement.danmaku)
    likes = log1p_safe(engagement.likes)
    comments = log1p_safe(engagement.num_comments)
    favorites = log1p_safe(engagement.favorites)

    return 0.40 * views + 0.25 * danmaku + 0.20 * likes + 0.10 * comments + 0.05 * favorites


def score_bilibili_items(items: List[schema.BilibiliItem]) -> List[schema.BilibiliItem]:
    """Compute scores for Bilibili items.

    Uses same weight structure as YouTube (relevance + recency + engagement).
    """
    if not items:
        return items

    eng_raw = [compute_bilibili_engagement_raw(item.engagement) for item in items]
    eng_normalized = normalize_to_100(eng_raw)

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        if eng_normalized[i] is not None:
            eng_score = int(eng_normalized[i])
        else:
            eng_score = DEFAULT_ENGAGEMENT

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score +
            WEIGHT_ENGAGEMENT * eng_score
        )

        if eng_raw[i] is None:
            overall -= UNKNOWN_ENGAGEMENT_PENALTY

        item.score = max(0, min(100, int(overall)))

    return items


def compute_zhihu_engagement_raw(engagement: Optional[schema.Engagement]) -> Optional[float]:
    """Compute raw engagement score for Zhihu item.

    Formula: 0.50*log1p(voteups) + 0.30*log1p(comments) + 0.15*log1p(thanks) + 0.05*log1p(collects)
    Voteups (赞同) are the primary signal on Zhihu; collects (收藏) indicate lasting value.
    """
    if engagement is None:
        return None

    if engagement.voteups is None and engagement.num_comments is None:
        return None

    voteups = log1p_safe(engagement.voteups)
    comments = log1p_safe(engagement.num_comments)
    thanks = log1p_safe(engagement.thanks)
    collects = log1p_safe(engagement.collects)

    return 0.50 * voteups + 0.30 * comments + 0.15 * thanks + 0.05 * collects


def score_zhihu_items(items: List[schema.ZhihuItem]) -> List[schema.ZhihuItem]:
    """Compute scores for Zhihu items.

    Uses same weight structure as Reddit/X (relevance + recency + engagement).
    """
    if not items:
        return items

    eng_raw = [compute_zhihu_engagement_raw(item.engagement) for item in items]
    eng_normalized = normalize_to_100(eng_raw)

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        if eng_normalized[i] is not None:
            eng_score = int(eng_normalized[i])
        else:
            eng_score = DEFAULT_ENGAGEMENT

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score +
            WEIGHT_ENGAGEMENT * eng_score
        )

        if eng_raw[i] is None:
            overall -= UNKNOWN_ENGAGEMENT_PENALTY

        # Zhihu dates are often less precise
        if item.date_confidence == "low":
            overall -= 5
        elif item.date_confidence == "med":
            overall -= 2

        item.score = max(0, min(100, int(overall)))

    return items


def score_weibo_items(items: List[schema.WeiboItem]) -> List[schema.WeiboItem]:
    """Compute scores for Weibo items.

    Uses same engagement formula as X (likes + reposts + comments).
    """
    if not items:
        return items

    eng_raw = [compute_x_engagement_raw(item.engagement) for item in items]
    eng_normalized = normalize_to_100(eng_raw)

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        if eng_normalized[i] is not None:
            eng_score = int(eng_normalized[i])
        else:
            eng_score = DEFAULT_ENGAGEMENT

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score +
            WEIGHT_ENGAGEMENT * eng_score
        )

        if eng_raw[i] is None:
            overall -= UNKNOWN_ENGAGEMENT_PENALTY

        # Weibo dates from public interface are less precise
        if item.date_confidence == "low":
            overall -= 5
        elif item.date_confidence == "med":
            overall -= 2

        item.score = max(0, min(100, int(overall)))

    return items


def score_douyin_items(items: List[schema.DouyinItem]) -> List[schema.DouyinItem]:
    """Compute scores for Douyin items.

    Uses same engagement formula as TikTok (views + likes + comments + shares).
    """
    if not items:
        return items

    eng_raw = [compute_tiktok_engagement_raw(item.engagement) for item in items]
    eng_normalized = normalize_to_100(eng_raw)

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        if eng_normalized[i] is not None:
            eng_score = int(eng_normalized[i])
        else:
            eng_score = DEFAULT_ENGAGEMENT

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )

        overall = (
            WEIGHT_RELEVANCE * rel_score +
            WEIGHT_RECENCY * rec_score +
            WEIGHT_ENGAGEMENT * eng_score
        )

        if eng_raw[i] is None:
            overall -= UNKNOWN_ENGAGEMENT_PENALTY

        # Douyin dates are often less precise
        if item.date_confidence == "low":
            overall -= 5
        elif item.date_confidence == "med":
            overall -= 2

        item.score = max(0, min(100, int(overall)))

    return items


def score_baidu_items(items: List[schema.BaiduItem]) -> List[schema.BaiduItem]:
    """Compute scores for Baidu search items.

    Uses websearch-like weights (relevance + recency, no engagement data).
    """
    if not items:
        return items

    for item in items:
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=0,
        )

        overall = (
            WEBSEARCH_WEIGHT_RELEVANCE * rel_score +
            WEBSEARCH_WEIGHT_RECENCY * rec_score
        )

        # Apply source penalty
        overall -= WEBSEARCH_SOURCE_PENALTY

        # Apply date confidence adjustments
        if item.date_confidence == "high":
            overall += WEBSEARCH_VERIFIED_BONUS
        elif item.date_confidence == "low":
            overall -= WEBSEARCH_NO_DATE_PENALTY

        item.score = max(0, min(100, int(overall)))

    return items


def score_websearch_items(items: List[schema.WebSearchItem]) -> List[schema.WebSearchItem]:
    """Compute scores for WebSearch items WITHOUT engagement metrics.

    Uses reweighted formula: 55% relevance + 45% recency - 15pt source penalty.
    This ensures WebSearch items rank below comparable Reddit/X items.

    Date confidence adjustments:
    - High confidence (URL-verified date): +10 bonus
    - Med confidence (snippet-extracted date): no change
    - Low confidence (no date signals): -20 penalty

    Args:
        items: List of WebSearch items

    Returns:
        Items with updated scores
    """
    if not items:
        return items

    for item in items:
        # Relevance subscore (model-provided, convert to 0-100)
        rel_score = int(item.relevance * 100)

        # Recency subscore
        rec_score = dates.recency_score(item.date)

        # Store subscores (engagement is 0 for WebSearch - no data)
        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=0,  # Explicitly zero - no engagement data available
        )

        # Compute overall score using WebSearch weights
        overall = (
            WEBSEARCH_WEIGHT_RELEVANCE * rel_score +
            WEBSEARCH_WEIGHT_RECENCY * rec_score
        )

        # Apply source penalty (WebSearch < Reddit/X for same relevance/recency)
        overall -= WEBSEARCH_SOURCE_PENALTY

        # Apply date confidence adjustments
        # High confidence (URL-verified): reward with bonus
        # Med confidence (snippet-extracted): neutral
        # Low confidence (no date signals): heavy penalty
        if item.date_confidence == "high":
            overall += WEBSEARCH_VERIFIED_BONUS  # Reward verified recent dates
        elif item.date_confidence == "low":
            overall -= WEBSEARCH_NO_DATE_PENALTY  # Heavy penalty for unknown

        item.score = max(0, min(100, int(overall)))

    return items


def sort_items(items: List[Union[schema.RedditItem, schema.XItem, schema.WebSearchItem, schema.YouTubeItem, schema.HackerNewsItem, schema.PolymarketItem, schema.ArxivItem, schema.PatentItem, schema.BookItem, schema.TikTokItem, schema.InstagramItem, schema.BlueskyItem, schema.TruthSocialItem, schema.BilibiliItem, schema.ZhihuItem, schema.WeiboItem, schema.DouyinItem, schema.BaiduItem]]) -> List:
    """Sort items by score (descending), then date, then source priority.

    Args:
        items: List of items to sort

    Returns:
        Sorted items
    """
    def sort_key(item):
        # Primary: score descending (negate for descending)
        score = -item.score

        # Secondary: date descending (recent first)
        date = item.date or "0000-00-00"
        # Sanitize date: remove non-digit characters before parsing
        clean_date = re.sub(r"[^\d]", "", date[:10])
        if clean_date and len(clean_date) >= 8:
            date_key = -int(clean_date)
        else:
            date_key = 0

        # Tertiary: source priority
        if isinstance(item, schema.RedditItem):
            source_priority = 0
        elif isinstance(item, schema.XItem):
            source_priority = 1
        elif isinstance(item, schema.YouTubeItem):
            source_priority = 2
        elif isinstance(item, schema.HackerNewsItem):
            source_priority = 3
        elif isinstance(item, schema.PolymarketItem):
            source_priority = 4
        elif isinstance(item, schema.ArxivItem):
            source_priority = 5
        elif isinstance(item, schema.PatentItem):
            source_priority = 6
        elif isinstance(item, schema.BookItem):
            source_priority = 7
        elif isinstance(item, schema.TikTokItem):
            source_priority = 8
        elif isinstance(item, schema.InstagramItem):
            source_priority = 9
        elif isinstance(item, schema.BlueskyItem):
            source_priority = 10
        elif isinstance(item, schema.TruthSocialItem):
            source_priority = 11
        elif isinstance(item, schema.BilibiliItem):
            source_priority = 12
        elif isinstance(item, schema.ZhihuItem):
            source_priority = 13
        elif isinstance(item, schema.WeiboItem):
            source_priority = 14
        elif isinstance(item, schema.DouyinItem):
            source_priority = 15
        else:  # BaiduItem or WebSearchItem
            source_priority = 16

        # Quaternary: title/text for stability
        text = getattr(item, "title", "") or getattr(item, "text", "")

        return (score, date_key, source_priority, text)

    return sorted(items, key=sort_key)
