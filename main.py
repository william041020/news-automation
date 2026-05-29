#!/usr/bin/env python3
"""
Automacao de Conteudo — Gestor de Trafego
CLI para geração, gerenciamento e análise de conteúdo.
"""

import os
import sys
import click
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

# Ensure this directory is in the path for imports
_here = Path(__file__).parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

import db
import fetcher
import generator
import formatter
import notifier

load_dotenv()

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def safe_echo(message: str, **kwargs):
    """Print safely handling Unicode encoding errors."""
    try:
        click.echo(message, **kwargs)
    except UnicodeEncodeError:
        safe_msg = message.encode('ascii', errors='ignore').decode('ascii')
        click.echo(safe_msg, **kwargs)


@click.group()
def cli():
    """Automacao de conteudo para gestores de trafego."""
    db.init_db()


@cli.command()
@click.option("--topic", default=None, help="Topico customizado para busca (ex: 'TikTok ads')")
@click.option("--no-telegram", is_flag=True, help="Nao enviar para Telegram")
def run(topic: str, no_telegram: bool):
    """Gera conteudo dos feeds e salva como Markdown."""
    click.echo("Gerando conteudo para gestor de trafego...\n")

    # Validate Groq API
    if not os.getenv("GROQ_API_KEY"):
        click.echo("ERRO: GROQ_API_KEY nao encontrada no .env", err=True)
        return

    client = generator.get_groq_client()

    # Fetch articles
    if topic:
        click.echo(f"Buscando noticias sobre '{topic}'...")
        articles = fetcher.fetch_for_topic(topic, max_articles=3)
    else:
        click.echo("Buscando noticias dos feeds configurados...")
        articles = fetcher.fetch_articles(max_articles=3)

    if not articles:
        click.echo("Nenhuma noticia encontrada.")
        return

    safe_echo(f"  {len(articles)} pautas encontradas:")
    for a in articles:
        safe_echo(f"    - {a['title'][:70]}...")

    # Generate content
    click.echo("\nGerando roteiros, carrosseis e threads...")
    contents = []
    for i, article in enumerate(articles, 1):
        click.echo(f"  Pauta {i}/{len(articles)}...", nl=False)
        click.echo(" ", nl=False)  # Progress indicator
        try:
            content = generator.generate_content(article, client)
            contents.append(content)
            click.echo("OK")
        except Exception as e:
            click.echo(f"ERRO: {e}", err=True)
            contents.append({})

    # Save to database
    click.echo("\nSalvando no banco de dados...")
    run_date = date.today().strftime("%Y-%m-%d")
    for article, content in zip(articles, contents):
        if content:
            db.save_article(run_date, article, content)
    click.echo(f"  {len([c for c in contents if c])} artigos salvos")

    # Save to Markdown
    click.echo("Salvando Markdown...")
    markdown = formatter.format_markdown(articles, contents)
    filename = f"conteudo_{date.today().strftime('%Y%m%d')}.md"
    filepath = OUTPUT_DIR / filename
    filepath.write_text(markdown, encoding="utf-8")
    click.echo(f"  Salvo em: {filepath}")

    # Send to Telegram
    if not no_telegram:
        click.echo("Enviando para Telegram...")
        preview = formatter.format_telegram_preview(articles, contents)
        notifier.send_telegram(preview, filepath)

    click.echo("\nPronto!")


@cli.group()
def feeds():
    """Gerenciar feeds RSS."""
    pass


@feeds.command("list")
def feeds_list():
    """Lista todos os feeds."""
    all_feeds = db.get_feeds(active_only=False)

    if not all_feeds:
        click.echo("Nenhum feed configurado.")
        return

    click.echo("\nFeeds configurados:\n")
    for feed in all_feeds:
        status = "[ATIVO]" if feed["active"] else "[INATIVO]"
        click.echo(f"  ID {feed['id']}: {feed['name']}")
        click.echo(f"    {status}")
        click.echo(f"    {feed['url']}\n")


@feeds.command("add")
@click.argument("url")
@click.argument("name")
def feeds_add(url: str, name: str):
    """Adiciona um novo feed."""
    try:
        feed_id = db.add_feed(url, name)
        click.echo(f"Feed adicionado! ID: {feed_id}")
    except ValueError as e:
        click.echo(f"Erro: {e}", err=True)


@feeds.command("remove")
@click.argument("feed_id", type=int)
def feeds_remove(feed_id: int):
    """Desativa um feed."""
    db.toggle_feed(feed_id, active=False)
    click.echo(f"Feed {feed_id} desativado.")


@feeds.command("enable")
@click.argument("feed_id", type=int)
def feeds_enable(feed_id: int):
    """Reativa um feed."""
    db.toggle_feed(feed_id, active=True)
    click.echo(f"Feed {feed_id} ativado.")


@cli.group()
def history():
    """Ver historico de gerações."""
    pass


@history.command("list")
@click.option("--limit", default=10, help="Numero de gerações a mostrar")
def history_list(limit: int):
    """Lista ultimas gerações."""
    runs = db.get_history(limit=limit)

    if not runs:
        click.echo("Nenhuma geração encontrada.")
        return

    safe_echo("\nHistorico de gerações:\n")
    for run in runs:
        safe_echo(f"  {run['run_date']} - {run['count']} artigos")
        for article in run["articles"]:
            safe_echo(f"    * ID {article['id']}: {article['title'][:60]}...")
            if article["gancho_tema"]:
                safe_echo(f"      Angulo: {article['gancho_tema']}")
        safe_echo("")


