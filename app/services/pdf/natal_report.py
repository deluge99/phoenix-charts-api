# app/services/pdf/natal_report.py
#
# Natal PDF Report Body Framework
# --------------------------------
# This module is responsible for drawing the portrait A4
# natal report body onto a ReportLab canvas.
#
# Page 1 of the PDF (wheel) is handled by wheel_page.draw_wheel_page.
# Page 2+ (this module) should contain all the textual/report content.

from typing import Dict, Any

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

from app.schemas.natal import NatalRequest


def draw_natal_report_body(c: canvas.Canvas, data: Dict[str, Any], req: NatalRequest) -> None:
    """Draw the natal report body onto the current page(s) of the canvas.

    This function assumes the canvas has already been set to portrait A4
    (c.setPageSize(A4)) and is being called AFTER the wheel page.

    It will:
      - Render a title/header
      - Print birth data section
      - Optionally dump planet positions, houses, and aspects if present
      - Automatically spill onto additional pages if vertical space runs out
    """

    page_width, page_height = A4

    # Layout constants (local to this function)
    LEFT_MARGIN = 25 * mm
    RIGHT_MARGIN = 25 * mm
    TOP_MARGIN = 25 * mm
    BOTTOM_MARGIN = 25 * mm
    LINE_HEIGHT = 12  # 12pt leading

    # mutable cursor for vertical position
    x_start = LEFT_MARGIN
    y = page_height - TOP_MARGIN

    def new_page_header() -> None:
        """Start a new portrait page and reset the y cursor with a header."""
        nonlocal y
        c.showPage()
        c.setPageSize(A4)
        y = page_height - TOP_MARGIN

        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_start, y, "Natal Chart Report")
        y -= LINE_HEIGHT * 2

    def ensure_space(lines: int = 1) -> None:
        """Ensure there is enough vertical space; if not, start a new page."""
        nonlocal y
        required = lines * LINE_HEIGHT + BOTTOM_MARGIN
        if y - required <= 0:
            new_page_header()

    def draw_heading(text: str, size: int = 14) -> None:
        nonlocal y
        ensure_space(2)
        c.setFont("Helvetica-Bold", size)
        c.drawString(x_start, y, text)
        # scale heading vertical spacing slightly with font size
        y -= LINE_HEIGHT * (size / 12.0) + 2

    def draw_label_value(label: str, value: str, size: int = 10) -> None:
        nonlocal y
        if not value:
            return
        ensure_space(1)
        c.setFont("Helvetica-Bold", size)
        c.drawString(x_start, y, f"{label}:")
        c.setFont("Helvetica", size)
        c.drawString(x_start + 70, y, value)
        y -= LINE_HEIGHT

    def draw_bullet_line(text: str, size: int = 10) -> None:
        nonlocal y
        ensure_space(1)
        c.setFont("Helvetica", size)
        c.drawString(x_start + 10, y, f"• {text}")
        y -= LINE_HEIGHT

    # --- PAGE HEADER ---
    c.setFont("Helvetica-Bold", 18)
    title_name = data.get("subject", {}).get("name") or getattr(req, "name", "Natal Chart")
    c.drawString(x_start, y, f"Natal Chart for {title_name}")
    y -= LINE_HEIGHT * 2

    # --- BIRTH DATA SECTION ---
    subject = data.get("subject", {})

    birth_date = subject.get("birth_date") or subject.get("date")
    birth_time = subject.get("birth_time") or subject.get("time")
    city = subject.get("city") or subject.get("place") or getattr(req, "city", None)
    country = subject.get("country") or getattr(req, "country", None)
    tz = subject.get("tz_str") or getattr(req, "tz_str", None)

    draw_heading("Birth Data")
    draw_label_value("Name", title_name)
    draw_label_value("Date", str(birth_date) if birth_date else "")
    draw_label_value("Time", str(birth_time) if birth_time else "")
    draw_label_value("Location", ", ".join([p for p in [city, country] if p]))
    draw_label_value("Time Zone", tz or "")

    # --- PLANET POSITIONS SECTION ---
    # We try to be robust about data shape. If your chart data uses a different
    # key, you can update this section to match.
    planets = (
        data.get("planets")
        or data.get("points")
        or data.get("bodies")
        or []
    )

    if planets:
        draw_heading("Planet Positions")
        c.setFont("Helvetica-Bold", 10)
        ensure_space(2)
        c.drawString(x_start, y, "Planet")
        c.drawString(x_start + 120, y, "Position")
        c.drawString(x_start + 260, y, "House")
        y -= LINE_HEIGHT
        c.setFont("Helvetica", 10)

        for p in planets:
            ensure_space(1)
            name = p.get("name") or p.get("label") or "?"
            pos = p.get("position_str") or p.get("position") or ""
            house = str(p.get("house", ""))

            c.drawString(x_start, y, name)
            c.drawString(x_start + 120, y, pos)
            if house:
                c.drawString(x_start + 260, y, f"House {house}")
            y -= LINE_HEIGHT

    # --- HOUSES SECTION (optional) ---
    houses = data.get("houses") or []
    if houses:
        draw_heading("House Cusps")
        c.setFont("Helvetica-Bold", 10)
        ensure_space(2)
        c.drawString(x_start, y, "House")
        c.drawString(x_start + 120, y, "Cusp Position")
        y -= LINE_HEIGHT
        c.setFont("Helvetica", 10)

        for h in houses:
            ensure_space(1)
            num = h.get("number") or h.get("house") or "?"
            pos = h.get("position_str") or h.get("position") or ""
            c.drawString(x_start, y, str(num))
            c.drawString(x_start + 120, y, pos)
            y -= LINE_HEIGHT

    # --- ASPECTS SECTION (optional) ---
    aspects = data.get("aspects") or []
    if aspects:
        draw_heading("Major Aspects")
        for asp in aspects:
            ensure_space(1)
            p1 = asp.get("p1") or asp.get("planet1") or "?"
            p2 = asp.get("p2") or asp.get("planet2") or "?"
            aspect_name = asp.get("aspect_name") or asp.get("type") or "aspect"
            orb = asp.get("orb")

            line = f"{p1} {aspect_name} {p2}"
            if orb is not None:
                line += f" (orb {orb}°)"
            draw_bullet_line(line)

    # You can continue with more detailed text/interpretation sections here,
    # using ensure_space() + draw_heading() + draw_bullet_line() patterns.