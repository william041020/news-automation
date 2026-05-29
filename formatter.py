"""
Content formatting for Markdown, PDF and Telegram.
"""

from datetime import datetime


def _render_roteiro(md: str, label: str, r: dict) -> str:
    if not r:
        return md
    tipo = r.get("tipo", "")
    titulo = r.get("titulo", "")
    duracao = r.get("duracao", "~45s")
    gancho = r.get("gancho", "")
    nota_gancho = r.get("nota_gancho", "")
    desenvolvimento = r.get("desenvolvimento", "")
    cta = r.get("cta", "")
    nota_cta = r.get("nota_cta", "")

    md += f"### {label}  —  `{tipo}`  _{duracao}_\n\n"
    if titulo:
        md += f"> **\"{titulo}\"**\n\n"

    if gancho:
        md += f"**GANCHO:**\n\n"
        md += f"> {gancho}\n\n"
    if nota_gancho:
        md += f"*{nota_gancho}*\n\n"

    if desenvolvimento:
        md += f"**DESENVOLVIMENTO:**\n\n{desenvolvimento}\n\n"

    if cta:
        md += f"**CTA:**\n\n"
        md += f"> {cta}\n\n"
    if nota_cta:
        md += f"*{nota_cta}*\n\n"

    return md


def format_markdown(articles: list[dict], contents: list[dict]) -> str:
    """Format articles and generated content as Markdown."""
    today = datetime.now().strftime("%d/%m/%Y")
    now = datetime.now().strftime("%d/%m/%Y as %H:%M")

    md = "# Conteudo Diario — Trafego Pago para Empresarios\n"
    md += f"**Data:** {today}\n\n"
    md += "---\n\n"

    valid_pairs = [(a, c) for a, c in zip(articles, contents) if c]

    if not valid_pairs:
        md += "_Nenhum conteudo gerado hoje._\n"
        return md

    for i, (article, content) in enumerate(valid_pairs, 1):
        md += f"## Pauta {i}: {article['title']}\n\n"
        md += f"**Fonte:** {article['source']}"
        if article.get("link"):
            md += f"  |  [Ver noticia]({article['link']})"
        md += "\n\n"

        # 3 Roteiros
        md = _render_roteiro(md, "Roteiro 01", content.get("roteiro_1", {}))
        md += "---\n\n"
        md = _render_roteiro(md, "Roteiro 02", content.get("roteiro_2", {}))
        md += "---\n\n"
        md = _render_roteiro(md, "Roteiro 03", content.get("roteiro_3", {}))

        # Carrossel
        cs = content.get("carrossel", {})
        if cs:
            md += "---\n\n"
            md += "### Carrossel\n\n"
            if cs.get("titulo_capa"):
                md += f"**🖼 Capa:** {cs['titulo_capa']}\n\n"
            if cs.get("subtitulo_capa"):
                md += f"*{cs['subtitulo_capa']}*\n\n"
            for key, label in [
                ("slide_2", "📌 Slide 2 — Problema"),
                ("slide_3", "🔍 Slide 3 — Por que erra"),
                ("slide_4", "⚠️  Slide 4 — Consequência"),
                ("slide_5", "✅ Slide 5 — Solução"),
                ("slide_6_cta", "👇 Slide 6 — CTA"),
            ]:
                if cs.get(key):
                    md += f"**{label}:**\n{cs[key]}\n\n"

        # Legenda
        legenda = content.get("legenda_sugerida", "")
        if legenda:
            md += "---\n\n"
            md += "### Legenda Sugerida\n\n"
            md += f"{legenda}\n\n"

        md += "═" * 60 + "\n\n"

    md += f"*Gerado em {now}*\n"
    return md


def format_telegram_preview(articles: list[dict], contents: list[dict]) -> str:
    """Format a short preview for Telegram."""
    today = datetime.now().strftime("%d/%m/%Y")
    lines = [f"*Newsletter Diaria — Trafego Pago*", f"_{today}_", ""]

    for i, (article, content) in enumerate(zip(articles, contents), 1):
        if not content:
            continue
        r1 = content.get("roteiro_1", {})
        titulo = r1.get("titulo", "")
        gancho = r1.get("gancho", "")[:120]
        lines.append(f"*Pauta {i}* — _{r1.get('tipo', '')}_")
        if titulo:
            lines.append(f'Titulo: "{titulo}"')
        if gancho:
            lines.append(f'Gancho: "{gancho}..."')
        lines.append("")

    lines.append("_PDF completo com 3 roteiros + carrossel + legenda por pauta no anexo._")
    return "\n".join(lines)
