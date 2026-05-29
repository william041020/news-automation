"""
PDF generation for daily content newsletter.
"""

from datetime import datetime
from pathlib import Path


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
            self.rect(0, 0, 210, 297, 'F')
            self.set_font("Helvetica", "B", 18)
            self.set_text_color(0, 200, 100)
            self.set_y(12)
            self.cell(0, 10, "Newsletter de Conteudo — Trafego Pago", align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_font("Helvetica", "", 11)
            self.set_text_color(150, 150, 150)
            self.cell(0, 6, f"Gerado em {today}", align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(4)
            self.set_draw_color(0, 200, 100)
            self.set_line_width(0.5)
            self.line(15, self.get_y(), 195, self.get_y())
            self.ln(6)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, f"Pagina {self.page_no()} — Conteudo gerado automaticamente", align="C")

        def section_title(self, title: str):
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(0, 200, 100)
            self.set_fill_color(20, 30, 25)
            self.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT", fill=True)
            self.ln(2)

        def label(self, text: str):
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(200, 200, 200)
            self.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")

        def body_text(self, text: str, color=(220, 220, 220)):
            self.set_font("Helvetica", "", 10)
            self.set_text_color(*color)
            self.multi_cell(0, 6, text)
            self.ln(2)

        def quote_text(self, text: str):
            self.set_fill_color(25, 40, 30)
            self.set_font("Helvetica", "BI", 10)
            self.set_text_color(0, 220, 100)
            self.set_x(20)
            self.multi_cell(170, 6, f'"{text}"', fill=True)
            self.ln(3)

        def note_text(self, text: str):
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(130, 130, 130)
            self.multi_cell(0, 5, text)
            self.ln(2)

        def divider(self):
            self.set_draw_color(40, 40, 50)
            self.set_line_width(0.3)
            self.line(15, self.get_y(), 195, self.get_y())
            self.ln(5)

        def roteiro_block(self, label_text: str, roteiro: dict):
            if not roteiro:
                return
            self.section_title(f"  {label_text}")

            gancho = roteiro.get("gancho", "")
            desenvolvimento = roteiro.get("desenvolvimento", "")
            cta = roteiro.get("cta", "")
            nota = roteiro.get("nota_entrega", roteiro.get("nota_gancho", ""))

            if gancho:
                self.label("GANCHO:")
                self.quote_text(gancho)

            if nota:
                self.note_text(f"Entrega: {nota}")

            if desenvolvimento:
                self.label("DESENVOLVIMENTO:")
                self.body_text(desenvolvimento)

            if cta:
                self.label("CTA:")
                self.quote_text(cta)
                nota_cta = roteiro.get("nota_cta", "")
                if nota_cta:
                    self.note_text(f"Como fechar: {nota_cta}")

            self.ln(3)

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(15, 15, 15)

    valid_pairs = [(a, c) for a, c in zip(articles, contents) if c]

    for i, (article, content) in enumerate(valid_pairs, 1):
        pdf.add_page()

        # Pauta header
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, f"PAUTA {i}", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(200, 200, 200)
        pdf.multi_cell(0, 6, article["title"])
        pdf.ln(1)

        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 150, 100)
        fonte_text = f"Fonte: {article['source']}"
        if article.get("link"):
            fonte_text += f"  |  {article['link']}"
        pdf.multi_cell(0, 5, fonte_text)
        pdf.ln(4)

        pdf.divider()

        # Roteiros
        pdf.roteiro_block("ROTEIRO 1", content.get("roteiro_1", {}))
        pdf.divider()
        pdf.roteiro_block("ROTEIRO 2", content.get("roteiro_2", {}))
        pdf.divider()
        pdf.roteiro_block("ROTEIRO 3", content.get("roteiro_3", {}))

        # Carrossel
        carrossel = content.get("carrossel", {})
        if carrossel and any(carrossel.get(k) for k in ["titulo_capa", "slide_2"]):
            pdf.divider()
            pdf.section_title("  CARROSSEL")

            if carrossel.get("titulo_capa"):
                pdf.label("CAPA:")
                pdf.body_text(carrossel["titulo_capa"], color=(0, 220, 100))

            if carrossel.get("subtitulo_capa"):
                pdf.body_text(carrossel["subtitulo_capa"])

            slides = [
                ("slide_2", "Slide 2 — PROBLEMA:"),
                ("slide_3", "Slide 3 — POR QUE ERRA:"),
                ("slide_4", "Slide 4 — CONSEQUENCIA:"),
                ("slide_5", "Slide 5 — SOLUCAO:"),
                ("slide_6_cta", "Slide 6 — CTA:"),
            ]
            for key, title in slides:
                if carrossel.get(key):
                    pdf.label(title)
                    pdf.body_text(carrossel[key])

        # Legenda
        legenda = content.get("legenda_sugerida", "")
        if legenda:
            pdf.divider()
            pdf.section_title("  LEGENDA SUGERIDA")
            pdf.body_text(legenda, color=(0, 220, 100))

        pdf.ln(4)

    # Output path
    if not output_path:
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = str(output_dir / f"newsletter_{now}.pdf")

    pdf.output(output_path)
    return output_path
