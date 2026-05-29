"""
PDF generation for daily content newsletter.
"""

from datetime import datetime
from pathlib import Path


def _safe(text: str) -> str:
    """Remove characters that can cause encoding issues."""
    if not text:
        return ""
    replacements = {
        "—": "-", "–": "-", "‘": "'", "’": "'",
        "“": '"', "”": '"', "…": "...", "â": "a",
        "ã": "a", "é": "e", "ê": "e", "í": "i",
        "ó": "o", "ô": "o", "ú": "u", "ü": "u",
        "ç": "c", "Ç": "C", "à": "a", "á": "a",
        "Á": "A", "É": "E", "Í": "I", "Ó": "O",
        "Ú": "U", "õ": "o", "è": "e",
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    # Remove any remaining non-latin1 characters
    return text.encode("latin-1", errors="replace").decode("latin-1")


def generate_pdf(articles: list[dict], contents: list[dict], output_path: str = None) -> str:
    """Generate a PDF newsletter from articles and content."""
    try:
        from fpdf import FPDF
    except ImportError:
        print("fpdf2 not installed. Run: pip install fpdf2")
        return None

    today = datetime.now().strftime("%d/%m/%Y")
    now = datetime.now().strftime("%d%m%Y_%H%M")

    class PDF(FPDF):
        def header(self):
            self.set_fill_color(15, 15, 20)
            self.rect(0, 0, 210, 20, "F")
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(0, 200, 100)
            self.set_y(5)
            self.cell(0, 8, _safe("Newsletter Diaria - Trafego Pago para Empresarios"), align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_font("Helvetica", "", 9)
            self.set_text_color(150, 150, 150)
            self.cell(0, 5, _safe(f"Gerado em {today}"), align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(3)

        def footer(self):
            self.set_y(-12)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, _safe(f"Pagina {self.page_no()} - Conteudo gerado automaticamente"), align="C")

        def section_bg(self, title: str, r=20, g=40, b=30):
            self.set_fill_color(r, g, b)
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(0, 210, 90)
            self.cell(0, 8, _safe(f"  {title}"), fill=True, new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

        def label(self, text: str):
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(180, 180, 180)
            self.cell(0, 5, _safe(text), new_x="LMARGIN", new_y="NEXT")

        def body(self, text: str, color=(220, 220, 220)):
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*color)
            self.multi_cell(0, 5.5, _safe(text))
            self.ln(2)

        def quote(self, text: str):
            self.set_fill_color(20, 35, 25)
            self.set_font("Helvetica", "BI", 10)
            self.set_text_color(0, 220, 100)
            self.set_x(18)
            self.multi_cell(175, 5.5, _safe(f'"{text}"'), fill=True)
            self.ln(3)

        def note(self, text: str):
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(130, 130, 130)
            self.set_x(18)
            self.multi_cell(175, 5, _safe(text))
            self.ln(2)

        def divider(self, light=False):
            color = (50, 50, 60) if not light else (35, 35, 45)
            self.set_draw_color(*color)
            self.set_line_width(0.3)
            self.line(15, self.get_y(), 195, self.get_y())
            self.ln(4)

        def roteiro_block(self, num: str, r: dict):
            if not r:
                return
            tipo = r.get("tipo", "")
            titulo = r.get("titulo", "")
            duracao = r.get("duracao", "~45s")
            gancho = r.get("gancho", "")
            nota_gancho = r.get("nota_gancho", "")
            desenvolvimento = r.get("desenvolvimento", "")
            cta = r.get("cta", "")
            nota_cta = r.get("nota_cta", "")

            self.section_bg(f"ROTEIRO {num}  |  {tipo}  |  {duracao}")

            if titulo:
                self.set_font("Helvetica", "B", 13)
                self.set_text_color(255, 255, 255)
                self.cell(0, 7, _safe(f'"{titulo}"'), new_x="LMARGIN", new_y="NEXT")
                self.ln(3)

            if gancho:
                self.label("GANCHO:")
                self.quote(gancho)
            if nota_gancho:
                self.note(nota_gancho)

            if desenvolvimento:
                self.label("DESENVOLVIMENTO:")
                self.body(desenvolvimento)

            if cta:
                self.label("CTA:")
                self.quote(cta)
            if nota_cta:
                self.note(nota_cta)

            self.ln(3)

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(15, 22, 15)

    valid_pairs = [(a, c) for a, c in zip(articles, contents) if c]

    for i, (article, content) in enumerate(valid_pairs, 1):
        pdf.add_page()

        # Pauta header
        pdf.set_font("Helvetica", "B", 15)
        pdf.set_text_color(0, 200, 100)
        pdf.cell(0, 9, _safe(f"PAUTA {i}"), new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(220, 220, 220)
        pdf.multi_cell(0, 6, _safe(article["title"]))

        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(100, 140, 100)
        fonte = f"Fonte: {article['source']}"
        pdf.cell(0, 5, _safe(fonte), new_x="LMARGIN", new_y="NEXT")
        if article.get("link"):
            link_text = article["link"][:80]
            pdf.cell(0, 5, _safe(link_text), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

        pdf.divider()

        # Roteiros
        pdf.roteiro_block("01", content.get("roteiro_1", {}))
        pdf.divider()
        pdf.roteiro_block("02", content.get("roteiro_2", {}))
        pdf.divider()
        pdf.roteiro_block("03", content.get("roteiro_3", {}))

        # Carrossel
        cs = content.get("carrossel", {})
        if cs and cs.get("titulo_capa"):
            pdf.divider()
            pdf.section_bg("CARROSSEL", r=15, g=30, b=50)

            if cs.get("titulo_capa"):
                pdf.set_font("Helvetica", "B", 12)
                pdf.set_text_color(100, 180, 255)
                pdf.cell(0, 7, _safe(cs["titulo_capa"]), new_x="LMARGIN", new_y="NEXT")
            if cs.get("subtitulo_capa"):
                pdf.set_font("Helvetica", "I", 10)
                pdf.set_text_color(180, 180, 180)
                pdf.cell(0, 5, _safe(cs["subtitulo_capa"]), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

            slides = [
                ("slide_2", "Slide 2 - PROBLEMA"),
                ("slide_3", "Slide 3 - POR QUE ERRA"),
                ("slide_4", "Slide 4 - CONSEQUENCIA"),
                ("slide_5", "Slide 5 - SOLUCAO"),
                ("slide_6_cta", "Slide 6 - CTA"),
            ]
            for key, label in slides:
                if cs.get(key):
                    pdf.label(label + ":")
                    pdf.body(cs[key], color=(200, 200, 200))

        # Legenda
        legenda = content.get("legenda_sugerida", "")
        if legenda:
            pdf.divider()
            pdf.section_bg("LEGENDA SUGERIDA", r=35, g=20, b=40)
            pdf.body(legenda, color=(200, 180, 255))

        pdf.ln(4)

    if not output_path:
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = str(output_dir / f"newsletter_{now}.pdf")

    pdf.output(output_path)
    return output_path
