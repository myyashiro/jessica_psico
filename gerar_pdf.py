import re
from fpdf import FPDF

EARTH  = (140, 145, 108)
SAND   = (172, 176, 135)
ALMOND = (227, 232, 213)
DARK   = (35, 39, 26)
TEXT   = (55, 65, 40)
LIGHT  = (88, 101, 74)
WHITE  = (255, 255, 255)

ARIAL        = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_BOLD   = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL_ITALIC = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
GEORGIA      = "/System/Library/Fonts/Supplemental/Georgia.ttf"
GEORGIA_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
GEORGIA_ITAL = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
GEORGIA_BOLD_ITAL = "/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf"

def clean(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    return text.strip()

def parse_md(md):
    items = []
    in_table = False
    table_rows = []

    for raw in md.splitlines():
        line = raw.rstrip()

        if line.startswith("> "):
            items.append(("quote", line[2:].strip().strip("*")))
            continue

        if line.startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            table_rows.append(cells)
            in_table = True
            continue

        if in_table:
            items.append(("table", table_rows))
            table_rows = []
            in_table = False

        if re.match(r"^-{3,}$", line):
            items.append(("hr", ""))
            continue

        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            items.append((f"h{len(m.group(1))}", m.group(2).strip()))
            continue

        m = re.match(r"^[-*]\s+(.+)$", line)
        if m:
            items.append(("li", m.group(1).strip()))
            continue

        if line == "":
            items.append(("blank", ""))
            continue

        items.append(("p", line))

    if table_rows:
        items.append(("table", table_rows))

    return items


class PersonasPDF(FPDF):
    def setup_fonts(self):
        self.add_font("Arial", "", ARIAL, uni=True)
        self.add_font("Arial", "B", ARIAL_BOLD, uni=True)
        self.add_font("Arial", "I", ARIAL_ITALIC, uni=True)
        self.add_font("Georgia", "", GEORGIA, uni=True)
        self.add_font("Georgia", "B", GEORGIA_BOLD, uni=True)
        self.add_font("Georgia", "I", GEORGIA_ITAL, uni=True)
        self.add_font("Georgia", "BI", GEORGIA_BOLD_ITAL, uni=True)

    def header(self):
        pass

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-14)
            self.set_font("Arial", "", 7)
            self.set_text_color(*LIGHT)
            self.cell(0, 6,
                f"Jessica Miyagawa  ·  Psicologa TCC  ·  CRP 06/211924     {self.page_no() - 1}",
                align="C")

    def rule(self, color=SAND, thickness=0.3):
        self.set_draw_color(*color)
        self.set_line_width(thickness)
        self.line(22, self.get_y(), 188, self.get_y())

    def section_label(self, text):
        self.set_font("Arial", "B", 7)
        self.set_text_color(*EARTH)
        self.set_x(22)
        self.cell(166, 4, text.upper(), new_x="LMARGIN", new_y="NEXT")
        self.rule()
        self.ln(4)


pdf = PersonasPDF()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.set_margins(22, 20, 22)
pdf.setup_fonts()

# ── CAPA ──────────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.set_fill_color(*DARK)
pdf.rect(0, 0, 210, 297, "F")

pdf.set_y(48)
pdf.set_x(24)
pdf.set_font("Arial", "B", 7)
pdf.set_text_color(*SAND)
pdf.cell(0, 5, "DOCUMENTO ESTRATEGICO  ·  CONFIDENCIAL", new_x="LMARGIN", new_y="NEXT")

pdf.ln(16)
pdf.set_x(24)
pdf.set_font("Georgia", "I", 44)
pdf.set_text_color(*ALMOND)
pdf.multi_cell(162, 14, "Estudo de\nPersonas")

pdf.ln(6)
pdf.set_x(24)
pdf.set_font("Georgia", "I", 16)
pdf.set_text_color(172, 176, 135)
pdf.multi_cell(162, 8, "Psicologa Jessica Miyagawa\nTCC  ·  Moema/SP  ·  Online")

pdf.ln(14)
pdf.set_fill_color(*SAND)
pdf.rect(24, pdf.get_y(), 40, 0.7, "F")
pdf.ln(12)

pdf.set_x(24)
pdf.set_font("Arial", "", 8)
pdf.set_text_color(140, 160, 110)
pdf.multi_cell(162, 6,
    "Documento estrategico para:\n"
    "Pagina de Vendas  ·  Roteiros de Video  ·  Jornada de WhatsApp")

pdf.ln(10)
pdf.set_x(24)
pdf.set_draw_color(*SAND)
pdf.set_line_width(0.3)
pdf.rect(24, pdf.get_y(), 162, 12)
pdf.set_font("Arial", "", 7)
pdf.set_text_color(140, 155, 100)
pdf.set_x(24)
pdf.cell(162, 12,
    "TCC  ·  RELACIONAMENTOS  ·  BEM-ESTAR FEMININO  ·  SAO PAULO  ·  ONLINE BRASIL",
    align="C", new_x="LMARGIN", new_y="NEXT")

