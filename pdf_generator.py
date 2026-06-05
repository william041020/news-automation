"""
PDF generation for daily content newsletter.
Uses Arial (Windows system font) for full UTF-8/accent support.
"""

from datetime import datetime
from pathlib import Path

ARIAL          = "C:/Windows/Fonts/arial.ttf"
ARIAL_BOLD     = "C:/Windows/Fonts/arialbd.ttf"
ARIAL_ITALIC   = "C:/Windows/Fonts/ariali.ttf"
ARIAL_BOLDITALIC = "C:/Windows/Fonts/arialbi.ttf"


def generate_pdf(articles: list[dict], contents: list[dict], output_path: str = None) -> str:
    """Generate a PDF newsletter from articles and content."""
    try:
        from fpdf import FPDF
    except ImportError:
        print("fpdf2 not installed. Run: pip install fpdf2")
        return None

    today = datetime.now().strftime("%d/%m/%Y")
    now   = datetime.now().strftime("%d%m%Y_%H%M")

    class PDF(FPDF):
        def setup_fonts(self):
            self.add_font("Arial",  "",   ARIAL)
            self.add_font("Arial",  "B",  ARIAL_BOLD)
            self.add_font("Arial",  "I",  ARIAL_ITALIC)
            self.add_font("Arial",  "BI", ARIAL_BOLDITALIC)

        def header(self):
            self.set_fill_color(15, 15, 20)
            self.rect(0, 0, 210, 22, "F")
            self.set_font("Arial", "B", 14)
            self.set_text_color(0, 200, 100)
            self.set_y(6)
            self.cell(0, 8, "Newsletter Diária - Tráfego Pago para Empresários", align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_font("Arial", "", 9)
            self.set_text_color(150, 150, 150)
            self.cell(0, 5, f"Gerado em {today}", align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(3)

        def footer(self):
            self.set_y(-12)
            self.set_font("Arial", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, f"Página {self.page_no()} — Conteúdo gerado automaticamente", align="C")

        def section_bg(self, title: str, r=20, g=40, b=30):
            self.set_fill_color(r, g, b)
            self.set_font("Arial", "B", 11)
            self.set_text_color(0, 210, 90)
            self.cell(0, 8, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

        def label(self, text: str):
            self.set_font("Arial", "B", 9)
            self.set_text_color(180, 180, 180)
            self.cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")

        def body(self, text: str, color=(220, 220, 220)):
            self.set_font("Arial", "", 10)
            self.set_text_color(*color)
            self.multi_cell(0, 5.5, text)
            self.ln(2)

        def quote(self, text: str):
            self.set_fill_color(20, 35, 25)
            self.set_font("Arial", "BI", 10)
            self.set_text_color(0, 220, 100)
            self.set_x(18)
            self.multi_cell(175, 5.5, f'"{text}"', fill=True)
            self.ln(3)

        def note(self, text: str):
            self.set_font("Arial", "I", 9)
            self.set_text_color(130, 130, 130)
            self.set_x(18)
            self.multi_cell(175, 5, text)
            self.ln(2)

        def divider(self):
            self.set_draw_color(40, 40, 50)
            self.set_line_width(0.3)
            self.line(15, self.get_y(), 195, self.get_y())
            self.ln(4)

        def roteiro_block(self, num: str, r: dict):
            if not r:
                return
            tipo        = r.get("tipo", "")
            titulo      = r.get("titulo", "")
            duracao     = r.get("duracao", "~45s")
            gancho      = r.get("gancho", "")
            nota_gancho = r.get("nota_gancho", "")
            desenv      = r.get("desenvolvimento", "")
            cta         = r.get("cta", "")
            nota_cta    = r.get("nota_cta", "")

            self.section_bg(f"ROTEIRO {num}  |  {tipo}  |  {duracao}")

            if titulo:
                self.set_font("Arial", "B", 13)
                self.set_text_color(255, 255, 255)
                self.cell(0, 7, f'"{titulo}"', new_x="LMARGIN", new_y="NEXT")
                self.ln(3)

            if gancho:
                self.label("GANCHO:")
                self.quote(gancho)
            if nota_gancho:
                self.note(nota_gancho)

            if desenv:
                self.label("DESENVOLVIMENTO:")
                self.body(desenv)

            if cta:
                self.label("CTA:")
                self.quote(cta)
            if nota_cta:
                self.note(nota_cta)

            self.ln(3)

    pdf = PDF()
    pdf.setup_fonts()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(15, 25, 15)

    valid_pairs = [(a, c) for a, c in zip(articles, contents) if c]

    for i, (article, content) in enumerate(valid_pairs, 1):
        pdf.add_page()

        # Pauta header
        pdf.set_font("Arial", "B", 15)
        pdf.set_text_color(0, 200, 100)
        pdf.cell(0, 9, f"PAUTA {i}", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(220, 220, 220)
        pdf.multi_cell(0, 6, article["title"])

        pdf.set_font("Arial", "I", 8)
        pdf.set_text_color(100, 140, 100)
        pdf.cell(0, 5, f"Fonte: {article['source']}", new_x="LMARGIN", new_y="NEXT")
        if article.get("link"):
            pdf.cell(0, 5, article["link"][:90], new_x="LMARGIN", new_y="NEXT")
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

            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(100, 180, 255)
            pdf.cell(0, 7, cs["titulo_capa"], new_x="LMARGIN", new_y="NEXT")

            if cs.get("subtitulo_capa"):
                pdf.set_font("Arial", "I", 10)
                pdf.set_text_color(180, 180, 180)
                pdf.cell(0, 5, cs["subtitulo_capa"], new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)

            slides = [
                ("slide_2",    ">> Slide 2 — Problema:"),
                ("slide_3",    ">> Slide 3 — Por que erra:"),
                ("slide_4",    ">> Slide 4 — Consequência:"),
                ("slide_5",    ">> Slide 5 — Solução:"),
                ("slide_6_cta",">> Slide 6 — CTA:"),
            ]
            for key, lbl in slides:
                val = cs.get(key, "")
                if val:
                    # Remove label prefix if model accidentally duplicated it
                    for prefix in ["PROBLEMA:", "POR QUE ERRA:", "CONSEQUENCIA:", "CONSEQUÊNCIA:", "SOLUCAO:", "SOLUÇÃO:", "CTA:"]:
                        if val.upper().startswith(prefix):
                            val = val[len(prefix):].strip()
                    pdf.label(lbl)
                    pdf.body(val, color=(200, 200, 200))

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
