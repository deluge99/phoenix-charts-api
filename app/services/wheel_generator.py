from io import BytesIO

from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from pathlib import Path
from svglib.svglib import svg2rlg

from app.services.phoenix_theme import apply_phoenix_perfection

import logging
logger = logging.getLogger("phoenix_charts.wheel")

REPO_ROOT = Path(__file__).resolve().parents[2]
LOGO_PATH = REPO_ROOT / "images" / "PhoenixLogo.png"


def svg_to_pdf_bytes(
    svg: str,
    theme: str = "classic",
    *,
    name: str = "",
    chart_type: str = "",
) -> bytes:

    themed_svg = apply_phoenix_perfection(svg, theme)

    drawing = svg2rlg(BytesIO(themed_svg.encode("utf-8")))
    if drawing is None:
        raise ValueError("SVG parse failed")

    buffer = BytesIO()
    page_width, page_height = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))

    # ────────────────────────────────────────
    # NO PAGE-WIDE BACKGROUND FILL ANYMORE
    # ────────────────────────────────────────

    # Header
    header_y = page_height - 0.5 * inch

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_width / 2, header_y, "Phoenix Oracle™")

    name_text = (name or "").strip()
    if name_text:
        c.setFont("Helvetica", 12)
        c.drawCentredString(page_width / 2, header_y - 14, name_text)

    ct = (chart_type or "").strip()
    if ct:
        pretty_type = (
            f"{ct.replace('_', ' ').title()} Chart"
            if "chart" not in ct.lower()
            else ct.replace("_", " ").title()
        )
        c.setFont("Helvetica-Oblique", 11)
        c.drawCentredString(page_width / 2, header_y - 28, pretty_type)

    # Logo
    try:
        if LOGO_PATH.exists():
            img = ImageReader(str(LOGO_PATH))
            size = 0.9 * inch
            c.drawImage(
                img,
                page_width - size - 0.4 * inch,
                page_height - size - 0.25 * inch,
                width=size,
                height=size,
                preserveAspectRatio=True,
                mask="auto",
            )
    except Exception as e:
        logger.warning("[wheel_generator] Failed to draw logo: %s", e)

    # Wheel SVG
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