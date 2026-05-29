"""
RSS feed fetching logic.
"""

import re
import feedparser
from html import unescape
from urllib.parse import quote
from typing import Optional
import db


def clean_html(text: str) -> str:
    """Remove HTML tags and unescape entities."""
    text = re.sub(r"<[^>]+>", "", text)
    return unescape(text).strip()


def fetch_articles(max_articles: int = 3, use_active_feeds: bool = True) -> list[dict]:
    """Fetch articles from configured feeds."""
    feeds = db.get_feeds(active_only=use_active_feeds)

    if not feeds:
        return []

    seen = set()
    articles = []

    for feed in feeds:
        if len(articles) >= max_articles:
            break

        try:
            parsed = feedparser.parse(feed["url"])
            for entry in parsed.entries[:4]:
                title = clean_html(entry.get("title", ""))
                if not title or title in seen:
                    continue

                seen.add(title)
                summary = clean_html(entry.get("summary", entry.get("description", "")))
                source = entry.get("source", {}).get("title", parsed.feed.get("title", "Google News"))

                articles.append({
                    "title": title,
                    "summary": summary[:600],
                    "link": entry.get("link", ""),
                    "source": source,
                })

                if len(articles) >= max_articles:
                    break

        except Exception as e:
            print(f"  Aviso: erro ao buscar feed '{feed['name']}': {e}")

    return articles[:max_articles]


def fetch_for_topic(topic: str, max_articles: int = 3, lang: str = "pt-BR") -> list[dict]:
    """Fetch articles from Google News RSS for a custom topic."""
    # Build Google News RSS URL for the topic
    url = f"https://news.google.com/rss/search?q={quote(topic)}&hl={lang}&gl=BR&ceid=BR:pt-419"

    seen = set()
    articles = []

    try:
        parsed = feedparser.parse(url)
        for entry in parsed.entries[:10]:
            title = clean_html(entry.get("title", ""))
            if not title or title in seen:
                continue

            seen.add(title)
            summary = clean_html(entry.get("summary", entry.get("description", "")))
            source = entry.get("source", {}).get("title", parsed.feed.get("title", "Google News"))

            articles.append({
                "title": title,
                "summary": summary[:600],
                "link": entry.get("link", ""),
                "source": source,
            })

            if len(articles) >= max_articles:
                break

    except Exception as e:
        print(f"  Erro ao buscar topico '{topic}': {e}")

    return articles