@history.command("show")
@click.argument("article_id", type=int)
def history_show(article_id: int):
    """Exibe conteudo completo de um artigo."""
    article = db.get_article(article_id)

    if not article:
        click.echo(f"Artigo {article_id} nao encontrado.", err=True)
        return

    click.echo(f"\n{'='*70}")
    click.echo(f"Artigo {article['id']}")
    click.echo(f"{'='*70}\n")

    click.echo(f"Titulo: {article['title']}")
    click.echo(f"Fonte: {article['source']}")
    click.echo(f"Data: {article['run_date']}\n")

    if article.get("content"):
        content = article["content"]

        click.echo(f"ANGULO: {content.get('gancho_tema', '')}\n")

        # Roteiro A
        r1 = content.get("roteiro_1", {})
        click.echo(f"ROTEIRO A — {r1.get('tipo', '')}")
        click.echo(f"  Titulo: {r1.get('titulo', '')}")
        click.echo(f"  Gancho: {r1.get('gancho', '')}\n")

        # Roteiro B
        r2 = content.get("roteiro_2", {})
        click.echo(f"ROTEIRO B — {r2.get('tipo', '')}")
        click.echo(f"  Titulo: {r2.get('titulo', '')}")
        click.echo(f"  Gancho: {r2.get('gancho', '')}\n")

        # Carrossel
        cs = content.get("carrossel", {})
        click.echo(f"CARROSSEL: {cs.get('titulo_capa', '')}\n")

        # Thread
        thread = content.get("thread", {})
        if thread:
            click.echo("THREAD (X / LinkedIn):")
            for i in range(1, 9):
                post_key = f"post_{i}"
                if post_key in thread:
                    click.echo(f"  {i}. {thread[post_key]}")
            click.echo()


@cli.group()
def perf():
    """Rastrear performance de posts."""
    pass


@perf.command("log")
def perf_log():
    """Log interativo de metricas de um post."""
    # Get recent articles
    runs = db.get_history(limit=5)
    articles_list = []

    for run in runs:
        for article in run["articles"]:
            articles_list.append((article["id"], f"{article['title'][:50]}... ({run['run_date']})"))

    if not articles_list:
        click.echo("Nenhum artigo encontrado.", err=True)
        return

    click.echo("\nArtigos recentes:\n")
    for i, (article_id, display) in enumerate(articles_list, 1):
        click.echo(f"  {i}. {display}")

    choice = click.prompt("\nEscolha um artigo", type=click.IntRange(1, len(articles_list)))
    article_id, _ = articles_list[choice - 1]

    # Get platforms
    platforms = ["instagram", "reels", "carrossel", "thread", "linkedin"]
    click.echo("\nPlataformas:")
    for i, platform in enumerate(platforms, 1):
        click.echo(f"  {i}. {platform}")

    platform_choice = click.prompt("Escolha a plataforma", type=click.IntRange(1, len(platforms)))
    platform = platforms[platform_choice - 1]

    # Get roteiro
    roteiros = ["A", "B", "carrossel", "thread"]
    click.echo("\nRoteiros:")
    for i, roteiro in enumerate(roteiros, 1):
        click.echo(f"  {i}. {roteiro}")

    roteiro_choice = click.prompt("Escolha o roteiro", type=click.IntRange(1, len(roteiros)))
    roteiro = roteiros[roteiro_choice - 1]

    # Input metrics
    views = click.prompt("Views", type=int, default=0)
    saves = click.prompt("Saves", type=int, default=0)
    likes = click.prompt("Likes", type=int, default=0)
    comments = click.prompt("Comments", type=int, default=0)
    posted_at = click.prompt("Data do post (YYYY-MM-DD)", default=str(date.today()))

    # Save to database
    perf_id = db.log_performance(article_id, platform, roteiro, views, saves, likes, comments, posted_at)
    click.echo(f"\nMetrica registrada! ID: {perf_id}")


@perf.command("stats")
def perf_stats():
    """Exibe analise de performance."""
    stats = db.get_stats()

    click.echo("\n" + "="*70)
    click.echo("ANALISE DE PERFORMANCE")
    click.echo("="*70 + "\n")

    # By roteiro type
    if stats["by_roteiro"]:
        click.echo("POR TIPO DE ROTEIRO:")
        for row in stats["by_roteiro"]:
            tipo = row["tipo"] or "N/A"
            avg_views = row["avg_views"] or 0
            avg_saves = row["avg_saves"] or 0
            avg_likes = row["avg_likes"] or 0
            avg_comments = row["avg_comments"] or 0

            click.echo(f"  {tipo}")
            click.echo(f"    Views: {avg_views:.0f} | Saves: {avg_saves:.0f} | Likes: {avg_likes:.0f} | Comments: {avg_comments:.0f}")
        click.echo()

    # By format
    if stats["by_format"]:
        click.echo("POR FORMATO:")
        for row in stats["by_format"]:
            format_name = row["format"] or "N/A"
            avg_views = row["avg_views"] or 0
            avg_saves = row["avg_saves"] or 0

            click.echo(f"  {format_name}: Views {avg_views:.0f} | Saves {avg_saves:.0f}")
        click.echo()

    # Top themes
    if stats["top_themes"]:
        click.echo("TOP TEMAS (gancho_tema):")
        for i, row in enumerate(stats["top_themes"], 1):
            tema = row["gancho_tema"]
            avg_saves = row["avg_saves"] or 0
            save_rate = row["save_rate"] or 0

            click.echo(f"  {i}. {tema}")
            click.echo(f"     Saves: {avg_saves:.0f} | Save Rate: {save_rate}")
        click.echo()


if __name__ == "__main__":
    cli()
