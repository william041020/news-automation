#!/usr/bin/env python3
"""
Add marketing/traffic management RSS feeds to database.
Run this once: python add_marketing_feeds.py
"""

import sys
from pathlib import Path

_here = Path(__file__).parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

import db

# High-quality feeds about paid traffic, ads, marketing + local business
MARKETING_FEEDS = [
    # Official platforms
    ("Google Ads Blog", "https://www.blog.google/products/ads/feed/"),
    ("Facebook Business News", "https://www.facebook.com/business/news/feed/"),
    ("Meta Business Blog", "https://business.facebook.com/blog/posts/"),

    # Digital Marketing
    ("Neil Patel Blog", "https://neilpatel.com/blog/feed/"),
    ("Search Engine Journal", "https://www.searchenginejournal.com/feed/"),
    ("HubSpot Marketing Blog", "https://blog.hubspot.com/marketing/feed"),
    ("Social Media Examiner", "https://www.socialmediaexaminer.com/feed/"),

    # SEO/SEM/PPC
    ("Moz Blog", "https://moz.com/blog/feed"),
    ("Ahrefs Blog", "https://ahrefs.com/blog/feed/"),
    ("SEMrush Blog", "https://www.semrush.com/blog/feed/"),

    # Copywriting & Conversion
    ("Conversion Rate Experts", "https://www.conversion-rate-experts.com/feed/"),
    ("CrazyEgg Blog", "https://www.crazyegg.com/blog/feed/"),
    ("Unbounce Blog", "https://unbounce.com/blog/feed/"),

    # Advertising & Trends
    ("AdWeek", "https://www.adweek.com/feed/"),
    ("Marketing Land", "https://marketingland.com/feed/"),
    ("eMarketer", "https://www.emarketer.com/feed"),

    # Video Marketing (TikTok/YouTube trends)
    ("YouTube Creator Blog", "https://creatoracademy.youtube.com/feed"),
    ("TikTok Creator Fund News", "https://www.tiktok.com/@tiktokbusiness/feed/"),

    # Instagram/Social
    ("Instagram Marketing Blog", "https://business.instagram.com/blog/posts/feed/"),
    ("Later Blog", "https://later.com/blog/feed/"),

    # Content Marketing
    ("Content Marketing Institute", "https://contentmarketinginstitute.com/feed/"),
    ("Copyblogger", "https://www.copyblogger.com/feed/"),

    # LOCAL BUSINESS - Noticias e dicas para pequenos negocios
    ("SEBRAE - Empreendedorismo", "https://www.sebrae.com.br/sites/PortalSebrae/feed/"),
    ("Pequenas Empresas & Grandes Negócios", "https://globoplay.globo.com/v/8526768/"),
    ("Business Insider Brasil", "https://businessinsider.com.br/feed/"),
    ("Exame - Negócios", "https://exame.com/feed/"),

    # HEALTHCARE BUSINESS (clinicas, consultórios, medicos)
    ("Consultórios Brasil", "https://www.consultoriosbrasil.com.br/feed/"),
    ("Dental Business", "https://www.dentalbusiness.com.br/feed/"),

    # RETAIL / E-COMMERCE para lojas
    ("E-Commerce Brasil", "https://www.ecommercebrasil.com.br/feed/"),
    ("Retail Analytics", "https://www.retailanalytics.com.br/feed/"),

    # RESTAURANTS / FOOD BUSINESS
    ("Food Business News", "https://www.foodbusinessnews.net/feed/"),
]

def add_feeds():
    """Add all marketing feeds to database."""
    db.init_db()

    print("=" * 60)
    print("ADICIONANDO FEEDS DE MARKETING DIGITAL")
    print("=" * 60)

    added = 0
    skipped = 0

    for name, url in MARKETING_FEEDS:
        try:
            db.add_feed(url, name)
            print(f"✓ {name}")
            added += 1
        except ValueError as e:
            print(f"⊘ {name} (já existe ou erro: {e})")
            skipped += 1
        except Exception as e:
            print(f"✗ {name} (erro: {e})")

    print("=" * 60)
    print(f"✓ {added} feeds adicionados")
    print(f"⊘ {skipped} feeds ignorados (já existem)")
    print("=" * 60)
    print("\n✓ Pronto! Suas feeds estão atualizadas com as melhores")
    print("  fontes de marketing digital, tráfego pago e copywriting viral!")

if __name__ == "__main__":
    add_feeds()
