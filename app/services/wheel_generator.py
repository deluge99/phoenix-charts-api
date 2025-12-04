from io import BytesIO

from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from svglib.svglib import svg2rlg

from app.services.phoenix_theme import apply_phoenix_perfection


def svg_to_pdf_bytes(svg: str, theme: str = "classic") -> bytes:
    """
    Apply Phoenix perfection (colors + theme) and convert SVG to PDF bytes.
    Mirrors the flow from test_wheel_perfection.py but returns bytes.
    """
    themed_svg = apply_phoenix_perfection(svg, theme)

    drawing = svg2rlg(BytesIO(themed_svg.encode("utf-8")))
    if drawing is None:
        raise ValueError("SVG parse failed")

    buffer = BytesIO()
    page_width, page_height = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))

    max_size = min(page_width, page_height) - 80
    scale = max_size / max(drawing.width, drawing.height)
    drawing.scale(scale, scale)

    renderPDF.draw(
        drawing,
        c,
        (page_width - drawing.width * scale) / 2,
        (page_height - drawing.height * scale) / 2,
    )

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()
