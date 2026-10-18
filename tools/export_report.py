"""Render the APA DOCX as a PDF with embedded Times New Roman fonts.

Consumes the generated Word content, paragraphs, tables, and embedded figures.
Requires python-docx and ReportLab. Explicit page breaks preserve the intended
section layout; independent PDF pagination checks are part of final QA.
"""

import argparse
from functools import partial
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.table import Table as WordTable
from docx.text.paragraph import Paragraph as WordParagraph
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]


def render(font_dir):
    font_dir = Path(font_dir)
    for name, filename in (("TNR", "times.ttf"), ("TNR-Bold", "timesbd.ttf"),
                           ("TNR-Italic", "timesi.ttf"), ("TNR-BoldItalic", "timesbi.ttf")):
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    pdfmetrics.registerFontFamily("TNR", normal="TNR", bold="TNR-Bold",
                                  italic="TNR-Italic", boldItalic="TNR-BoldItalic")
    source = Document(ROOT / "docs/final_report.docx")
    body_style = ParagraphStyle("Body", fontName="TNR", fontSize=12, leading=24,
                                firstLineIndent=36, spaceAfter=0, spaceBefore=0)
    flow = []
    for element in source.element.body:
        if element.tag == qn("w:p"):
            p = WordParagraph(element, source)
            if any(br.get(qn("w:type")) == "page" for br in element.iter(qn("w:br"))):
                flow.append(PageBreak())
                continue
            blips = list(element.iter(qn("a:blip")))
            if blips:
                for blip in blips:
                    part = source.part.related_parts[blip.get(qn("r:embed"))]
                    drawing = Image(BytesIO(part.blob))
                    drawing.drawHeight *= 468 / drawing.drawWidth
                    drawing.drawWidth = 468
                    flow.append(drawing)
                continue
            if not p.text:
                flow.append(Spacer(1, 24))
                continue
            pieces = []
            for run in p.runs:
                text = escape(run.text).replace("\n", "<br/>")
                if run.italic:
                    text = f"<i>{text}</i>"
                if run.bold:
                    text = f"<b>{text}</b>"
                pieces.append(text)
            fmt = p.paragraph_format
            kwargs = {}
            if fmt.first_line_indent is not None:
                kwargs["firstLineIndent"] = fmt.first_line_indent.pt
            if fmt.left_indent is not None:
                kwargs["leftIndent"] = fmt.left_indent.pt
            if p.alignment is not None:
                kwargs["alignment"] = {WD_ALIGN_PARAGRAPH.CENTER: TA_CENTER,
                                        WD_ALIGN_PARAGRAPH.RIGHT: TA_RIGHT}.get(p.alignment, TA_LEFT)
            if p.style.name.startswith("Heading"):
                kwargs.update(firstLineIndent=0, alignment=TA_CENTER, keepWithNext=True)
                content = "<b>" + "".join(pieces) + "</b>"
            else:
                content = "".join(pieces)
            flow.append(Paragraph(content, ParagraphStyle("Paragraph", parent=body_style, **kwargs)))
        elif element.tag == qn("w:tbl"):
            table = WordTable(element, source)
            cells = []
            cell_style = ParagraphStyle("Cell", fontName="TNR", fontSize=11, leading=14)
            for index, row in enumerate(table.rows):
                values = []
                for cell in row.cells:
                    text = escape(cell.text)
                    values.append(Paragraph(f"<b>{text}</b>" if index == 0 else text, cell_style))
                cells.append(values)
            rendered = Table(cells, colWidths=[83, 90, 98, 98, 99], hAlign="LEFT")
            rendered.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LINEABOVE", (0, 0), (-1, 0), 0.6, colors.black),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
                ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.black),
            ]))
            flow.append(rendered)

    def page_number(canvas, document):
        canvas.saveState()
        canvas.setFont("TNR", 12)
        canvas.drawRightString(letter[0] - 72, letter[1] - 42, str(document.page))
        canvas.restoreState()

    destination = ROOT / "docs/final_report.pdf"
    pdf = SimpleDocTemplate(str(destination), pagesize=letter, leftMargin=72,
                            rightMargin=72, topMargin=72, bottomMargin=72,
                            title=source.core_properties.title,
                            author=source.core_properties.author)
    pdf.build(flow, onFirstPage=page_number, onLaterPages=page_number,
              canvasmaker=partial(Canvas, initialFontName="TNR"))
    print(f"Created {destination}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font-dir", default="C:/Windows/Fonts",
                        help="directory containing times.ttf, timesbd.ttf, timesi.ttf, timesbi.ttf")
    render(parser.parse_args().font_dir)
