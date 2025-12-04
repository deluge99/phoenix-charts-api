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
    """
    Apply Phoenix perfection (colors + theme), add a small header + logo,
    and convert SVG → PDF bytes.

    Header:
      Phoenix Oracle
      {name}
      {Chart Type}
    """
    themed_svg = apply_phoenix_perfection(svg, theme)

    drawing = svg2rlg(BytesIO(themed_svg.encode("utf-8")))
    if drawing is None:
        raise ValueError("SVG parse failed")

    buffer = BytesIO()
    page_width, page_height = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))

    # -----------------------------
    # 1) Phoenix Oracle Header Text
    # -----------------------------
    header_y = page_height - 0.5 * inch

    # Line 1: Phoenix Oracle
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_width / 2, header_y, "Phoenix Oracle™")

    # Line 2: Name (if any)
    name_text = (name or "").strip()
    if name_text:
        c.setFont("Helvetica", 12)
        c.drawCentredString(page_width / 2, header_y - 14, name_text)

    # Line 3: Chart type (if any)
    ct = (chart_type or "").strip()
    if ct:
        base_type = ct.replace("_", " ").title()
        # Append "Chart" unless it already includes the word
        pretty_type = (
            f"{base_type} Chart"
            if "chart" not in base_type.lower()
            else base_type
        )
        c.setFont("Helvetica-Oblique", 11)
        c.drawCentredString(page_width / 2, header_y - 28, pretty_type)

    # -----------------------------
    # 2) Phoenix Logo (top-right)
    # -----------------------------
    try:
        if LOGO_PATH.exists():
            img = ImageReader(str(LOGO_PATH))
            logo_size = 0.9 * inch
            x = page_width - logo_size - 0.4 * inch
            y = page_height - logo_size - 0.25 * inch

            c.drawImage(
                img,
                x,
                y,
                width=logo_size,
                height=logo_size,
                preserveAspectRatio=True,
                mask="auto",
            )
        else:
            logger.warning("[wheel_generator] Logo not found at %s", LOGO_PATH)
    except Exception as e:
        logger.warning("[wheel_generator] Failed to draw logo: %s", e)

    # -----------------------------
    # 3) Draw wheel SVG (old layout)
    # -----------------------------
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