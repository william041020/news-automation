"""
Content formatting for Markdown and Telegram.
"""

from datetime import datetime


def format_markdown(articles: list[dict], contents: list[dict]) -> str:
    """Format articles and generated content as Markdown."""
    today = datetime.now().strftime("%d/%m/%Y")
    now = datetime.now().strftime("%d/%m/%Y as %H:%M")

    md = "# Conteudo Diario — Gestor de Trafego\n"
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
        md += f"**Angulo:** {content.get('gancho_tema', '')}\n\n"

        # Roteiro 1
        r1 = content.get("roteiro_1", {})
        md += f"### Roteiro A — {r1.get('tipo', '')}  _{r1.get('duracao', '')}_\n\n"
        md += f"**\"{r1.get('titulo', '')}\"**\n\n"

        md += "**GANCHO:**\n\n"
        md += f"> {r1.get('gancho', '')}\n\n"
        md += f"*{r1.get('nota_gancho', '')}*\n\n"

        md += "**DESENVOLVIMENTO:**\n\n"
        md += f"{r1.get('desenvolvimento', '')}\n\n"

        md += "**CTA:**\n\n"
        md += f"> {r1.get('cta', '')}\n\n"
        md += f"*{r1.get('nota_cta', '')}*\n\n"

        # Roteiro 2
        r2 = content.get("roteiro_2", {})
        md += f"### Roteiro B — {r2.get('tipo', '')}  _{r2.get('duracao', '')}_\n\n"
        md += f"**\"{r2.get('titulo', '')}\"**\n\n"

        md += "**GANCHO:**\n\n"
        md += f"> {r2.get('gancho', '')}\n\n"
        md += f"*{r2.get('nota_gancho', '')}*\n\n"

        md += "**DESENVOLVIMENTO:**\n\n"
        md += f"{r2.get('desenvolvimento', '')}\n\n"

        md += "**CTA:**\n\n"
        md += f"> {r2.get('cta', '')}\n\n"
        md += f"*{r2.get('nota_cta', '')}*\n\n"

        # Carrossel
        cs = content.get("carrossel", {})
        md += "### Carrossel\n\n"
        md += f"**Capa:** {cs.get('titulo_capa', '')}\n"
        md += f"**Subcapa:** {cs.get('subtitulo_capa', '')}\n\n"
        md += f"- **Slide 2:** {cs.get('slide_2', '')}\n"
        md += f"- **Slide 3:** {cs.get('slide_3', '')}\n"
        md += f"- **Slide 4:** {cs.get('slide_4', '')}\n"
        md += f"- **Slide 5:** {cs.get('slide_5', '')}\n"
        md += f"- **Slide 6 (CTA):** {cs.get('slide_6_cta', '')}\n\n"

        # Thread
        thread = content.get("thread", {})
        if thread:
            md += "### Thread (X / LinkedIn)\n\n"
            for post_num in range(1, 9):
                post_key = f"post_{post_num}"
                if post_key in thread:
                    md += f"**Post {post_num}:**\n\n"
                    md += f"> {thread[post_key]}\n\n"

        # Legenda
        md += "### Legenda Sugerida\n\n"
        md += f"{content.get('legenda_sugerida', '')}\n\n"

        md += "---\n\n"

    md += f"*Gerado em {now}*\n"
    return md


def format_telegram_preview(articles: list[dict], contents: list[dict]) -> str:
    """Format a short preview for Telegram."""
    today = datetime.now().strftime("%d/%m/%Y")
    lines = [f"*Conteudo Diario — Trafego Pago*", f"_{today}_", ""]

    for i, (article, content) in enumerate(zip(articles, contents), 1):
        if not content:
            continue

        r1 = content.get("roteiro_1", {})
        lines.append(f"*Pauta {i}* — {content.get('gancho_tema', '')}")
        lines.append(f"Roteiro A: _{r1.get('titulo', '')}_")

        gancho_preview = r1.get('gancho', '')[:100]
        lines.append(f"Gancho: \"{gancho_preview}...\"")
        lines.append("")

    lines.append("_Arquivo completo com 2 roteiros + carrossel + thread por pauta no anexo._")
    return "\n".join(lines)
