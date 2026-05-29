#!/usr/bin/env python3
"""
Disable irrelevant English/US feeds and keep only Brazilian + marketing ones.
Run once: python fix_feeds.py
"""

import sys
from pathlib import Path

_here = Path(__file__).parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

import db

# Feeds irrelevantes para o mercado BR - desativar
IRRELEVANT_KEYWORDS = [
    "adweek", "adage", "marketing land", "marketingland",
    "facebook business news", "meta business blog",
    "instagram marketing blog", "youtube creator",
    "tiktok creator fund", "dental business",
    "retail analytics", "food business news",
    "conversion rate experts", "crazyegg",
    "moz blog", "ahrefs", "semrush",
]

def fix_feeds():
    db.init_db()
    all_feeds = db.get_feeds(active_only=False)

    print("=" * 60)
    print("AJUSTANDO FEEDS - DESATIVANDO IRRELEVANTES")
    print("=" * 60)

    disabled = 0
    kept = 0

    for feed in all_feeds:
        name_lower = feed["name"].lower()
        url_lower = feed["url"].lower()

        should_disable = any(
            kw in name_lower or kw in url_lower
            for kw in IRRELEVANT_KEYWORDS
        )

        if should_disable and feed["active"]:
            db.toggle_feed(feed["id"], False)
            print(f"✗ DESATIVADO: {feed['name']}")
            disabled += 1
        elif feed["active"]:
            print(f"✓ MANTIDO:    {feed['name']}")
            kept += 1

    print("=" * 60)
    print(f"✗ {disabled} feeds desativadas")
    print(f"✓ {kept} feeds ativas")
    print("=" * 60)
    print("\nAgora rode: python main.py run")

if __name__ == "__main__":
    fix_feeds()
