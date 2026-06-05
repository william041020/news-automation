"""
PDF generation for daily content newsletter.
Clean white design with green branding. Arial font for full accent support.
"""

from datetime import datetime
from pathlib import Path

ARIAL           = "C:/Windows/Fonts/arial.ttf"
ARIAL_BOLD      = "C:/Windows/Fonts/arialbd.ttf"
ARIAL_ITALIC    = "C:/Windows/Fonts/ariali.ttf"
ARIAL_BOLDITALIC= "C:/Windows/Fonts/arialbi.ttf"

# Brand colors
GREEN       = (0, 160, 80)
DARK_GREEN  = (0, 100, 50)
DARK        = (30, 30, 30)
GRAY        = (100, 100, 100)
LIGHT_GRAY  = (240, 240, 240)
WHITE       = (255, 255, 255)
BLUE_ACCENT = (30, 100, 200)
PURPLE      = (120, 60, 180)

LOGO_PATH = None  # Set via set_logo()


def set_logo(path: str):
    global LOGO_PATH
    LOGO_PATH = path


def generate_pdf(articles: list[dict], contents: list[dict], output_path: str = None) -> str:
    try:
        from fpdf import FPDF
    except ImportError:
        print("fpdf2 not installed. Run: pip install fpdf2")
        return None

    today = datetime.now().strftime("%d/%m/%Y")
    now   = datetime.now().strftime("%d%m%Y_%H%M")

    class PDF(FPDF):
        def setup_fonts(self):
            self.add_font("Arial", "",   ARIAL)
            self.add_font("Arial", "B",  ARIAL_BOLD)
            self.add_font("Arial", "I",  ARIAL_ITALIC)
            self.add_font("Arial", "BI", ARIAL_BOLDITALIC)

        def header(self):
            # Green top bar
            self.set_fill_color(*DARK_GREEN)
            self.rect(0, 0, 210, 18, "F")

            # Logo (if available)
            if LOGO_PATH and Path(LOGO_PATH).exists():
                try:
                    self.image(LOGO_PATH, x=8, y=2, h=14)
                except Exception:
                    pass

            # Title
            self.set_font("Arial", "B", 13)
            self.set_text_color(*WHITE)
            self.set_y(4)
            self.cell(0, 6, "Newsletter Diária — Tráfego Pago para Empresários", align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_font("Arial", "", 8)
            self.set_text_color(180, 230, 200)
            self.cell(0, 4, f"Gerado em {today}", align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(5)

        def footer(self):
            self.set_y(-12)
            self.set_draw_color(*LIGHT_GRAY)
            self.set_line_width(0.3)
            self.line(15, self.get_y(), 195, self.get_y())
            self.set_font("Arial", "I", 7)
            self.set_text_color(*GRAY)
            self.cell(0, 8, f"Página {self.page_no()} — Conteúdo gerado automaticamente", align="C")

        def pauta_header(self, num: int, title: str, source: str, link: str):
            # Numbered badge
            self.set_fill_color(*GREEN)
            self.set_font("Arial", "B", 11)
            self.set_text_color(*WHITE)
            self.cell(22, 8, f"  PAUTA {num}", fill=True, new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

            # Title
            self.set_font("Arial", "B", 12)
            self.set_text_color(*DARK)
            self.multi_cell(0, 6, title)
            self.ln(1)

            # Source
            self.set_font("Arial", "I", 8)
            self.set_text_color(*GRAY)
            self.cell(0, 4, f"Fonte: {source}", new_x="LMARGIN", new_y="NEXT")
            if link:
                self.cell(0, 4, link[:95], new_x="LMARGIN", new_y="NEXT")
            self.ln(4)

        def section_header(self, text: str, bg=GREEN, text_color=WHITE):
            self.set_fill_color(*bg)
            self.set_font("Arial", "B", 10)
            self.set_text_color(*text_color)
            self.cell(0, 7, f"  {text}", fill=True, new_x="LMARGIN", new_y="NEXT")
            self.ln(3)

        def tag(self, text: str):
            """Small colored tag for roteiro type."""
            self.set_fill_color(230, 245, 235)
            self.set_font("Arial", "B", 8)
            self.set_text_color(*DARK_GREEN)
            self.cell(0, 5, f"  {text}", fill=True, new_x="LMARGIN", new_y="NEXT")
            self.ln(1)

        def roteiro_title(self, text: str):
            self.set_font("Arial", "B", 14)
            self.set_text_color(*DARK)
            self.multi_cell(0, 7, f'"{text}"')
            self.ln(2)

        def field_label(self, text: str):
            self.set_font("Arial", "B", 9)
            self.set_text_color(*GREEN)
            self.cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")

        def quote_box(self, text: str):
            self.set_fill_color(235, 250, 240)
            self.set_draw_color(*GREEN)
            self.set_line_width(0.5)
            # Left border accent
            x = self.get_x()
            y = self.get_y()
            self.set_font("Arial", "BI", 10)
            self.set_text_color(*DARK)
            self.set_x(20)
            self.multi_cell(173, 6, text, fill=True)
            # Draw green left border
            h = self.get_y() - y
            self.set_fill_color(*GREEN)
            self.rect(15, y, 3, h, "F")
            self.ln(3)

        def note_text(self, text: str):
            self.set_font("Arial", "I", 8)
            self.set_text_color(*GRAY)
            self.set_x(20)
            self.multi_cell(173, 5, text)
            self.ln(2)

        def body_text(self, text: str):
            self.set_font("Arial", "", 10)
            self.set_text_color(*DARK)
            self.multi_cell(0, 5.5, text)
            self.ln(2)

        def divider(self):
            self.set_draw_color(*LIGHT_GRAY)
            self.set_line_width(0.4)
            self.line(15, self.get_y(), 195, self.get_y())
            self.ln(5)

        def roteiro_block(self, num: str, r: dict):
            if not r:
                return

            tipo    = r.get("tipo", "")
            titulo  = r.get("titulo", "")
            duracao = r.get("duracao", "~45s")
            gancho  = r.get("gancho", "")
            nota_g  = r.get("nota_gancho", "")
            desenv  = r.get("desenvolvimento", "")
            cta     = r.get("cta", "")
            nota_c  = r.get("nota_cta", "")

            self.section_header(f"ROTEIRO {num}  ·  {duracao}")
            if tipo:
                self.tag(tipo)
            if titulo:
                self.roteiro_title(titulo)

            if gancho:
                self.field_label("GANCHO")
                self.quote_box(gancho)
            if nota_g:
                self.note_text(nota_g)

            if desenv:
                self.field_label("DESENVOLVIMENTO")
                self.body_text(desenv)

            if cta:
                self.field_label("CTA")
                self.quote_box(cta)
            if nota_c:
                self.note_text(nota_c)

            self.ln(2)

        def carrossel_block(self, cs: dict):
            if not cs or not cs.get("titulo_capa"):
                return
            self.section_header("CARROSSEL", bg=BLUE_ACCENT)

            self.set_font("Arial", "B", 13)
            self.set_text_color(*BLUE_ACCENT)
            self.set_x(15)
            self.multi_cell(180, 7, cs["titulo_capa"])
            if cs.get("subtitulo_capa"):
                self.set_font("Arial", "I", 10)
                self.set_text_color(*GRAY)
                self.set_x(15)
                self.multi_cell(180, 5, cs["subtitulo_capa"])
            self.ln(3)

            slides = [
                ("slide_2",     "Slide 2 — Problema"),
                ("slide_3",     "Slide 3 — Por que erra"),
                ("slide_4",     "Slide 4 — Consequência"),
                ("slide_5",     "Slide 5 — Solução"),
                ("slide_6_cta", "Slide 6 — CTA"),
            ]
            for key, lbl in slides:
                val = cs.get(key, "")
                if val:
                    for pfx in ["PROBLEMA:", "POR QUE ERRA:", "CONSEQUENCIA:", "CONSEQUÊNCIA:", "SOLUCAO:", "SOLUÇÃO:", "CTA:"]:
                        if val.upper().startswith(pfx):
                            val = val[len(pfx):].strip()
                    # Slide box
                    self.set_fill_color(*LIGHT_GRAY)
                    self.set_font("Arial", "B", 8)
                    self.set_text_color(*BLUE_ACCENT)
                    self.cell(0, 5, f"  {lbl}", fill=True, new_x="LMARGIN", new_y="NEXT")
                    self.set_font("Arial", "", 10)
                    self.set_text_color(*DARK)
                    self.set_x(18)
                    self.multi_cell(175, 5.5, val)
                    self.ln(2)

        def legenda_block(self, text: str):
            if not text:
                return
            self.section_header("LEGENDA SUGERIDA", bg=PURPLE)
            self.set_font("Arial", "", 10)
            self.set_text_color(*DARK)
            self.multi_cell(0, 6, text)
            self.ln(3)

    pdf = PDF()
    pdf.setup_fonts()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(15, 25, 15)

    valid_pairs = [(a, c) for a, c in zip(articles, contents) if c]

    for i, (article, content) in enumerate(valid_pairs, 1):
        pdf.add_page()

        pdf.pauta_header(i, article["title"], article["source"], article.get("link", ""))
        pdf.divider()

        pdf.roteiro_block("01", content.get("roteiro_1", {}))
        pdf.divider()
        pdf.roteiro_block("02", content.get("roteiro_2", {}))
        pdf.divider()
        pdf.roteiro_block("03", content.get("roteiro_3", {}))
        pdf.divider()

        pdf.carrossel_block(content.get("carrossel", {}))
        pdf.divider()
        pdf.legenda_block(content.get("legenda_sugerida", ""))

    if not output_path:
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = str(output_dir / f"newsletter_{now}.pdf")

    pdf.output(output_path)
    return output_path