pdf.set_y(262)
pdf.set_x(24)
pdf.set_font("Arial", "", 7)
pdf.set_text_color(100, 115, 80)
pdf.cell(0, 5,
    "Jessica Miyagawa  ·  CRP 06/211924  ·  Especializacao TCC IPq-USP  ·  Maio 2026",
    new_x="LMARGIN", new_y="NEXT")

# ── CONTEÚDO ──────────────────────────────────────────────────────────────────
pdf.add_page()

with open("Personas_Jessica_Miyagawa.md", "r", encoding="utf-8") as f:
    raw_md = f.read()

items = parse_md(raw_md)
LM, RW = 22, 166
skip_h1 = True
last = None

for i, (typ, val) in enumerate(items):

    if typ == "h1" and skip_h1:
        skip_h1 = False
        continue

    if typ == "h1":
        if last not in (None, "blank"):
            pdf.add_page()
        pdf.set_fill_color(*DARK)
        pdf.rect(0, pdf.get_y() - 3, 210, 26, "F")
        pdf.set_x(LM)
        pdf.set_font("Georgia", "I", 22)
        pdf.set_text_color(*WHITE)
        pdf.multi_cell(RW, 9, clean(val))
        pdf.set_fill_color(*EARTH)
        pdf.rect(0, pdf.get_y(), 210, 1.5, "F")
        pdf.ln(8)

    elif typ == "h2":
        pdf.add_page()
        pdf.set_fill_color(*ALMOND)
        pdf.rect(0, pdf.get_y() - 3, 210, 20, "F")
        pdf.set_x(LM)
        pdf.set_font("Georgia", "I", 16)
        pdf.set_text_color(*DARK)
        pdf.multi_cell(RW, 8, clean(val))
        pdf.set_draw_color(*SAND)
        pdf.set_line_width(0.5)
        pdf.line(LM, pdf.get_y(), LM + RW, pdf.get_y())
        pdf.ln(7)

    elif typ == "h3":
        pdf.ln(3)
        pdf.section_label(clean(val))

    elif typ == "h4":
        pdf.ln(2)
        pdf.set_x(LM)
        pdf.set_font("Arial", "B", 8)
        pdf.set_text_color(*DARK)
        pdf.multi_cell(RW, 5, clean(val).upper())
        pdf.ln(1)

    elif typ == "table":
        col1, col2 = 58, RW - 58
        alt = False
        for row in val:
            if len(row) < 2 or (row[0] == "" and row[1] == ""):
                continue
            label = clean(row[0])
            value = clean(row[1]) if len(row) > 1 else ""
            lines_est = max(1, len(value) // 46 + 1)
            rh = max(6.5, lines_est * 5.2)
            x0, y0 = LM, pdf.get_y()
            bg = (242, 245, 234) if alt else WHITE
            pdf.set_fill_color(*bg)
            pdf.set_font("Arial", "B", 8)
            pdf.set_text_color(*EARTH)
            pdf.set_xy(x0, y0)
            pdf.multi_cell(col1, rh / lines_est, label, border=0, fill=True)
            pdf.set_xy(x0 + col1, y0)
            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(*TEXT)
            pdf.multi_cell(col2, rh / lines_est, value, border=0, fill=True)
            pdf.set_draw_color(210, 215, 195)
            pdf.set_line_width(0.2)
            pdf.line(LM, pdf.get_y(), LM + RW, pdf.get_y())
            alt = not alt
        pdf.ln(5)

    elif typ == "quote":
        y0 = pdf.get_y()
        pdf.set_x(LM + 6)
        pdf.set_font("Georgia", "I", 10.5)
        pdf.set_text_color(*DARK)
        txt = "“" + clean(val) + "”"
        pdf.multi_cell(RW - 6, 6, txt)
        y1 = pdf.get_y()
        pdf.set_fill_color(*SAND)
        pdf.rect(LM, y0, 2, y1 - y0, "F")
        pdf.set_fill_color(242, 246, 234)
        pdf.rect(LM + 2, y0, RW - 2, y1 - y0, "F")
        pdf.set_xy(LM + 6, y0)
        pdf.set_font("Georgia", "I", 10.5)
        pdf.set_text_color(*DARK)
        pdf.multi_cell(RW - 6, 6, txt)
        pdf.ln(2)

    elif typ == "li":
        pdf.set_x(LM + 3)
        pdf.set_font("Arial", "", 8)
        pdf.set_text_color(*EARTH)
        pdf.cell(5, 5.5, "·")
        pdf.set_text_color(*TEXT)
        pdf.multi_cell(RW - 8, 5.5, clean(val))

    elif typ == "p":
        pdf.set_x(LM)
        pdf.set_font("Arial", "", 9.5)
        pdf.set_text_color(*TEXT)
        pdf.multi_cell(RW, 5.5, clean(val))
        pdf.ln(1)

    elif typ == "hr":
        pdf.ln(3)
        pdf.rule(SAND, 0.3)
        pdf.ln(5)

    elif typ == "blank":
        if last not in ("blank", "h1", "h2", "h3", "hr", None):
            pdf.ln(2.5)

    last = typ

pdf.output("Personas_Jessica_Miyagawa.pdf")
print("PDF gerado: Personas_Jessica_Miyagawa.pdf")
