"""
Database layer — SQLite3 operations for feeds, articles, and performance tracking.
"""

import os
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = Path(os.environ.get("DATABASE_PATH", str(Path(__file__).parent / "data.db")))

# Feeds iniciais (do main.py original)
INITIAL_FEEDS = [
    ("https://news.google.com/rss/search?q=meta+ads+facebook+ads+atualiza%C3%A7%C3%A3o&hl=pt-BR&gl=BR&ceid=BR:pt-419", "Meta Ads / Facebook Ads"),
    ("https://news.google.com/rss/search?q=google+ads+atualiza%C3%A7%C3%A3o+2025&hl=pt-BR&gl=BR&ceid=BR:pt-419", "Google Ads"),
    ("https://news.google.com/rss/search?q=tr%C3%A1fego+pago+performance+marketing&hl=pt-BR&gl=BR&ceid=BR:pt-419", "Trafego Pago e Performance"),
    ("https://news.google.com/rss/search?q=marketing+digital+convers%C3%A3o+leads+brasil&hl=pt-BR&gl=BR&ceid=BR:pt-419", "Marketing Digital e Conversao"),
    ("https://news.google.com/rss/search?q=comportamento+consumidor+digital+compra+online&hl=pt-BR&gl=BR&ceid=BR:pt-419", "Comportamento do Consumidor Online"),
    ("https://news.google.com/rss/search?q=intelig%C3%AAncia+artificial+anuncios+marketing+2025&hl=pt-BR&gl=BR&ceid=BR:pt-419", "Inteligencia Artificial e Anuncios"),
]


def get_connection():
    """Get SQLite connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database schema and seed initial feeds."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_date TEXT NOT NULL,
            title TEXT NOT NULL,
            source TEXT,
            link TEXT,
            summary TEXT,
            content_json TEXT,
            gancho_tema TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id INTEGER REFERENCES articles(id),
            platform TEXT,
            roteiro TEXT,
            views INTEGER,
            saves INTEGER,
            likes INTEGER,
            comments INTEGER,
            posted_at TEXT,
            logged_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Seed initial feeds (only if table is empty)
    cursor.execute("SELECT COUNT(*) as count FROM feeds")
    if cursor.fetchone()["count"] == 0:
        for url, name in INITIAL_FEEDS:
            try:
                cursor.execute("INSERT INTO feeds (url, name, active) VALUES (?, ?, 1)", (url, name))
            except sqlite3.IntegrityError:
                pass

    conn.commit()
    conn.close()


def get_feeds(active_only: bool = True) -> list[dict]:
    """Get all feeds or only active ones."""
    conn = get_connection()
    cursor = conn.cursor()

    if active_only:
        cursor.execute("SELECT id, url, name, active FROM feeds WHERE active = 1 ORDER BY name")
    else:
        cursor.execute("SELECT id, url, name, active FROM feeds ORDER BY name")

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_feed(url: str, name: str) -> int:
    """Add a new feed, return its ID."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO feeds (url, name, active) VALUES (?, ?, 1)", (url, name))
        conn.commit()
        feed_id = cursor.lastrowid
        conn.close()
        return feed_id
    except sqlite3.IntegrityError:
        conn.close()
        raise ValueError(f"Feed with URL '{url}' already exists")


def toggle_feed(feed_id: int, active: bool) -> None:
    """Enable or disable a feed."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE feeds SET active = ? WHERE id = ?", (1 if active else 0, feed_id))
    conn.commit()
    conn.close()


def save_article(run_date: str, article: dict, content_json: dict) -> int:
    """Save an article and its generated content, return article ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO articles (run_date, title, source, link, summary, content_json, gancho_tema)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        run_date,
        article["title"],
        article.get("source", ""),
        article.get("link", ""),
        article.get("summary", ""),
        json.dumps(content_json, ensure_ascii=False),
        content_json.get("gancho_tema", ""),
    ))

    conn.commit()
    article_id = cursor.lastrowid
    conn.close()
    return article_id


