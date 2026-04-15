"""Data schemas for last30days skill."""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


@dataclass
class Engagement:
    """Engagement metrics."""
    # Reddit fields
    score: Optional[int] = None
    num_comments: Optional[int] = None
    upvote_ratio: Optional[float] = None

    # X fields
    likes: Optional[int] = None
    reposts: Optional[int] = None
    replies: Optional[int] = None
    quotes: Optional[int] = None

    # YouTube fields
    views: Optional[int] = None

    # Polymarket fields
    volume: Optional[float] = None
    liquidity: Optional[float] = None

    # TikTok/Instagram fields
    shares: Optional[int] = None

    # Bilibili fields
    danmaku: Optional[int] = None
    favorites: Optional[int] = None

    # Zhihu fields
    voteups: Optional[int] = None
    thanks: Optional[int] = None
    collects: Optional[int] = None

    # Douyin fields
    collects: Optional[int] = None

    # Hot search fields
    hot_score: Optional[float] = None
    answers: Optional[int] = None
    followers: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {}
        if self.score is not None:
            d['score'] = self.score
        if self.num_comments is not None:
            d['num_comments'] = self.num_comments
        if self.upvote_ratio is not None:
            d['upvote_ratio'] = self.upvote_ratio
        if self.likes is not None:
            d['likes'] = self.likes
        if self.reposts is not None:
            d['reposts'] = self.reposts
        if self.replies is not None:
            d['replies'] = self.replies
        if self.quotes is not None:
            d['quotes'] = self.quotes
        if self.views is not None:
            d['views'] = self.views
        if self.volume is not None:
            d['volume'] = self.volume
        if self.liquidity is not None:
            d['liquidity'] = self.liquidity
        if self.shares is not None:
            d['shares'] = self.shares
        if self.danmaku is not None:
            d['danmaku'] = self.danmaku
        if self.favorites is not None:
            d['favorites'] = self.favorites
        if self.voteups is not None:
            d['voteups'] = self.voteups
        if self.thanks is not None:
            d['thanks'] = self.thanks
        if self.collects is not None:
            d['collects'] = self.collects
        if self.hot_score is not None:
            d['hot_score'] = self.hot_score
        if self.answers is not None:
            d['answers'] = self.answers
        if self.followers is not None:
            d['followers'] = self.followers
        return d if d else None


@dataclass
class Comment:
    """Reddit comment."""
    score: int
    date: Optional[str]
    author: str
    excerpt: str
    url: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            'score': self.score,
            'date': self.date,
            'author': self.author,
            'excerpt': self.excerpt,
            'url': self.url,
        }


@dataclass
class SubScores:
    """Component scores."""
    relevance: int = 0
    recency: int = 0
    engagement: int = 0

    def to_dict(self) -> Dict[str, int]:
        return {
            'relevance': self.relevance,
            'recency': self.recency,
            'engagement': self.engagement,
        }


