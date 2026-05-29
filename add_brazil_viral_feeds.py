#!/usr/bin/env python3
"""
Add Brazil-focused viral feeds + trends for content creation.
Focus on trending topics that can be angled to business/ads context.
Run once: python add_brazil_viral_feeds.py
"""

import sys
from pathlib import Path

_here = Path(__file__).parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

import db

# Brazil trending + viral feeds - curated for angle-ability to business/ads
BRAZIL_VIRAL_FEEDS = [
    # BREAKING NEWS + TRENDS BR
    ("G1 - Portal de Noticias", "https://g1.globo.com/feed.rss"),
    ("Folha de S.Paulo", "https://feeds.folha.uol.com.br/folha/rss052.xml"),
    ("UOL Noticias", "https://noticias.uol.com.br/feed/"),
    ("O Globo", "https://oglobo.globo.com/feed.rss"),
    ("Estadao", "https://www.estadao.com.br/feed/"),

    # ECONOMIA + NEGÓCIOS BR (facil de ângular)
    ("Exame Negocios", "https://exame.com/feed/"),
    ("InfoMoney", "https://www.infomoney.com.br/feed/"),
    ("Valor Economico", "https://www.valor.com.br/feed/"),
    ("Pequenas Empresas", "https://revistapegn.globo.com/feed.rss"),

    # TECH + INNOVATION (trends de tecnologia no BR)
    ("TechTudo", "https://techtudo.com.br/feed.rss"),
    ("Gizmodo Brasil", "https://gizmodo.uol.com.br/feed/"),
    ("Tecnoblog", "https://www.tecnoblog.net/feed/"),

    # INTERNET CULTURA + TRENDS (o que ta viral)
    ("BuzzFeed Brasil", "https://buzzfeed.com/br/feed.xml"),
    ("Huffpost Brasil", "https://www.huffpostbrasil.com/feed.xml"),
    ("Vice Brasil", "https://www.vice.com/pt_br/rss.xml"),

    # LIFESTYLE + COMPORTAMENTO (geração Z, tendências)
    ("Revista Quem", "https://www.quem.com.br/feed/"),
    ("Revista Glamour BR", "https://glamour.globo.com/feed.rss"),
    ("Revista Vogue Brasil", "https://vogue.globo.com/feed.rss"),

    # SOCIAL MEDIA + INFLUENCERS (o que influenciadores estão falando)
    ("Social Media Trends BR", "https://www.socialbakers.com/blog/feed/"),

    # EMPREENDEDORISMO + STARTUPS (como vender, como crescer)
    ("StartupBase", "https://www.startupbase.com.br/feed/"),
    ("Endeavor Brasil", "https://www.endeavor.org.br/feed/"),
    ("Sebrae Blog", "https://blog.sebrae.com.br/feed/"),

    # SAÚDE + BELEZA (clinicas, saloes, consultórios)
    ("Saude Info", "https://saude.ig.com.br/feed/"),
    ("Beleza da Bem", "https://www.beleza.ig.com.br/feed/"),

    # EDUCAÇÃO + CURSOS (negócio digital em alta)
    ("Edtech Brasil", "https://edtechbrasil.com/feed/"),

    # ENTERTAINMENT + HUMOR (o que vai viralizar)
    ("Catraca Livre", "https://catracalivre.com.br/feed/"),
    ("Hypeness", "https://www.hypeness.com.br/feed/"),
]

def add_feeds():
    """Add all Brazil viral feeds to database."""
    db.init_db()

    print("=" * 70)
    print("ADICIONANDO FEEDS VIRAIS + TRENDS DO BRASIL")
    print("=" * 70)

    added = 0
    skipped = 0

    for name, url in BRAZIL_VIRAL_FEEDS:
        try:
            db.add_feed(url, name)
            print(f"✓ {name}")
            added += 1
        except ValueError as e:
            print(f"⊘ {name} (já existe)")
            skipped += 1
        except Exception as e:
            print(f"✗ {name} (erro)")

    print("=" * 70)
    print(f"✓ {added} feeds adicionados com sucesso!")
    print(f"⊘ {skipped} feeds já existentes")
    print("=" * 70)
    print("\n✓ PRONTO! Você tem acesso a:")
    print("  • Trending topics BR (o que tá VIRAL AGORA)")
    print("  • Notícias que podem ser ânguled para negócios")
    print("  • Economia, tech, lifestyle, influencers")
    print("  • Tudo que funciona para VIRALIZAR no BR!")
    print("\n💡 Dica: Qualquer tema pode ser relacionado a anúncios/negócios")
    print("   Se é viral → Você consegue ângular para sua audiência!")

if __name__ == "__main__":
    add_feeds()