def get_history(limit: int = 10) -> list[dict]:
    """Get last N unique run dates with article counts and titles."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT run_date, COUNT(*) as count
        FROM articles
        GROUP BY run_date
        ORDER BY run_date DESC
        LIMIT ?
    """, (limit,))

    runs = cursor.fetchall()
    result = []

    for run in runs:
        cursor.execute("""
            SELECT id, title, gancho_tema
            FROM articles
            WHERE run_date = ?
            ORDER BY id DESC
        """, (run["run_date"],))

        articles = [dict(row) for row in cursor.fetchall()]
        result.append({
            "run_date": run["run_date"],
            "count": run["count"],
            "articles": articles,
        })

    conn.close()
    return result


def get_article(article_id: int) -> Optional[dict]:
    """Get complete article data including generated content."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, run_date, title, source, link, summary, content_json, gancho_tema, created_at
        FROM articles
        WHERE id = ?
    """, (article_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    article = dict(row)
    if article["content_json"]:
        article["content"] = json.loads(article["content_json"])
    return article


def log_performance(
    article_id: int,
    platform: str,
    roteiro: str,
    views: int,
    saves: int,
    likes: int,
    comments: int,
    posted_at: str,
) -> int:
    """Log performance metrics for a post, return performance record ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO performance (article_id, platform, roteiro, views, saves, likes, comments, posted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (article_id, platform, roteiro, views, saves, likes, comments, posted_at))

    conn.commit()
    perf_id = cursor.lastrowid
    conn.close()
    return perf_id


def get_stats() -> dict:
    """Get aggregated performance stats by roteiro type, format, and theme."""
    conn = get_connection()
    cursor = conn.cursor()

    # Stats by roteiro type (from content_json)
    cursor.execute("""
        SELECT
            json_extract(content_json, '$.roteiro_1.tipo') as tipo,
            COUNT(*) as count,
            AVG(COALESCE(p.views, 0)) as avg_views,
            AVG(COALESCE(p.saves, 0)) as avg_saves,
            AVG(COALESCE(p.likes, 0)) as avg_likes,
            AVG(COALESCE(p.comments, 0)) as avg_comments
        FROM articles a
        LEFT JOIN performance p ON a.id = p.article_id AND p.roteiro = 'A'
        WHERE json_extract(content_json, '$.roteiro_1.tipo') IS NOT NULL
        GROUP BY tipo
        ORDER BY avg_saves DESC
    """)

    by_roteiro = [dict(row) for row in cursor.fetchall()]

    # Stats by format (carrossel vs reels)
    cursor.execute("""
        SELECT
            'carrossel' as format,
            COUNT(*) as count,
            AVG(COALESCE(p.views, 0)) as avg_views,
            AVG(COALESCE(p.saves, 0)) as avg_saves,
            AVG(COALESCE(p.likes, 0)) as avg_likes,
            AVG(COALESCE(p.comments, 0)) as avg_comments
        FROM articles a
        LEFT JOIN performance p ON a.id = p.article_id AND p.roteiro = 'carrossel'
        WHERE json_extract(content_json, '$.carrossel.titulo_capa') IS NOT NULL
    """)

    by_format = [dict(row) for row in cursor.fetchall()]

    # Top themes by saves
    cursor.execute("""
        SELECT
            gancho_tema,
            COUNT(*) as count,
            AVG(COALESCE(p.views, 0)) as avg_views,
            AVG(COALESCE(p.saves, 0)) as avg_saves,
            ROUND(AVG(COALESCE(p.saves, 0)) * 1.0 / NULLIF(AVG(COALESCE(p.views, 0)), 0), 2) as save_rate
        FROM articles a
        LEFT JOIN performance p ON a.id = p.article_id
        WHERE gancho_tema IS NOT NULL AND gancho_tema != ''
        GROUP BY gancho_tema
        ORDER BY avg_saves DESC
        LIMIT 5
    """)

    top_themes = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "by_roteiro": by_roteiro,
        "by_format": by_format,
        "top_themes": top_themes,
    }
