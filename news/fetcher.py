"""
news/fetcher.py — Fetches and filters articles from RSS feeds.
"""

import feedparser
import logging
from datetime import datetime, timezone
from news.feeds import FEEDS, ALL_KEYWORDS

logger = logging.getLogger(__name__)


def _is_relevant(title: str, summary: str) -> bool:
    """Return True if the article contains at least one relevant keyword."""
    text = (title + " " + summary).lower()
    return any(kw in text for kw in ALL_KEYWORDS)


def fetch_all_articles() -> list[dict]:
    """
    Fetch fresh articles from all RSS feeds.
    Returns a list of article dicts, sorted newest first.
    """
    articles = []

    for feed_cfg in FEEDS:
        try:
            parsed = feedparser.parse(feed_cfg["url"])
            for entry in parsed.entries[:10]:   # Max 10 per feed per run
                title   = entry.get("title",   "").strip()
                summary = entry.get("summary", "").strip()
                link    = entry.get("link",    "").strip()

                if not title or not link:
                    continue

                if not _is_relevant(title, summary):
                    continue

                # Parse publish date
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    try:
                        published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                    except Exception:
                        published = datetime.now(timezone.utc)
                else:
                    published = datetime.now(timezone.utc)

                articles.append({
                    "title":     title,
                    "summary":   summary[:500],   # cap summary length
                    "link":      link,
                    "source":    feed_cfg["name"],
                    "category":  feed_cfg["category"],
                    "published": published,
                })

        except Exception as e:
            logger.warning(f"Failed to fetch feed '{feed_cfg['name']}': {e}")

    # Deduplicate by link
    seen   = set()
    unique = []
    for a in articles:
        if a["link"] not in seen:
            seen.add(a["link"])
            unique.append(a)

    # Sort newest first
    unique.sort(key=lambda x: x["published"], reverse=True)
    return unique