@dataclass
class RedditItem:
    """Normalized Reddit item."""
    id: str
    title: str
    url: str
    subreddit: str
    date: Optional[str] = None
    date_confidence: str = "low"
    engagement: Optional[Engagement] = None
    top_comments: List[Comment] = field(default_factory=list)
    comment_insights: List[str] = field(default_factory=list)
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'subreddit': self.subreddit,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'top_comments': [c.to_dict() for c in self.top_comments],
            'comment_insights': self.comment_insights,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class XItem:
    """Normalized X item."""
    id: str
    text: str
    url: str
    author_handle: str
    date: Optional[str] = None
    date_confidence: str = "low"
    engagement: Optional[Engagement] = None
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'text': self.text,
            'url': self.url,
            'author_handle': self.author_handle,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class WebSearchItem:
    """Normalized web search item (no engagement metrics)."""
    id: str
    title: str
    url: str
    source_domain: str  # e.g., "medium.com", "github.com"
    snippet: str
    date: Optional[str] = None
    date_confidence: str = "low"
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'source_domain': self.source_domain,
            'snippet': self.snippet,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class YouTubeItem:
    """Normalized YouTube item."""
    id: str  # video_id
    title: str
    url: str
    channel_name: str
    date: Optional[str] = None
    date_confidence: str = "high"  # YouTube dates are always reliable
    engagement: Optional[Engagement] = None
    transcript_snippet: str = ""
    relevance: float = 0.7
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'channel_name': self.channel_name,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'transcript_snippet': self.transcript_snippet,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class HackerNewsItem:
    """Normalized Hacker News item."""
    id: str           # "HN1", "HN2", ...
    title: str
    url: str          # Original article URL
    hn_url: str       # news.ycombinator.com/item?id=...
    author: str       # HN username
    date: Optional[str] = None
    date_confidence: str = "high"  # Algolia provides exact timestamps
    engagement: Optional[Engagement] = None  # points + num_comments
    top_comments: List[Comment] = field(default_factory=list)
    comment_insights: List[str] = field(default_factory=list)
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'hn_url': self.hn_url,
            'author': self.author,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'top_comments': [c.to_dict() for c in self.top_comments],
            'comment_insights': self.comment_insights,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class PolymarketItem:
    """Normalized Polymarket prediction market item."""
    id: str           # "PM1", "PM2", ...
    title: str        # Event title
    question: str     # Top market question
    url: str          # Event page URL
    outcome_prices: List[tuple] = field(default_factory=list)  # [(name, price), ...]
    outcomes_remaining: int = 0
    price_movement: Optional[str] = None  # "down 11.7% this month"
    date: Optional[str] = None
    date_confidence: str = "high"  # API provides exact timestamps
    engagement: Optional[Engagement] = None  # volume + liquidity
    end_date: Optional[str] = None
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'title': self.title,
            'question': self.question,
            'url': self.url,
            'outcome_prices': self.outcome_prices,
            'outcomes_remaining': self.outcomes_remaining,
            'price_movement': self.price_movement,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'end_date': self.end_date,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class ArxivItem:
    """Normalized arXiv paper item."""
    id: str           # "AR1", "AR2", ...
    title: str
    url: str          # arxiv.org/abs/...
    pdf_url: str
    authors: List[str] = field(default_factory=list)
    date: Optional[str] = None
    date_confidence: str = "high"
    summary: str = ""
    categories: List[str] = field(default_factory=list)
    engagement: Optional[Engagement] = None  # citations if available
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'pdf_url': self.pdf_url,
            'authors': self.authors,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'summary': self.summary,
            'categories': self.categories,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class PatentItem:
    """Normalized patent item."""
    id: str           # "PAT1", "PAT2", ...
    title: str
    url: str
    patent_number: str = ""
    assignee: str = ""
    date: Optional[str] = None
    date_confidence: str = "high"
    abstract: str = ""
    cpc_codes: List[str] = field(default_factory=list)
    engagement: Optional[Engagement] = None
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'patent_number': self.patent_number,
            'assignee': self.assignee,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'abstract': self.abstract,
            'cpc_codes': self.cpc_codes,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class BookItem:
    """Normalized book item."""
    id: str           # "BK1", "BK2", ...
    title: str
    url: str
    authors: List[str] = field(default_factory=list)
    publisher: str = ""
    date: Optional[str] = None
    date_confidence: str = "med"
    description: str = ""
    isbn: str = ""
    page_count: Optional[int] = None
    engagement: Optional[Engagement] = None
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'authors': self.authors,
            'publisher': self.publisher,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'description': self.description,
            'isbn': self.isbn,
            'page_count': self.page_count,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class TikTokItem:
    """Normalized TikTok item."""
    id: str
    caption: str
    url: str
    author_handle: str
    date: Optional[str] = None
    date_confidence: str = "low"
    engagement: Optional[Engagement] = None
    transcript_snippet: str = ""
    hashtags: List[str] = field(default_factory=list)
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'caption': self.caption,
            'url': self.url,
            'author_handle': self.author_handle,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'transcript_snippet': self.transcript_snippet,
            'hashtags': self.hashtags,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class InstagramItem:
    """Normalized Instagram item."""
    id: str
    caption: str
    url: str
    author_handle: str
    date: Optional[str] = None
    date_confidence: str = "low"
    engagement: Optional[Engagement] = None
    hashtags: List[str] = field(default_factory=list)
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'caption': self.caption,
            'url': self.url,
            'author_handle': self.author_handle,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'hashtags': self.hashtags,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class BlueskyItem:
    """Normalized Bluesky item."""
    id: str
    text: str
    url: str
    author_handle: str
    display_name: str = ""
    date: Optional[str] = None
    date_confidence: str = "low"
    engagement: Optional[Engagement] = None
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'text': self.text,
            'url': self.url,
            'author_handle': self.author_handle,
            'display_name': self.display_name,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class TruthSocialItem:
    """Normalized Truth Social item."""
    id: str
    text: str
    url: str
    author_handle: str
    display_name: str = ""
    date: Optional[str] = None
    date_confidence: str = "low"
    engagement: Optional[Engagement] = None
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'text': self.text,
            'url': self.url,
            'author_handle': self.author_handle,
            'display_name': self.display_name,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class BilibiliItem:
    """Normalized Bilibili item."""
    id: str  # bvid
    title: str
    url: str
    bvid: str
    channel_name: str
    date: Optional[str] = None
    date_confidence: str = "high"
    engagement: Optional[Engagement] = None
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'bvid': self.bvid,
            'channel_name': self.channel_name,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class ZhihuItem:
    """Normalized Zhihu item."""
    id: str
    title: str
    excerpt: str
    url: str
    author: str
    date: Optional[str] = None
    date_confidence: str = "med"
    engagement: Optional[Engagement] = None
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'title': self.title,
            'excerpt': self.excerpt,
            'url': self.url,
            'author': self.author,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class WeiboItem:
    """Normalized Weibo item."""
    id: str
    text: str
    url: str
    author_handle: str
    date: Optional[str] = None
    date_confidence: str = "low"
    engagement: Optional[Engagement] = None
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'text': self.text,
            'url': self.url,
            'author_handle': self.author_handle,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class DouyinItem:
    """Normalized Douyin item."""
    id: str
    text: str
    url: str
    author_handle: str
    date: Optional[str] = None
    date_confidence: str = "low"
    engagement: Optional[Engagement] = None
    transcript_snippet: str = ""
    hashtags: List[str] = field(default_factory=list)
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'text': self.text,
            'url': self.url,
            'author_handle': self.author_handle,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'engagement': self.engagement.to_dict() if self.engagement else None,
            'transcript_snippet': self.transcript_snippet,
            'hashtags': self.hashtags,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class BaiduItem:
    """Normalized Baidu search item."""
    id: str
    title: str
    url: str
    source_domain: str
    snippet: str
    date: Optional[str] = None
    date_confidence: str = "low"
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0
    cross_refs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'source_domain': self.source_domain,
            'snippet': self.snippet,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
        if self.cross_refs:
            d['cross_refs'] = self.cross_refs
        return d


