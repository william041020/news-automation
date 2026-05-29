#!/usr/bin/env python3
"""
Web Dashboard for News Automation
Flask app with routes for viewing, managing, and generating content
"""

import os
import sys
import json
import threading
from datetime import date, datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS

# Ensure this directory is in the path for imports
_here = Path(__file__).parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

import db
import fetcher
import generator
import formatter

# Initialize Flask
app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(16)

# Generation status tracker
_run_status = {
    "running": False,
    "log": [],
    "done": False,
    "status": "idle",
}


def log_run(message: str):
    """Add message to generation log."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    msg = f"[{timestamp}] {message}"
    _run_status["log"].append(msg)
    print(msg)


def run_generation_async(topic: str = None):
    """Background thread for content generation."""
    try:
        _run_status["running"] = True
        _run_status["log"] = []
        _run_status["done"] = False

        log_run("Iniciando geração de conteúdo...")

        # Get Groq client
        log_run("Conectando à API Groq...")
        try:
            client = generator.get_groq_client()
        except ValueError as e:
            log_run(f"❌ Erro: {e}")
            _run_status["done"] = True
            return

        # Fetch articles
        if topic:
            log_run(f"Buscando artigos sobre '{topic}'...")
            articles = fetcher.fetch_for_topic(topic, max_articles=3)
        else:
            log_run("Buscando artigos dos feeds configurados...")
            articles = fetcher.fetch_articles(max_articles=3)

        if not articles:
            log_run("❌ Nenhum artigo encontrado")
            _run_status["done"] = True
            return

        log_run(f"✓ {len(articles)} artigos encontrados")

        # Generate content
        log_run("Gerando conteúdo...")
        run_date = date.today().strftime("%Y-%m-%d")
        contents = []
        successful = 0

        for i, article in enumerate(articles, 1):
            log_run(f"  Artigo {i}/{len(articles)}: {article['title'][:50]}...")
            try:
                content = generator.generate_content(article, client)
                if content:
                    contents.append(content)
                    successful += 1
                    # Save to database immediately
                    db.save_article(run_date, article, content)
                    log_run(f"    ✓ Salvo no banco")
                else:
                    log_run(f"    ⚠ Falha na geração (schema inválido)")
                    contents.append({})
            except Exception as e:
                log_run(f"    ❌ Erro: {e}")
                contents.append({})

        log_run(f"✓ {successful}/{len(articles)} artigos gerados com sucesso")

        # Save Markdown
        log_run("Salvando Markdown...")
        markdown = formatter.format_markdown(articles, contents)
        output_dir = _here / "output"
        output_dir.mkdir(exist_ok=True)
        filename = f"conteudo_{date.today().strftime('%Y%m%d')}.md"
        filepath = output_dir / filename
        filepath.write_text(markdown, encoding="utf-8")
        log_run(f"✓ Salvo: {filename}")

        # Save PDF
        log_run("Gerando PDF...")
        try:
            import pdf_generator
            pdf_path = pdf_generator.generate_pdf(articles, contents)
            if pdf_path:
                log_run(f"✓ PDF: {Path(pdf_path).name}")
            else:
                log_run("⚠ PDF nao gerado (instale: pip install fpdf2)")
        except Exception as e:
            log_run(f"⚠ PDF nao gerado: {e}")

        log_run("✓ Geração concluída!")
        _run_status["done"] = True

    except Exception as e:
        log_run(f"❌ Erro fatal: {e}")
        _run_status["done"] = True
    finally:
        _run_status["running"] = False


# Routes
@app.route("/")
def index():
    """Dashboard home."""
    # Get statistics
    runs = db.get_history(limit=1)
    articles = db.get_history(limit=20)
    feeds = db.get_feeds()
    stats_data = db.get_stats()

    # Calculate stats
    total_articles = sum(run["count"] for run in articles)
    today_articles = runs[0]["count"] if runs else 0
    today_date = runs[0]["run_date"] if runs else "--"
    active_feeds = len([f for f in feeds if f["active"]])

    # Count performance tracked posts
    tracked_posts = 0
    if stats_data["by_roteiro"]:
        for row in stats_data["by_roteiro"]:
            if row["avg_saves"] and row["avg_saves"] > 0:
                tracked_posts += 1

    # Get recent articles
    recent_articles = []
    for run in articles[:3]:
        recent_articles.extend(run["articles"][:3])
    recent_articles = recent_articles[:10]

    stats = {
        "total_articles": total_articles,
        "today_articles": today_articles,
        "today_date": today_date,
        "active_feeds": active_feeds,
        "total_feeds": len(feeds),
        "tracked_posts": tracked_posts,
    }

    return render_template("index.html", stats=stats, recent_articles=recent_articles)


@app.route("/history")
def history():
    """View generation history."""
    runs = db.get_history(limit=20)
    return render_template("history.html", runs=runs)


@app.route("/history/<int:article_id>")
def view_article(article_id: int):
    """View single article."""
    article = db.get_article(article_id)
    if not article:
        flash("Artigo não encontrado", "error")
        return redirect(url_for("history"))

    # Parse JSON content if present
    if article.get("content_json"):
        article["content"] = json.loads(article["content_json"])

    return render_template("article.html", article=article)


@app.route("/feeds")
def feeds():
    """Manage feeds."""
    all_feeds = db.get_feeds(active_only=False)
    return render_template("feeds.html", feeds=all_feeds)


@app.route("/feeds/add", methods=["POST"])
def feeds_add():
    """Add new feed."""
    url = request.form.get("url", "").strip()
    name = request.form.get("name", "").strip()

    if not url or not name:
        flash("URL e nome são obrigatórios", "error")
    else:
        try:
            db.add_feed(url, name)
            flash(f"Feed '{name}' adicionado com sucesso!", "success")
        except ValueError as e:
            flash(f"Erro: {e}", "error")

    return redirect(url_for("feeds"))


@app.route("/feeds/toggle/<int:feed_id>", methods=["POST"])
def feeds_toggle(feed_id: int):
    """Toggle feed active status."""
    all_feeds = db.get_feeds(active_only=False)
    feed = next((f for f in all_feeds if f["id"] == feed_id), None)

    if feed:
        db.toggle_feed(feed_id, not feed["active"])
        status = "ativado" if not feed["active"] else "desativado"
        flash(f"Feed #{feed_id} {status}!", "success")
    else:
        flash("Feed não encontrado", "error")

    return redirect(url_for("feeds"))


@app.route("/performance")
def performance():
    """View performance stats and log metrics."""
    articles = db.get_history(limit=20)
    articles_list = []

    for run in articles:
        for article in run["articles"]:
            articles_list.append(article)

    articles_list = articles_list[:50]

    # Get all performance records
    performance_records = []
    # Query directly from db (need to add function to db.py for this)

    today = date.today().strftime("%Y-%m-%d")
    stats_data = db.get_stats()

    return render_template(
        "performance.html",
        articles=articles_list,
        performance_records=performance_records,
        today=today,
    )


@app.route("/performance/log", methods=["POST"])
def performance_log():
    """Log performance metrics."""
    article_id = request.form.get("article_id", type=int)
    platform = request.form.get("platform", "").strip()
    roteiro = request.form.get("roteiro", "").strip()
    views = request.form.get("views", type=int, default=0)
    saves = request.form.get("saves", type=int, default=0)
    likes = request.form.get("likes", type=int, default=0)
    comments = request.form.get("comments", type=int, default=0)
    posted_at = request.form.get("posted_at", "").strip()

    if not all([article_id, platform, roteiro]):
        flash("Todos os campos são obrigatórios", "error")
        return redirect(url_for("performance"))

    try:
        db.log_performance(article_id, platform, roteiro, views, saves, likes, comments, posted_at)
        flash("Métricas registradas com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao registrar: {e}", "error")

    return redirect(url_for("performance", article_id=article_id))


# API Routes
@app.route("/api/run", methods=["POST"])
def api_run():
    """Start content generation."""
    if _run_status["running"]:
        return jsonify({"error": "Generation already in progress"}), 400

    data = request.get_json() or {}
    topic = data.get("topic")

    # Start background thread
    thread = threading.Thread(target=run_generation_async, args=(topic,), daemon=True)
    thread.start()

    return jsonify({"started": True})


@app.route("/api/run/status")
def api_run_status():
    """Get generation status."""
    return jsonify({
        "running": _run_status["running"],
        "done": _run_status["done"],
        "status": _run_status["status"],
        "log": _run_status["log"][-20:],  # Last 20 lines
    })


@app.route("/api/last-run")
def api_last_run():
    """Get last run date."""
    runs = db.get_history(limit=1)
    if runs:
        run_date = runs[0]["run_date"]
        # Format as "hoje", "ontem", or date
        today = date.today().strftime("%Y-%m-%d")
        if run_date == today:
            formatted = "hoje"
        else:
            formatted = run_date
        return jsonify({"last_run": formatted})
    return jsonify({"last_run": "Nunca"})


@app.route("/api/performance-stats")
def api_performance_stats():
    """Get performance stats for charts."""
    stats = db.get_stats()
    return jsonify(stats)


@app.before_request
def before_request():
    """Initialize database on startup."""
    db.init_db()


if __name__ == "__main__":
    # Initialize database
    db.init_db()

    # Print info
    print("\n" + "="*60)
    print("[*] News Automation Dashboard v2.0")
    print("="*60)
    print("\nAbrindo http://localhost:5000...")
    print("Pressione Ctrl+C para parar.\n")

    # Open browser if possible (only local development)
    if os.environ.get("RAILWAY_ENVIRONMENT") is None:
        try:
            import webbrowser
            webbrowser.open("http://localhost:5000")
        except:
            pass

    # Run Flask - read port from environment or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, port=port, use_reloader=False)