@dataclass
class Report:
    """Full research report."""
    topic: str
    range_from: str
    range_to: str
    generated_at: str
    mode: str  # 'reddit-only', 'x-only', 'both', 'web-only', etc.
    openai_model_used: Optional[str] = None
    xai_model_used: Optional[str] = None
    reddit: List[RedditItem] = field(default_factory=list)
    x: List[XItem] = field(default_factory=list)
    web: List[WebSearchItem] = field(default_factory=list)
    youtube: List[YouTubeItem] = field(default_factory=list)
    hackernews: List[HackerNewsItem] = field(default_factory=list)
    polymarket: List[PolymarketItem] = field(default_factory=list)
    arxiv: List[ArxivItem] = field(default_factory=list)
    patents: List[PatentItem] = field(default_factory=list)
    books: List[BookItem] = field(default_factory=list)
    # New v2.9.6+ sources
    tiktok: List[TikTokItem] = field(default_factory=list)
    instagram: List[InstagramItem] = field(default_factory=list)
    bluesky: List[BlueskyItem] = field(default_factory=list)
    truthsocial: List[TruthSocialItem] = field(default_factory=list)
    # New v2.9.8+ Chinese platforms
    bilibili: List[BilibiliItem] = field(default_factory=list)
    zhihu: List[ZhihuItem] = field(default_factory=list)
    weibo: List[WeiboItem] = field(default_factory=list)
    douyin: List[DouyinItem] = field(default_factory=list)
    baidu: List[BaiduItem] = field(default_factory=list)
    best_practices: List[str] = field(default_factory=list)
    prompt_pack: List[str] = field(default_factory=list)
    context_snippet_md: str = ""
    # Status tracking
    reddit_error: Optional[str] = None
    x_error: Optional[str] = None
    web_error: Optional[str] = None
    youtube_error: Optional[str] = None
    hackernews_error: Optional[str] = None
    polymarket_error: Optional[str] = None
    arxiv_error: Optional[str] = None
    patents_error: Optional[str] = None
    books_error: Optional[str] = None
    tiktok_error: Optional[str] = None
    instagram_error: Optional[str] = None
    bluesky_error: Optional[str] = None
    truthsocial_error: Optional[str] = None
    bilibili_error: Optional[str] = None
    zhihu_error: Optional[str] = None
    weibo_error: Optional[str] = None
    douyin_error: Optional[str] = None
    baidu_error: Optional[str] = None
    # Handle resolution
    resolved_x_handle: Optional[str] = None
    # Cache info
    from_cache: bool = False
    cache_age_hours: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {
            'topic': self.topic,
            'range': {
                'from': self.range_from,
                'to': self.range_to,
            },
            'generated_at': self.generated_at,
            'mode': self.mode,
            'openai_model_used': self.openai_model_used,
            'xai_model_used': self.xai_model_used,
            'reddit': [r.to_dict() for r in self.reddit],
            'x': [x.to_dict() for x in self.x],
            'web': [w.to_dict() for w in self.web],
            'youtube': [y.to_dict() for y in self.youtube],
            'hackernews': [h.to_dict() for h in self.hackernews],
            'polymarket': [p.to_dict() for p in self.polymarket],
            'arxiv': [a.to_dict() for a in self.arxiv],
            'patents': [p.to_dict() for p in self.patents],
            'books': [b.to_dict() for b in self.books],
            'tiktok': [t.to_dict() for t in self.tiktok],
            'instagram': [i.to_dict() for i in self.instagram],
            'bluesky': [b.to_dict() for b in self.bluesky],
            'truthsocial': [t.to_dict() for t in self.truthsocial],
            'bilibili': [b.to_dict() for b in self.bilibili],
            'zhihu': [z.to_dict() for z in self.zhihu],
            'weibo': [w.to_dict() for w in self.weibo],
            'douyin': [d.to_dict() for d in self.douyin],
            'baidu': [b.to_dict() for b in self.baidu],
            'best_practices': self.best_practices,
            'prompt_pack': self.prompt_pack,
            'context_snippet_md': self.context_snippet_md,
        }
        if self.resolved_x_handle:
            d['resolved_x_handle'] = self.resolved_x_handle
        if self.reddit_error:
            d['reddit_error'] = self.reddit_error
        if self.x_error:
            d['x_error'] = self.x_error
        if self.web_error:
            d['web_error'] = self.web_error
        if self.youtube_error:
            d['youtube_error'] = self.youtube_error
        if self.hackernews_error:
            d['hackernews_error'] = self.hackernews_error
        if self.polymarket_error:
            d['polymarket_error'] = self.polymarket_error
        if self.arxiv_error:
            d['arxiv_error'] = self.arxiv_error
        if self.patents_error:
            d['patents_error'] = self.patents_error
        if self.books_error:
            d['books_error'] = self.books_error
        if self.tiktok_error:
            d['tiktok_error'] = self.tiktok_error
        if self.instagram_error:
            d['instagram_error'] = self.instagram_error
        if self.bluesky_error:
            d['bluesky_error'] = self.bluesky_error
        if self.truthsocial_error:
            d['truthsocial_error'] = self.truthsocial_error
        if self.bilibili_error:
            d['bilibili_error'] = self.bilibili_error
        if self.zhihu_error:
            d['zhihu_error'] = self.zhihu_error
        if self.weibo_error:
            d['weibo_error'] = self.weibo_error
        if self.douyin_error:
            d['douyin_error'] = self.douyin_error
        if self.baidu_error:
            d['baidu_error'] = self.baidu_error
        if self.from_cache:
            d['from_cache'] = self.from_cache
        if self.cache_age_hours is not None:
            d['cache_age_hours'] = self.cache_age_hours
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Report":
        """Create Report from serialized dict (handles cache format)."""
        # Handle range field conversion
        range_data = data.get('range', {})
        range_from = range_data.get('from', data.get('range_from', ''))
        range_to = range_data.get('to', data.get('range_to', ''))

        # Reconstruct Reddit items
        reddit_items = []
        for r in data.get('reddit', []):
            eng = None
            if r.get('engagement'):
                eng = Engagement(**r['engagement'])
            comments = [Comment(**c) for c in r.get('top_comments', [])]
            subs = SubScores(**r.get('subs', {})) if r.get('subs') else SubScores()
            reddit_items.append(RedditItem(
                id=r['id'],
                title=r['title'],
                url=r['url'],
                subreddit=r['subreddit'],
                date=r.get('date'),
                date_confidence=r.get('date_confidence', 'low'),
                engagement=eng,
                top_comments=comments,
                comment_insights=r.get('comment_insights', []),
                relevance=r.get('relevance', 0.5),
                why_relevant=r.get('why_relevant', ''),
                subs=subs,
                score=r.get('score', 0),
                cross_refs=r.get('cross_refs', []),
            ))

        # Reconstruct X items
        x_items = []
        for x in data.get('x', []):
            eng = None
            if x.get('engagement'):
                eng = Engagement(**x['engagement'])
            subs = SubScores(**x.get('subs', {})) if x.get('subs') else SubScores()
            x_items.append(XItem(
                id=x['id'],
                text=x['text'],
                url=x['url'],
                author_handle=x['author_handle'],
                date=x.get('date'),
                date_confidence=x.get('date_confidence', 'low'),
                engagement=eng,
                relevance=x.get('relevance', 0.5),
                why_relevant=x.get('why_relevant', ''),
                subs=subs,
                score=x.get('score', 0),
                cross_refs=x.get('cross_refs', []),
            ))

        # Reconstruct Web items
        web_items = []
        for w in data.get('web', []):
            subs = SubScores(**w.get('subs', {})) if w.get('subs') else SubScores()
            web_items.append(WebSearchItem(
                id=w['id'],
                title=w['title'],
                url=w['url'],
                source_domain=w.get('source_domain', ''),
                snippet=w.get('snippet', ''),
                date=w.get('date'),
                date_confidence=w.get('date_confidence', 'low'),
                relevance=w.get('relevance', 0.5),
                why_relevant=w.get('why_relevant', ''),
                subs=subs,
                score=w.get('score', 0),
                cross_refs=w.get('cross_refs', []),
            ))

        # Reconstruct YouTube items
        youtube_items = []
        for y in data.get('youtube', []):
            eng = None
            if y.get('engagement'):
                eng = Engagement(**y['engagement'])
            subs = SubScores(**y.get('subs', {})) if y.get('subs') else SubScores()
            youtube_items.append(YouTubeItem(
                id=y['id'],
                title=y['title'],
                url=y['url'],
                channel_name=y.get('channel_name', ''),
                date=y.get('date'),
                date_confidence=y.get('date_confidence', 'high'),
                engagement=eng,
                transcript_snippet=y.get('transcript_snippet', ''),
                relevance=y.get('relevance', 0.7),
                why_relevant=y.get('why_relevant', ''),
                subs=subs,
                score=y.get('score', 0),
                cross_refs=y.get('cross_refs', []),
            ))

        # Reconstruct HackerNews items
        hn_items = []
        for h in data.get('hackernews', []):
            eng = None
            if h.get('engagement'):
                eng = Engagement(**h['engagement'])
            comments = [Comment(**c) for c in h.get('top_comments', [])]
            subs = SubScores(**h.get('subs', {})) if h.get('subs') else SubScores()
            hn_items.append(HackerNewsItem(
                id=h['id'],
                title=h['title'],
                url=h.get('url', ''),
                hn_url=h.get('hn_url', ''),
                author=h.get('author', ''),
                date=h.get('date'),
                date_confidence=h.get('date_confidence', 'high'),
                engagement=eng,
                top_comments=comments,
                comment_insights=h.get('comment_insights', []),
                relevance=h.get('relevance', 0.5),
                why_relevant=h.get('why_relevant', ''),
                subs=subs,
                score=h.get('score', 0),
                cross_refs=h.get('cross_refs', []),
            ))

        # Reconstruct Polymarket items (backward compat: key may not exist)
        pm_items = []
        for p in data.get('polymarket', []):
            eng = None
            if p.get('engagement'):
                eng = Engagement(**p['engagement'])
            subs = SubScores(**p.get('subs', {})) if p.get('subs') else SubScores()
            pm_items.append(PolymarketItem(
                id=p['id'],
                title=p['title'],
                question=p.get('question', ''),
                url=p['url'],
                outcome_prices=p.get('outcome_prices', []),
                outcomes_remaining=p.get('outcomes_remaining', 0),
                price_movement=p.get('price_movement'),
                date=p.get('date'),
                date_confidence=p.get('date_confidence', 'high'),
                engagement=eng,
                end_date=p.get('end_date'),
                relevance=p.get('relevance', 0.5),
                why_relevant=p.get('why_relevant', ''),
                subs=subs,
                score=p.get('score', 0),
                cross_refs=p.get('cross_refs', []),
            ))

        # Reconstruct arXiv items
        arxiv_items = []
        for a in data.get('arxiv', []):
            subs = SubScores(**a.get('subs', {})) if a.get('subs') else SubScores()
            arxiv_items.append(ArxivItem(
                id=a['id'],
                title=a['title'],
                url=a['url'],
                pdf_url=a.get('pdf_url', ''),
                authors=a.get('authors', []),
                date=a.get('date'),
                date_confidence=a.get('date_confidence', 'high'),
                summary=a.get('summary', ''),
                categories=a.get('categories', []),
                engagement=None,
                relevance=a.get('relevance', 0.5),
                why_relevant=a.get('why_relevant', ''),
                subs=subs,
                score=a.get('score', 0),
                cross_refs=a.get('cross_refs', []),
            ))

        # Reconstruct Patent items
        patent_items = []
        for p in data.get('patents', []):
            subs = SubScores(**p.get('subs', {})) if p.get('subs') else SubScores()
            patent_items.append(PatentItem(
                id=p['id'],
                title=p['title'],
                url=p['url'],
                patent_number=p.get('patent_number', ''),
                assignee=p.get('assignee', ''),
                date=p.get('date'),
                date_confidence=p.get('date_confidence', 'high'),
                abstract=p.get('abstract', ''),
                cpc_codes=p.get('cpc_codes', []),
                engagement=None,
                relevance=p.get('relevance', 0.5),
                why_relevant=p.get('why_relevant', ''),
                subs=subs,
                score=p.get('score', 0),
                cross_refs=p.get('cross_refs', []),
            ))

        # Reconstruct Book items
        book_items = []
        for b in data.get('books', []):
            subs = SubScores(**b.get('subs', {})) if b.get('subs') else SubScores()
            book_items.append(BookItem(
                id=b['id'],
                title=b['title'],
                url=b['url'],
                authors=b.get('authors', []),
                publisher=b.get('publisher', ''),
                date=b.get('date'),
                date_confidence=b.get('date_confidence', 'med'),
                description=b.get('description', ''),
                isbn=b.get('isbn', ''),
                page_count=b.get('page_count'),
                engagement=None,
                relevance=b.get('relevance', 0.5),
                why_relevant=b.get('why_relevant', ''),
                subs=subs,
                score=b.get('score', 0),
                cross_refs=b.get('cross_refs', []),
            ))

        return cls(
            topic=data['topic'],
            range_from=range_from,
            range_to=range_to,
            generated_at=data['generated_at'],
            mode=data['mode'],
            openai_model_used=data.get('openai_model_used'),
            xai_model_used=data.get('xai_model_used'),
            reddit=reddit_items,
            x=x_items,
            web=web_items,
            youtube=youtube_items,
            hackernews=hn_items,
            polymarket=pm_items,
            arxiv=arxiv_items,
            patents=patent_items,
            books=book_items,
            tiktok=data.get('tiktok', []),
            instagram=data.get('instagram', []),
            bluesky=data.get('bluesky', []),
            truthsocial=data.get('truthsocial', []),
            bilibili=data.get('bilibili', []),
            zhihu=data.get('zhihu', []),
            weibo=data.get('weibo', []),
            douyin=data.get('douyin', []),
            baidu=data.get('baidu', []),
            best_practices=data.get('best_practices', []),
            prompt_pack=data.get('prompt_pack', []),
            context_snippet_md=data.get('context_snippet_md', ''),
            reddit_error=data.get('reddit_error'),
            x_error=data.get('x_error'),
            web_error=data.get('web_error'),
            youtube_error=data.get('youtube_error'),
            hackernews_error=data.get('hackernews_error'),
            polymarket_error=data.get('polymarket_error'),
            arxiv_error=data.get('arxiv_error'),
            patents_error=data.get('patents_error'),
            books_error=data.get('books_error'),
            tiktok_error=data.get('tiktok_error'),
            instagram_error=data.get('instagram_error'),
            bluesky_error=data.get('bluesky_error'),
            truthsocial_error=data.get('truthsocial_error'),
            bilibili_error=data.get('bilibili_error'),
            zhihu_error=data.get('zhihu_error'),
            weibo_error=data.get('weibo_error'),
            douyin_error=data.get('douyin_error'),
            baidu_error=data.get('baidu_error'),
            resolved_x_handle=data.get('resolved_x_handle'),
            from_cache=data.get('from_cache', False),
            cache_age_hours=data.get('cache_age_hours'),
        )


def create_report(
    topic: str,
    from_date: str,
    to_date: str,
    mode: str,
    openai_model: Optional[str] = None,
    xai_model: Optional[str] = None,
) -> Report:
    """Create a new report with metadata."""
    return Report(
        topic=topic,
        range_from=from_date,
        range_to=to_date,
        generated_at=datetime.now(timezone.utc).isoformat(),
        mode=mode,
        openai_model_used=openai_model,
        xai_model_used=xai_model,
    )
